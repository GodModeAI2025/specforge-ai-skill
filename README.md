# SpecForge — Specs schmieden, nicht schreiben
**Spec-Driven Requirements Engineering als KI-Skill für Claude.**

SpecForge kombiniert [GitHub Spec Kit](https://github.com/github/spec-kit), Harness-Patterns (Golden Principles, Spec-First Chain, STRIDE, Folder Convention) mit EARS-Syntax, Gherkin Acceptance Criteria und automatischen KRITIS/NIS2-NFRs zu einem modularen, selbsttragenden Skill-System.

---

## Was ist SpecForge?

SpecForge ist ein Claude-Skill (Cowork Plugin / Project Knowledge), der Requirements Engineering von der Idee bis zum implementierungsreifen Backlog automatisiert — mit Governance-Enforcement statt optionalen Richtlinien.

**Leitprinzip:** Governance ist ein Compiler, kein Komitee.

### Was SpecForge erzeugt

| Artefakt | Beschreibung |
|----------|-------------|
| `constitution.md` | Projektprinzipien, Golden Principles, regulatorischer Rahmen, DoD |
| `spec.md` | Funktionale Spezifikation mit EARS-Requirements und Gherkin-ACs |
| `plan.md` | Technischer Implementierungsplan mit ADRs |
| `research.md` | Technische Tiefenrecherche (Versionen, CVEs, Kompatibilität) |
| `quickstart.md` | Entwickler-Schnelleinstieg |
| `tasks.md` | Task-Breakdown mit Spec-First Chain und Parallelisierungsmarkern |

### Was SpecForge prüft

- **10 Golden Principles** (GP-01 bis GP-10) — enforceable, nicht optional
- **STRIDE-Analyse** — alle 6 Kategorien für security-relevante Stories
- **NFR-Scan mit F-Stufen** — automatischer Scan gegen 41 KRITIS/NIS2-Prüfpunkte + erweiterbar über Extensions (z.B. DORA mit 58 Prüfpunkten). 6-stufiges Schweregrad-System (F0–F5) mit CONDITIONAL-Gate
- **Cross-Artifact-Konsistenz** — Spec ↔ Plan ↔ Tasks Abgleich mit Re-Analyze-Loop
- **EARS-Konformität** — jedes Requirement in einem der 5 EARS-Patterns
- **Gherkin-Qualität** — min. 2 Szenarien pro Story
- **8 Anti-Patterns** (AP-01 bis AP-08) — inkl. SOPHIST-Verletzung (Passiv, Negation, Generik)
- **Story-Quality-Score (SQS)** — numerische Qualitätsbewertung (0–5) pro Story in Review und Analyze
- **Testfall-Ableitung** (Modus 10 Derive) — Gherkin → strukturierte Testfälle mit Testabdeckungsmatrix
- **Enforcement Engine** — Phase Gates G0–G5 mit State Machine, F-Stufen-basiertem Gate-System (PASS/CONDITIONAL/FAIL), Skip-Protokoll und Artefakt-Vollständigkeits-Check
- **Regulierungs-Extensions** — erweiterbar über `references/custom/@{regulierung}/` mit Manifest-Auto-Detection. Mitgeliefert: DORA (EU 2022/2554), BAIT (Stub)

---

## Installation

### Variante 1: Claude.ai — Als Projekt-Knowledge

1. Öffne ein Claude-Projekt unter [claude.ai](https://claude.ai)
2. Gehe zu **Project Knowledge**
3. Lade den gesamten `specforge/`-Ordner hoch (SKILL.md + references/)
4. SpecForge ist sofort aktiv — der Skill erkennt den Modus aus dem Kontext

### Variante 2: Claude Cowork — Als Plugin/Skill

1. Kopiere den gesamten Skill-Ordner in dein Cowork-Plugin-Verzeichnis:
   ```
   mein-plugin/
   └── skills/
       └── specforge/
           ├── SKILL.md
           └── references/
               ├── 01-specify.md
               ├── 02-clarify.md
               ├── ...
               ├── checklists/
               ├── templates/
               ├── conventions/
               └── enforcement/
   ```
2. Registriere den Skill in deiner `plugin.json`
3. SpecForge ist als Skill verfügbar

### Variante 3: Claude Code — Als Projekt-Kontext

1. Lege den Skill-Ordner in dein Repo:
   ```
   .claude/
   └── knowledge/
       └── specforge/
           ├── SKILL.md
           └── references/
   ```
2. Alternativ: Referenziere die Datei in deiner `CLAUDE.md`:
   ```markdown
   ## Knowledge
   Read .claude/knowledge/specforge/SKILL.md for Requirements Engineering guidance.
   ```

---

## Verwendung

### Modus 1: Specify — Spezifikation erstellen

Beschreibe ein Feature, Problem oder eine Idee. SpecForge erzeugt eine vollständige `spec.md`.

```
"Ich brauche eine Authentifizierung mit MFA für unser Kundenportal.
 Benutzer sollen sich per E-Mail + Passwort + TOTP einloggen können.
 Sessions laufen nach 8 Stunden ab."
```

SpecForge wird:
- Max. 3 Klärungsfragen stellen (im Clarify-Modus max. 5 pro Runde)
- Regulatorische Anforderungen eigenständig recherchieren
- Min. 3 Stakeholder-Perspektiven durchspielen
- Spec mit EARS-Requirements und Gherkin-ACs schreiben
- KRITIS-NFRs automatisch prüfen und ergänzen
- STRIDE-Analyse für security-relevante Stories durchführen

### Modus 2: Clarify — Offene Fragen klären

```
"Kläre die offenen Fragen in meiner Spec."
```

SpecForge scannt die spec.md nach Lücken, vagen Begriffen und unbestätigten Annahmen. Fragen werden mit Schweregrad (BLOCKER / MAJOR / MINOR) priorisiert.

### Modus 3: Plan & Tasks — Von Spec zum Backlog

```
"Erstelle einen Plan mit TypeScript, PostgreSQL und Next.js.
 Dann generiere die Tasks."
```

SpecForge erzeugt:
- `plan.md` mit Architekturentscheidungen und ADRs
- `research.md` mit Tech-Stack-Recherche
- `quickstart.md` als Entwickler-Schnelleinstieg
- `tasks.md` mit Spec-First Chain Annotationen

Neu in v3: Brownfield-vs-Greenfield-Erkennung, Explore-Phase mit parallelen Architektur-Varianten, Morphological Box + Pugh Matrix.

### Modus 4: Analyze — Konsistenzprüfung

```
"Prüfe die Konsistenz meiner Artefakte."
```

5-Dimensionen-Check: Spec↔Plan, Plan↔Tasks, Spec↔Tasks, GP-Compliance, Security/Compliance. Re-Analyze-Loop (max. 5 Iterationen) bis keine Blocker mehr offen sind.

### Modus 5: Checklist — Quality Gates

```
"Erstelle eine Spec-Readiness-Checklist."
"Erstelle eine DSGVO-Compliance-Checklist."
```

4 Checklist-Typen: Spec-Readiness (Typ A), Compliance (Typ B), Security (Typ C), Domain-spezifisch (Typ D). Wiederverwendbare Prüflisten — "Unit Tests für Prosa".

### Modus 6: Stakeholder-Simulation

```
"Simuliere einen Security Reviewer und einen Datenschutzbeauftragten
 für meine Spec."
```

8 Rollen verfügbar: Product Owner, System Architect, Contract Guardian, Security Reviewer, Data Engineer, Harness Auditor, Endnutzer, Datenschutzbeauftragter. Neu in v3: Deterministische Rollenauswahl per Keyword-Matching, Gate-Integration (Findings blockieren Gate G4), Simulations-Limit.

### Modus 7: Review — Bestehende Requirements prüfen

```
"Prüfe diese User Stories auf Qualität und Compliance."
[Stories einfügen oder hochladen]
```

3-Ebenen-Review: Requirement-Qualität, Governance-Compliance, Security & Compliance. Neu in v3: GP-Score-Formel für reproduzierbare Bewertungen, vollständig spezifizierter 3-Ebenen-Katalog.

### Modus 8: Management & Traceability

```
"Erstelle eine Traceability Matrix."
"Führe einen Spec-First Chain Audit durch."
"Prüfe auf stale Marker."
```

Neu in v3: 7 Management-Funktionen (Traceability Matrix, SFC-Audit, ExecPlan-Übersicht, Tech-Debt-Report, Spec-Diff, Freshness-Check, Analyze-Historie). KRITIS-Skip-Protokoll für übersprungene Phase Gates.

### Modus 9: Discover — Bestandsdokumentation

```
"Dokumentiere den Bestand dieses Systems."
"Erstelle eine Spec aus dem vorhandenen Code."
"Reverse-engineer die Anforderungen."
```

Reverse Spec: Vom bestehenden System rückwärts zur vollwertigen spec.md. Zwei verpflichtende QS-Schleifen — erst Vollständigkeitsprüfung, dann Konsistenz- und Stringenzprüfung. Neu in v3: 5W-Analyse als Pflichtblock, QS-Loops mit max. 5 Iterationen und Terminierung, eigene RE Gates (G0-RE bis G4-RE).

---

## Workflow

SpecForge folgt dem erweiterten SpecKit-v3-Workflow mit vorgelagerter Komplexitätseinschätzung:

```
[Cynefin+Impact] → Constitution → Specify → Clarify → Plan+Research+Quickstart → Tasks → Analyze → Implement → Review
```

Jede Phase hat ein Phase Gate. Überspringen nur mit expliziter Begründung und Skip-Protokoll.

```
┌────────────────┐   ┌──────────┐   ┌─────────┐   ┌─────────┐
│ PHASE 0:       │──▶│ CONSTIT. │──▶│  SPEC   │──▶│ CLARIFY │
│ Cynefin+Impact │   └──────────┘   └─────────┘   └─────────┘
└────────────────┘                                      │
┌──────────┐   ┌─────────────┐   ┌───────────┐   ┌─────▼────────────┐
│  REVIEW  │◀──│  IMPLEMENT  │◀──│  ANALYZE  │◀──│ PLAN+RESEARCH    │
└──────────┘   └─────────────┘   └───────────┘   └──────────────────┘
                                    ▲    │
                                    └────┘ Re-Analyze Loop
```

---

## Folder Convention

SpecForge schlägt bei jedem neuen Projekt diese Verzeichnisstruktur vor:

```
ARCHITECTURE.md
constitution.md
tech-debt-tracker.md
specs/
  principles/          ← Design Principles (P*.md)
  decisions/           ← Architecture Decision Records (adr-*.md)
  system/              ← Systemweite Spezifikationen
  use-cases/           ← Feature-Specs (1 Ordner pro Feature)
    001-feature-name/
      spec.md
      plan.md
      research.md
      quickstart.md
      tasks.md
      contracts/
plans/
  active/              ← Laufende ExecPlans (EP-*.md)
  completed/           ← Abgeschlossene ExecPlans
design/                ← Wireframes, Datenmodelle, Diagramme
```

---

## Golden Principles

| ID | Prinzip | Kurzregel |
|----|---------|-----------|
| GP-01 | Schema-Hygiene | Matching Fixtures + Testabdeckung |
| GP-02 | Spec-before-Code | Keine Implementierung ohne Spec |
| GP-03 | ADR-Disziplin | Cross-Modul-Entscheidungen brauchen ADRs |
| GP-04 | ExecPlan-Pflicht | 5+ Dateiänderungen → ExecPlan |
| GP-05 | Invariant-Traceability | Tests referenzieren Invariant-IDs |
| GP-06 | Keine stale Marker | TODO/TBD/FIXME mit Datum + Owner |
| GP-07 | Dokument-Platzierung | Dateien in Convention-Verzeichnissen |
| GP-08 | Prinzip-Unverletzlichkeit | Verstöße blockieren bis gelöst |
| GP-09 | Abhängigkeitsrichtung | Consumer ≠ Provider-Interna |
| GP-10 | Schulden-Tracking | Debt in tech-debt-tracker.md |

---

## Skill-Architektur

SpecForge v3 ist als **Multi-File-Skill** aufgebaut — ein Orchestrator (SKILL.md) dispatcht zu 9 Fachmodulen und 9 Support-Dateien in einer `references/`-Verzeichnisstruktur:

```
specforge/
├── SKILL.md                              (395 Zeilen — Orchestrator)
└── references/
    ├── 01-specify.md                     (163 Zeilen)
    ├── 02-clarify.md                     (159 Zeilen)
    ├── 03-plan.md                        (242 Zeilen)
    ├── 04-analyze.md                     (141 Zeilen)
    ├── 05-checklist.md                   (132 Zeilen)
    ├── 06-stakeholder-sim.md             (155 Zeilen)
    ├── 07-review.md                      (173 Zeilen)
    ├── 08-management.md                  (199 Zeilen)
    ├── 09-discover.md                    (215 Zeilen)
    ├── checklists/
    │   ├── ears-syntax.md                (79 Zeilen)
    │   ├── golden-principles.md          (100 Zeilen)
    │   ├── kritis-nfr.md                (95 Zeilen)
    │   └── stride-guide.md              (127 Zeilen)
    ├── templates/
    │   ├── spec-template.md              (181 Zeilen)
    │   └── constitution-template.md      (154 Zeilen)
    ├── conventions/
    │   ├── folder-convention.md          (105 Zeilen)
    │   └── spec-first-chain.md           (102 Zeilen)
    └── enforcement/
        └── enforcement-engine.md         (226 Zeilen)
```

**19 Dateien, 3.143 Zeilen total.**

### Warum Multi-File?

- **Separation of Concerns** — Orchestrator bleibt kompakt (395 Zeilen), Module werden nur bei Bedarf geladen
- **Wartbarkeit** — einzelne Module unabhängig aktualisierbar
- **Erweiterbarkeit** — neue Modi, Checklisten oder Profile über `references/custom/` hinzufügbar
- **Audit-freundlich** — jede Datei unabhängig bewertbar und testbar
- **Context-Window-effizient** — statt 3.143 Zeilen auf einmal lädt Claude nur Orchestrator + benötigtes Modul

### Was jedes Modul enthält (Standard-Sektionen)

Jedes der 9 Fachmodule (M01–M09) folgt einer einheitlichen Struktur:

| Sektion | Beschreibung |
|---------|-------------|
| Profil-Steuerung | KRITIS/Standard/Startup-spezifisches Verhalten |
| Ablauf (deterministisch) | Nummerierte Phasen mit konkreten Schritten |
| Output-Template | Markdown-Template für erzeugte Artefakte |
| Stringenz-Regeln (Enforcement) | Tabellarische Regeln mit Schweregraden |
| Erweiterbarkeit | Custom-Extension-Punkte mit Pfaden |
| Fehlerbehandlung | Tabellarische Edge-Case-Behandlung (≥5 Fälle) |
| GP-Mapping | Zuordnung relevanter Golden Principles |
| Erzeugte Artefakte | Artefakt-Tabelle mit Pfaden |

### Orchestrator-Features (SKILL.md)

| Feature | Beschreibung |
|---------|-------------|
| Pre-Flight Checks | specforge.json laden, Profil-Resolution, Referenz-Verfügbarkeit |
| Dispatch-Tabelle | Modus → Modul-Mapping mit Trigger-Keywords |
| Profil-Resolution Cascade | CLI-Flag → specforge.json → Nutzer-Frage → Standard |
| Calendar Versioning | `v<YYMM>` mit Suffix (`-green`, `-yellow`) für Audit-Status |
| Session-Retrospektive | Automatische Zusammenfassung am Session-Ende |
| Erweiterbarkeit | 8 Built-in Extension Points (EARS, Profile, APs, GPs, Modi, ...) |
| Fehlerbehandlung | KRITISCH vs. OPTIONAL Referenzen mit spezifischem Verhalten |
| Audit Trail | Jede Enforcement-Entscheidung wird protokolliert |

---

## Eigenen Skill nach diesem Muster erstellen

SpecForge kann als Blaupause für eigene Skills dienen. Hier die Methodik:

### 1. Frontmatter definieren
```yaml
---
name: MeinSkill
description: Kurzbeschreibung mit Trigger-Keywords. Verwende diesen Skill
  IMMER bei: keyword1, keyword2, keyword3. Auch bei "natürlichsprachlicher
  Trigger", "weiterer Trigger".
---
```

**Regeln für gute Trigger:**
- Technische Begriffe UND natürlichsprachliche Formulierungen
- "Verwende diesen Skill IMMER bei:" signalisiert Claude den Aktivierungszeitpunkt
- "Auch bei:" für indirekte Trigger ("prüfe meine X", "was fehlt bei Y")

### 2. Session-Isolation festlegen

Entscheide: Darf der Skill auf Memories/Vorwissen zugreifen oder ist jede Session ein Blank Slate?

```markdown
## Wissensquellen
MeinSkill arbeitet ausschließlich mit:
1. Session-Kontext
2. Eigenrecherche via Web Search
3. Skill-eigene Referenzen
```

### 3. Modi definieren

Jeder Modus hat:
- **Trigger:** Woran erkennt der Skill, dass dieser Modus gemeint ist?
- **Phasen:** Welche Schritte werden durchlaufen?
- **Artefakte:** Was wird erzeugt?
- **Abschlusskriterium:** Wann ist der Modus fertig?

```markdown
### Modus N: [Name]
**Trigger:** [Beschreibung]
**Phase Na: [Schritt]**
1. ...
2. ...
**Erzeugte Artefakte:**
- ...
```

### 4. Output-Formate als Templates definieren

Gib Claude exakte Templates mit Platzhaltern:

```markdown
## Output-Format: [Artefakt-Typ]
\```markdown
### [ID] [Titel]
**Typ**: ...
**Priorität**: ...
#### Abschnitt
[Inhalt]
\```
```

### 5. Qualitätsregeln als enforceable Constraints

Nicht "versuche X" sondern "X ist Pflicht":

```markdown
## Qualitätsregeln (immer aktiv)
1. **Regel** — Enforcement-Beschreibung
2. **Regel** — Enforcement-Beschreibung
```

### 6. Interaktionsregeln für Gesprächsführung

```markdown
## Interaktionsregeln
1. Max. N Fragen pro Runde
2. Nach [Aktion] einmal validieren
3. Smarte Annahmen mit `[Annahme: ...]` kennzeichnen
```

### 7. Referenzen als separate Dateien

Statt alles inline: Module in `references/` auslagern und per Dispatch-Tabelle referenzieren:

```markdown
## Dispatch-Tabelle
| Modus | Modul | Laden |
|-------|-------|-------|
| 1: Specify | references/01-specify.md | Bei Modus-Aktivierung |
```

### 8. Standardisierte Modul-Sektionen

Jedes Modul sollte enthalten: Profil-Steuerung, Ablauf, Output-Template, Stringenz-Regeln, Erweiterbarkeit, Fehlerbehandlung, GP-Mapping, Erzeugte Artefakte.

### 9. Skill testen

Teste jeden Modus mit:
- Minimalem Input (erkennt der Skill den Modus?)
- Komplexem Input (erzeugt er alle Artefakte?)
- Edge Cases (was passiert bei fehlendem Kontext?)
- Sprachtest (Deutsch → Deutsch, Englisch → Englisch?)

---

## Quellen & Einflüsse

| Quelle | Beitrag zu SpecForge |
|--------|---------------------|
| [GitHub Spec Kit](https://github.com/github/spec-kit) | Spec-Driven Development Workflow, Slash-Commands, Phasenmodell |
| Harness-Patterns | Golden Principles, Spec-First Chain, Folder Convention, Reviewer-Agenten, Hook-Architektur |
| [EARS](https://ieeexplore.ieee.org/document/5328509) | Easy Approach to Requirements Syntax — 5 Requirement-Patterns |
| [Gherkin](https://cucumber.io/docs/gherkin/) | Acceptance Criteria als Given/When/Then |
| [STRIDE](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats) | Threat Modeling Framework — 6 Bedrohungskategorien |
| KRITIS / NIS2 / DSGVO | Regulatorischer Rahmen für kritische Infrastrukturen |
| Cynefin Framework (Dave Snowden, 1999) | Phase 0 — Komplexitätseinschätzung vor Modus-Wahl |
| Impact Mapping (Gojko Adzic, 2012) | Phase 0 — Zielorientierte Scope-Validierung |
| Socratic Method (Platon/Sokrates) | Clarify-Modus — Sokratische Spezifikationsklärung |
| Five Whys (Taiichi Ohno, Toyota) | BLOCKER-Analyse in Clarify |
| MECE Principle (Barbara Minto, McKinsey) | Analyze-Modus — Konsistenzprüfung über 5 Dimensionen |
| Devil's Advocate + Steelmanning | Stakeholder-Simulation — systematische Gegenargumentation |
| Morphological Box (Fritz Zwicky, 1940er) | Plan-Modus — Systematische Lösungsraum-Exploration |
| Pugh Matrix (Stuart Pugh, 1991) | Plan-Modus — Strukturierte Technologiebewertung |
| DDD taktisches Design (Eric Evans, 2003) | Datenmodell in spec.md |
| BLUF + Pyramid Principle (US-Militär / Barbara Minto) | Spec-Zusammenfassungen |
| MoSCoW (Dai Clegg, DSDM) | Story-Priorisierung |
| ADR nach Nygard (Michael Nygard, 2011) | Architecture Decision Records |

---

## Versionierung

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

---

## Lizenz

MIT — siehe [LICENSE](LICENSE).

---

## Mitwirken

Issues und Pull Requests willkommen. Insbesondere:
- Neue Reviewer-Agenten-Definitionen für spezifische Domänen
- **Branchenspezifische NFR-Checklisten** — siehe [CONTRIBUTING-CHECKLISTS.md](CONTRIBUTING-CHECKLISTS.md) für Schema, Validierung und Beispiele. Die DORA-Extension (`references/custom/@dora/`) dient als Referenzimplementierung.
- Übersetzungen (Englische Version)
- Integration mit weiteren KI-Agenten (Cursor, Copilot, Gemini)
- Custom Extensions für `references/custom/`

### Regulierungs-Extensions

| Regulierung | Branche | Status | Pfad |
|-------------|---------|--------|------|
| DORA (EU 2022/2554) | Finanzsektor | ✅ Fertig (58 Prüfpunkte) | `references/custom/@dora/` |
| BAIT | Banken (DE) | 🔧 Stub (8 Prüfpunkte) | `references/custom/@bait/` |
| MaRisk | Finanzsektor (DE) | Offen | — |
| PCI-DSS 4.0 | Zahlungsverkehr | Offen | — |
| EnWG / IT-Sicherheitskatalog | Energiesektor | Offen | — |
