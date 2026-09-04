#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Faehrt specforge check ueber die Golden Specs und vergleicht mit expected.json.

Ebene 1 der Eval-Suite: deterministisch, ohne Netz, ohne Modell, ohne
Schluessel. Was hier gruen ist, bleibt gruen — eine Abweichung ist eine
Regression und keine Schwankung.

Ebene 2, also das Nachfahren derselben Faelle durch die Claude-API, ist
bewusst nicht Teil dieses Skripts. Ein Lauf gegen ein Sprachmodell ist nicht
reproduzierbar und gehoert nicht in eine Pipeline, die bei jedem Push laeuft.

Aufruf:

    python3 evals/run_static.py            alle Faelle
    python3 evals/run_static.py 04         nur passende Faelle
    python3 evals/run_static.py --ausgabe  zusaetzlich die Gate-Ausgabe zeigen

Exit 0 wenn alle Faelle bestehen, sonst 1. Nur Standardbibliothek.
"""

import json
import os
import subprocess
import sys

GOLDEN = "golden"
EXPECTED = "expected.json"


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def cases(root, filters):
    base = os.path.join(root, "evals", GOLDEN)
    found = []
    for name in sorted(os.listdir(base)):
        directory = os.path.join(base, name)
        if not os.path.isfile(os.path.join(directory, EXPECTED)):
            continue
        if filters and not any(needle in name for needle in filters):
            continue
        found.append((name, directory))
    return found


def load_expected(directory):
    with open(os.path.join(directory, EXPECTED), encoding="utf-8") as handle:
        return json.load(handle)


def run_check(root, directory, extra=()):
    command = [sys.executable, os.path.join(root, "cli", "specforge"),
               "check", directory, "--json"] + list(extra)
    return subprocess.run(command, capture_output=True, text=True)


def gate_output(root, directory):
    command = [sys.executable, os.path.join(root, "cli", "specforge"),
               "check", directory]
    return subprocess.run(command, capture_output=True, text=True).stdout


def as_tuples(items):
    return sorted((item["check"], item["severity"], item["subject"])
                  for item in items)


def compare(name, expected, process):
    """Gibt eine Liste von Abweichungen zurueck, leer heisst bestanden."""
    problems = []
    if process.returncode != expected["exit_code"]:
        problems.append("Exit-Code %d statt %d"
                        % (process.returncode, expected["exit_code"]))
    try:
        actual = json.loads(process.stdout)
    except ValueError:
        problems.append("Ausgabe ist kein JSON: %s"
                        % (process.stderr.strip() or process.stdout[:120]))
        return problems

    found = as_tuples(actual["findings"])
    wanted = as_tuples(expected["befunde"])
    if found != wanted:
        for item in wanted:
            if item not in found:
                problems.append("erwarteter Befund fehlt: %s" % (item,))
        for item in found:
            if item not in wanted:
                problems.append("unerwarteter Befund: %s" % (item,))
    return problems


def main(argv):
    show_output = "--ausgabe" in argv
    filters = [arg for arg in argv if not arg.startswith("--")]

    root = repo_root()
    selected = cases(root, filters)
    if not selected:
        print("Keine Faelle gefunden.")
        return 1

    failed = []
    print("Golden Specs, Ebene 1 (deterministisch)")
    print("")
    for name, directory in selected:
        expected = load_expected(directory)
        process = run_check(root, directory)
        problems = compare(name, expected, process)
        status = "bestanden" if not problems else "ABWEICHUNG"
        print("  %-32s %-10s Exit %d, erwartet %d, %d Befund(e)"
              % (name, status, process.returncode, expected["exit_code"],
                 len(expected["befunde"])))
        print("      %s" % expected["beschreibung"])
        if show_output:
            for line in gate_output(root, directory).split("\n"):
                print("      | %s" % line)
        for problem in problems:
            print("      -> %s" % problem)
        if problems:
            failed.append(name)

    print("")
    print("%d von %d Faellen bestanden"
          % (len(selected) - len(failed), len(selected)))
    if failed:
        print("Abweichungen: %s" % ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
