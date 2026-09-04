# -*- coding: utf-8 -*-
"""Liest die Risiko-Akzeptanz nach dem CONDITIONAL-Akzeptanz-Protokoll.

Das Format steht in references/enforcement/enforcement-engine.md, Abschnitt
I.5. Ein Block sieht so aus:

    ## Risiko-Akzeptanz: T-002

    **Gate:** G4 — Analyze → Implement
    **Prüfpunkt:** orphan_task — T-002 ohne Story-Referenz
    **F-Stufe:** F3 (gewichtiger Mangel)
    **Risiko:** ...
    **Akzeptiert durch:** Leitung Betrieb
    **Kompensation:** ...
    **Frist:** 2026-10-01
    **Datum:** 2026-09-04

Vorher genuegte es, dass Pruefpunktname und Betreff irgendwo im Text des
Blocks als Teilstring vorkamen. Damit hob eine Datei, die die Akzeptanz
ausdruecklich verweigert, das Gate auf, denn sie nennt beide Namen. Eine
Freigabe, die kein Dokument verlangt, ist keine Freigabe.

Ein Block hebt einen F3-Befund deshalb nur auf, wenn alle Pflichtfelder des
Protokolls ausgefuellt sind, die Frist ein Datum im Format YYYY-MM-DD traegt
und noch nicht abgelaufen ist, die F-Stufe zum Befund passt und die
Ueberschrift den Betreff als eigenes Wort nennt. Was daran fehlt, meldet der
Checker als eigene Zeile, statt es zu verschlucken.

Nur Standardbibliothek.
"""

import datetime
import re

HEADING_RE = re.compile(r"^##\s+Risiko-Akzeptanz\s*:\s*(.*)$")
FIELD_RE = re.compile(
    r"^\*\*([^*:]+?)\*\*\s*:\s*(.*)$|^\*\*([^*:]+?):\*\*\s*(.*)$")
LEVEL_RE = re.compile(r"\bF([0-5])\b")
DATE_RE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")

# Die Pflichtfelder des Protokolls, in der Reihenfolge des Abschnitts I.5.
REQUIRED = ("Gate", "Prüfpunkt", "F-Stufe", "Risiko", "Akzeptiert durch",
            "Kompensation", "Frist", "Datum")


class Block(object):
    def __init__(self, subject, line):
        self.subject = subject
        self.line = line
        self.fields = {}

    def value(self, name):
        return (self.fields.get(name) or "").strip()

    @property
    def level(self):
        match = LEVEL_RE.search(self.value("F-Stufe"))
        return "F" + match.group(1) if match else None

    def date(self, name):
        match = DATE_RE.search(self.value(name))
        if not match:
            return None
        try:
            return datetime.date(int(match.group(1)), int(match.group(2)),
                                 int(match.group(3)))
        except ValueError:
            return None

    def problems(self, today):
        """Was diesen Block als Freigabe untauglich macht, im Klartext."""
        found = []
        missing = [name for name in REQUIRED if not self.value(name)]
        if missing:
            found.append("Pflichtfeld fehlt oder ist leer: %s"
                         % ", ".join(missing))
        if self.value("F-Stufe") and self.level is None:
            found.append("F-Stufe %r ist keine Stufe zwischen F0 und F5"
                         % self.value("F-Stufe"))
        deadline = self.date("Frist")
        if self.value("Frist") and deadline is None:
            found.append("Frist %r ist kein Datum im Format YYYY-MM-DD"
                         % self.value("Frist"))
        elif deadline is not None and deadline < today:
            found.append("Frist %s ist am %s abgelaufen"
                         % (deadline.isoformat(), today.isoformat()))
        if self.value("Datum") and self.date("Datum") is None:
            found.append("Datum %r ist kein Datum im Format YYYY-MM-DD"
                         % self.value("Datum"))
        return found

    def __repr__(self):
        return "<Risiko-Akzeptanz %s, Zeile %d>" % (self.subject, self.line)


def names(text, needle):
    """True, wenn needle als eigenes Wort in text steht.

    Teilstring genuegt nicht: 'T-002' darf nicht auf 'T-0021' passen.
    """
    if not needle:
        return False
    return re.search(r"(?<![\w.-])%s(?![\w.-])" % re.escape(needle),
                     text) is not None


def parse(path):
    """Liest eine Akzeptanz-Datei und gibt die Bloecke zurueck."""
    with open(path, encoding="utf-8") as handle:
        lines = handle.read().split("\n")

    blocks = []
    current = None
    for number, line in enumerate(lines, 1):
        heading = HEADING_RE.match(line)
        if heading:
            current = Block(heading.group(1).strip(), number)
            blocks.append(current)
            continue
        if line.startswith("## ") or line.startswith("# "):
            current = None
            continue
        if current is None:
            continue
        field = FIELD_RE.match(line.strip())
        if field:
            key = field.group(1) or field.group(3)
            value = field.group(2) if field.group(1) else field.group(4)
            current.fields[key.strip()] = value.strip()
    return blocks


def matches(block, finding):
    """Passt der Block zu diesem Befund?

    Die Ueberschrift traegt den Betreff, so wie das Protokoll es vorsieht.
    Der Pruefpunktname darf in der Ueberschrift oder im Feld Pruefpunkt
    stehen; der Linter fuehrt beides in der Befundzeile.
    """
    if not names(block.subject, finding.subject):
        return False
    if not (names(block.subject, finding.check)
            or names(block.value("Prüfpunkt"), finding.check)):
        return False
    return block.level == finding.level


def apply(findings, path, today=None):
    """Gibt (akzeptierte Befunde, Meldungen) zurueck.

    Akzeptiert werden nur F3-Befunde: F4 blockiert ohne Ausnahme, und was
    milder als F3 ist, braucht keine Freigabe.
    """
    if not path:
        return [], []
    today = today or datetime.date.today()
    blocks = parse(path)
    messages = []
    accepted = []
    used = set()

    for finding in findings:
        if finding.level != "F3":
            continue
        for index, block in enumerate(blocks):
            if not matches(block, finding):
                continue
            problems = block.problems(today)
            if problems:
                for problem in problems:
                    messages.append(
                        "Block '%s' (Zeile %d) akzeptiert %s %s nicht: %s"
                        % (block.subject, block.line, finding.check,
                           finding.subject, problem))
                continue
            accepted.append(finding)
            used.add(index)
            break

    for index, block in enumerate(blocks):
        if index in used:
            continue
        problems = block.problems(today)
        if problems:
            # Ein Block, der zu keinem Befund passt und ausserdem
            # unvollstaendig ist, hat bisher gar nichts gemeldet. Genau so
            # sah die Datei aus, die die Akzeptanz verweigerte und trotzdem
            # als Akzeptanz wirkte.
            messages.append(
                "Block '%s' (Zeile %d) ist keine gueltige Akzeptanz: %s"
                % (block.subject, block.line, "; ".join(problems)))
            continue
        messages.append(
            "Block '%s' (Zeile %d) passt zu keinem offenen F3-Befund"
            % (block.subject, block.line))

    if not blocks:
        messages.append(
            "Datei %s enthaelt keinen Block '## Risiko-Akzeptanz: <Betreff>'"
            % path)
    return accepted, messages
