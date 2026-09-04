#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Haelt das Schweregrad-Vokabular auf einem Dialekt.

SpecForge hatte zwei Skalen nebeneinander: die F-Stufen F0 bis F5 aus
references/enforcement/enforcement-engine.md und die aelteren Werte BLOCKER,
MAJOR und MINOR in der Modulprosa. Beide beschreiben denselben Befund, das
Mapping zwischen ihnen ist aber verlustbehaftet: F0, F2 und F5 sind ueber den
Legacy-Weg nicht erreichbar. Wer die alten Werte in einer neuen Regel
verwendet, erzeugt damit ein Gate, das strenger blockiert als das Regelwerk
verlangt.

Das Skript prueft drei Dinge:

1. BLOCKER, MAJOR und MINOR kommen nur noch an einer einzigen Stelle vor:
   im Abschnitt "Abwaertskompatibilitaet (Legacy-Mapping)" der
   enforcement-engine.md. Dort sind sie der Eingangs-Uebersetzer fuer alte
   specforge.json-Dateien ohne severity_model und nichts sonst. Die
   Versionsnotation MAJOR.MINOR.PATCH ist keine Schweregrad-Angabe und wird
   vorher aus dem Text genommen. Gesucht wird ohne Ruecksicht auf Gross- und
   Kleinschreibung, denn "Ein Blocker im Gate" ist die naheliegende deutsche
   Schreibweise und war bis dahin unsichtbar. Ausgenommen sind die
   Meldekategorien "Major Incident" und "Klassifikation als Major" aus DORA
   Art. 19: dort ist Major ein Vorfalltyp und keine Schwere.
2. Die Kurzform der alten Skala, die Spalte "(B/M/m)", kommt nirgends mehr
   vor. Sie ist derselbe zweite Dialekt in drei Buchstaben und wurde von der
   Suche nach den ausgeschriebenen Werten nie gesehen.
3. Jede F-Stufen-Angabe im Payload liegt zwischen F0 und F5. Ein F6 waere
   ein Tippfehler, den sonst niemand bemerkt, weil er wie eine gueltige
   Stufe aussieht.

Geprueft werden alle Markdown- und HTML-Dateien des Repos ausser den
Verzeichnissen .git und dist. Ausgenommen ist docs/f-stufen-entscheidung.md:
die Entscheidungsdokumentation der Umstellung muss die alten Werte nennen
duerfen, sonst laesst sich nicht nachlesen, welcher Pruefpunkt vorher welchen
Wert hatte.

Die dritte Pruefung laeuft nur ueber den Payload, also SKILL.md und
references/. In README und Landingpage ist ein F gefolgt von einer Ziffer
nicht zwingend eine F-Stufe.

Exit 0 wenn alles stimmt, sonst 1. Nur Standardbibliothek.
"""

import os
import re
import sys

# Ohne IGNORECASE blieb "Ein Blocker im Gate" unsichtbar, also gerade die
# Schreibweise, die im deutschen Fliesstext naheliegt. Die Endungen decken
# die Beugung ab ("Blockern", "Blockers").
LEGACY_RE = re.compile(r"\b(BLOCKER|MAJOR|MINOR)(?:N|S)?\b", re.I)
# Die Kurzform derselben Skala. Sie stand als Spaltenkopf "Befunde (B/M/m)"
# im ausgelieferten Report-Template, neben einer Gesamtbewertung mit vier
# F-Stufen, und wurde von der Suche oben nie erfasst.
SHORT_SCALE_RE = re.compile(r"\(\s*B\s*/\s*M\s*/\s*m\s*\)")
# MAJOR.MINOR und v{MAJOR}.{MINOR}.{PATCH} sind Versionsangaben, keine
# Schweregrade. Sie werden vor der Suche entfernt, nicht als Treffer gewertet.
SEMVER_RE = re.compile(r"\{?MAJOR\}?\.\{?MINOR\}?(?:\.\{?PATCH\}?)?", re.I)
# Fachbegriffe der Regulierung. DORA Art. 19 fuehrt den "Major Incident" als
# Meldekategorie; das Wort bezeichnet dort einen Vorfalltyp und nicht die
# Schwere eines Befunds. Diese Liste ist so kurz wie moeglich zu halten:
# jeder weitere Eintrag ist eine Stelle, an der der zweite Dialekt
# zurueckkommen kann.
FACHBEGRIFF_RE = re.compile(r"Major[- ]Incidents?|als Major\b", re.I)
F_LEVEL_RE = re.compile(r"\bF\s?(\d+)\b")

SKIP_DIRS = (".git", "dist", "node_modules", "__pycache__")
SUFFIXES = (".md", ".html")

# Der einzige Ort im Payload, an dem die Legacy-Werte stehen duerfen.
ALLOWED_FILE = "references/enforcement/enforcement-engine.md"
ALLOWED_HEADING = "### Abwärtskompatibilität (Legacy-Mapping)"

# Die Entscheidungsdokumentation der Umstellung. Sie haelt fest, welcher
# Pruefpunkt vorher welchen Wert hatte, und muss die alten Werte deshalb
# nennen koennen. Sie liegt ausserhalb des Payloads und wird nicht
# ausgeliefert. Diese Liste ist bewusst kurz zu halten: jede weitere Datei
# darin ist eine Stelle, an der der zweite Dialekt zurueckkehren kann.
ALLOWED_FILES = ("docs/f-stufen-entscheidung.md",)


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def source_files(root):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames
                             if d not in SKIP_DIRS and not d.startswith("."))
        for name in sorted(filenames):
            if not name.endswith(SUFFIXES):
                continue
            path = os.path.join(dirpath, name)
            files.append(os.path.relpath(path, root).replace(os.sep, "/"))
    return sorted(files)


def read_lines(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read().split("\n")


def allowed_range(lines):
    """Zeilennummern des Legacy-Mapping-Abschnitts, 1-basiert.

    Der Abschnitt beginnt bei seiner Ueberschrift und endet vor der naechsten
    Ueberschrift gleicher oder hoeherer Ebene. Verankert wird an der
    Ueberschrift, nicht an Zeilennummern, damit der Bereich mitwandert.
    """
    start = None
    for number, line in enumerate(lines, 1):
        if line.strip() == ALLOWED_HEADING:
            start = number
            continue
        if start is None:
            continue
        stripped = line.strip()
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            if level <= 3:
                return start, number - 1
    if start is None:
        return None
    return start, len(lines)


def is_payload(rel):
    return rel == "SKILL.md" or rel.startswith("references/")


def main():
    root = repo_root()
    errors = []
    checked = 0
    legacy_allowed = 0

    for rel in source_files(root):
        lines = read_lines(os.path.join(root, rel))
        checked += 1

        if rel in ALLOWED_FILES:
            print("Uebersprungen:           %s (Entscheidungsdokumentation)"
                  % rel)
            continue

        window = None
        if rel == ALLOWED_FILE:
            window = allowed_range(lines)
            if window is None:
                errors.append("%s: Abschnitt '%s' fehlt, damit hat das "
                              "Legacy-Mapping keinen definierten Ort"
                              % (rel, ALLOWED_HEADING))

        for number, line in enumerate(lines, 1):
            text = FACHBEGRIFF_RE.sub("", SEMVER_RE.sub("", line))
            if SHORT_SCALE_RE.search(line):
                errors.append("%s:%d: Kurzform (B/M/m) der alten Skala "
                              "statt F-Stufen: %s"
                              % (rel, number, line.strip()[:70]))
            for match in LEGACY_RE.finditer(text):
                if window is not None and window[0] <= number <= window[1]:
                    legacy_allowed += 1
                    continue
                errors.append("%s:%d: %s statt F-Stufe: %s"
                              % (rel, number, match.group(1),
                                 line.strip()[:70]))

            if not is_payload(rel):
                continue
            for level in F_LEVEL_RE.findall(line):
                if int(level) > 5:
                    errors.append("%s:%d: F%s gibt es nicht, gueltig ist F0 "
                                  "bis F5: %s"
                                  % (rel, number, level, line.strip()[:70]))

    print("Geprueft:                %d Markdown- und HTML-Dateien" % checked)
    print("Legacy-Mapping:          %s, %d zulaessige Vorkommen"
          % (ALLOWED_FILE, legacy_allowed))

    if errors:
        print("")
        print("FEHLER (%d):" % len(errors))
        for message in errors:
            print("  - %s" % message)
        return 1

    print("")
    print("OK: F-Stufen sind der einzige Schweregrad-Dialekt.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
