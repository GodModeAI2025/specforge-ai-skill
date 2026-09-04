#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Faehrt specforge check ueber die Fixtures und prueft Exit-Code und Befunde.

Die Unit-Tests pruefen die Bausteine des Linters. Dieses Skript prueft den
Aufruf, so wie ihn eine fremde Pipeline macht: ueber die Kommandozeile, mit
dem Exit-Code als Ergebnis. Beides zusammen deckt den Weg vom Prozessaufruf
bis zum Befund ab.

Erwartet wird je Fixture ein Exit-Code und die Menge der Befunde als Paare
aus Pruefpunkt und F-Stufe. Eine Abweichung in beide Richtungen ist ein
Fehler: ein Befund zu wenig genauso wie einer zu viel.

Exit 0 wenn alles stimmt, sonst 1. Nur Standardbibliothek.
"""

import json
import os
import subprocess
import sys

# Fixture -> (Exit-Code, zusaetzliche Argumente, [(Pruefpunkt, F-Stufe), ...])
ERWARTUNG = {
    "01-valide": (0, [], []),
    "02-gherkin-fehlt": (1, [], [
        ("gherkin_minimum", "F4"),
    ]),
    "03-vage-begriffe": (1, [], [
        ("vague_terms", "F4"),
        ("vague_terms", "F4"),
        ("vague_terms", "F4"),
        ("sophist", "F3"),
    ]),
    "03-vage-begriffe-nach-clarify": (1, ["--nach-clarify"], [
        ("vague_terms", "F4"),
        ("vague_terms", "F4"),
        ("vague_terms", "F4"),
        ("sophist", "F3"),
        ("open_marker", "F3"),
        ("open_marker", "F3"),
    ]),
    "04-orphan-task": (2, [], [
        ("orphan_task", "F3"),
    ]),
    "05-leer": (1, [], [
        ("no_stories", "F4"),
    ]),
    "06-formatfremd": (1, [], [
        ("no_stories", "F4"),
    ]),
}


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fixture_dir(root, name):
    """'03-vage-begriffe-nach-clarify' zeigt auf dasselbe Verzeichnis."""
    base = name.replace("-nach-clarify", "")
    return os.path.join(root, "tests", "fixtures", base)


def run(root, name, extra):
    command = [sys.executable, os.path.join(root, "cli", "specforge"),
               "check", fixture_dir(root, name), "--json"] + extra
    process = subprocess.run(command, capture_output=True, text=True)
    return process


def main():
    root = repo_root()
    errors = []
    report = []

    for name in sorted(ERWARTUNG):
        expected_code, extra, expected = ERWARTUNG[name]
        process = run(root, name, extra)
        if process.returncode != expected_code:
            errors.append("%s: Exit-Code %d statt %d\n%s"
                          % (name, process.returncode, expected_code,
                             process.stderr.strip()))
            continue
        try:
            data = json.loads(process.stdout)
        except ValueError as error:
            errors.append("%s: Ausgabe ist kein JSON (%s)" % (name, error))
            continue
        found = sorted((item["check"], item["severity"])
                       for item in data["findings"])
        if found != sorted(expected):
            errors.append("%s: Befunde %s statt %s"
                          % (name, found, sorted(expected)))
            continue
        report.append((name, expected_code, len(found)))

    print("Geprueft: %d Fixture-Laeufe" % len(ERWARTUNG))
    for name, code, count in report:
        print("  %-34s Exit %d, %d Befund(e)" % (name, code, count))

    if errors:
        print("")
        print("FEHLER (%d):" % len(errors))
        for message in errors:
            print("  - %s" % message)
        return 1

    print("")
    print("OK: specforge check meldet die erwarteten F-Stufen und "
          "Exit-Codes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
