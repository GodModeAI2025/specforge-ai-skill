# Modus 7: Review — Bestehende Requirements prüfen

**Trigger:** Bestehende Requirements, Specs oder Stories als Input.
**Methode:** 3-Ebenen-Prüfkatalog mit deterministischer Schweregrad-Zuordnung.

## Profil-Steuerung

- **KRITIS:** Alle 3 Ebenen Pflicht; STRIDE vollständig (alle 6 Kategorien); GP-Score ≥ 9/10; Keine offenen BLOCKER/MAJOR erlaubt
- **Standard:** Ebene 1 + 2 Pflicht; Ebene 3 für SEC-Stories; GP-Score ≥ 8/10; BLOCKER müssen gelöst, MAJOR dokumentiert
- **Startup:** Ebene 1 Pflicht; Ebene 2 + 3 empfohlen; GP-Score ≥ 6/10; Soft-Empfehlungen statt Blocker

## Ablauf (deterministisch)

### Phase 7a: Vorbereitung
1. Profil aus specforge.json lesen
2. Input identifizieren (spec.md, einzelne Story, Requirements-Dokument)
3. Referenzdateien laden:
   → `references/checklists/ears-syntax.md` für EARS-Prüfung
   → `references/checklists/golden-principles.md` für GP-Compliance
   → `references/checklists/stride-guide.md` (bei KRITIS oder SEC-Stories)
   → `references/checklists/kritis-nfr.md` (bei KRITIS)
   → `references/custom/*.md` (falls vorhanden)

### Phase 7b: Prüfung — 3 Ebenen

Jede Ebene wird vollständig durchlaufen. Keine Ebene darf übersprungen werden, wenn laut Profil Pflicht.

#### Ebene 1 — Requirement-Qualität (alle Profile: Pflicht)

| # | Kriterium | Prüfung | Schweregrad bei Verstoß |
|---|-----------|---------|------------------------|
| RQ-01 | Eindeutigkeit | Keine vagen Begriffe aus Blocklist (enforcement-engine.md) | BLOCKER (AP-04) |
| RQ-02 | Testbarkeit | Konkretes Pass/Fail-Kriterium vorhanden | MAJOR |
| RQ-03 | EARS-Konformität | Explizit benanntes EARS-Pattern; korrekte Syntax | MAJOR |
| RQ-04 | Gherkin-Qualität | ≥2 Szenarien pro Story (Happy Path + Fehlerfall) | MAJOR (AP-06) |
| RQ-05 | Atomarität | Ein Requirement = eine testbare Aussage | MINOR |
| RQ-06 | Anti-Pattern-Freiheit | AP-01 bis AP-08 geprüft | Schweregrad laut AP-Tabelle |
| RQ-07 | Annahmen-Markierung | Alle Annahmen als `[Annahme: ...]` gekennzeichnet | MAJOR (AP-03) |
| RQ-08 | ID-Schema | SF-[Präfix]-[NNN] Format eingehalten | MINOR |

#### Story-Quality-Score (SQS) — numerische Qualitätsbewertung

Zusätzlich zur binären Prüfung (bestanden/nicht bestanden) erzeugt der Review einen numerischen **Story-Quality-Score (SQS)** pro Story. Der SQS misst *Formulierungsqualität*, nicht Governance-Compliance (das ist der GP-Score).

| Dimension | Gewichtung | 0 Punkte | 2.5 Punkte | 5 Punkte |
|-----------|-----------|----------|-----------|----------|
| **Titel-Qualität** | 15% | <5 Wörter, kein Feature erkennbar | Feature erkennbar, <30 Zeichen | 8–12 Wörter, Feature + Kontext + Nutzen, 50–80 Zeichen |
| **Description-Vollständigkeit** | 25% | "As a/I want/so that" fehlt oder generisch ("der Nutzer") | Alle 3 Teile vorhanden, aber Nutzen vage | Konkrete Rolle, klares Feature, messbarer Geschäftswert |
| **Gherkin-Tiefe** | 25% | Kein Gherkin oder nur Happy Path | 2 Szenarien (Happy + 1 Fehlerfall) | ≥3 Szenarien (Happy + Fehlerfall + Edge Case), messbare Then-Schritte |
| **SOPHIST-Konformität** | 20% | ≥3 SOPHIST-Verletzungen (AP-08) | 1–2 Verletzungen | Keine Verletzungen: aktive Sprache, eindeutige Begriffe, konkrete Werte |
| **EARS-Präzision** | 15% | Kein EARS-Pattern erkennbar | Pattern benannt, aber Syntax fehlerhaft | Pattern korrekt, alle Bedingungen explizit |

**SQS-Berechnung:** Gewichteter Durchschnitt aller Dimensionen → Ergebnis 0.0–5.0

**SQS-Schwellen:**

| SQS | Bewertung | Gate-Auswirkung |
|-----|-----------|-----------------|
| ≥ 4.0 | Produktionsreif | Keine |
| 3.0–3.9 | Sprint-ready, Optimierungen möglich | F1 (INFO) — Empfehlung zur Verbesserung |
| 2.0–2.9 | Überarbeitungsbedarf | F2 (WARNING) — Pflicht-Task vor Go-Live |
| < 2.0 | Grundlegend überarbeiten | F3 (CONDITIONAL) — Risiko-Akzeptanz oder Überarbeitung |

**SQS im Review-Protokoll (Ergänzung):**
```markdown
### Story-Quality-Score
| Story-ID | Titel | Description | Gherkin | SOPHIST | EARS | **SQS** |
|----------|-------|-------------|---------|---------|------|---------|
| SF-FUNC-001 | 4.5 | 4.0 | 3.5 | 5.0 | 4.0 | **4.15** |

**Durchschnitt-SQS:** [X.X] / 5.0
```

#### Ebene 2 — Governance-Compliance (Scope laut Profil)

| # | Golden Principle | Prüfung | Pflicht ab Profil |
|---|-----------------|---------|-------------------|
| GC-01 | GP-01 Schema-Hygiene | API-Contracts mit Fixtures + Tests | Standard |
| GC-02 | GP-02 Spec-before-Code | Jeder Task hat Spec-Referenz | Alle |
| GC-03 | GP-03 ADR-Disziplin | Modulübergreifende Entscheidungen → ADR | Standard |
| GC-04 | GP-04 ExecPlan-Pflicht | Tasks mit 5+ Dateien → EP-*.md | Standard |
| GC-05 | GP-05 Invariant-Traceability | Tests referenzieren Invariant-IDs | KRITIS |
| GC-06 | GP-06 Keine stale Marker | TODO/TBD/FIXME mit Datum + Owner | Alle |
| GC-07 | GP-07 Folder Convention | Artefakte in Convention-Verzeichnissen | Alle |
| GC-08 | GP-08 Prinzip-Unverletzlichkeit | GP-Verstöße blockieren bis Lösung | KRITIS |
| GC-09 | GP-09 Abhängigkeitsrichtung | Consumer → Provider-Interface, nicht Interna | Standard |
| GC-10 | GP-10 Schulden-Tracking | Tech-Debt in tech-debt-tracker.md | Standard |

**Startup-Minimum:** Nur GP-02 + GP-07 prüfen.

**GP-Score-Berechnung:** `GP-Score = Anzahl erfüllter GPs / Anzahl laut Profil aktiver GPs`
- KRITIS: GP-01–GP-10 alle aktiv → Score = X/10
- Standard: GP-01–GP-08 aktiv (konfigurierbar) → Score = X/8 (normiert auf /10)
- Startup: GP-02 + GP-07 aktiv → Score = X/2 (normiert auf /10)

#### Ebene 3 — Security & Compliance (Scope laut Profil)

| # | Prüfung | KRITIS | Standard | Startup |
|---|---------|--------|----------|---------|
| SC-01 | STRIDE alle 6 Kategorien | Pflicht | SEC-Stories | Optional |
| SC-02 | KRITIS-NFRs (AVA, SEC, AUD, PER, DAT, OPS) | Pflicht | — | — |
| SC-03 | NIS2-Artikel-Mapping | Pflicht | Optional | — |
| SC-04 | DSGVO Art. 25, 35 bei PII | Pflicht | Pflicht | Optional |
| SC-05 | Custom Security Checks | Falls vorhanden | Falls vorhanden | — |

**Referenzen laden:**
- KRITIS: `references/checklists/stride-guide.md` + `references/checklists/kritis-nfr.md`
- Standard: `references/checklists/stride-guide.md` (bei SEC-Stories)
- Startup: Nur bei expliziter Anfrage

### Phase 7c: GP-Score berechnen

```
GP-Score = Erfüllte GPs / Aktive GPs (laut Profil)

Schwellwerte:
  KRITIS:  ≥ 9/10 → PASS | < 9/10 → FAIL
  Standard: ≥ 8/10 → PASS | < 8/10 → FAIL
  Startup:  ≥ 6/10 → PASS | < 6/10 → FAIL
```

### Phase 7d: Konsolidierung

1. Findings aller 3 Ebenen zusammenführen
2. Sortierung: BLOCKER → MAJOR → MINOR
3. Gesamtbewertung ableiten:
   - **Freigabefähig:** Keine BLOCKER, GP-Score ≥ Schwelle
   - **Überarbeitung empfohlen:** Keine BLOCKER, aber MAJOR-Findings > 3 oder GP-Score knapp
   - **Nicht freigabefähig:** BLOCKER vorhanden oder GP-Score < Schwelle

## Output: Review-Protokoll (deterministisch)

```markdown
## Review-Protokoll: [ID / Titel]
**Profil:** [KRITIS / Standard / Startup]
**Geprüfte Ebenen:** [1, 2, 3]
**Input:** [spec.md / Story / Requirements-Quelle]

### Ebene 1 — Requirement-Qualität
| # | Kriterium | Bewertung | Schweregrad | Befund | Vorschlag |
|---|-----------|----------|------------|--------|-----------|
| RQ-01 | Eindeutigkeit | ✅/❌ | — / BLOCKER | [Befund] | [Vorschlag] |

### Ebene 2 — Governance-Compliance
| # | Golden Principle | Status | Schweregrad | Befund | Aktion |
|---|-----------------|--------|------------|--------|--------|
| GC-01 | GP-01 | ✅/❌/n.a. | — / MAJOR | [Befund] | [Aktion] |

### Ebene 3 — Security & Compliance
| Kategorie | Geprüft | Befund | Schweregrad | Mitigation |
|-----------|---------|--------|------------|-----------|
| Spoofing | ✅/❌ | [Befund] | MAJOR | [Maßnahme] |

### Zusammenfassung
**BLOCKER:** [Anzahl] | **MAJOR:** [Anzahl] | **MINOR:** [Anzahl]
**GP-Score:** [X/10] (Schwelle: [Y/10])
**Gesamtbewertung:** [Freigabefähig / Überarbeitung empfohlen / Nicht freigabefähig]
```

## Stringenz-Regeln (Enforcement)

| Regel | Enforcement | Schweregrad |
|-------|-----------|------------|
| Vage Begriffe aus Blocklist | Automatisch in Ebene 1 (RQ-01): "schnell", "viele", "einfach", "skalierbar", "sicher", "zuverlässig" → AP-04 | BLOCKER |
| Fragen-Budget | Max. 3 Fragen pro Runde an den Nutzer; Review-interne Prüfung unbegrenzt | n.a. |
| Anti-Pattern-Prüfung | AP-01–AP-08 + custom APs aus `references/custom/anti-patterns-custom.md` | Schweregrad laut AP-Tabelle |
| Artefakt-Erzeugung als Datei | review-protocol.md als separate Datei, nicht inline | MAJOR |
| Gherkin-Minimum | ≥2 Szenarien pro Story (RQ-04) — Unterschreitung = MAJOR (AP-06) | MAJOR |
| EARS-Pflicht | Jede Story hat explizit benanntes Pattern (RQ-03) | MAJOR |
| Schweregrad-Zuweisung | Deterministisch nach enforcement-engine.md Schweregrad-Tabelle | n.a. |

## Erweiterbarkeit

| Erweiterungspunkt | Wie | Wo |
|-------------------|-----|-----|
| Neue Ebene-1-Prüfpunkte | RQ-09+ in `references/custom/review-quality-custom.md` | Custom Extension |
| Neue GP-Checks | GP-11+ in `references/custom/golden-principles-custom.md` | Custom Extension |
| Branchenspezifische Security-Checks | SC-06+ in `references/custom/@branche-compliance/security-checks.md` | Custom Extension |
| Neue Anti-Patterns | AP-08+ in `references/custom/anti-patterns-custom.md` | Custom Extension |
| Custom Review-Rollen (→ Modus 6 Integration) | `references/custom/@team-review-rollen/rollen/*.md` | Custom Extension |

## Fehlerbehandlung

| Situation | Reaktion |
|-----------|---------|
| Kein Input / leerer Input | → Fehlermeldung: "Bitte spec.md oder Requirements übergeben" |
| specforge.json fehlt | → Standard-Profil anwenden, Hinweis ausgeben |
| Profil-Wechsel mid-session | → Review mit neuem Profil-Scope wiederholen |
| Input ohne EARS-Format | → Ebene 1 RQ-03 als MAJOR markieren, Reformulierung vorschlagen |
| Fehlende Referenzdateien | → Klare Fehlermeldung: "[Datei] nicht gefunden — Prüfpunkt übersprungen, als FAIL gewertet" |
| Mixed-Language Input | → Sprachverhalten gemäß Orchestrator (DE/EN nachfragen) |
| Widersprüchliche Anforderungen | → Als AP-03 (Implizite Annahmen) + eigenständiges Finding dokumentieren |
| Übermäßig viele Stories (>20) | → Top-20 nach Schweregrad priorisieren, Rest als Batch-Review |

## Abgrenzung

- **Review (Modus 7)** = Einzelne Requirements/Stories prüfen (Qualität einzelner Artefakte)
- **Analyze (Modus 4)** = Cross-Artefakt-Konsistenz (System als Ganzes)
- **Stakeholder-Sim (Modus 6)** = Perspektivische Blindspot-Analyse (Rollen-basiert)

## Erzeugte Artefakte

| Artefakt | Pfad |
|----------|------|
| review-protocol.md | specs/use-cases/\<feature\>/ |
| Aktualisierte spec.md (optional) | specs/use-cases/\<feature\>/ |
