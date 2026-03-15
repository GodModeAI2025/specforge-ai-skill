# SpecForge — Specs schmieden, nicht schreiben

**Spec-Driven Requirements Engineering als KI-Skill für Claude.**

SpecForge kombiniert [GitHub Spec Kit](https://github.com/github/spec-kit), Harness-Patterns (Golden Principles, Spec-First Chain, STRIDE, Folder Convention) mit EARS-Syntax, Gherkin Acceptance Criteria und automatischen KRITIS/NIS2-NFRs zu einem einzigen, selbsttragenden Skill.

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
- **KRITIS/NIS2-NFRs** — automatischer Scan gegen 41 Prüfpunkte in 6 Kategorien
- **Cross-Artifact-Konsistenz** — Spec ↔ Plan ↔ Tasks Abgleich mit Re-Analyze-Loop
- **EARS-Konformität** — jedes Requirement in einem der 5 EARS-Patterns
- **Gherkin-Qualität** — min. 2 Szenarien pro Story

---

## Installation

### Variante 1: Claude.ai — Als Projekt-Knowledge

1. Öffne ein Claude-Projekt unter [claude.ai](https://claude.ai)
2. Gehe zu **Project Knowledge**
3. Lade `SKILL.md` als Knowledge-Datei hoch
4. SpecForge ist sofort aktiv — der Skill erkennt den Modus aus dem Kontext

### Variante 2: Claude Cowork — Als Plugin/Skill

1. Kopiere `SKILL.md` in dein Cowork-Plugin-Verzeichnis:
   ```
   mein-plugin/
   └── skills/
       └── specforge/
           └── SKILL.md
   ```
2. Registriere den Skill in deiner `plugin.json`
3. SpecForge ist als Skill verfügbar

### Variante 3: Claude Code — Als Projekt-Kontext

1. Lege `SKILL.md` in dein Repo:
   ```
   .claude/
   └── knowledge/
       └── specforge.md    ← Inhalt von SKILL.md
   ```
2. Alternativ: Referenziere die Datei in deiner `CLAUDE.md`:
   ```markdown
   ## Knowledge
   Read .claude/knowledge/specforge.md for Requirements Engineering guidance.
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

### Modus 4: Analyze — Konsistenzprüfung

```
"Prüfe die Konsistenz meiner Artefakte."
```

5-Dimensionen-Check: Spec↔Plan, Plan↔Tasks, Spec↔Tasks, GP-Compliance, Security/Compliance. Re-Analyze-Loop bis keine Blocker mehr offen sind.

### Modus 5: Checklist — Quality Gates

```
"Erstelle eine Spec-Readiness-Checklist."
"Erstelle eine DSGVO-Compliance-Checklist."
```

Wiederverwendbare Prüflisten — "Unit Tests für Prosa".

### Modus 6: Stakeholder-Simulation

```
"Simuliere einen Security Reviewer und einen Datenschutzbeauftragten
 für meine Spec."
```

8 Rollen verfügbar: Product Owner, System Architect, Contract Guardian, Security Reviewer, Data Engineer, Harness Auditor, Endnutzer, Datenschutzbeauftragter.

### Modus 7: Review — Bestehende Requirements prüfen

```
"Prüfe diese User Stories auf Qualität und Compliance."
[Stories einfügen oder hochladen]
```

3-Ebenen-Review: Requirement-Qualität, Governance-Compliance, Security & Compliance. Output als strukturiertes Review-Protokoll.

### Modus 8: Management & Traceability

```
"Erstelle eine Traceability Matrix."
"Führe einen Spec-First Chain Audit durch."
"Prüfe auf stale Marker."
```

### Modus 9: Discover — Bestandsdokumentation

```
"Dokumentiere den Bestand dieses Systems."
"Erstelle eine Spec aus dem vorhandenen Code."
"Reverse-engineer die Anforderungen."
```

Reverse Spec: Vom bestehenden System rückwärts zur vollwertigen spec.md. Zwei verpflichtende QS-Schleifen — erst Vollständigkeitsprüfung (jede Funktion/Endpunkt/Business Rule abgebildet?), dann Konsistenz- und Stringenzprüfung (MECE, EARS-Reinheit, Begriffskonsistenz, Ist/Soll-Delta). Erzeugt zusätzlich `discovery-protocol.md` und optional `migration-delta.md`.

---

## Workflow

SpecForge folgt dem erweiterten SpecKit-v3-Workflow mit vorgelagerter Komplexitätseinschätzung:

```
[Cynefin+Impact] → Constitution → Specify → Clarify → Plan+Research+Quickstart → Tasks → Analyze → Implement → Review
```

Jede Phase hat ein Phase Gate. Überspringen nur mit expliziter Begründung.

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

SpecForge ist als **Single-File-Skill** aufgebaut — die gesamte SKILL.md (100 KB, 2.400+ Zeilen) enthält sowohl die Skill-Logik als auch alle 8 Referenz-Anhänge inline:

```
SKILL.md
├── Frontmatter (Name, Description, Trigger-Keywords)
├── Hauptteil
│   ├── Wissensquellen & Session-Isolation
│   ├── Architekturmodell (3-Schichten)
│   ├── Folder Convention
│   ├── Golden Principles Übersicht
│   ├── Workflow-Phasen (Gesamtübersicht)
│   ├── Modi 1–9 (Specify → Discover)
│   ├── Output-Format (User Story Template)
│   ├── Artefakt-Übersicht
│   ├── Sprachverhalten
│   ├── Interaktionsregeln (19 Regeln)
│   └── Qualitätsregeln (22 Regeln)
└── Anhänge A–H (Referenzdokumente)
    ├── A: Spec Template
    ├── B: Constitution Template
    ├── C: EARS-Syntax
    ├── D: KRITIS-NFR-Checkliste
    ├── E: STRIDE-Checkliste
    ├── F: Golden Principles (Detail)
    ├── G: Folder Convention (Detail)
    └── H: Spec-First Chain
```

### Warum Single-File?

- **Keine externen Abhängigkeiten** — funktioniert in Claude.ai, Cowork und Claude Code
- **Copy-Paste-Deployment** — eine Datei hochladen, fertig
- **Versionierung** — eine Datei = ein Commit = ein Zustand
- **Context-Window-freundlich** — Claude lädt den gesamten Skill auf einmal

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

### 7. Referenzen inline als Anhänge

Statt externe Dateien → Anhänge am Ende:

```markdown
## Anhang A: [Referenzname]

**Wann konsultieren:** [Konkreter Auslöser]

[Referenzinhalt]
```

### 8. Skill testen

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
| 2.2 | 2026-03 | +Modus 9 Discover (Bestandsdokumentation & Reverse Spec). Zwei verpflichtende QS-Schleifen: Vollständigkeit + Konsistenz/Stringenz. Rückwärts-Validierung. discovery-protocol.md und migration-delta.md als neue Artefakte. 19 Interaktions- + 22 Qualitätsregeln. |

---

## Lizenz

MIT — siehe [LICENSE](LICENSE).

---

## Mitwirken

Issues und Pull Requests willkommen. Insbesondere:
- Neue Reviewer-Agenten-Definitionen für spezifische Domänen
- Branchenspezifische NFR-Checklisten (Finanz, Pharma, Automotive)
- Übersetzungen (Englische Version der SKILL.md)
- Integration mit weiteren KI-Agenten (Cursor, Copilot, Gemini)
