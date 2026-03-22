# Modus 8: Management & Traceability

**Trigger:** Traceability-Matrix, Spec-Audit, Tech-Debt-Verwaltung, Spec-Diff, Freshness-Check.
**Methode:** Vollständige Rückverfolgbarkeit der Artefakt-Kette + automatisierte Pflege-Checks.

## Profil-Steuerung

- **KRITIS:** Vollständige Traceability Matrix Pflicht; Freshness-Check alle 14 Tage; Spec-First Chain Audit Pflicht; Alle Funktionen aktiv; Gate-Skip nur mit vollständigem Skip-Protokoll (Begründung, Risiko, Kompensation, Entscheider)
- **Standard:** Traceability empfohlen; Freshness-Check bei Reviews; Spec-First Chain Audit empfohlen
- **Startup:** Tech-Debt-Tracking empfohlen; Traceability bei Bedarf; Freshness auf aktive Artefakte beschränkt

## Funktionen (7 Management-Modi)

### Funktion 8.1: Traceability Matrix

Vollständige Rückverfolgbarkeit über die gesamte Artefakt-Kette:

```
Constitution → GP → spec.md → Clarifications → Stories → ACs
  → plan.md → research.md → tasks.md → Work Items
```

**Prüfung (deterministisch):**

| Prüfpunkt | Was wird geprüft | Schweregrad bei Lücke |
|-----------|-----------------|----------------------|
| TM-01 | Jede Story hat Spec-Referenz (GP-02) | BLOCKER |
| TM-02 | Jeder Task hat Story-Referenz | MAJOR (AP-07: Orphan Artifact) |
| TM-03 | Jede Story hat ≥2 Gherkin-ACs | MAJOR (AP-06) |
| TM-04 | Jede modulübergreifende Entscheidung hat ADR (GP-03) | MAJOR |
| TM-05 | Tasks mit 5+ Dateien haben ExecPlan (GP-04) | MAJOR |
| TM-06 | Constitution referenziert aktive GPs laut Profil | MINOR |
| TM-07 | ARCHITECTURE.md enthält aktuelle Codemap | MINOR |

**Output:**
```markdown
## Traceability Matrix: [Feature-Name]
**Profil:** [KRITIS / Standard / Startup]
**Prüfdatum:** [YYYY-MM-DD]

| Quelle | Ziel | Status | Lücke | Schweregrad |
|--------|------|--------|-------|------------|
| spec.md SF-FUNC-001 | Task T-001 | ✅ Verknüpft | — | — |
| spec.md SF-SEC-003 | — | ❌ Kein Task | Orphan Spec | MAJOR |
| Task T-005 | — | ❌ Keine Story | Orphan Task | MAJOR |

**Abdeckung:** [X/Y] Spec-Einträge mit Task (Z%)
**GP-02 Compliance:** [PASS / FAIL]
```

### Funktion 8.2: Spec-First Chain Audit

Prüft ob die 8-Schritt-Kette (→ `references/conventions/spec-first-chain.md`) für jeden Task eingehalten wurde.

| Prüfpunkt | Was wird geprüft | Schweregrad |
|-----------|-----------------|------------|
| SFC-01 | Spec-Update vor Code (Schritt 1, GP-02) | BLOCKER |
| SFC-02 | Schema-Update bei API-Änderung (Schritt 2) | MAJOR |
| SFC-03 | Fixture-Update bei Schema-Änderung (Schritt 3, GP-01) | MAJOR |
| SFC-04 | Contract Tests ausgeführt (Schritt 6) | MAJOR |
| SFC-05 | Breaking Changes dokumentiert (Schritt 7) | MAJOR |
| SFC-06 | ARCHITECTURE.md aktuell (Schritt 8) | MINOR |

**Output:**
```markdown
## Spec-First Chain Audit: [Feature-Name]

| Task | Steps erwartet | Steps durchgeführt | Lücken | Status |
|------|---------------|-------------------|--------|--------|
| T-001 | 1,2,3,4,6,8 | 1,2,3,4,6,8 | — | ✅ |
| T-002 | 1,4,5,6 | 1,4,6 | 5 (Consumer) | ⚠️ MAJOR |

**Chain-Compliance:** [X/Y] Tasks vollständig ([Z%])
```

### Funktion 8.3: ExecPlan-Verwaltung

- **Aktive ExecPlans:** `plans/active/EP-*.md`
- **Abgeschlossene ExecPlans:** `plans/completed/EP-*.md`
- **Prüfung:** Jeder Task mit 5+ Dateiänderungen hat EP-*.md (GP-04)
- **Lifecycle:** Active → Completed nach Task-Abschluss (automatisch verschieben)

### Funktion 8.4: Tech-Debt-Register (GP-10)

Verwaltung aller bekannten technischen Schulden in `tech-debt-tracker.md`.

**Pflicht-Felder pro Eintrag:**
```markdown
| ID | Beschreibung | Owner | Priorität | Auswirkung auf NFRs | Erstellt | Ziel-Sprint |
| TD-001 | [Beschreibung] | @owner | HOCH/MITTEL/NIEDRIG | [betroffene NFRs] | YYYY-MM-DD | Sprint X |
```

**Schweregrad-Eskalation:** MINOR → MAJOR wenn Debt auf NFRs wirkt (Performance, Security, Availability).

### Funktion 8.5: Spec-Diff

Vergleicht zwei Versionen eines Artefakts und bewertet die Änderungen:

| Änderungstyp | Bewertung | Aktion |
|-------------|----------|--------|
| Neue Story hinzugefügt | Neutral | Prüfen: Hat Story ACs? EARS? |
| Story entfernt | MAJOR | Prüfen: Begründung dokumentiert? Orphan-Check |
| AC geändert | MINOR | Prüfen: Tests noch valide? |
| NFR geändert | MAJOR | Prüfen: Architektur-Impact? ADR nötig? |
| Breaking API Change | BLOCKER | Prüfen: Schritt 7 (Log Breaking Changes) |

### Funktion 8.6: Freshness Check (GP-06)

| Prüfpunkt | Kriterium | Schweregrad |
|-----------|----------|------------|
| FR-01 | Stale Marker (TODO/TBD/FIXME) ohne Datum + Owner | MINOR |
| FR-02 | Stale Marker älter als 14 Tage | MAJOR |
| FR-03 | Verwaiste Schemas (Schema ohne Spec-Referenz) | MAJOR |
| FR-04 | ARCHITECTURE.md älter als letzte strukturelle Änderung | MINOR |
| FR-05 | spec.md Version älter als zugehörige Tasks | MAJOR |

**Freshness-Intervall nach Profil:**
- KRITIS: Alle 14 Tage automatisch
- Standard: Bei jedem Review
- Startup: Bei Bedarf

### Funktion 8.7: Analyze-Historie

Tracking aller bisherigen Analyze-Runs und deren Ergebnisse:

```markdown
## Analyze-Historie: [Feature-Name]

| Run | Datum | GP-Score | BLOCKER | MAJOR | MINOR | Status |
|-----|-------|---------|---------|-------|-------|--------|
| #1 | YYYY-MM-DD | 6/10 | 2 | 5 | 3 | ❌ FAIL |
| #2 | YYYY-MM-DD | 8/10 | 0 | 2 | 3 | ✅ PASS |

**Trend:** GP-Score steigt / fällt / stabil
**Fix-Zyklen bis PASS:** [Anzahl]
```

## Stringenz-Regeln (Enforcement)

Folgende Regeln werden bei jeder Management-Funktion **automatisch** durchgesetzt:

| Regel | Enforcement | Schweregrad bei Verstoß |
|-------|-----------|------------------------|
| Traceability-Lücken (Orphan Specs/Tasks) | Automatisch bei TM-01 bis TM-07 | BLOCKER (GP-02) / MAJOR (AP-07) |
| Spec-First Chain Compliance | Automatisch bei SFC-01 bis SFC-06 | BLOCKER (SFC-01) / MAJOR |
| Vage Begriffe in Spec-Diffs | Jede Änderung gegen Blocklist prüfen: "schnell", "viele", "einfach", "skalierbar", "sicher", "zuverlässig" | BLOCKER (AP-04) |
| Fragen-Budget | Max. 3 Fragen pro Runde an den Nutzer | n.a. (Budget-Überschreitung = Skip) |
| Anti-Pattern-Prüfung bei Spec-Diff | AP-01–AP-07 + custom APs aus `references/custom/anti-patterns-custom.md` bei jeder Spec-Änderung | Schweregrad laut AP-Tabelle |
| Artefakt-Erzeugung als Datei | Alle Reports als separate .md-Dateien, nicht inline | MAJOR |
| Schweregrad-Zuweisung | Deterministisch nach enforcement-engine.md Tabelle | n.a. (systemweit) |
| Freshness-Intervall | KRITIS: 14 Tage; Standard: bei Review; Startup: bei Bedarf | MAJOR (bei Überschreitung KRITIS) |

## Erweiterbarkeit

| Erweiterungspunkt | Wie | Wo |
|-------------------|-----|-----|
| Neue Traceability-Prüfpunkte | TM-08+ in `references/custom/traceability-custom.md` | Custom Extension |
| Neue SFC-Schritte | Schritt 9+ in `references/custom/spec-first-chain-custom.md` | Custom Extension |
| Branchenspezifische Freshness-Regeln | `references/custom/@branche-compliance/freshness-rules.md` | Custom Extension |
| Neue Anti-Patterns für Spec-Diff | `references/custom/anti-patterns-custom.md` (AP-08+) | Custom Extension |
| Custom Tech-Debt-Kategorien | Erweiterbar über zusätzliche Spalten in tech-debt-tracker.md | Projekt-spezifisch |
| Neue Management-Funktionen | 8.8+ als `references/custom/management-custom.md` | Custom Extension |

## Fehlerbehandlung

| Situation | Reaktion |
|-----------|---------|
| Kein specforge.json | → Standard-Profil, Hinweis ausgeben |
| Leere/fehlende spec.md | → Fehlermeldung: "spec.md nicht gefunden — Traceability nicht möglich" |
| Fehlende Referenzdateien | → Klare Fehlermeldung mit Dateipfad; betroffene Funktion als FAIL |
| Profil-Wechsel mid-session | → Prüftiefe neu evaluieren |
| Artefakte in falschen Verzeichnissen | → GP-07 Finding dokumentieren |
| Mixed-Language Input | → Sprachverhalten gemäß Orchestrator |
| Widersprüchliche Versionen | → Neuere Version als SSOT, Delta dokumentieren |
| Übermäßig viele Artefakte (>50 Stories) | → Traceability-Matrix paginieren, Top-Findings priorisieren |

## GP-Mapping

| GP | Relevanz in Modus 8 |
|----|---------------------|
| GP-01 | SFC-Audit: Schema + Fixture Matching |
| GP-02 | Traceability: Spec-before-Code |
| GP-03 | Traceability: ADR-Vollständigkeit |
| GP-04 | ExecPlan-Verwaltung |
| GP-05 | Traceability: Invariant-Tests |
| GP-06 | Freshness Check |
| GP-07 | Folder Convention Compliance |
| GP-08 | Meta: GP-Verstöße blockieren |
| GP-09 | SFC-Audit: Consumer/Provider-Richtung |
| GP-10 | Tech-Debt-Register |

## Erzeugte Artefakte

| Artefakt | Pfad |
|----------|------|
| traceability-matrix.md | specs/use-cases/\<feature\>/ |
| sfc-audit.md | specs/use-cases/\<feature\>/ |
| tech-debt-tracker.md | Projekt-Root |
| analyze-history.md | specs/use-cases/\<feature\>/ |
