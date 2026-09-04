#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests fuer scripts/check-severity-dialect.py.

Der Waechter haelt das Schweregrad-Vokabular auf den F-Stufen. Seine
Ausnahmeliste ist der empfindliche Teil: jeder Eintrag darin ist eine Stelle,
an der der zweite Dialekt zurueckkommen kann, und ein zu weit gefasster
Eintrag macht den Waechter still, ohne dass die Ausgabe das zeigt. Genau das
war der Fall, als die Ausnahme "als Major" hiess und mit IGNORECASE lief:
sie gab die deutsche Einstufungsformel frei, also den Satzbau, in dem der
alte Wert im Fliesstext ueberhaupt vorkommt.

Aufruf aus dem Repo-Wurzelverzeichnis:

    python3 -m unittest discover -s tests -v

Nur Standardbibliothek.
"""

import importlib.util
import io
import os
import re
import unittest
from contextlib import redirect_stdout

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PFAD = os.path.join(ROOT, "scripts", "check-severity-dialect.py")

_spec = importlib.util.spec_from_file_location("check_severity_dialect", PFAD)
waechter = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(waechter)


def treffer(zeile):
    """Die Legacy-Treffer einer Zeile, so wie main() sie zaehlt."""
    text = waechter.FACHBEGRIFF_RE.sub("", waechter.SEMVER_RE.sub("", zeile))
    return [match.group(1) for match in waechter.LEGACY_RE.finditer(text)]


class DialektTest(unittest.TestCase):
    def test_deutsche_einstufungsformel_wird_gemeldet(self):
        self.assertEqual(
            treffer("Ein Befund dieser Art gilt als Major und blockiert."),
            ["Major"])

    def test_kleingeschriebene_einstufung_wird_gemeldet(self):
        self.assertEqual(
            treffer("Ein zweiter Befund wird als major eingestuft."),
            ["major"])

    def test_deutsche_grossschreibung_wird_gemeldet(self):
        self.assertEqual(treffer("Loop bis Blocker-frei."), ["Blocker"])

    def test_dora_meldekategorie_bleibt_frei(self):
        self.assertEqual(
            treffer("Ist der Meldefluss fuer Major Incidents definiert?"), [])
        self.assertEqual(
            treffer("| INC-04 | Major-Incident-Meldung — Initial |"), [])

    def test_dora_klassifikation_bleibt_frei(self):
        self.assertEqual(
            treffer("Initialnotifikation ≤4h nach Klassifikation als Major, "
                    "max. 24h nach Erkennung"), [])

    def test_versionsnotation_ist_kein_schweregrad(self):
        self.assertEqual(treffer("v{MAJOR}.{MINOR}.{PATCH}"), [])
        self.assertEqual(treffer("Schema MAJOR.MINOR.PATCH"), [])

    def test_kurzform_der_alten_skala(self):
        self.assertTrue(waechter.SHORT_SCALE_RE.search("| Befunde (B/M/m) |"))
        self.assertFalse(waechter.SHORT_SCALE_RE.search("| F4/F3/F2/F1 |"))

    def test_ausnahmeliste_bleibt_kurz(self):
        """Zwei woertliche DORA-Begriffe, nicht mehr, und ohne IGNORECASE."""
        self.assertEqual(waechter.FACHBEGRIFF_RE.pattern,
                         r"Major[- ]Incidents?|Klassifikation als Major")
        self.assertFalse(waechter.FACHBEGRIFF_RE.flags & re.I)

    def test_repo_haelt_den_dialekt_ein(self):
        with redirect_stdout(io.StringIO()):
            code = waechter.main()
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
