#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests fuer specforge check.

Aufruf aus dem Repo-Wurzelverzeichnis:

    python3 -m unittest discover -s tests -v

Nur Standardbibliothek, kein pytest. Die CI dieses Repos installiert nichts,
und ein Test, der erst ein pip install braucht, laeuft in einer fremden
Pipeline nicht.
"""

import datetime
import io
import json
import os
import sys
import unittest
from contextlib import redirect_stdout

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "cli"))

from specforge_check import acceptance  # noqa: E402
from specforge_check import config as config_mod  # noqa: E402
from specforge_check import extensions  # noqa: E402
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


class OhneStoryTest(unittest.TestCase):
    """Eine Spec ohne erkannte Story darf kein bestandener Lauf sein."""

    def test_leere_datei_ist_f4(self):
        code, output = run_cli([fixture("05-leer")])
        self.assertEqual(code, 1)
        self.assertIn("[F4] Keine pruefbare Story", output)
        self.assertIn("Datei ist leer", output)
        self.assertNotIn("Alle Pruefpunkte erfuellt", output)

    def test_fremdes_story_format_ist_f4(self):
        code, output = run_cli([fixture("06-formatfremd")])
        self.assertEqual(code, 1)
        self.assertIn("kein Story-Kopf", output)
        self.assertNotIn("Alle Pruefpunkte erfuellt", output)

    def test_checks_config_kann_die_stufe_nicht_senken(self):
        """Die Stufe steht im Code, nicht in der Konfiguration."""
        configuration = config_mod.Config({
            "severity_model": {},
            "checks_config": {"G1": {"no_stories": {"severity": "F1"}}},
        })
        document = spec_mod.parse_spec(fixture("05-leer", "spec.md"))
        findings = rules.run(document, None, configuration)
        self.assertEqual([(f.check, f.level) for f in findings],
                         [("no_stories", "F4")])


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

    def test_fehlende_akzeptanzdatei_ist_exit_3(self):
        code, _ = run_cli([fixture("04-orphan-task"), "--risiko-akzeptanz",
                           fixture("04-orphan-task", "gibt-es-nicht.md")])
        self.assertEqual(code, 3)

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


class RisikoAkzeptanzTest(unittest.TestCase):
    """Eine Freigabe, die kein Dokument verlangt, ist keine Freigabe."""

    HEUTE = datetime.date(2026, 9, 5)

    def _findings(self):
        document = spec_mod.parse_spec(fixture("04-orphan-task", "spec.md"))
        tasks = spec_mod.parse_tasks(fixture("04-orphan-task", "tasks.md"))
        return rules.run(document, tasks, config_mod.Config())

    def _apply(self, datei):
        return acceptance.apply(self._findings(),
                                fixture("04-orphan-task", datei), self.HEUTE)

    def test_vollstaendiger_block_akzeptiert(self):
        accepted, messages = self._apply("risiko-akzeptanz.md")
        self.assertEqual([f.check for f in accepted], ["orphan_task"])
        self.assertEqual(messages, [])

    def test_ablehnung_akzeptiert_nicht(self):
        """Die Datei nennt Pruefpunkt und Betreff und verweigert trotzdem."""
        accepted, messages = self._apply("risiko-abgelehnt.md")
        self.assertEqual(accepted, [])
        self.assertEqual(len(messages), 1)
        self.assertIn("keine gueltige Akzeptanz", messages[0])

    def test_fehlende_pflichtfelder_akzeptieren_nicht(self):
        accepted, messages = self._apply("risiko-unvollstaendig.md")
        self.assertEqual(accepted, [])
        self.assertIn("Akzeptiert durch", messages[0])
        self.assertIn("Kompensation", messages[0])

    def test_abgelaufene_frist_akzeptiert_nicht(self):
        accepted, messages = self._apply("risiko-abgelaufen.md")
        self.assertEqual(accepted, [])
        self.assertIn("abgelaufen", messages[0])

    def test_frist_am_stichtag_gilt_noch(self):
        blocks = acceptance.parse(fixture("04-orphan-task",
                                          "risiko-abgelaufen.md"))
        self.assertEqual(blocks[0].problems(datetime.date(2020, 1, 1)), [])
        self.assertEqual(blocks[0].problems(datetime.date(2020, 1, 2)), [
            "Frist 2020-01-01 ist am 2020-01-02 abgelaufen"])

    def test_betreff_wird_als_ganzes_wort_gelesen(self):
        self.assertTrue(acceptance.names("orphan_task T-002", "T-002"))
        self.assertFalse(acceptance.names("orphan_task T-0021", "T-002"))

    def test_falsche_f_stufe_im_block_akzeptiert_nicht(self):
        blocks = acceptance.parse(fixture("04-orphan-task",
                                          "risiko-akzeptanz.md"))
        finding = self._findings()[0]
        self.assertTrue(acceptance.matches(blocks[0], finding))
        finding.level = "F4"
        self.assertFalse(acceptance.matches(blocks[0], finding))


class ExtensionTest(unittest.TestCase):
    def setUp(self):
        self.packages = extensions.load(ROOT)

    def test_dora_tabelle_wird_gelesen(self):
        self.assertIn("@dora", self.packages)
        self.assertIn("IRM", self.packages["@dora"])

    def test_perspektive_bestimmt_die_stufe(self):
        """Dieselbe Kategorie, drei Perspektiven, drei Stufen."""
        self.assertEqual(
            extensions.allowed_levels(self.packages, "IRM",
                                      "regulated_entity"), {"F4"})
        self.assertEqual(
            extensions.allowed_levels(self.packages, "IRM", "advisory"),
            {"F2"})

    def test_mehrdeutige_zelle_laesst_beide_stufen_zu(self):
        """'F4 (CTPP) / F3' ist eine Bedingung, kein Tippfehler."""
        nur_dora = extensions.load(ROOT, ["@dora"])
        self.assertEqual(
            extensions.allowed_levels(nur_dora, "IRM", "ict_provider"),
            {"F3", "F4"})

    def test_kollidierendes_kuerzel_vereinigt_die_stufen(self):
        """IRM fuehren @dora und @bait mit verschiedener Bedeutung.

        Sind beide aktiv, ist das Kuerzel nicht eindeutig. Der Checker
        beanstandet dann nur, was keine der beiden Extensions vorsieht.
        """
        self.assertIn("IRM", self.packages["@dora"])
        self.assertIn("IRM", self.packages["@bait"])
        self.assertEqual(
            extensions.allowed_levels(self.packages, "IRM", "advisory"),
            {"F2"})
        self.assertEqual(
            extensions.allowed_levels(self.packages, "IRM", "ict_provider"),
            {"F3", "F4"})

    def test_unbekannte_kategorie_bleibt_ungeprueft(self):
        self.assertIsNone(
            extensions.allowed_levels(self.packages, "ZZZ", "advisory"))

    def test_default_spalte_greift_ohne_perspektive(self):
        self.assertEqual(
            extensions.allowed_levels(self.packages, "GOV", None), {"F3"})


class NfrLueckeTest(unittest.TestCase):
    """Was die Perspektive im Linter bewirkt.

    Die Stufe der Luecke selbst steht im Marker, den der Autor gesetzt hat.
    Die Perspektive entscheidet, ob diese Einstufung zur F-Stufen-Tabelle
    der Extension passt: dieselbe Spec ergibt fuer regulated_entity nur den
    nfr_gap (Fall 03) und fuer advisory zusaetzlich nfr_severity (Fall 06).
    Fall 04 zeigt die zur Perspektive passende mildere Einstufung, die als
    F2 das Gate passiert; ueber BLOCKER/MAJOR/MINOR war dieser Wert nicht
    darstellbar.
    """

    def _run(self, name):
        path = os.path.join(ROOT, "evals", "golden", name, "spec.md")
        document = spec_mod.parse_spec(path)
        configuration = config_mod.load(config_mod.find(path))
        packages = extensions.load(ROOT)
        return rules.run(document, None, configuration, False, packages)

    def test_regulated_entity_blockiert(self):
        findings = self._run("03-dora-regulated-ohne-irm01")
        self.assertEqual([(f.check, f.level, f.subject) for f in findings],
                         [("nfr_gap", "F4", "IRM-01")])

    def test_paar_unterscheidet_sich_nur_in_der_perspektive(self):
        """Ein Beleg mit zwei Variablen belegt nichts."""
        def read(case):
            path = os.path.join(ROOT, "evals", "golden", case, "spec.md")
            with open(path, encoding="utf-8") as handle:
                return handle.read()

        self.assertEqual(read("03-dora-regulated-ohne-irm01"),
                         read("06-dora-falsche-f-stufe"))

    def test_nicht_markierte_luecke_bleibt_unbemerkt(self):
        """Grenze des Linters, festgehalten statt behauptet."""
        self.assertEqual(self._run("08-dora-luecke-undokumentiert"), [])

    def test_advisory_erzeugt_pflicht_task(self):
        findings = self._run("04-dora-advisory-ohne-irm01")
        self.assertEqual([(f.check, f.level, f.subject) for f in findings],
                         [("nfr_gap", "F2", "IRM-01")])

    def test_zu_harte_einstufung_ist_ein_befund(self):
        findings = self._run("06-dora-falsche-f-stufe")
        self.assertEqual([(f.check, f.level) for f in findings],
                         [("nfr_gap", "F4"), ("nfr_severity", "F3")])
        self.assertIn("verlangt F2", findings[1].message)


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
