#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests fuer specforge check.

Aufruf aus dem Repo-Wurzelverzeichnis:

    python3 -m unittest discover -s tests -v

Nur Standardbibliothek, kein pytest. Die CI dieses Repos installiert nichts,
und ein Test, der erst ein pip install braucht, laeuft in einer fremden
Pipeline nicht.
"""

import io
import json
import os
import sys
import unittest
from contextlib import redirect_stdout

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "cli"))

from specforge_check import config as config_mod  # noqa: E402
from specforge_check import rules, severity, spec as spec_mod  # noqa: E402
from specforge_check.__main__ import main  # noqa: E402

FIXTURES = os.path.join(ROOT, "tests", "fixtures")


def fixture(name, *parts):
    return os.path.join(FIXTURES, name, *parts)


def run_cli(argv):
    """Ruft den Checker auf und gibt (exit_code, ausgabe) zurueck."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = main(argv)
    return code, buffer.getvalue()


class ParserTest(unittest.TestCase):
    def test_stories_und_szenarien_werden_erkannt(self):
        document = spec_mod.parse_spec(fixture("01-valide", "spec.md"))
        self.assertEqual([s.id for s in document.stories],
                         ["SF-SEC-001", "SF-AVA-001"])
        self.assertEqual([len(s.scenarios) for s in document.stories], [2, 2])

    def test_pattern_feld_wird_gelesen(self):
        document = spec_mod.parse_spec(fixture("01-valide", "spec.md"))
        self.assertEqual(document.stories[0].pattern, "Event-Driven")
        self.assertEqual(document.stories[1].pattern, "State-Driven")

    def test_id_schema(self):
        self.assertTrue(spec_mod.valid_id("SF-SEC-001"))
        self.assertFalse(spec_mod.valid_id("SF-XXX-001"))
        self.assertFalse(spec_mod.valid_id("SF-SEC-1"))

    def test_tasks_referenzen(self):
        tasks = spec_mod.parse_tasks(fixture("01-valide", "tasks.md"))
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0][2], ["SF-SEC-001"])


class SeverityTest(unittest.TestCase):
    def test_legacy_wird_uebersetzt(self):
        self.assertEqual(severity.normalise("BLOCKER"), "F4")
        self.assertEqual(severity.normalise("MAJOR"), "F3")
        self.assertEqual(severity.normalise("MINOR"), "F1")

    def test_schreibweisen(self):
        self.assertEqual(severity.normalise("F 4"), "F4")
        self.assertEqual(severity.normalise(True), "F4")
        self.assertEqual(severity.normalise(False), "F1")
        self.assertIsNone(severity.normalise("F9"))


class ConfigTest(unittest.TestCase):
    def test_perspektive_schlaegt_default(self):
        configuration = config_mod.Config({
            "perspective": "advisory",
            "severity_model": {},
            "checks_config": {"G1": {"stride_complete": {"severity": {
                "_default": "F3", "regulated_entity": "F4",
                "advisory": "F1"}}}},
        })
        self.assertEqual(
            configuration.severity_for("stride_complete", "F3"), "F1")

    def test_default_bei_unbekannter_perspektive(self):
        configuration = config_mod.Config({
            "perspective": "ict_provider",
            "severity_model": {},
            "checks_config": {"G1": {"stride_complete": {"severity": {
                "_default": "F3", "advisory": "F1"}}}},
        })
        self.assertEqual(
            configuration.severity_for("stride_complete", "F4"), "F3")

    def test_ohne_default_gilt_f3(self):
        configuration = config_mod.Config({
            "severity_model": {},
            "checks_config": {"G1": {"stride_complete": {"severity": {
                "advisory": "F1"}}}},
        })
        self.assertEqual(
            configuration.severity_for("stride_complete", "F4"), "F3")

    def test_altkonfiguration_ohne_severity_model(self):
        configuration = config_mod.Config({
            "checks_config": {"G1": {"gherkin_minimum": {"required": True}}},
        })
        self.assertTrue(configuration.legacy)
        self.assertEqual(
            configuration.severity_for("gherkin_minimum", "F1"), "F4")

    def test_legacy_wert_in_checks_config(self):
        configuration = config_mod.Config({
            "checks_config": {"G1": {"vague_terms": {"severity": "MAJOR"}}},
        })
        self.assertEqual(configuration.severity_for("vague_terms", "F4"),
                         "F3")


class RuleTest(unittest.TestCase):
    def _findings(self, name, after_clarify=False, with_tasks=False):
        document = spec_mod.parse_spec(fixture(name, "spec.md"))
        tasks = (spec_mod.parse_tasks(fixture(name, "tasks.md"))
                 if with_tasks else None)
        configuration = config_mod.load(
            config_mod.find(fixture(name, "spec.md")))
        return rules.run(document, tasks, configuration, after_clarify)

    def test_valide_spec_ohne_befund(self):
        self.assertEqual(self._findings("01-valide", with_tasks=True), [])

    def test_fehlende_gherkin_szenarien_sind_f4(self):
        findings = self._findings("02-gherkin-fehlt")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].check, "gherkin_minimum")
        self.assertEqual(findings[0].level, "F4")
        self.assertEqual(findings[0].subject, "SF-OPS-001")

    def test_vage_begriffe_sind_f4(self):
        findings = [f for f in self._findings("03-vage-begriffe")
                    if f.check == "vague_terms"]
        self.assertEqual(sorted(f.message for f in findings), [
            "vager Begriff 'schnell'",
            "vager Begriff 'viele'",
            "vager Begriff 'zuverlässig'",
        ])
        self.assertEqual(set(f.level for f in findings), {"F4"})

    def test_marker_schuetzen_vor_falschbefund(self):
        """"einfach" steht nur in einem [Annahme:]-Marker und zaehlt nicht."""
        findings = self._findings("03-vage-begriffe")
        self.assertNotIn("vager Begriff 'einfach'",
                         [f.message for f in findings])

    def test_offene_marker_erst_nach_clarify(self):
        vorher = [f for f in self._findings("03-vage-begriffe")
                  if f.check == "open_marker"]
        nachher = [f for f in self._findings("03-vage-begriffe",
                                             after_clarify=True)
                   if f.check == "open_marker"]
        self.assertEqual(vorher, [])
        self.assertEqual(len(nachher), 2)
        self.assertEqual(set(f.level for f in nachher), {"F3"})

    def test_orphan_task_ist_f3(self):
        findings = [f for f in self._findings("04-orphan-task",
                                              with_tasks=True)
                    if f.check == "orphan_task"]
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].subject, "T-002")
        self.assertEqual(findings[0].level, "F3")


class ExitCodeTest(unittest.TestCase):
    def test_valide_spec_exit_0(self):
        code, output = run_cli([fixture("01-valide")])
        self.assertEqual(code, 0)
        self.assertIn("Ergebnis: PASS", output)

    def test_fehlende_gherkin_szenarien_exit_1(self):
        code, output = run_cli([fixture("02-gherkin-fehlt")])
        self.assertEqual(code, 1)
        self.assertIn("[F4] Gherkin-Szenarien", output)
        self.assertIn("Ergebnis: FAIL", output)

    def test_orphan_task_exit_2(self):
        code, output = run_cli([fixture("04-orphan-task")])
        self.assertEqual(code, 2)
        self.assertIn("Ergebnis: CONDITIONAL", output)

    def test_risiko_akzeptanz_hebt_exit_2_auf(self):
        code, _ = run_cli([fixture("04-orphan-task"),
                           "--risiko-akzeptanz",
                           fixture("04-orphan-task", "risiko-akzeptanz.md")])
        self.assertEqual(code, 0)

    def test_fehlender_pfad_exit_3(self):
        code, _ = run_cli([os.path.join(FIXTURES, "gibt-es-nicht")])
        self.assertEqual(code, 3)

    def test_json_ausgabe(self):
        code, output = run_cli([fixture("02-gherkin-fehlt"), "--json"])
        self.assertEqual(code, 1)
        data = json.loads(output)
        self.assertEqual(data["stories"], ["SF-OPS-001"])
        self.assertEqual(data["findings"][0]["severity"], "F4")
        self.assertEqual(data["findings"][0]["check"], "gherkin_minimum")


class KonfigurationsWirkungTest(unittest.TestCase):
    def test_checks_config_senkt_die_stufe(self):
        """Eine Perspektive darf die Default-Stufe ueberschreiben."""
        configuration = config_mod.Config({
            "perspective": "advisory",
            "severity_model": {},
            "checks_config": {"G1": {"gherkin_minimum": {"severity": {
                "_default": "F4", "advisory": "F2"}}}},
        })
        document = spec_mod.parse_spec(fixture("02-gherkin-fehlt", "spec.md"))
        findings = rules.run(document, None, configuration)
        self.assertEqual([f.level for f in findings], ["F2"])


if __name__ == "__main__":
    unittest.main()
