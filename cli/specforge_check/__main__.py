# -*- coding: utf-8 -*-
"""Kommandozeile: specforge check.

    python -m specforge_check <pfad> [optionen]
    cli/specforge check <pfad> [optionen]

<pfad> ist eine spec.md oder ein Verzeichnis, das eine enthaelt. Liegt eine
tasks.md daneben, wird sie mitgeprueft.

Exit-Codes:

    0  kein F4, kein offener F3
    1  mindestens ein F4-Befund — Gate blockiert
    2  mindestens ein F3-Befund ohne dokumentierte Risiko-Akzeptanz
    3  Aufrufproblem (Datei fehlt, Datei unlesbar)

Nur Standardbibliothek.
"""

import argparse
import os
import re
import sys

if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    from specforge_check import config as config_mod
    from specforge_check import report, rules, spec as spec_mod
else:
    from . import config as config_mod
    from . import report, rules, spec as spec_mod

ACCEPT_BLOCK_RE = re.compile(r"^##\s+Risiko-Akzeptanz\s*:", re.M)


def resolve(target):
    """Gibt (spec_pfad, tasks_pfad) zurueck."""
    if os.path.isdir(target):
        spec_path = os.path.join(target, "spec.md")
        tasks_path = os.path.join(target, "tasks.md")
        return spec_path, tasks_path if os.path.isfile(tasks_path) else None
    directory = os.path.dirname(os.path.abspath(target))
    tasks_path = os.path.join(directory, "tasks.md")
    return target, tasks_path if os.path.isfile(tasks_path) else None


def load_acceptance(path):
    """Blöcke aus dem CONDITIONAL-Akzeptanz-Protokoll.

    Format siehe enforcement-engine.md, Abschnitt "CONDITIONAL-Akzeptanz-
    Protokoll". Ein Block akzeptiert einen Befund, wenn er sowohl den
    Pruefpunkt-Namen als auch den Betreff nennt.
    """
    if not path:
        return []
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    parts = ACCEPT_BLOCK_RE.split(text)
    return [part for part in parts[1:] if part.strip()]


def accepted_findings(findings, blocks):
    accepted = []
    for finding in findings:
        if finding.level != "F3":
            continue
        for block in blocks:
            if finding.check in block and finding.subject in block:
                accepted.append(finding)
                break
    return accepted


def build_parser():
    parser = argparse.ArgumentParser(
        prog="specforge check",
        description="Prueft eine spec.md gegen die strukturellen Regeln des "
                    "SpecForge-Skills und meldet F-Stufen.")
    parser.add_argument("pfad", help="spec.md oder Verzeichnis")
    parser.add_argument("--tasks", help="tasks.md fuer die Traceability-"
                                        "Pruefung (sonst neben der Spec)")
    parser.add_argument("--config", help="specforge.json (sonst wird ab der "
                                          "Spec aufwaerts gesucht)")
    parser.add_argument("--nach-clarify", dest="after_clarify",
                        action="store_true",
                        help="offene [Annahme:]- und [Offen:]-Marker "
                             "beanstanden")
    parser.add_argument("--risiko-akzeptanz", dest="acceptance",
                        help="Datei mit CONDITIONAL-Akzeptanz-Protokollen")
    parser.add_argument("--json", dest="as_json", action="store_true",
                        help="Befunde als JSON statt als Gate-Ausgabe")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)

    spec_path, tasks_path = resolve(args.pfad)
    if args.tasks:
        tasks_path = args.tasks
    if not os.path.isfile(spec_path):
        sys.stderr.write("FEHLER: keine spec.md unter %s\n" % spec_path)
        return 3
    if tasks_path and not os.path.isfile(tasks_path):
        sys.stderr.write("FEHLER: tasks.md nicht gefunden: %s\n" % tasks_path)
        return 3

    config_path = args.config or config_mod.find(spec_path)
    configuration = config_mod.load(config_path)

    document = spec_mod.parse_spec(spec_path)
    tasks = spec_mod.parse_tasks(tasks_path) if tasks_path else None

    findings = rules.run(document, tasks, configuration, args.after_clarify)
    accepted = accepted_findings(findings, load_acceptance(args.acceptance))

    if args.as_json:
        print(report.as_json(document, findings, accepted))
    else:
        print("specforge check %s" % spec_path)
        print("Profil: %s · Perspektive: %s · Konfiguration: %s"
              % (configuration.profile or "nicht gesetzt",
                 configuration.perspective or "nicht gesetzt",
                 config_path or "keine"))
        if configuration.legacy:
            print("Hinweis: specforge.json ohne severity_model — "
                  "Legacy-Werte werden beim Einlesen einmal uebersetzt.")
        print("")
        for line in report.render(document, findings, tasks, accepted):
            print(line)

    open_levels = [f.level for f in findings if f not in accepted]
    if "F4" in open_levels:
        return 1
    if "F3" in open_levels:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
