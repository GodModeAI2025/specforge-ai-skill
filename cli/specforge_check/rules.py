# -*- coding: utf-8 -*-
"""Die Regeln, die ohne Sprachmodell entscheidbar sind.

Jede Regel traegt den Namen, unter dem sie in checks_config konfigurierbar
ist, und eine Default-F-Stufe. Die Defaults sind nicht erfunden, sie stehen
im Payload:

  ears_coverage     F4  Gate G1, references/01-specify.md, 07-review.md
  gherkin_minimum   F4  Gate G1, references/09-discover.md, 08-management.md
  vague_terms       F4  AP-04, Gate G2
  sophist           F3  AP-08
  open_marker       F3  SKILL.md, globale Regel 11
  id_schema         F1  references/01-specify.md, 07-review.md RQ-08
  id_unique         F4  doppelte ID bricht die Nachverfolgbarkeit
  orphan_task       F3  AP-07, references/08-management.md TM-02
  orphan_story      F3  AP-07, references/08-management.md
  nfr_severity      F3  falsch eingestufte NFR-Luecke, Gate G1 NFR-Scan

Die Regel no_stories hat ebenfalls keine konfigurierbare Stufe. Sie steht
fest auf F4, siehe NO_STORIES_LEVEL.

Die Regel nfr_gap hat keine Default-Stufe. Ihre F-Stufe steht im Marker
selbst ([NFR-Lücke F4: IRM-01 — ...]), so wie enforcement-engine.md das
NFR-Luecken-Format festlegt.

Wer einen anderen Wert braucht, setzt ihn in checks_config, nicht hier.
"""

import os
import re

# AP-04, Blocklist aus SKILL.md, globale Regel 4. Die Endungen decken die
# deutsche Beugung ab, ohne Woerter zu treffen, die den Stamm nur enthalten
# ("Sicherheit", "sicherstellen", "Vereinfachung").
VAGUE_TERMS = {
    "schnell": r"schnell(?:e[nmrs]?|es)?",
    "viele": r"viel(?:e[nmrs]?|es)?",
    "einfach": r"einfach(?:e[nmrs]?|es)?",
    "skalierbar": r"skalierbar(?:e[nmrs]?|es)?",
    "sicher": r"sicher(?:e[nmrs]?|es)?",
    "zuverlässig": r"zuverlässig(?:e[nmrs]?|es)?",
}

# AP-08, SOPHIST-Blocklist aus enforcement-engine.md. Aufgenommen sind nur
# die eindeutigen Trigger. "z.B." und "u.a." stehen dort mit der Einschraenkung
# "als einzige Spezifikation" und sind ohne Bedeutungspruefung nicht
# entscheidbar; sie bleiben der Session ueberlassen.
SOPHIST_TERMS = {
    "ggf.": r"ggf\.",
    "evtl.": r"evtl\.",
    "etc.": r"etc\.",
    "usw.": r"usw\.",
    "zeitnah": r"zeitnah",
    "umgehend": r"umgehend",
    "normalerweise": r"normalerweise",
    "in der Regel": r"in der Regel",
    "falls möglich": r"falls möglich",
    "regelmäßig": r"regelmäßig",
}

DEFAULTS = {
    "ears_coverage": "F4",
    "gherkin_minimum": "F4",
    "vague_terms": "F4",
    "sophist": "F3",
    "open_marker": "F3",
    "id_schema": "F1",
    "id_unique": "F4",
    "orphan_task": "F3",
    "orphan_story": "F3",
    "nfr_severity": "F3",
}

# Kategorie-Praefix einer NFR-Luecke: IRM-01, DAT-03, AVA-02.
NFR_ID_RE = re.compile(r"^([A-Z]{2,5})-(\d{2})\b")

GHERKIN_MINIMUM = 2

# Eine spec.md ohne erkannte Story ist der Fall, in dem der Linter am
# meisten schadet: er hat nichts geprueft und meldet trotzdem ein Ergebnis.
# Ein abgeschnittenes Artefakt, ein Pfad auf das falsche Verzeichnis, ein
# Story-Kopf in eigener Schreibweise sehen dann alle aus wie eine saubere
# Spec. Die Stufe steht deshalb hier und nicht in checks_config: wer sie
# herunterkonfigurieren koennte, haette das Loch wieder.
NO_STORIES_LEVEL = "F4"


class Finding(object):
    def __init__(self, check, level, subject, message, line=None,
                 remedy=None):
        self.check = check
        self.level = level
        self.subject = subject
        self.message = message
        self.line = line
        self.remedy = remedy

    def __repr__(self):
        return "<%s %s %s>" % (self.level, self.check, self.subject)


def _compiled(mapping):
    return [(label, re.compile(r"\b" + pattern + r"\b", re.I))
            for label, pattern in sorted(mapping.items())]


VAGUE_RE = _compiled(VAGUE_TERMS)
SOPHIST_RE = [(label, re.compile(pattern, re.I))
              for label, pattern in sorted(SOPHIST_TERMS.items())]


def check_no_stories(spec, config):
    """Kein Story-Kopf erkannt: der Lauf hat nichts geprueft.

    Leere Datei und Datei mit fremdem Story-Format sind zwei verschiedene
    Ursachen und bekommen zwei verschiedene Meldungen. Beide sind ein
    Befund, kein Ergebnis.
    """
    if spec.stories:
        return []
    if any(line.strip() for line in spec.lines):
        message = ("kein Story-Kopf im Format '### [SF-XXX-NNN] Titel' "
                   "gefunden")
        remedy = ("Story-Koepfe nach docs/spec-format.md schreiben; die "
                  "Datei hat Inhalt, aber keinen erkennbaren Abschnitt")
    else:
        message = "Datei ist leer"
        remedy = "Pfad pruefen: hier liegt keine ausgefuellte Spezifikation"
    return [Finding("no_stories", NO_STORIES_LEVEL,
                    os.path.basename(spec.path), message, None, remedy)]


def level_for(config, check):
    return config.severity_for(check, DEFAULTS[check])


def check_ears(spec, config):
    level = level_for(config, "ears_coverage")
    findings = []
    from .spec import known_pattern, EARS_PATTERNS
    for story in spec.stories:
        if story.pattern is None:
            findings.append(Finding(
                "ears_coverage", level, story.id,
                "kein Feld **Pattern:** in der Story", story.line,
                "Pattern ergaenzen, erlaubt: " + ", ".join(EARS_PATTERNS)))
        elif not known_pattern(story.pattern):
            findings.append(Finding(
                "ears_coverage", level, story.id,
                "unbekanntes EARS-Pattern %r" % story.pattern, story.line,
                "erlaubt: " + ", ".join(EARS_PATTERNS)))
    return findings


def check_gherkin(spec, config):
    level = level_for(config, "gherkin_minimum")
    findings = []
    for story in spec.stories:
        count = len(story.scenarios)
        if count < GHERKIN_MINIMUM:
            findings.append(Finding(
                "gherkin_minimum", level, story.id,
                "%d Szenario/Szenarien, mindestens %d verlangt"
                % (count, GHERKIN_MINIMUM), story.line,
                "Fehlerfall als zweites Scenario ergaenzen (AP-06)"))
    return findings


# Marker sind ausdruecklich vorlaeufig. Ein vager Begriff innerhalb von
# [Annahme: ...] oder [Offen: ...] ist kein AP-04-Befund, sondern genau das,
# wofuer der Marker da ist. Er faellt in Clarify auf, nicht hier.
PROVISIONAL_RE = re.compile(r"\[(?:Annahme|Offen|NFR-Lücke)[^\]]*\]")


def _scan(story, patterns, check, level, kind, remedy):
    findings = []
    seen = set()
    for number, line in story.lines:
        text = PROVISIONAL_RE.sub("", line)
        for label, expression in patterns:
            if label in seen:
                continue
            if expression.search(text):
                seen.add(label)
                findings.append(Finding(
                    check, level, story.id, "%s %r" % (kind, label), number,
                    remedy))
    return findings


def check_vague(spec, config):
    level = level_for(config, "vague_terms")
    findings = []
    for story in spec.stories:
        findings.extend(_scan(story, VAGUE_RE, "vague_terms", level,
                              "vager Begriff",
                              "durch messbaren Wert ersetzen (AP-04)"))
    return findings


def check_sophist(spec, config):
    level = level_for(config, "sophist")
    findings = []
    for story in spec.stories:
        findings.extend(_scan(story, SOPHIST_RE, "sophist", level,
                              "unbestimmte Formulierung",
                              "Bedingung oder Aufzaehlung ausschreiben "
                              "(AP-08)"))
    return findings


def check_markers(spec, config, after_clarify):
    """Offene [Annahme:]- und [Offen:]-Marker.

    Vor Clarify sind beide legitim, danach nicht mehr. Deshalb laeuft die
    Regel nur mit --nach-clarify.
    """
    if not after_clarify:
        return []
    level = level_for(config, "open_marker")
    findings = []
    for story in spec.stories:
        for number, kind, text in story.markers:
            findings.append(Finding(
                "open_marker", level, story.id,
                "offener Marker [%s: %s]" % (kind, text[:40]), number,
                "in Clarify (Modus 2) aufloesen"))
    return findings


def check_ids(spec, config):
    from .spec import valid_id, ID_PREFIXES
    findings = []
    schema_level = level_for(config, "id_schema")
    unique_level = level_for(config, "id_unique")
    seen = {}
    for story in spec.stories:
        if not valid_id(story.id):
            findings.append(Finding(
                "id_schema", schema_level, story.id,
                "ID folgt nicht SF-{Praefix}-{NNN}", story.line,
                "gueltige Praefixe: " + ", ".join(ID_PREFIXES)))
        if story.id in seen:
            findings.append(Finding(
                "id_unique", unique_level, story.id,
                "ID schon in Zeile %d vergeben" % seen[story.id], story.line,
                "eine ID zeigt auf genau eine Anforderung"))
        else:
            seen[story.id] = story.line
    return findings


def check_traceability(spec, tasks, config):
    """AP-07: Task ohne Story, Story ohne Task."""
    if tasks is None:
        return []
    findings = []
    task_level = level_for(config, "orphan_task")
    story_level = level_for(config, "orphan_story")
    known = set(story.id for story in spec.stories)
    referenced = set()
    for task_id, number, refs in tasks:
        valid = [ref for ref in refs if ref in known]
        referenced.update(valid)
        if not valid:
            findings.append(Finding(
                "orphan_task", task_level, task_id,
                "kein Verweis auf eine Story dieser Spec", number,
                "Story-ID im Task ergaenzen (AP-07)"))
    for story in spec.stories:
        if story.id not in referenced:
            findings.append(Finding(
                "orphan_story", story_level, story.id,
                "keine Entsprechung in tasks.md", story.line,
                "Task anlegen oder Story streichen (AP-07)"))
    return findings


def check_nfr_gaps(spec, config, packages):
    """Dokumentierte NFR-Luecken und ihre F-Stufe.

    Eine Luecke ist ein Befund in der Stufe, die der Marker nennt. Zusaetzlich
    wird die Stufe gegen die F-Stufen-Tabelle der aktiven Extension geprueft:
    dieselbe Kategorie bekommt je nach Perspektive eine andere Stufe, und
    genau das ist der Punkt, an dem eine pauschale Einstufung ein Gate zu
    hart oder zu weich macht.
    """
    from .extensions import allowed_levels
    findings = []
    severity_level = level_for(config, "nfr_severity")
    for story in spec.stories:
        for number, level, text in story.nfr_gaps:
            identifier = text.split("—")[0].strip()
            match = NFR_ID_RE.match(identifier)
            category = match.group(1) if match else None
            findings.append(Finding(
                "nfr_gap", level, identifier or story.id,
                "NFR-Luecke in Story %s" % story.id, number,
                "Anforderung spezifizieren oder F5 mit Begruendung "
                "dokumentieren"))
            if not category or not packages:
                continue
            allowed = allowed_levels(packages, category,
                                     config.perspective)
            if allowed and level not in allowed:
                findings.append(Finding(
                    "nfr_severity", severity_level, identifier,
                    "als %s eingestuft, die Perspektive %s verlangt %s"
                    % (level, config.perspective or "_default",
                       " oder ".join(sorted(allowed))), number,
                    "F-Stufe aus der F-Stufen-Zuordnung der Extension "
                    "uebernehmen"))
    return findings


def run(spec, tasks, config, after_clarify=False, packages=None):
    findings = []
    findings.extend(check_no_stories(spec, config))
    findings.extend(check_ids(spec, config))
    findings.extend(check_ears(spec, config))
    findings.extend(check_gherkin(spec, config))
    findings.extend(check_vague(spec, config))
    findings.extend(check_sophist(spec, config))
    findings.extend(check_markers(spec, config, after_clarify))
    findings.extend(check_nfr_gaps(spec, config, packages or {}))
    findings.extend(check_traceability(spec, tasks, config))
    return findings
