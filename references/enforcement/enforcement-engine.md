# Enforcement Engine

Phase Gates, Anti-Pattern-Erkennung, State Machine und Artefakt-Vollständigkeitsprüfung. Wird bei jedem Phasenübergang automatisch aktiviert. Verhalten skaliert mit dem gewählten Profil aus `specforge.json`.

---

## I.1 State Machine — Forward Path

```
   G0              G1              G2              G3                G4              G5
[START+PROFIL] → [SPECIFY] → [CLARIFY] → [PLAN+TASKS] → [ANALYZE] → [IMPLEMENT] → [COMPLETE]
                                  ↑                          ↑           │
                                  │                          └── Fix ────┘
                             (Loop bei BLOCKER)
```

## I.2 Ausführbare Phase Gates

Jedes Gate hat eine **konkrete Checkliste** mit Pass/Fail-Ergebnis. SpecForge prüft automatisch und gibt das Ergebnis aus, bevor der Übergang vorgeschlagen wird.

**Profil-Schwellen für GP-Score:** KRITIS ≥ 9/10 · Standard ≥ 8/10 · Startup ≥ 6/10

**Skip-Regeln nach Profil:**
- **KRITIS:** Skip nur mit vollständigem Skip-Protokoll (Begründung, Risiko, Kompensation, Entscheider)
- **Standard:** Skip mit Einzeiler-Begründung erlaubt
- **Startup:** Soft Gates — Empfehlungen statt Blocker

### Gate G0: Start → Specify
```
── Gate G0 ─────────────────────────────────
[ ] specforge.json erzeugt mit Profil
[ ] Cynefin-Einordnung (empfohlen)
[ ] Folder Convention bestätigt
[ ] constitution.md erzeugt mit GPs laut Profil
── Ergebnis: PASS | FAIL ───────────────────
```

### Gate G1: Specify → Clarify
```
── Gate G1 ─────────────────────────────────
[ ] spec.md erzeugt
[ ] EARS-Formulierung: X/Y Stories vollständig
[ ] Gherkin-Szenarien: ≥2 pro Story
[ ] Constitution referenziert
[ ] STRIDE: laut Profil geprüft
[ ] Keine offenen BLOCKER-Fragen
── Ergebnis: PASS | FAIL ───────────────────
```

### Gate G2: Clarify → Plan
```
── Gate G2 ─────────────────────────────────
[ ] Keine offenen BLOCKER-Fragen
[ ] Clarifications dokumentiert in spec.md
[ ] Vage Begriffe aufgelöst
[ ] [Annahme: ...]-Marker bestätigt oder verworfen
── Ergebnis: PASS | FAIL ───────────────────
```

### Gate G3: Plan+Tasks → Analyze
```
── Gate G3 ─────────────────────────────────
[ ] plan.md erzeugt
[ ] tasks.md erzeugt mit Spec-First Steps
[ ] ADRs für Cross-Modul-Entscheidungen (GP-03)
[ ] research.md vorhanden (Pflicht bei KRITIS/Standard)
[ ] quickstart.md vorhanden
[ ] ExecPlans für Tasks mit 5+ Dateien (GP-04)
── Ergebnis: PASS | FAIL ───────────────────
```

### Gate G4: Analyze → Implement
```
── Gate G4 ─────────────────────────────────
[ ] Keine BLOCKER-Befunde offen
[ ] GP-Score ≥ Profil-Schwelle
[ ] STRIDE vollständig (laut Profil)
[ ] Custom-Checks bestanden (falls vorhanden)
── Ergebnis: PASS | FAIL ───────────────────
```

### Gate G5: Implement → Complete
```
── Gate G5 ─────────────────────────────────
[ ] Artefakt-Vollständigkeits-Check (siehe I.5)
[ ] Alle Tasks aus tasks.md abgeschlossen
[ ] Spec-First Chain Compliance geprüft
[ ] ARCHITECTURE.md aktuell
[ ] Kein staler Marker ohne Owner (GP-06)
── Ergebnis: PASS | FAIL ───────────────────
```

### Skip-Protokoll (KRITIS: vollständig, Standard: Einzeiler, Startup: nicht nötig)

```markdown
## Skip-Protokoll: [Gate-ID]

**Gate:** [z.B. G2 — Clarify → Plan]
**Begründung:** [z.B. Spike/PoC, Nutzer hat explizit bestätigt]
**Risiko:** [Was wird durch Überspringen nicht geprüft?]
**Kompensation:** [Welche Maßnahmen reduzieren das Risiko?]
**Entscheider:** [Wer hat zugestimmt?]
**Datum:** [YYYY-MM-DD]
```

---

## I.3 Anti-Pattern-Erkennung (7 Patterns)

Bei jeder Story-Erzeugung und jedem Review automatisch prüfen:

| # | Anti-Pattern | Beschreibung | Erkennung | Schweregrad |
|---|-------------|-------------|-----------|-------------|
| AP-01 | Implementation Bias | Requirement beschreibt HOW statt WHAT | Technologie-Begriffe in Story-Text | MAJOR |
| AP-02 | Gold Plating | Überflüssige Features ohne Business Value | Story ohne Impact-Mapping-Referenz | MINOR |
| AP-03 | Implizite Annahmen | Unausgesprochene Voraussetzungen | Fehlende `[Annahme: ...]`-Marker | MAJOR |
| AP-04 | Vage Quantifizierung | Nicht messbare Anforderungen | "schnell", "viele", "einfach" etc. | BLOCKER |
| AP-05 | Scope Creep | Schleichende Erweiterung ohne Spec-Update | Tasks ohne Spec-Referenz (GP-02) | BLOCKER |
| AP-06 | Missing Negative | Nur Happy Path, keine Fehlerfälle | <2 Gherkin-Szenarien, kein Unwanted-Pattern | MAJOR |
| AP-07 | Orphan Artifact | Artefakt ohne Bezug zum Workflow | Task ohne Story, Story ohne Spec | MAJOR |

---

## I.4 5W-Pflichtblock (Reverse Engineering)

Bei Modus 9 (Discover) ist die 5W-Analyse das erste Pflicht-Artefakt — vor constitution.md und spec.md.

```markdown
## 5W-Analyse: [Systemname]

### WER — Akteure und Rollen
| Akteur | Rolle | Nutzungshäufigkeit | Evidenz |
|--------|-------|-------------------|---------|
| [Akteur] | [Rolle] | [Täglich/Wöchentlich/...] | [Code: auth.py, Doku: README] |

**Konfidenz:** [Hoch/Mittel/Niedrig]

### WAS — Kernfunktionen
| Funktion | Beschreibung | Evidenz |
|----------|-------------|---------|
| [Funktion] | [Was tut sie] | [Quellcode-Referenz, API-Endpoint] |

**Konfidenz:** [Hoch/Mittel/Niedrig]

### WARUM — Geschäftszweck
| Zweck | Begründung | Evidenz |
|-------|-----------|---------|
| [Geschäftsziel] | [Warum existiert dieses System] | [Stakeholder-Aussage, Doku] |

**Konfidenz:** [Hoch/Mittel/Niedrig]

### WIE — Technische Umsetzung
| Komponente | Technologie | Evidenz |
|-----------|------------|---------|
| [Komponente] | [Stack/Framework] | [Code, Config, Dependencies] |

**Konfidenz:** [Hoch/Mittel/Niedrig]

### WANN — Zeitliche Aspekte
| Aspekt | Detail | Evidenz |
|--------|--------|---------|
| Erstellung | [Zeitraum] | [Git-Historie, Dateidaten] |
| Letztes Update | [Datum] | [Commit-Log] |
| Nutzungsmuster | [Peak-Zeiten, Batch-Jobs] | [Logs, Monitoring, Cron] |

**Konfidenz:** [Hoch/Mittel/Niedrig]

### Gesamtkonfidenz
| Dimension | Konfidenz | Offene Fragen |
|-----------|----------|---------------|
| WER | ... | ... |
| WAS | ... | ... |
| WARUM | ... | ... |
| WIE | ... | ... |
| WANN | ... | ... |
```

**Abschlusskriterium:** Alle 5 Dimensionen bearbeitet. Konfidenz-Bewertung für jede Dimension. Offene Fragen als Input für Clarify-Phase dokumentiert.

---

## I.5 Artefakt-Vollständigkeits-Check (vor G5 COMPLETE)

Vor Abschluss eines Features prüft die Enforcement Engine die gesamte Artefaktkette:

| Artefakt | Pflicht | Prüfung |
|----------|---------|---------|
| specforge.json | Ja (einmal) | Existiert? Profil gesetzt? |
| constitution.md | Ja (einmal) | Existiert? GPs laut Profil enthalten? DoD definiert? |
| ARCHITECTURE.md | Ja (einmal) | Existiert? Codemap aktuell? Invarianten mit IDs? |
| spec.md | Ja | EARS vollständig? Gherkin ≥2? STRIDE laut Profil? NFRs? Clarifications? |
| plan.md | Ja | Architektur dokumentiert? ADRs vorhanden (GP-03)? |
| research.md | KRITIS/Standard | Research-Fragen beantwortet? Versions-Matrix? |
| quickstart.md | Ja | Setup-Anleitung? Konventionen? Erster Task? |
| tasks.md | Ja | Spec-First Steps markiert? ExecPlans bei 5+ Dateien (GP-04)? |
| tech-debt-tracker.md | Wenn Debt | Alle bekannten Schulden erfasst (GP-10)? |

**Ergebnis:**
```
COMPLETE-Readiness: [Ja / Nein]
Fehlende Artefakte: [Liste]
Unvollständige Artefakte: [Liste mit Befund]
GP-Score: [X/10]
```

---

## I.6 Reverse-Engineering Path (State Machine)

```
   G0-RE          G1-RE          G2-RE          G3-RE          G4-RE
[DISCOVER] → [5W-ANALYSE] → [SPEC-GEN] → [QS-1+QS-2] → [FINALIZE] → [PLAN?]
     │              │              │            │   │
     │         Pflicht-Artefakt    │       Vollständ. Konsist.
     │         vor spec.md         │       Loop       Loop
     └─── Discovery-Protokoll ─────┘
```

Phase Gates im Reverse-Path:
- **G0-RE:** Discovery-Protokoll erzeugt? Quellen dokumentiert?
- **G1-RE:** 5W-Analyse komplett? Alle 5 Dimensionen mit Konfidenz?
- **G2-RE:** spec.md erzeugt mit identischem Qualitätsanspruch wie Forward-Path?
- **G3-RE:** QS-Schleife 1 (Vollständigkeit) + QS-Schleife 2 (Konsistenz/Stringenz) bestanden?
- **G4-RE:** Finalisierung — spec.md konsistent, Ist/Soll-Delta dokumentiert?

Nach G4-RE Übergang in den Forward-Path ab G2 (Clarify) oder G3 (Plan).
