# Changelog

Versionsgeschichte von SpecForge. Die Einträge beschreiben den Stand der
jeweiligen Version und werden nicht rückwirkend geändert.

Schema und Geltungsbereich der Versionen stehen im [README](README.md),
Abschnitt Versionierung.

---

## Aktuelles Release

Diese Tabelle ist die Versionsquelle des Repos. Gelesen wird die erste
Datenzeile, ein neues Release kommt darüber. Niemand pflegt die Version ein
zweites Mal: das Packaging-Skript schreibt sie ins Archiv, der
Release-Workflow vergleicht den Tag damit, und `scripts/check-version.py`
prüft README und Landingpage dagegen.

| Tag | Skill-Version | Artefakt |
|-----|---------------|----------|
| `v3.2.0` | 3.2 | `specforge-skill.zip` |

Der Tag hat eine Stelle mehr als die Skill-Version: `v{MAJOR}.{MINOR}.{PATCH}`.
Die Patch-Stelle zählt Korrekturen, die den Funktionsumfang nicht verändern.
`v3.2.0` paketiert den Stand der Skill-Version 3.2 und ist das erste Release
dieses Repos. Der Artefaktname bleibt über Releases hinweg gleich, damit
`releases/latest/download/specforge-skill.zip` dauerhaft auf das jeweils
aktuelle Paket zeigt.

## Versionsgeschichte

Älteste Version zuerst.

| Version | Datum | Änderung |
|---------|-------|---------|
| 1.0 | 2025-10 | Initial: Specify, Plan, Tasks, Review, Stakeholder-Sim, Management |
| 2.0 | 2026-03 | +Clarify, +Analyze, +Checklist, +Research, +Quickstart. SpecKit v3 Alignment. RE Butler entfernt. Single-File-Architektur. |
| 2.1 | 2026-03 | +Phase 0 (Cynefin + Impact Mapping), 15 methodische Frameworks mit Aktivieren-Eingrenzen-Prüfen-Muster, Sokratische Klärung, MECE-Analyse, Devil's Advocate + Steelmanning, Morphological Box + Pugh Matrix, DDD-Datenmodell, BLUF-Zusammenfassungen. |
| 2.2 | 2026-03 | +Modus 9 Discover (Bestandsdokumentation & Reverse Spec). Zwei verpflichtende QS-Schleifen: Vollständigkeit + Konsistenz/Stringenz. Rückwärts-Validierung. discovery-protocol.md und migration-delta.md als neue Artefakte. |
| 2.3 | 2026-03 | +Anhang I Enforcement Engine: State Machine (INIT→COMPLETE), Phase Gates G0–G8, Skip-Protokoll, Vage-Begriffe-Scanner, Anti-Pattern-Erkennung. +5W-Pflichtblock für Reverse-Engineering. +Artefakt-Vollständigkeits-Check. +Session-Status-Anzeige. 21 Interaktions- + 26 Qualitätsregeln. |
| 3.0 (v202-green) | 2026-03 | **Architektur-Wechsel: Single-File → Multi-File.** Orchestrator (SKILL.md, 395 Zeilen) + 9 Fachmodule + 9 Support-Dateien = 19 Dateien, 3.143 Zeilen. Jedes Modul erhält standardisierte Sektionen: Stringenz-Regeln, Erweiterbarkeit, Fehlerbehandlung, GP-Mapping. Orchestrator mit Pre-Flight Checks, Profil-Resolution Cascade, Calendar Versioning, Audit Trail, Session-Retrospektive, 8 Built-in Extension Points. Deterministische Rollenauswahl (M06), GP-Score-Formel (M07), 7 Management-Funktionen (M08), QS-Loops mit Terminierung (M09). Autoresearch-optimiert: 600 Assertions, 6 Dimensionen, 68%→80% Score über 5 Iterationen. |
| 3.1 | 2026-03 | **DORA-Integration & F-Stufen-System.** +F-Stufen (F0–F5) nach PrüfbV §27 ersetzen binäres Pass/Fail. +CONDITIONAL als dritter Gate-Ausgang (Risiko-Akzeptanz). +Perspektive als orthogonale Dimension zu Profil (Lieferkettenrolle). +Manifest-Auto-Detection für Extensions. +DORA-Extension (58 Prüfpunkte, 6 Kategorien, 3 Perspektiven). +BAIT-Stub (8 Prüfpunkte). +CONTRIBUTING-CHECKLISTS.md mit Schema, Validierung und Kandidatenliste. +Erweiterter Audit Trail mit F-Stufen und Perspektive. |
| 3.2 | 2026-03 | **Qualitätserweiterungen aus RE-Skill-Analyse.** +AP-08 SOPHIST-Verletzung (Passiv, Negation, Generik, unvollständige Aufzählung, implizite Zeitangabe) mit SOPHIST-Blocklist. +`[Offen: ...]`-Marker für unvollständige Stories (F3 nach Clarify). +Story-Quality-Score (SQS) als numerische Qualitätsbewertung (0–5) in Review und Analyze. +Modus 10 Derive: Testfall-Ableitung aus Gherkin-Szenarien mit Testabdeckungsmatrix, 6 Testfall-Typen, Traceability. +MCP-Kontext-Pre-Flight in Specify für externe Quellen (Figma, GitHub, Confluence, Jira). |
