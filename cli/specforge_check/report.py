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
    "no_stories": "Keine pruefbare Story",
    "ears_coverage": "EARS-Formulierung",
    "gherkin_minimum": "Gherkin-Szenarien",
    "vague_terms": "Vage Begriffe (AP-04)",
    "sophist": "SOPHIST-Verletzung (AP-08)",
    "open_marker": "Offene Marker",
    "id_schema": "ID-Schema",
    "id_unique": "ID-Eindeutigkeit",
    "orphan_task": "Orphan Task (AP-07)",
    "orphan_story": "Orphan Spec (AP-07)",
    "nfr_gap": "NFR-Luecke",
    "nfr_severity": "F-Stufe der NFR-Luecke",
}

# Die AP-07-Pruefpunkte. Sie brauchen eine tasks.md; ohne sie hat dieser
# Lauf sie nicht angesehen.
TRACEABILITY_CHECKS = ("orphan_task", "orphan_story")

# Die Stufe "nicht anwendbar". Symbol und Gate-Ergebnis stehen in
# severity.GATE und werden von dort geholt, damit die F-Stufen-Tabelle aus
# enforcement-engine.md genau eine Abbildung im Code hat.
SKIP_LEVEL = "F5"

GATES = (
    ("G1", "Specify → Clarify",
     ("no_stories", "id_schema", "id_unique", "ears_coverage",
      "gherkin_minimum", "vague_terms", "sophist", "open_marker",
      "nfr_gap", "nfr_severity")),
    ("G4", "Analyze → Implement", TRACEABILITY_CHECKS),
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
        out.append(line("Gate %s: %s" % (gate, title)))
        if gate == "G4" and tasks is None:
            # Frueher fiel das Gate hier kommentarlos aus der Ausgabe. Eine
            # geloeschte oder falsch abgelegte tasks.md nahm damit die
            # AP-07-Pruefung heraus, und uebrig blieb ein Bericht, der nach
            # bestandenem Lauf aussah. Das Gate steht jetzt da und sagt,
            # dass es nichts geprueft hat.
            symbol, result = _symbol(SKIP_LEVEL)
            out.append("%s [%s] keine tasks.md gefunden: %s nicht geprueft"
                       % (symbol, SKIP_LEVEL,
                          " und ".join(LABELS[c] for c in checks)))
            out.append("   └─ tasks.md neben die spec.md legen oder mit "
                       "--tasks angeben; dieser Lauf sagt nichts ueber die "
                       "Nachverfolgbarkeit")
            out.append(line("Ergebnis: %s" % result))
            out.append("")
            continue
        printed = False
        skipped = False
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
            if gate == "G1":
                scope = "%d/%d Stories" % (len(spec.stories),
                                           len(spec.stories))
                empty = not spec.stories
            else:
                scope = "%d Tasks" % len(tasks or [])
                empty = not tasks
            if empty:
                # "Alle Pruefpunkte erfuellt" bei null Pruefgegenstaenden
                # ist eine Aussage ueber nichts. Sie wird hier nicht
                # gemacht, und das Ergebnis heisst dann auch nicht PASS.
                out.append("%s [%s] Nichts Pruefbares gefunden: %s"
                           % (_symbol(SKIP_LEVEL)[0], SKIP_LEVEL, scope))
                skipped = True
            else:
                out.append("✅ [F0] Alle Pruefpunkte erfuellt: %s" % scope)
        levels = [f.level for f in findings
                  if f.check in checks and f not in accepted]
        result = _symbol(SKIP_LEVEL)[1] if skipped else gate_result(levels)
        out.append(line("Ergebnis: %s" % result))
        out.append("")

    return out


def _symbol(level):
    result, symbol, _ = severity.GATE[level][0], severity.GATE[level][1], None
    return symbol, result


def skipped_checks(tasks):
    """Pruefpunkte, die dieser Lauf nicht angesehen hat.

    Ohne tasks.md laeuft AP-07 nicht. Wer die Ausgabe als JSON
    weiterverarbeitet, soll das an der Ausgabe sehen und nicht daran, dass
    zwei Pruefpunkte in findings fehlen.
    """
    return [] if tasks is not None else list(TRACEABILITY_CHECKS)


def as_json(spec, findings, accepted, acceptance_messages=(), tasks=None):
    return json.dumps({
        "spec": spec.path,
        "stories": [story.id for story in spec.stories],
        "skipped_checks": skipped_checks(tasks),
        "acceptance_problems": list(acceptance_messages),
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
