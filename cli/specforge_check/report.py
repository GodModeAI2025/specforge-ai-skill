# -*- coding: utf-8 -*-
"""Ausgabe im Gate-Ergebnis-Format.

Das Format steht in references/enforcement/enforcement-engine.md, Abschnitt
"Gate-Ergebnis-Format". Wer die Ausgabe des Checkers neben ein
Session-Protokoll legt, soll dieselbe Form sehen, sonst sind die beiden
Enforcement-Wege nicht vergleichbar.
"""

import json

from . import severity

LABELS = {
    "ears_coverage": "EARS-Formulierung",
    "gherkin_minimum": "Gherkin-Szenarien",
    "vague_terms": "Vage Begriffe (AP-04)",
    "sophist": "SOPHIST-Verletzung (AP-08)",
    "open_marker": "Offene Marker",
    "id_schema": "ID-Schema",
    "id_unique": "ID-Eindeutigkeit",
    "orphan_task": "Orphan Task (AP-07)",
    "orphan_story": "Orphan Spec (AP-07)",
}

GATES = (
    ("G1", "Specify → Clarify",
     ("id_schema", "id_unique", "ears_coverage", "gherkin_minimum",
      "vague_terms", "sophist", "open_marker")),
    ("G4", "Analyze → Implement", ("orphan_task", "orphan_story")),
)

RULE = "─"


def line(text, width=46):
    filler = max(1, width - len(text) - 4)
    return "── %s %s" % (text, RULE * filler)


def gate_result(levels):
    if "F4" in levels:
        return "FAIL"
    if "F3" in levels:
        return "CONDITIONAL"
    if "F2" in levels:
        return "WARNING"
    return "PASS"


def render(spec, findings, tasks, accepted):
    """Gibt die Textausgabe als Liste von Zeilen zurueck."""
    out = []
    by_check = {}
    for finding in findings:
        by_check.setdefault(finding.check, []).append(finding)

    for gate, title, checks in GATES:
        active = [c for c in checks if c in by_check]
        if gate == "G4" and tasks is None:
            continue
        out.append(line("Gate %s: %s" % (gate, title)))
        printed = False
        for check in checks:
            hits = by_check.get(check)
            if not hits:
                continue
            printed = True
            for finding in sorted(hits, key=lambda f: severity.rank(f.level)):
                symbol, result = _symbol(finding.level)
                suffix = " — akzeptiert" if finding in accepted else ""
                out.append("%s [%s] %s: %s — %s — %s%s"
                           % (symbol, finding.level, LABELS[check],
                              finding.subject, finding.message, result,
                              suffix))
                if finding.remedy:
                    out.append("   └─ %s" % finding.remedy)
        if not printed:
            scope = ("%d/%d Stories" % (len(spec.stories), len(spec.stories))
                     if gate == "G1" else "%d Tasks" % len(tasks or []))
            out.append("✅ [F0] Alle Pruefpunkte erfuellt: %s" % scope)
        levels = [f.level for f in findings
                  if f.check in checks and f not in accepted]
        result = gate_result(levels)
        out.append(line("Ergebnis: %s" % result))
        out.append("")

    return out


def _symbol(level):
    result, symbol, _ = severity.GATE[level][0], severity.GATE[level][1], None
    return symbol, result


def as_json(spec, findings, accepted):
    return json.dumps({
        "spec": spec.path,
        "stories": [story.id for story in spec.stories],
        "findings": [{
            "check": finding.check,
            "severity": finding.level,
            "subject": finding.subject,
            "line": finding.line,
            "message": finding.message,
            "accepted": finding in accepted,
        } for finding in sorted(
            findings, key=lambda f: (severity.rank(f.level), f.check,
                                     f.subject))],
    }, ensure_ascii=False, indent=2, sort_keys=False)
