# -*- coding: utf-8 -*-
"""Parser fuer spec.md und tasks.md.

Das Format ist in docs/spec-format.md festgeschrieben. Der Parser haelt sich
daran und raet nicht: was er nicht sicher erkennt, meldet er nicht als
erkannt, sondern gar nicht. Ein Checker, der zuviel errät, produziert
Befunde, die niemand nachvollziehen kann.
"""

import re

STORY_RE = re.compile(r"^###\s+\[([A-Za-z0-9_-]+)\]\s*(.*)$")
SECTION_RE = re.compile(r"^##\s+")
# **Pattern:** Wert und **Pattern**: Wert — beide Formen stehen im Template.
FIELD_RE = re.compile(r"^\*\*([^*:]+?)\*\*\s*:\s*(.*)$|^\*\*([^*:]+?):\*\*\s*(.*)$")
SCENARIO_RE = re.compile(r"^\s*Scenario:\s*(.*)$")
GHERKIN_STEP_RE = re.compile(r"^\s*(Given|When|Then|And|But)\b", re.I)
ID_RE = re.compile(r"^SF-([A-Z]{3,4})-(\d{3})$")
TASK_RE = re.compile(r"\bT-(\d{3})\b")
STORY_REF_RE = re.compile(r"\bSF-[A-Z]{3,4}-\d{3}\b")

MARKER_RE = re.compile(r"\[(Annahme|Offen)\s*:\s*([^\]]*)\]")
NFR_GAP_RE = re.compile(r"\[NFR-Lücke\s+F(\d)\s*:\s*([^\]]*)\]")

EARS_PATTERNS = ("Ubiquitous", "Event-Driven", "State-Driven", "Optional",
                 "Unwanted")
# Praefixe laut spec-template.md, Abschnitt ID-Schema.
ID_PREFIXES = ("FUNC", "SEC", "AVA", "INT", "AUD", "PER", "USA", "COM",
               "OPS", "DAT")


class Story(object):
    def __init__(self, ident, title, line):
        self.id = ident
        self.title = title
        self.line = line
        self.fields = {}
        self.scenarios = []
        self.markers = []
        self.nfr_gaps = []
        self.lines = []

    @property
    def pattern(self):
        return self.fields.get("Pattern")

    def __repr__(self):
        return "<Story %s, %d Szenarien>" % (self.id, len(self.scenarios))


class Spec(object):
    def __init__(self, path):
        self.path = path
        self.stories = []
        self.lines = []

    @property
    def text(self):
        return "\n".join(self.lines)


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read().split("\n")


def parse_spec(path):
    """Liest eine spec.md und gibt ein Spec-Objekt zurueck."""
    spec = Spec(path)
    spec.lines = read(path)

    current = None
    in_fence = False
    for number, line in enumerate(spec.lines, 1):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            if current is not None:
                current.lines.append((number, line))
            continue

        head = STORY_RE.match(line)
        if head:
            current = Story(head.group(1).strip(), head.group(2).strip(),
                            number)
            spec.stories.append(current)
            continue
        if SECTION_RE.match(line):
            current = None
            continue
        if current is None:
            continue

        current.lines.append((number, line))

        field = FIELD_RE.match(line)
        if field:
            key = field.group(1) or field.group(3)
            value = field.group(2) if field.group(1) else field.group(4)
            current.fields[key.strip()] = value.strip()

        scenario = SCENARIO_RE.match(line)
        if scenario:
            current.scenarios.append((number, scenario.group(1).strip()))

        for marker in MARKER_RE.finditer(line):
            current.markers.append((number, marker.group(1),
                                    marker.group(2).strip()))
        for gap in NFR_GAP_RE.finditer(line):
            current.nfr_gaps.append((number, "F" + gap.group(1),
                                     gap.group(2).strip()))

    return spec


def parse_tasks(path):
    """Liest eine tasks.md und gibt [(task_id, zeile, [story_ids])] zurueck."""
    tasks = []
    for number, line in enumerate(read(path), 1):
        match = TASK_RE.search(line)
        if not match:
            continue
        refs = STORY_REF_RE.findall(line)
        tasks.append(("T-" + match.group(1), number, refs))
    return tasks


def valid_id(ident):
    match = ID_RE.match(ident)
    if not match:
        return False
    return match.group(1) in ID_PREFIXES


def known_pattern(value):
    if not value:
        return False
    return value.strip().lower() in [p.lower() for p in EARS_PATTERNS]
