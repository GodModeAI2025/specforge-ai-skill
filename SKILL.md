---
name: specforge
description: >
  Spec-Driven Requirements Engineering mit Governance-Enforcement.
  Kombiniert GitHub Spec Kit, Harness-Patterns, EARS-Syntax, Gherkin
  und NIS2/KRITIS-NFRs. Erzeugt spec.md, plan.md, tasks.md und mehr.
  Verwende diesen Skill IMMER bei Requirements schreiben, User Stories,
  Spezifikation erstellen, Spec-Driven Development, EARS, Gherkin,
  Requirements Review, Stakeholder-Analyse, KRITIS, NIS2, STRIDE,
  ADR, Clarify, Analyze, Checklist, Research, Quickstart. Auch bei
  "erstelle eine Spezifikation", "was fehlt in diesem Requirement",
  "simuliere einen Security Officer", "STRIDE-Analyse",
  "pruefe Konsistenz", "erstelle Checkliste".
---

# SpecForge — Specs schmieden, nicht schreiben

Spec-Driven RE für KRITIS-regulierte Scrum-Umgebungen. Kern: GitHub Spec Kit + Harness-Patterns (Golden Principles, Spec-First Chain, STRIDE, Folder Convention) + EARS + Gherkin + automatische NIS2/KRITIS-NFRs.

**Leitprinzip: Governance ist ein Compiler, kein Komitee.** Specs sind Verträge, keine Vorschläge. Enforcement ist automatisch, nicht optional.

### Methodische Grundlagen — Aktivierte Frameworks

SpecForge integriert etablierte Methoden der Softwaretechnik, des Requirements Engineering und der Entscheidungstheorie. Jede Methode wird nach dem **Aktivieren-Eingrenzen-Prüfen-Muster** eingesetzt:

1. **Aktivieren** — Etablierte Methode aufrufen (z.B. Socratic Method)
2. **Eingrenzen** — Auf den SpecForge-Kontext einschränken (z.B. max 5 Fragen, Schweregrad-Labels)
3. **Prüfen** — Verifizieren, ob das Ergebnis den Zweck erfüllt

| Methode | Herkunft | Einsatz in SpecForge |
|---------|----------|---------------------|
| EARS Requirements | Alistair Mavin (Rolls-Royce) | Requirement-Syntax (Anhang C) |
| STRIDE | Microsoft | Threat Modeling (Anhang E) |
| BDD / Gherkin | Dan North | Acceptance Criteria |
| MoSCoW Prioritization | Dai Clegg (DSDM) | Story-Priorisierung (Must/Should/Could/Won't) |
| SSOT (Single Source of Truth) | — | spec.md als autoritative Quelle (GP-02) |
| Socratic Method | Platon/Sokrates (~400 v. Chr.) | Clarify-Modus (Modus 2) |
| MECE Principle | Barbara Minto (McKinsey) | Analyze-Modus (Modus 4) |
| Devil's Advocate + Steelmanning | Advocatus Diaboli (1587) | Stakeholder-Simulation (Modus 6) |
| Five Whys | Taiichi Ohno (Toyota) | BLOCKER-Analyse in Clarify |
| Cynefin Framework | Dave Snowden (1999) | Komplexitätseinschätzung vor Modus-Wahl |
| Impact Mapping | Gojko Adzic (2012) | Optionaler Pre-Specify-Schritt |
| DDD (taktisches Design) | Eric Evans (2003) | Datenmodell in spec.md |
| BLUF + Pyramid Principle | US-Militär / Barbara Minto (1987) | Spec-Zusammenfassungen |
| Morphological Box + Pugh Matrix | Fritz Zwicky (1940er) / Stuart Pugh (1991) | Technologieentscheidungen in plan.md |
| ADR nach Nygard | Michael Nygard (2011) | Architecture Decision Records |

---

## Wissensquellen — Strikte Session-Isolation

**KRITISCHE REGEL — VOR ALLEM ANDEREN BEACHTEN:**

SpecForge arbeitet **ausschließlich** mit:

1. **Session-Kontext**: Informationen aus der **aktuellen** Konversation
2. **Eigenrecherche via Web Search**: Regulatorische Vorgaben, Standards, Domänenwissen — eigenständig recherchiert
3. **Skill-eigene Referenzen**: Anhänge A–I (inline am Ende dieser Datei)

**VERBOTEN:** Memories, Vorwissen über Nutzer/Projekte/Organisationen, Annahmen ohne Session-Grundlage.

**Jede Session ist ein Blank Slate.**

---

## Architekturmodell

SpecForge folgt dem Drei-Schichten-Modell:

```
┌─────────────────────────────────────────────────────┐
│  SKILL LAYER (SpecForge)                            │
│  Modi, EARS, Gherkin, KRITIS-NFR, STRIDE, Review    │
│  Clarify, Analyze, Checklist, Research               │
├─────────────────────────────────────────────────────┤
│  ADAPTER LAYER (Projektspezifisch)                  │
│  constitution.md, ARCHITECTURE.md, Golden Principles│
│  Invariants, review-paths.conf                      │
├─────────────────────────────────────────────────────┤
│  CONVENTION LAYER (Fix für alle Projekte)           │
│  Folder Convention, specs/, plans/, design/          │
│  tech-debt-tracker.md                               │
└─────────────────────────────────────────────────────┘
```

SpecForge erzeugt die Adapter- und Convention-Layer-Artefakte. Der Skill selbst ist die Plugin-Schicht.

---

## Folder Convention (Pflichtstruktur)

Bei jedem neuen Projekt schlägt SpecForge diese Verzeichnisstruktur vor. Sie ist fix und nicht verhandelbar — alle weiteren Artefakte referenzieren diese Pfade.

```
ARCHITECTURE.md          ← Codemap, Doc Map, Golden Principles, Invariants
constitution.md          ← Projektprinzipien, Baseline-NFRs, DoD

specs/
  principles/            ← Design Principles (P*.md)
  decisions/             ← Architecture Decision Records (adr-*.md)
  system/                ← System-Spezifikationen (domain-models, APIs)
  use-cases/             ← Feature-/Capability-Specs (spec.md pro Feature)

plans/
  active/                ← ExecPlans in Arbeit (EP-*.md)
  completed/             ← Abgeschlossene ExecPlans

design/                  ← Design-Dokumente, Wireframes, Datenmodelle
tech-debt-tracker.md     ← Schuldenregister mit IDs und Verantwortlichen
```

Siehe Anhang G (Folder Convention) für Details und Namenskonventionen.

---

## Golden Principles (GP-01 bis GP-10)

Jede `constitution.md` enthält die Golden Principles als enforceable Regeln. SpecForge prüft jede Spezifikation gegen diese Prinzipien.

| ID | Prinzip | Regel | Enforcement |
|----|---------|-------|-------------|
| GP-01 | Schema-Hygiene | Matching Fixtures + Testabdeckung | Spec-First Chain |
| GP-02 | Spec-before-Code | Keine Implementierung ohne Spec-Eintrag | Spec-Phase Gate |
| GP-03 | ADR-Disziplin | Modulübergreifende Entscheidungen brauchen ADRs | Review-Routing |
| GP-04 | ExecPlan-Pflicht | 5+ Dateiänderungen brauchen einen ExecPlan | Tasks-Phase Gate |
| GP-05 | Invariant-Traceability | Tests referenzieren Invariant-IDs | Traceability Matrix |
| GP-06 | Keine stale Marker | TODO/TBD/FIXME brauchen Datum + Owner | Freshness Check |
| GP-07 | Dokument-Platzierung | Dateien in Convention-Verzeichnissen | Folder Convention |
| GP-08 | Prinzip-Unverletzlichkeit | Verstöße blockieren bis gelöst | Self-Assessment |
| GP-09 | Abhängigkeitsrichtung | Consumer ≠ Provider-Interna | Review Agents |
| GP-10 | Schulden-Tracking | Debt in tech-debt-tracker.md | Harness Auditor |

Siehe Anhang F (Golden Principles) für Details und Beispiele.

---

## Workflow-Phasen — Gesamtübersicht

SpecForge folgt dem erweiterten SpecKit-v3-Workflow. Jede Phase hat ein Phase Gate — Überspringen ist nur bei expliziter Begründung erlaubt.

### Phase 0: Komplexitätseinschätzung (Cynefin) + Impact Mapping

Vor jedem neuen Feature prüft SpecForge zwei Dinge:

**Methode 1: Cynefin Framework (Dave Snowden, 1999)** — Sensemaking-Framework mit 5 Domänen.
**Delta:** Feature einordnen, um Formalismus-Grad zu bestimmen:
- **Klar** → Specify direkt, Clarify optional → schlanker Durchlauf
- **Kompliziert** → Voller Workflow (Specify → Clarify → Plan → Analyze) → Expertenwissen nötig
- **Komplex** → Spike/PoC zuerst, dann erst Specify → Emergente Anforderungen
- **Chaotisch** → Sofort handeln, nachträglich spezifizieren → Krisenmodus
**Verify:** Passt der gewählte Formalismus-Grad zur Domäne des Features?

**Methode 2: Impact Mapping (Gojko Adzic, 2012)** — Zielorientierte Scope-Steuerung.
**Delta:** 4 Ebenen als Eingangsprüfung vor Specify:
1. **Ziel (Warum?)** — Welches Geschäftsziel wird verfolgt?
2. **Akteure (Wer?)** — Wer kann die gewünschte Auswirkung erzeugen oder verhindern?
3. **Auswirkungen (Wie?)** — Wie muss sich das Verhalten der Akteure ändern?
4. **Liefergegenstände (Was?)** — Was müssen wir bauen?
**Verify:** Lässt sich jedes geplante Feature auf ein Geschäftsziel zurückführen? Wenn nein → Scope Creep erkannt, bevor die Spec geschrieben wird.

**Phase 0 ist optional**, aber empfohlen bei: neuen Produkten, Features ohne klaren Business Case, Stakeholder-Konflikten über Prioritäten.

```
┌───────────────────────────────────────────────────────────────────────┐
│                        SpecForge Workflow                             │
│                                                                       │
│  ┌──────────┐   ┌──────────┐   ┌─────────┐   ┌──────────────────┐   │
│  │ 0 CYNEF. │──▶│ 1 CONST. │──▶│ 2 SPEC  │──▶│ 3 CLARIFY        │   │
│  │ +IMPACT  │   │          │   │         │   │ (Socratic)       │   │
│  └──────────┘   └──────────┘   └─────────┘   └──────────────────┘   │
│       │              │             │                │                 │
│       ▼              ▼             ▼                ▼                 │
│  Cynefin-Einord. constitution  spec.md        Clarifications         │
│  Impact Map      .md                          in spec.md             │
│                                                                       │
│  ┌──────────────────┐   ┌─────────┐   ┌──────────────────┐          │
│  │ 4 PLAN+RESEARCH  │──▶│ 5 TASKS │──▶│ 6 ANALYZE (MECE) │          │
│  └──────────────────┘   └─────────┘   └──────────────────┘          │
│       │                      │              │ ▲                       │
│       ▼                      ▼              ▼ │ Loop                  │
│  plan.md, research.md   tasks.md       Fix ──┘                       │
│  quickstart.md                                                        │
│                                                                       │
│  ┌───────────┐   ┌──────────┐                                       │
│  │ 7 IMPLMNT │──▶│ 8 REVIEW │                                       │
│  └───────────┘   └──────────┘                                       │
│                       │                                              │
│                       ▼                                              │
│                  Review-Protokoll                                     │
│                                                                       │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─   │
│  Jederzeit: CHECKLIST · STAKEHOLDER-SIM (Devil's Advocate)           │
│             TRACEABILITY · CYNEFIN-REASSESSMENT                      │
└───────────────────────────────────────────────────────────────────────┘
```

---

## Modi

SpecForge erkennt den Modus aus dem Kontext. Im Zweifel wird gefragt.

### Modus 1: Specify — Interaktive Spezifikation

**Trigger:** Feature, Problem, Idee oder Prozess wird beschrieben.

**Phase 1a: Constitution + Folder Setup (einmalig pro Projekt)**

Wenn noch keine Projektprinzipien existieren:
1. Folder Convention vorschlagen und bestätigen lassen
2. `constitution.md` erzeugen mit: Projektprinzipien, Golden Principles (GP-01–GP-10), regulatorischem Rahmen (KRITIS/NIS2/DSGVO), Sicherheits-Baseline, Definition of Done auf Spec-Ebene
3. Lücken gezielt erfragen — maximal 3 Fragen pro Runde

Siehe Anhang B (Constitution Template) für das vollständige Template.

**Phase 1b: Spec erstellen**

1. **Kontexterfassung** — Max. 3 Fragen zu Domäne, Nutzergruppe, Systemgrenzen
2. **Web-Recherche** — Eigenständig regulatorische/domänenspezifische Anforderungen recherchieren
3. **Stakeholder-Simulation** — Mind. 3 Perspektiven durchspielen (siehe Modus 3)
4. **Spec schreiben** — Im Spec-Kit-Format `spec.md` (siehe Anhang A)
5. **EARS-Formulierung** — Jedes Requirement in EARS-Syntax (siehe Anhang C)
6. **KRITIS-NFR-Scan** — Automatisch gegen Checkliste (siehe Anhang D)
7. **STRIDE-Analyse** — Security-Review gegen alle 6 Kategorien (siehe Anhang E)
8. **Self-Assessment** — Spec gegen Constitution + Golden Principles prüfen
9. **Validierung** — Nutzer einmal fragen: "Deckt das dein Szenario ab?"

---

### Modus 2: Clarify — Sokratische Spezifikationsklärung

**Methode:** Socratic Method (Platon/Sokrates, ~400 v. Chr.) — geführte Entdeckung durch Fragen statt direkter Instruktion. Aktiviert: Maieutik (Hebammenkunst der Ideen), Elenchos (Aufdecken von Widersprüchen), Aporie (produktive Verwirrung), Annahmen-sichtbar-machen.
**Delta:** Fokus auf Stakeholder-Konflikte, implizite Annahmen und Systemgrenzen. Max. 5 Fragen pro Runde. Jede Frage referenziert eine Story-ID. Schweregrade steuern die Priorisierung.
**Verify:** Haben die Fragen Annahmen sichtbar gemacht, die vorher implizit waren?

**Trigger:** `spec.md` existiert, offene Fragen oder unterspezifizierte Bereiche vorhanden. Empfohlen: **immer** zwischen Specify und Plan ausführen.

**Wann Pflicht:**
- Vor jeder Plan-Phase (es sei denn, der Nutzer erklärt explizit "Spike" oder "explorativer Prototyp")
- Wenn spec.md vage Begriffe, TBD-Marker oder offene Fragen enthält
- Wenn Stakeholder-Simulation Lücken identifiziert hat

**Wann optional:**
- Spike / Proof-of-Concept mit bewusst reduziertem Scope
- Triviale Änderungen an bestehender, bereits geklärter Spec

**Ablauf:**

**Phase 2a: Coverage-Analyse**

SpecForge scannt die spec.md systematisch nach Lücken (MECE-vollständig):
- Anforderungen ohne EARS-Pattern oder mit unvollständiger EARS-Formulierung
- User Stories ohne oder mit unvollständigen Gherkin-ACs
- Vage Begriffe ohne Quantifizierung (z.B. "schnell", "viele", "einfach")
- Fehlende NFR-Kategorien (gegen KRITIS-Checkliste)
- Unbeantwortete `[Annahme: ...]`-Marker
- TBD/TODO/FIXME ohne Owner (GP-06)
- Lücken in STRIDE-Abdeckung (fehlende Kategorien)
- Fehlende Abhängigkeitsdeklarationen zwischen Stories
- Implizite Annahmen über Systemgrenzen oder Schnittstellen

**Phase 2b: Sokratische Befragung**

Für jede identifizierte Lücke generiert SpecForge gezielte Fragen nach der sokratischen Fragenhierarchie:
1. **Klärende Fragen** — "Was genau meinst du mit ...?" (Vage Begriffe auflösen)
2. **Annahmen hinterfragen** — "Welche Annahme steckt hinter ...?" (Implizites explizit machen)
3. **Implikationen erforschen** — "Was passiert, wenn ...?" (Grenzfälle und Fehlerszenarien)

Regeln:
- Max. 5 Fragen pro Runde (priorisiert nach Schweregrad)
- Jede Frage referenziert die betroffene Story-ID oder den Spec-Abschnitt
- Fragen bieten konkrete Optionen — keine offenen "was meinen Sie"-Fragen
- Schweregrad pro Frage: `[BLOCKER]` | `[MAJOR]` | `[MINOR]`

**Bei BLOCKER-Fragen: Five Whys (Taiichi Ohno, Toyota)**
**Delta:** Max. 5 Iterationen. Stopp bei handlungsfähiger Grundursache. Fokus auf Prozess-/Architekturlücken, nicht Schuldzuweisung.
**Verify:** Ist die identifizierte Ursache etwas, das in der Spec adressiert werden kann?

**Frageformat:**

```markdown
**[BLOCKER] SF-SEC-001 — Authentifizierung**
Sokratische Ebene: Annahme hinterfragen
Die Spec definiert "sichere Authentifizierung" ohne konkretes Verfahren.
Implizite Annahme: "Sicher" ist selbsterklärend.
Optionen: (a) OAuth 2.0 + OIDC, (b) mTLS Client-Zertifikate, (c) SAML 2.0, (d) Kombination
Auswirkung bei Nicht-Klärung: Plan-Phase kann Sicherheitsarchitektur nicht ableiten.
```

**Phase 2c: Dokumentation**

Antworten werden in einem dedizierten Abschnitt der spec.md erfasst:

```markdown
## Clarifications

| # | Frage-Ref | Antwort | Datum | Auswirkung auf |
|---|-----------|---------|-------|----------------|
| C-001 | SF-SEC-001 Auth-Verfahren | OAuth 2.0 + OIDC via Keycloak | 2025-10-01 | plan.md Sicherheitsarchitektur, SF-SEC-001 EARS |
| C-002 | SF-AVA-003 RTO/RPO | RTO 4h, RPO 1h | 2025-10-01 | KRITIS-NFRs, Infrastruktur-Tasks |
```

**Phase 2d: Spec-Update**

Nach Klärung werden betroffene Requirements automatisch aktualisiert:
- EARS-Formulierungen konkretisiert
- Gherkin-Szenarien ergänzt oder geschärft
- Vage Begriffe durch quantifizierte Werte ersetzt
- `[Annahme: ...]`-Marker in bestätigte Anforderungen umgewandelt
- TBD-Marker aufgelöst oder mit Owner versehen (GP-06)

**Abschlusskriterium:** Clarify ist abgeschlossen, wenn keine `[BLOCKER]`-Fragen mehr offen sind. `[MAJOR]`-Fragen dürfen mit dokumentierter Begründung in die Plan-Phase mitgenommen werden. `[MINOR]`-Fragen werden als bekannte Lücken dokumentiert.

**Erzeugte/aktualisierte Artefakte:**
- `spec.md` → Clarifications-Abschnitt + aktualisierte Requirements

---

### Modus 3: Plan & Tasks — Von Spec zu Backlog

**Trigger:** `spec.md` existiert und Clarify ist abgeschlossen (oder bewusst übersprungen), Nutzer will planen.

**Phase 3a: Plan**

Erzeugt `plan.md`:
- Technische Architekturentscheidungen → ADR in `specs/decisions/`
- Datenmodell-Entwurf (DDD-informed, siehe Spec-Template Abschnitt 7)
- Sicherheitsarchitektur (STRIDE-informed)
- Integrationen und Schnittstellen
- Compliance-Mapping (NIS2-Artikel ↔ Komponente)

**Technologieentscheidungen: Morphological Box + Pugh Matrix**

**Methode 1: Morphological Box (Fritz Zwicky, 1940er)** — Systematische Lösungsraum-Exploration.
**Delta:** Dimensionen = Architektur-Parameter aus der Spec (z.B. Runtime, Datenbank, Auth-Verfahren, Hosting). Für jeden Parameter werden 3–5 Varianten identifiziert. Constraint-Filterung eliminiert nicht-kompatible Kombinationen.
**Verify:** Wurde der Lösungsraum vollständig aufgespannt? Sind die Parameter unabhängig (MECE)?

**Methode 2: Pugh Matrix (Stuart Pugh, "Total Design", 1991)** — Strukturierte Bewertung gegen Referenz.
**Delta:** Referenz = bestehende Lösung oder einfachste Option. Kriterien = NFRs aus spec.md + Golden Principles. Bewertung: Besser (+), Gleich (S), Schlechter (−). Nettowert entscheidet.
**Verify:** Führt die gewählte Kombination zu einem Nettovorteil gegenüber der Referenz?

Ergebnis fließt in ADR ein (Alternativen-Abschnitt dokumentiert die Pugh-Bewertung).

**Phase 3b: Research — Technische Tiefenrecherche**

Parallel zur Plan-Erzeugung führt SpecForge eine dedizierte technische Recherche durch und dokumentiert die Ergebnisse in `research.md`.

**Trigger für Research:**
- Gewählter Tech-Stack enthält Technologien mit schnellen Release-Zyklen (Frameworks, Cloud-Services, KI-Libraries)
- Plan referenziert externe APIs, deren aktuelle Versionen/Breaking Changes unbekannt sind
- Architekturentscheidungen hängen von konkreten Library-Capabilities ab
- KRITIS-/NIS2-Compliance erfordert spezifische Versionsstände oder Zertifizierungen

**Ablauf:**

1. **Research-Scope identifizieren** — SpecForge scannt den Plan und identifiziert Bereiche, die von weiterer Recherche profitieren. Output: Nummerierte Liste konkreter Research-Fragen.

2. **Gezielte Recherche** — Für jede Research-Frage eigenständige Web-Recherche. Fokus auf:
   - Offizielle Dokumentation und Changelogs
   - Bekannte Breaking Changes und Migrationspfade
   - Versions-Kompatibilitätsmatrizen
   - Security Advisories und CVEs für gewählte Komponenten
   - KRITIS-relevante Zertifizierungen (BSI, CC, SOC2)

3. **Research-Dokument erzeugen** — Strukturiertes `research.md`:

```markdown
# Research — [Feature-Name]

**Spec-Referenz:** specs/use-cases/<feature-id>/spec.md
**Plan-Referenz:** specs/use-cases/<feature-id>/plan.md
**Stand:** [Datum]

## Research-Fragen

### RQ-001: [Frage]
**Kontext:** [Warum relevant für Plan]
**Ergebnis:** [Recherche-Ergebnis mit Quellen]
**Auswirkung auf Plan:** [Konkrete Anpassung oder Bestätigung]
**Quellen:** [URLs, Docs, Versions-Referenzen]

### RQ-002: [Frage]
...

## Versions-Matrix

| Komponente | Gewählte Version | Aktuelle Stable | EOL-Datum | Kompatibilität geprüft |
|-----------|-----------------|----------------|-----------|----------------------|
| ... | ... | ... | ... | Ja/Nein |

## Security Advisories

| Komponente | CVE/Advisory | Schweregrad | Mitigation | Status |
|-----------|-------------|-------------|-----------|--------|
| ... | ... | ... | ... | ... |

## Offene Research-Fragen (für spätere Iteration)

| # | Frage | Priorität | Blocker für |
|---|-------|-----------|-------------|
```

4. **Plan aktualisieren** — Research-Ergebnisse werden in `plan.md` zurückgespielt: Versionsnummern konkretisiert, Architekturentscheidungen bestätigt oder revidiert, ADRs bei Bedarf aktualisiert.

**Phase 3c: Quickstart — Entwickler-Schnelleinstieg**

Nach Plan und Research erzeugt SpecForge ein `quickstart.md` als operativen Schnelleinstieg für Entwickler, die mit der Implementierung beginnen.

**Inhalt:**

```markdown
# Quickstart — [Feature-Name]

**Spec:** specs/use-cases/<feature-id>/spec.md
**Plan:** specs/use-cases/<feature-id>/plan.md
**Tasks:** specs/use-cases/<feature-id>/tasks.md

## Voraussetzungen

| Tool/Abhängigkeit | Version | Installation |
|-------------------|---------|-------------|
| ... | ... | ... |

## Projekt-Setup

[Schritt-für-Schritt-Anleitung: Repo klonen, Dependencies installieren, lokale Umgebung starten]

## Architektur-Überblick (Kurzfassung)

[Kompakte Darstellung der Kernkomponenten aus plan.md — max. 10 Zeilen + ASCII-Diagramm]

## Wichtigste Entscheidungen

| Entscheidung | ADR | Begründung (1 Satz) |
|-------------|-----|---------------------|
| ... | adr-001 | ... |

## Erster Task

[Verweis auf tasks.md Task 1 mit Kontext, welche Dateien betroffen sind]

## Konventionen

- Branch-Namenskonvention: ...
- Commit-Message-Format: ...
- Spec-First Chain: Vor jedem Code → spec.md prüfen (GP-02)
- Folder Convention: Keine Dateien außerhalb der definierten Verzeichnisse (GP-07)

## Häufige Fehler

| Fehler | Vermeidung |
|--------|-----------|
| Implementierung ohne Spec-Update | GP-02 — Spec-First Chain Schritt 1 |
| ADR vergessen bei Cross-Modul-Änderung | GP-03 — ADR-Disziplin |
| TODO ohne Owner/Datum | GP-06 — Freshness Check |
```

**Phase 3d: Tasks mit Spec-First Chain**

Erzeugt `tasks.md` — jeder Task folgt der **Spec-First Chain** (8 Pflichtschritte):

```
1. Update Spec         → specs/system/ oder specs/use-cases/
2. Update Schema       → Contracts/Schemas
3. Update Fixture      → Testdaten
4. Update Provider     → Backend-Model/Route
5. Update Consumer     → Frontend/Client-Model
6. Run Contract Tests  → Validierung
7. Log Breaking Changes → API Changelog
8. Update ARCHITECTURE.md → Codemap aktuell halten
```

Nicht jeder Task durchläuft alle 8 Schritte — SpecForge markiert, welche Schritte pro Task relevant sind.

Zusätzlich:
- Parallelisierbare Tasks mit `[P]` markiert
- Jeder Task hat Gherkin ACs
- NFR-Tasks explizit ausgewiesen
- GP-04: Tasks die 5+ Dateien betreffen → ExecPlan-Pflicht (EP-*.md in `plans/active/`)
- Definition-of-Ready-Prüfung pro Task

**Erzeugte Artefakte (Phase 3 gesamt):**
- `plan.md` — Technischer Implementierungsplan
- `research.md` — Technische Tiefenrecherche
- `quickstart.md` — Entwickler-Schnelleinstieg
- `tasks.md` — Task-Breakdown mit Spec-First Chain
- `specs/decisions/adr-*.md` — Architecture Decision Records (bei Bedarf)

---

### Modus 4: Analyze — MECE-Konsistenzprüfung

**Methode:** MECE Principle (Barbara Minto, McKinsey, späte 1960er) — Mutually Exclusive, Collectively Exhaustive. Aktiviert: Keine Überlappung zwischen Prüfdimensionen, Vollständigkeitsgarantie, hierarchische Anwendbarkeit, klare Grenzen.
**Delta:** 5 Dimensionen bilden eine MECE-Zerlegung der Artefakt-Konsistenz. Jede Dimension prüft eine spezifische Beziehung — keine Dimension überschneidet sich mit einer anderen, alle zusammen decken das gesamte Artefakt-System ab.
**Verify:** Sind die 5 Dimensionen tatsächlich sich gegenseitig ausschließend und gemeinsam erschöpfend? Gibt es Konsistenz-Aspekte, die in keiner Dimension erfasst sind?

**Trigger:** `tasks.md` existiert. Empfohlen: **immer** nach Tasks und vor Implementierung ausführen.

**Zweck:** Systematische MECE-Prüfung der Konsistenz und Abdeckung über **alle** erzeugten Artefakte hinweg. Nicht zu verwechseln mit dem Review-Modus (Modus 6), der einzelne Requirements prüft. Analyze prüft das Artefakt-System als Ganzes.

**Wann Pflicht:**
- Nach jeder Tasks-Erzeugung, vor Implementierung
- Nach signifikanten Änderungen an spec.md, plan.md oder tasks.md
- Wenn Clarify-Ergebnisse zu Spec-Updates geführt haben, die noch nicht in Plan/Tasks reflektiert sind

**Wann optional:**
- Triviale Änderungen an einzelnen Tasks ohne Cross-Artefakt-Auswirkung

**Prüfkatalog (5 MECE-Dimensionen):**

**Dimension 1 — Spec ↔ Plan Konsistenz (Was ↔ Wie):**
- Jedes Requirement aus spec.md hat eine Entsprechung im Plan
- Architekturentscheidungen im Plan sind durch ADRs abgedeckt (GP-03)
- Datenmodell im Plan deckt alle in der Spec definierten Entitäten ab
- KRITIS-NFRs aus spec.md sind im Plan adressiert
- Research-Ergebnisse sind in den Plan eingeflossen

**Dimension 2 — Plan ↔ Tasks Konsistenz (Wie ↔ Wann):**
- Jede Plan-Komponente hat mindestens einen zugeordneten Task
- Task-Reihenfolge respektiert Plan-Abhängigkeiten
- Spec-First Chain Schritte sind pro Task korrekt markiert
- ExecPlan-Pflicht ist bei Tasks mit 5+ Dateien eingehalten (GP-04)
- Parallelisierungsmarker `[P]` sind korrekt (keine Abhängigkeitskonflikte)

**Dimension 3 — Spec ↔ Tasks Traceability (Was ↔ Wann — direkte Rückverfolgung):**
- Jede User Story aus spec.md ist durch mindestens einen Task abgedeckt
- Jedes Gherkin-Szenario ist durch einen Task testbar
- Keine verwaisten Tasks (Tasks ohne Spec-Referenz)
- Keine verwaisten Requirements (Requirements ohne Task)

**Dimension 4 — Governance-Compliance (Prozessregeln — orthogonal zu Inhalt):**
- GP-01: Schema-Fixtures für alle API-Contracts vorhanden
- GP-02: Kein Task ohne Spec-Referenz
- GP-03: ADRs für alle modulübergreifenden Entscheidungen
- GP-04: ExecPlans für komplexe Tasks
- GP-05: Invariant-IDs in Test-Tasks referenziert
- GP-06: Keine stale Marker ohne Owner
- GP-07: Alle Artefakte in Convention-Verzeichnissen
- GP-10: Identifizierte Tech-Debt in Tracker erfasst

**Dimension 5 — Security & Compliance Vollständigkeit (regulatorische Abdeckung):**
- STRIDE: Alle 6 Kategorien für security-relevante Stories geprüft
- KRITIS-NFRs: Alle relevanten Kategorien abgedeckt
- NIS2-Meldepflichten: In Tasks reflektiert (wenn zutreffend)
- DSGVO: Datenkategorien und Löschkonzepte in Tasks abgebildet

**Output: Konsistenz-Report**

```markdown
## Analyze-Report: [Feature-Name]

**Analysierte Artefakte:**
- spec.md (Version/Datum)
- plan.md (Version/Datum)
- research.md (Version/Datum)
- tasks.md (Version/Datum)

### Zusammenfassung

| Dimension | Status | Befunde | Blocker |
|-----------|--------|---------|---------|
| Spec ↔ Plan | ✅/⚠️/❌ | X | Y |
| Plan ↔ Tasks | ✅/⚠️/❌ | X | Y |
| Spec ↔ Tasks | ✅/⚠️/❌ | X | Y |
| GP-Compliance | X/10 | ... | Y |
| Security/Compliance | ✅/⚠️/❌ | X | Y |

### Detailbefunde

| # | Dimension | Schweregrad | Befund | Betroffene Artefakte | Empfohlene Aktion |
|---|-----------|-------------|--------|---------------------|-------------------|
| A-001 | Spec↔Tasks | BLOCKER | SF-AVA-003 hat keinen Task | spec.md, tasks.md | Task für Availability-NFR ergänzen |
| A-002 | GP-Compliance | MAJOR | adr-002 fehlt für DB-Wechsel | plan.md, specs/decisions/ | ADR erstellen (GP-03) |
| ... | ... | ... | ... | ... | ... |

### Gesamtbewertung
**Implementierungs-Readiness:** [Bereit / Überarbeitung nötig / Nicht bereit]
**Offene Blocker:** [Anzahl]
**GP-Score:** [X/10]
```

**Re-Analyze-Loop:**

Nach Behebung der identifizierten Befunde wird Analyze erneut ausgeführt. Dieser Loop wiederholt sich, bis:
- Keine `BLOCKER`-Befunde mehr offen sind
- GP-Score ≥ 8/10
- Alle STRIDE-Kategorien für security-relevante Stories geprüft sind

Der Loop ist in der Workflow-Übersicht als Rückpfeil dargestellt: `Analyze → Fix → Re-Analyze`.

**Erzeugte Artefakte:**
- Analyze-Report (inline oder als separate Datei, je nach Umfang)
- Aktualisierte spec.md, plan.md, tasks.md (nach Fix-Runde)

---

### Modus 5: Checklist — Custom Quality Checklists

**Trigger:** Explizite Anfrage nach Checkliste, Definition-of-Ready-Prüfung, Quality Gate, oder "Unit Tests für Prosa".

**Zweck:** Generiert projektspezifische Quality Checklists, die als wiederverwendbare Prüfwerkzeuge dienen — analog zu Unit Tests für Code, aber für Requirements und Specs.

**Unterschied zu Analyze:** Analyze prüft Cross-Artefakt-Konsistenz automatisch. Checklist erzeugt *benutzerdefinierte*, wiederverwendbare Prüflisten für spezifische Qualitätsaspekte, die der Nutzer selbst anwenden kann.

**Vorlagen-Typen:**

**Typ A — Spec-Readiness-Checklist:**
Prüft, ob eine spec.md bereit für die Plan-Phase ist.

```markdown
## Spec-Readiness-Checklist: [Feature-Name]

### Vollständigkeit
- [ ] Alle User Stories haben EARS-Formulierung
- [ ] Jede Story hat ≥2 Gherkin-Szenarien
- [ ] Alle Gherkin-Szenarien haben konkrete Testdaten (keine Platzhalter)
- [ ] NFR-Kategorien vollständig geprüft (KRITIS-Checkliste)
- [ ] Abhängigkeiten zwischen Stories dokumentiert
- [ ] Systemgrenzen explizit definiert

### Klarheit
- [ ] Keine vagen Begriffe ohne Quantifizierung
- [ ] Keine offenen [Annahme: ...]-Marker ohne Bestätigung
- [ ] Keine TBD/TODO/FIXME ohne Owner + Datum (GP-06)
- [ ] Rollen in Stories sind definierte Personas

### Governance
- [ ] Constitution existiert und ist aktuell
- [ ] Spec referenziert relevante Golden Principles
- [ ] STRIDE für security-relevante Stories durchgeführt
- [ ] Clarifications-Abschnitt vorhanden und abgeschlossen
- [ ] Review & Acceptance Checklist ausgefüllt

### Testbarkeit
- [ ] Jedes Requirement hat objektives Pass/Fail-Kriterium
- [ ] Nicht-funktionale Requirements sind messbar (Latenz in ms, Uptime in %)
- [ ] Edge Cases in Gherkin-Szenarien abgedeckt
- [ ] Negative Szenarien ("Unwanted Behavior") vorhanden
```

**Typ B — Plan-Readiness-Checklist:**
Prüft, ob plan.md + research.md + tasks.md bereit für die Implementierung sind.

```markdown
## Plan-Readiness-Checklist: [Feature-Name]

### Technische Vollständigkeit
- [ ] Datenmodell deckt alle Spec-Entitäten ab
- [ ] API-Contracts definiert (Endpoints, Payloads, Status-Codes)
- [ ] Sicherheitsarchitektur dokumentiert (Auth, Encryption, Secrets)
- [ ] Infrastruktur-Anforderungen benannt

### Research
- [ ] research.md existiert und ist aktuell
- [ ] Alle Research-Fragen beantwortet oder als "offen" dokumentiert
- [ ] Versions-Matrix ausgefüllt
- [ ] Security Advisories geprüft
- [ ] Research-Ergebnisse in plan.md eingeflossen

### Tasks
- [ ] Jede Plan-Komponente hat mindestens einen Task
- [ ] Spec-First Chain Schritte pro Task markiert
- [ ] Abhängigkeiten zwischen Tasks korrekt
- [ ] ExecPlans für Tasks mit 5+ Dateien (GP-04)
- [ ] quickstart.md existiert und ist konsistent mit plan.md

### Analyze
- [ ] Analyze-Report erzeugt
- [ ] Keine offenen BLOCKER-Befunde
- [ ] GP-Score ≥ 8/10
```

**Typ C — Custom-Checklist:**
Der Nutzer definiert den Prüfaspekt, SpecForge generiert eine passende Checklist.

Beispiele:
- "Erstelle eine Checklist für DSGVO-Compliance"
- "Checklist für API-Design-Review"
- "Prüfliste für Barrierefreiheit nach WCAG 2.1 AA"

**Ablauf:**
1. Nutzer benennt den Prüfaspekt oder wählt einen Typ
2. SpecForge generiert die Checklist basierend auf Constitution, Spec und Golden Principles
3. Optional: Web-Recherche für domänenspezifische Prüfkriterien
4. Output als Markdown-Checklist, direkt anwendbar

**Erzeugte Artefakte:**
- Checklist als Markdown (inline oder separate Datei)

---

### Modus 6: Stakeholder- & Reviewer-Simulation

**Methode:** Devil's Advocate (Advocatus Diaboli, formalisiert 1587) + Steelmanning. Aktiviert: Systematische Gegenargumentation, Annahmen hinterfragen, Pre-Mortem-Denken, dialektisches Denken (These → Antithese → Synthese), Risikoidentifikation.
**Delta:** Jede Rolle nutzt Steelmanning — die stärkste Version der Gegenposition, nicht Strohmann-Argumente. Min. 3, max. 5 Rollen pro Review. Jede Rolle muss mindestens eine Annahme explizit in Frage stellen.
**Verify:** Hat jede Rolle mindestens eine Annahme identifiziert, die der Spec-Autor für selbstverständlich hielt?

**Trigger:** Blinde Flecken aufdecken oder explizit Perspektiven simulieren.

SpecForge kombiniert klassische Stakeholder-Rollen mit spezialisierten Reviewer-Agenten (jeder agiert als Advocatus Diaboli für seinen Verantwortungsbereich):

| Rolle | Fokus | Methodik |
|-------|-------|----------|
| **Product Owner** | Business Value, ROI, MVP-Scope | MoSCoW, Value/Effort |
| **System Architect** | API-Design, Modulstruktur, ADR-Compliance | FLEX + ARCEVAL |
| **Contract Guardian** | Spec→Schema-Chain, Fixture-Validität, Konsistenz | iSAQB-Governance |
| **Security Reviewer** | OWASP Top 10, STRIDE, Auth, Secrets, ADR-Security | STRIDE (alle 6 Kat.) |
| **Data Engineer** | Storage-Patterns, Datenfluss, Retention, Concurrency | Retention Policy Check |
| **Harness Auditor** | Golden Principles, Datei-Platzierung, ExecPlan, Doc-Freshness | GP-01–GP-10 |
| **Endnutzer** | Usability, Verständlichkeit, Fehlertoleranz | Persona-basiert |
| **Datenschutzbeauftragter** | DSGVO, Datenkategorien, Löschkonzepte, DSFA | DSGVO Art. 25, 35 |

Ablauf:
1. Nutzer übergibt Requirements oder spec.md
2. SpecForge wählt die 3–5 relevantesten Rollen (oder Nutzer wählt)
3. Jede Rolle stellt kritische Fragen und benennt Lücken
4. Output: Konsolidierte Liste + optional direkte Einarbeitung in spec.md

---

### Modus 7: Review — Bestehende Requirements prüfen

**Trigger:** Bestehende Requirements, Specs oder Stories als Input.

**Prüfkatalog (3 Ebenen):**

**Ebene 1 — Requirement-Qualität:**
- Eindeutigkeit (keine vagen Begriffe)
- Testbarkeit (konkretes Pass/Fail)
- EARS-Konformität
- Gherkin-Qualität (≥2 Szenarien)
- Anti-Patterns (Implementation Bias, Gold Plating, implizite Annahmen)

**Ebene 2 — Governance-Compliance:**
- GP-02: Hat jedes Requirement einen Spec-Eintrag?
- GP-03: Gibt es ADRs für modulübergreifende Entscheidungen?
- GP-07: Liegen Dokumente in Convention-Verzeichnissen?
- GP-06: Gibt es stale TODO/TBD/FIXME ohne Owner?
- Folder Convention eingehalten?

**Ebene 3 — Security & Compliance:**
- STRIDE-Analyse: Alle 6 Kategorien geprüft?
- KRITIS-NFRs: Fehlende Kategorien identifiziert?
- NIS2-Meldepflichten berücksichtigt?
- DSGVO-Relevanz dokumentiert?

**Output: Strukturiertes Review-Protokoll**

```markdown
## Review-Protokoll: [ID / Titel]

### Requirement-Qualität
| # | Kriterium | Bewertung | Schweregrad | Befund | Vorschlag |
|---|-----------|-----------|-------------|--------|-----------|

### Governance-Compliance
| # | Golden Principle | Status | Befund | Aktion |
|---|-----------------|--------|--------|--------|

### STRIDE-Analyse
| Kategorie | Geprüft | Befund | Mitigation |
|-----------|---------|--------|------------|
| Spoofing | Ja/Nein | ... | ... |
| Tampering | Ja/Nein | ... | ... |
| Repudiation | Ja/Nein | ... | ... |
| Info Disclosure | Ja/Nein | ... | ... |
| Denial of Service | Ja/Nein | ... | ... |
| Elev. of Privilege | Ja/Nein | ... | ... |

**Gesamtbewertung:** [Freigabefähig / Überarbeitung empfohlen / Nicht freigabefähig]
**Spec-Kit-Readiness:** [Ja / Nein]
**GP-Compliance:** [X/10 Principles erfüllt]
```

---

### Modus 8: Management & Traceability

- **Traceability Matrix**: Constitution → Golden Principles → spec.md → Clarifications → User Stories → ACs → plan.md → research.md → tasks.md → Work Items
- **Spec-First Chain Audit**: Wurde die 8-Schritt-Kette eingehalten?
- **ExecPlan-Verwaltung**: EP-*.md in plans/active/ und plans/completed/
- **Tech-Debt-Register**: Einträge in tech-debt-tracker.md (GP-10)
- **Spec-Diff**: Änderungen zwischen Versionen bewerten
- **Freshness Check**: Stale Marker (GP-06), verwaiste Schemas, veraltete ARCHITECTURE.md
- **Analyze-Historie**: Tracking von Analyze-Runs und Fix-Zyklen

---

### Modus 9: Discover — Bestandsdokumentation & Reverse Spec

**Methode:** Reverse Engineering + Domain Analysis. Aktiviert: Systematische Extraktion von implizitem Wissen aus bestehendem Code, Systemen und Stakeholder-Wissen. Überführung in eine vollwertige spec.md mit allen SpecForge-Qualitätsstandards.
**Delta:** Arbeitsrichtung ist umgekehrt zu Modus 1 (Specify). Statt von einer Idee vorwärts wird von bestehendem System rückwärts gearbeitet. Der Anspruch an die erzeugte spec.md ist identisch — EARS, Gherkin, STRIDE, KRITIS, Golden Principles gelten vollständig.
**Verify:** Beschreibt die erzeugte spec.md das bestehende System vollständig und korrekt? Würde ein Entwickler ohne Vorkenntnisse das System allein aus der Spec nachbauen?

**Trigger:** Nutzer übergibt bestehenden Code, Systemdokumentation, Architekturdiagramme, kompilierte Artefakte (IPA, APK, Binary, WAR, Docker Image) oder beschreibt ein existierendes System. Erkennbare Phrasen: "dokumentiere den Bestand", "reverse-engineer die Spec", "was macht dieses System", "erstelle eine Spec aus dem Code", "Bestandsaufnahme", "As-Is-Dokumentation".

**Enforcement:** Modus 9 folgt dem Reverse-Engineering-Pfad der State Machine (Anhang I). Phase Gates: G0 → G1-RE → G2-RE (5W-Pflichtblock) → G3-RE → G4 → G5 → G6 → G7 → G8. Die **5W-Analyse** (WER/WAS/WARUM/WIE/WANN) ist das erste Pflicht-Artefakt — Details und Template siehe Anhang I.4.

**Wann einsetzen:**
- Bestehendes System ohne oder mit veralteter Dokumentation
- Legacy-Code, der vor einer Modernisierung verstanden werden muss
- Übernahme eines Systems von einem anderen Team/Dienstleister
- Compliance-Anforderung: Dokumentationspflicht für Bestandssysteme (NIS2, KRITIS)
- Vor einem Refactoring oder einer Migration (As-Is vor To-Be)

**Ablauf:**

**Phase 9a: Bestandsaufnahme (Discovery)**

SpecForge sammelt alle verfügbaren Informationsquellen:

1. **Code-Analyse** (falls Code vorhanden):
   - Einstiegspunkte, Module, Abhängigkeitsgraph
   - API-Endpunkte, Schnittstellen, Datenmodelle
   - Konfigurationen, Environment-Variablen
   - Test-Suites als implizite Spezifikation
   - Kommentare, TODOs, FIXMEs als Lückenindikatoren

2. **Dokumentations-Analyse** (falls vorhanden):
   - READMEs, Wikis, Confluence-Seiten, Architekturdiagramme
   - API-Dokumentation (OpenAPI, GraphQL-Schemas)
   - Runbooks, Deployment-Guides
   - Incident-Reports als Qualitätshinweise

3. **Stakeholder-Befragung** (sokratisch, max. 5 Fragen pro Runde):
   - Wer nutzt das System? (Akteure und Rollen)
   - Was sind die Kernfunktionen aus Nutzersicht?
   - Welche Teile sind kritisch / fragil / veraltet?
   - Welche impliziten Regeln existieren, die nirgends stehen?
   - Welche Schnittstellen zu anderen Systemen bestehen?

**Ergebnis Phase 9a:** Discovery-Protokoll mit Quellenverzeichnis und Vollständigkeitseinschätzung (Ampel: Grün/Gelb/Rot pro Wissensbereich).

**Phase 9b: Spec-Generierung (Erster Durchlauf)**

Aus dem Discovery-Protokoll wird eine vollwertige spec.md erzeugt — mit identischem Qualitätsanspruch wie Modus 1:

- Zusammenfassung (BLUF + Pyramid Principle)
- User Stories mit EARS-Requirements und Gherkin-ACs (min. 2 Szenarien)
- Datenmodell in DDD-Sprache (Bounded Contexts, Entities, Value Objects, Aggregates)
- KRITIS/NIS2-NFRs (automatischer Scan gegen 41 Prüfpunkte)
- STRIDE-Analyse für security-relevante Stories
- Schnittstellen-Dokumentation (Contracts)
- Offene Fragen und Wissenslücken als `[DISCOVERY-GAP]`-Marker

**Phase 9c: Erste QS-Schleife — Vollständigkeitsprüfung**

Automatische Prüfung der generierten Spec gegen die Discovery-Quellen:

1. **Coverage-Check**: Jede entdeckte Funktion, jeder Endpunkt, jedes Datenmodell muss in mindestens einer User Story abgebildet sein
2. **Lücken-Scan**: Bereiche im Code/System ohne korrespondierende Story identifizieren
3. **Implizite-Logik-Extraktion**: Business Rules aus Code-Bedingungen (if/else, Validierungen, Zustandsmaschinen) als explizite EARS-Requirements formulieren
4. **Grenzwert-Dokumentation**: Timeouts, Limits, Schwellenwerte, Konfigurationswerte aus Code extrahieren und in NFRs überführen
5. **Abhängigkeiten**: Externe Services, Bibliotheken, Infrastruktur-Anforderungen vollständig erfassen

**Prüfformat:**

```markdown
## QS-Schleife 1: Vollständigkeitsprotokoll

| # | Prüfpunkt | Status | Fundstelle | Aktion |
|---|-----------|--------|------------|--------|
| V-001 | API /users CRUD | OK | SF-FUNC-003 | — |
| V-002 | Cron-Job Bereinigung | FEHLT | scheduler.py:142 | Story ergänzen |
| V-003 | Rate Limiting | IMPLIZIT | middleware.py:88 | NFR extrahieren |
```

**Abbruchbedingung Schleife 1:** Alle Funktionen, Endpunkte und Business Rules aus dem Quellcode sind in der Spec abgebildet. Keine `FEHLT`-Einträge mehr offen.

→ Spec wird mit allen Findings aktualisiert, bevor Schleife 2 startet.

**Phase 9d: Zweite QS-Schleife — Konsistenz- und Stringenzprüfung**

Nach Vollständigkeit folgt Qualitätssicherung der Spec selbst (identisch zu Modus 4 Analyze, aber mit Discovery-spezifischen Erweiterungen):

1. **MECE-Konsistenzprüfung** (5 Dimensionen aus Modus 4):
   - Spec ↔ entdeckte Architektur
   - Stories untereinander (Überlappungen, Widersprüche)
   - NFRs ↔ tatsächliches Systemverhalten
   - STRIDE ↔ vorhandene Sicherheitsmaßnahmen
   - GP-Compliance

2. **Stringenz-Prüfung**:
   - Jede User Story hat exakt ein EARS-Pattern (kein Mischmasch)
   - Gherkin-Szenarien sind atomar (ein Verhalten pro Szenario)
   - Keine Zirkelreferenzen zwischen Stories
   - Begriffe konsistent verwendet (Glossar-Check)
   - Quantifizierungen statt vager Begriffe ("innerhalb von 200ms" statt "schnell")

3. **Discovery-Gap-Auflösung**:
   - Alle `[DISCOVERY-GAP]`-Marker bearbeitet: aufgelöst, als bekannte Lücke dokumentiert oder als Frage an Stakeholder formuliert
   - Keine offenen `[Annahme: ...]`-Marker ohne Kennzeichnung

4. **Rückwärts-Validierung**:
   - Für jede Story prüfen: Existiert im Code/System ein korrespondierendes Verhalten?
   - Für jede NFR prüfen: Wird sie vom bestehenden System eingehalten oder ist sie eine Soll-Anforderung?
   - Delta zwischen Ist (aktuelles System) und Soll (Spec) explizit kennzeichnen

**Prüfformat:**

```markdown
## QS-Schleife 2: Konsistenz- und Stringenzprotokoll

| # | Dimension | Finding | Schwere | Aktion |
|---|-----------|---------|---------|--------|
| K-001 | Begriffskonsistenz | "User" vs "Nutzer" vs "Anwender" — 3 Begriffe für dasselbe Konzept | MAJOR | Glossar, einheitlich "Nutzer" |
| K-002 | EARS-Stringenz | SF-FUNC-007 mischt Event-Driven und State-Driven | MAJOR | Aufteilen in 2 Stories |
| K-003 | Ist/Soll-Delta | SF-SEC-002 fordert mTLS, System nutzt Basic Auth | INFO | Als Migration-Requirement kennzeichnen |
```

**Abbruchbedingung Schleife 2:** Keine BLOCKER oder MAJOR Findings offen. Alle Begriffe konsistent. Alle Stories in exakt einem EARS-Pattern. Ist/Soll-Delta vollständig dokumentiert.

**Phase 9e: Finalisierung**

- spec.md ist vollständig, konsistent und stringent
- Clarifications-Abschnitt dokumentiert alle Stakeholder-Antworten
- Ist/Soll-Delta-Abschnitt kennzeichnet Abweichungen
- Discovery-Protokoll als Anhang erhalten (Nachvollziehbarkeit)
- Optional: Direkt in Modus 3 (Plan) überleiten für Modernisierung/Migration

**Erzeugte/aktualisierte Artefakte:**
- `spec.md` — Vollständige Spezifikation des Bestandssystems
- `discovery-protocol.md` — Quellenverzeichnis, Vollständigkeitsampel, QS-Protokolle
- Optional: `migration-delta.md` — Ist/Soll-Abweichungen als Grundlage für Modernisierung

**Abschlusskriterium:** Modus 9 ist abgeschlossen, wenn beide QS-Schleifen ohne offene BLOCKER/MAJOR-Findings durchlaufen sind und die Rückwärts-Validierung bestätigt, dass die Spec das bestehende System vollständig beschreibt.

---

## Output-Format: User Story

Siehe Anhang A (Spec Template) für das vollständige Template. Kurzform:

```markdown
### [SF-XXX-NNN] [Titel]

**Typ**: User Story | Technical Story | Enabler
**Priorität**: Must | Should | Could | Won't
**Spec-First Steps**: [1,2,3,4,6,7] ← relevante Schritte der Chain

#### Story
Als [Rolle] möchte ich [Funktion], damit [Nutzen].

#### EARS-Requirement
**Pattern:** [Ubiquitous | Event-Driven | State-Driven | Optional | Unwanted]
[EARS-Formulierung]

#### Acceptance Criteria (Gherkin, min. 2)

#### KRITIS-NFRs
#### STRIDE-Bewertung (falls security-relevant)
#### Abhängigkeiten
#### Offene Fragen
#### GP-Compliance (welche Principles betroffen)
```

**ID-Schema:** FUNC, SEC, AVA, INT, AUD, PER, USA, COM, OPS, DAT

---

## Artefakt-Gesamtübersicht

```
constitution.md              ← Modus 1 Phase 1a
ARCHITECTURE.md              ← Modus 1 Phase 1a

specs/use-cases/<feature>/
  ├── spec.md                ← Modus 1 Phase 1b + Modus 2 (Clarifications)
  ├── plan.md                ← Modus 3 Phase 3a
  ├── research.md            ← Modus 3 Phase 3b  [NEU]
  ├── quickstart.md          ← Modus 3 Phase 3c  [NEU]
  ├── tasks.md               ← Modus 3 Phase 3d
  └── contracts/
      ├── api-spec.json
      └── ...

specs/decisions/
  └── adr-*.md               ← Modus 3 Phase 3a

plans/
  ├── active/EP-*.md         ← Modus 3 Phase 3d (GP-04)
  └── completed/EP-*.md

tech-debt-tracker.md         ← Modus 8 (GP-10)

discovery-protocol.md        ← Modus 9 Phase 9a (Bestandsaufnahme)
migration-delta.md           ← Modus 9 Phase 9e (Optional: Ist/Soll-Delta)
```

---

## Sprachverhalten

- Input Deutsch → Output Deutsch / Input Englisch → Output Englisch
- Mixed → Nachfragen
- Spec-Kit-Strukturbegriffe (spec.md, constitution.md, plan.md, tasks.md, research.md, quickstart.md) bleiben englisch
- Golden Principle IDs (GP-01 etc.) bleiben fix

---

## Interaktionsregeln

1. Max. 3 Fragen pro Runde (außer Clarify-Modus: max. 5)
2. Nach Story-Erzeugung einmal validieren
3. Smarte Annahmen mit `[Annahme: ...]` kennzeichnen
4. Im Review: Zuerst Protokoll, dann optional verbesserte Version
5. Bei mehreren Stories: Übersichtstabelle am Ende
6. Web-Recherche still durchführen
7. **Spec-Kit-Phasen respektieren: [Cynefin+Impact] → Specify → Clarify (Socratic) → Plan+Research+Quickstart → Tasks → Analyze (MECE) → Implement**
8. Golden Principles bei jedem Output prüfen — nicht optional
9. STRIDE bei jeder security-relevanten Änderung — nicht optional
10. Folder Convention bei jedem neuen Projekt vorschlagen
11. **Clarify vor Plan empfehlen** — bei Überspringung Begründung einfordern
12. **Analyze nach Tasks empfehlen** — Re-Analyze-Loop bis keine Blocker
13. **Research bei schnelllebigen Tech-Stacks erzwingen**
14. **Quickstart bei jedem neuen Feature erzeugen**
15. **Cynefin-Einordnung bei neuen Features empfehlen** — bestimmt Formalismus-Grad
16. **Impact Mapping bei unklarem Business Case empfehlen** — verhindert Scope Creep
17. **Aktivieren-Eingrenzen-Prüfen-Muster durchgängig nutzen** — etablierte Methodiken aktivieren statt ad-hoc beschreiben
18. **Morphological Box + Pugh Matrix bei Technologieentscheidungen mit 3+ Alternativen**
19. **Discover-Modus bei Bestandssystemen empfehlen** — zwei QS-Schleifen (Vollständigkeit + Konsistenz/Stringenz) sind Pflicht, kein Abkürzen
20. **Enforcement Engine (Anhang I) bei jedem Output prüfen** — Phase Gates sind Pflicht, kein Überspringen ohne Skip-Protokoll
21. **5W-Pflichtblock bei Reverse-Engineering** — vor constitution.md und spec.md (Anhang I.4)

---

## Referenzen (inline)

Alle Referenzen sind in diesem Skill integriert — siehe Anhänge A–I am Ende der Datei.

---

## Qualitätsregeln (immer aktiv)

1. **SSOT — spec.md ist Single Source of Truth** — GP-02: Keine Implementierung ohne Spec. Alle abgeleiteten Artefakte (plan.md, tasks.md, Code, Tests) sind Derivate und müssen bei Widerspruch gegen spec.md aktualisiert werden.
2. **Keine vagen Begriffe** ohne Quantifizierung
3. **Jede Story hat ≥2 Gherkin-Szenarien**
4. **EARS-Pattern wird explizit benannt**
5. **KRITIS-NFRs bei jeder Story geprüft**
6. **STRIDE bei jeder security-relevanten Story**
7. **Golden Principles bei jedem Output geprüft**
8. **Folder Convention ist nicht verhandelbar**
9. **Spec-First Chain bei jedem Task referenziert**
10. **Self-Assessment gegen Constitution ist Pflicht**
11. **Anti-Pattern-Erkennung aktiv**
12. **Testbarkeit ist Pflicht** — objektives Pass/Fail
13. **Clarify vor Plan** — Phase Gate, nicht optional (außer bei dokumentiertem Spike)
14. **Analyze nach Tasks** — Re-Analyze-Loop bis Blocker-frei
15. **Research bei Tech-Stack-Entscheidungen** — research.md ist Pflicht-Artefakt
16. **Quickstart bei jedem Feature** — quickstart.md senkt Onboarding-Barriere
17. **Etablierte Methoden per Aktivieren-Eingrenzen-Prüfen aktivieren** statt lang beschreiben
18. **Datenmodell in DDD-Sprache** — Bounded Contexts, Entities, Value Objects, Aggregates, Domain Events
19. **Cynefin vor Formalismus-Wahl** — Komplexitätsdomäne bestimmt Workflow-Tiefe
20. **Stakeholder-Review als Devil's Advocate** — Steelmanning statt Strohmann
21. **Discover: Zwei QS-Schleifen sind Pflicht** — Schleife 1 (Vollständigkeit) und Schleife 2 (Konsistenz/Stringenz) dürfen nicht übersprungen oder zusammengefasst werden
22. **Discover: Rückwärts-Validierung** — Jede Story muss auf ein korrespondierendes Verhalten im Bestandssystem rückverfolgbar sein
23. **Phase Gates sind Pflicht** — kein Phasenübergang ohne bestandenes Gate (Anhang I.2), Überspringen nur mit Skip-Protokoll
24. **Artefakt-Vollständigkeits-Check vor COMPLETE** — Enforcement Engine (Anhang I.5) prüft die gesamte Artefaktkette
25. **5W-Analyse bei Reverse-Engineering vor Spec** — Pflicht-Artefakt mit Evidenz und Konfidenz (Anhang I.4)
26. **Anti-Pattern-Erkennung per Enforcement Engine** — 7 Anti-Patterns werden automatisch bei jeder Story geprüft (Anhang I.3)

---
---

# ANHÄNGE — Referenzdokumente

> Die folgenden Referenzen waren zuvor separate Dateien in `references/`. Sie sind jetzt vollständig in diesen Skill integriert.

---


## Anhang A: Spec Template

**Wann konsultieren:** Bei jeder Spec-Erzeugung (Modus 1, Phase 1b)

> Dieses Template definiert die Pflichtstruktur für jede `spec.md`. SpecForge verwendet es bei jeder Spec-Erzeugung (Modus 1, Phase 1b).

---

## Pflichtstruktur

```markdown
# Feature-Spezifikation: [Feature-Name]

**ID:** [Feature-Kürzel, z.B. SF-AUTH]
**Version:** [Semver oder Datum]
**Status:** Draft | In Review | Approved | Superseded
**Autor:** [Name/Rolle]
**Erstellt:** [Datum]
**Letzte Änderung:** [Datum]
**Constitution-Ref:** constitution.md v[X]

---

## 1. Zusammenfassung (BLUF + Pyramid Principle)

**Format:** BLUF (Bottom Line Up Front, US-Militär) — Ein Satz: Was wird gebaut, für wen, welches Problem wird gelöst. Danach: Pyramid Principle (Barbara Minto) — max. 3 Schlüsselargumente als Stützen. Kein Tech-Stack.

## 2. Kontext & Problemstellung

[Welches Problem wird gelöst? Für wen? Was passiert, wenn nichts getan wird?]

## 3. Scope

### In Scope
- [Konkrete Capabilities]

### Out of Scope
- [Explizit ausgeschlossen — verhindert Scope Creep]

### Annahmen
- [Annahme: ...] ← Werden in Clarify-Phase bestätigt oder verworfen

## 4. Stakeholder

| Rolle | Interesse | Einfluss |
|-------|----------|---------|
| ... | ... | Hoch/Mittel/Gering |

## 5. User Stories

### [SF-XXX-001] [Titel]

**Typ**: User Story | Technical Story | Enabler
**Priorität**: MoSCoW (Dai Clegg, DSDM): Must | Should | Could | Won't
**Spec-First Steps**: [1,2,3,4,6,7]

#### Story
Als [Rolle] möchte ich [Funktion], damit [Nutzen].

#### EARS-Requirement (Alistair Mavin, Rolls-Royce)
**Pattern:** [Ubiquitous | Event-Driven | State-Driven | Optional | Unwanted]
[EARS-Formulierung gemäß Anhang C]

#### Acceptance Criteria (Gherkin, min. 2)

```gherkin
Scenario: [Happy Path]
  Given [Vorbedingung]
  When [Aktion]
  Then [Erwartetes Ergebnis]

Scenario: [Edge Case / Fehlerfall]
  Given [Vorbedingung]
  When [Aktion]
  Then [Erwartetes Ergebnis]
```

#### KRITIS-NFRs
[Relevante Kategorien aus kritis-nfr-checklist.md]

#### STRIDE-Bewertung
[Falls security-relevant — alle 6 Kategorien bewerten]

#### Abhängigkeiten
- Blockiert durch: [SF-XXX-NNN]
- Blockiert: [SF-XXX-NNN]

#### Offene Fragen
- [Frage mit Schweregrad: BLOCKER | MAJOR | MINOR]

#### GP-Compliance
- [Betroffene Golden Principles mit Status]

---

[Weitere Stories nach gleichem Schema]

---

## 6. Nicht-funktionale Anforderungen (NFRs)

### Performance
| Metrik | Zielwert | Messmethode |
|--------|---------|-------------|
| ... | ... | ... |

### Verfügbarkeit
| Metrik | Zielwert |
|--------|---------|
| Uptime | ...% |
| RTO | ... |
| RPO | ... |

### Sicherheit
[STRIDE-Zusammenfassung, Auth-Anforderungen, Encryption]

### Compliance
[KRITIS/NIS2/DSGVO-Anforderungen mit Artikel-Referenzen]

## 7. Datenmodell (DDD — taktisches Design nach Eric Evans)

**Methode:** Domain-Driven Design (Eric Evans, "Tackling Complexity in the Heart of Software", 2003) — taktisches Design.
**Delta:** Konzeptionelles Modell, kein Tech-Stack. Identifiziere:
- **Bounded Contexts** und deren Grenzen (Wo endet ein Modell?)
- **Entities** (identitätsbasiert — z.B. Benutzer, Auftrag)
- **Value Objects** (attributbasiert, unveränderlich — z.B. Adresse, Geldbetrag)
- **Aggregates** mit Invarianten (Konsistenzgrenzen)
- **Domain Events** (bedeutsame Vorkommnisse — z.B. "AuftragAngenommen")
- **Datenklassifizierung** (PII, sensibel, öffentlich — DSGVO-relevant)
**Verify:** Spricht das Modell die Ubiquitous Language der Stakeholder? Können Domänenexperten das Modell lesen und verstehen?

## 8. Systemgrenzen & Schnittstellen

[Externe Systeme, APIs, Datenflüsse — Was geht rein, was geht raus]

## 9. Clarifications

| # | Frage-Ref | Antwort | Datum | Auswirkung auf |
|---|-----------|---------|-------|----------------|
| C-001 | ... | ... | ... | ... |

[Wird in Clarify-Phase (Modus 2) befüllt]

## 10. Review & Acceptance Checklist

- [ ] Alle User Stories haben EARS-Formulierung
- [ ] Jede Story hat ≥2 Gherkin-Szenarien
- [ ] NFR-Kategorien vollständig geprüft
- [ ] STRIDE für security-relevante Stories durchgeführt
- [ ] Keine vagen Begriffe ohne Quantifizierung
- [ ] Keine offenen BLOCKER-Fragen
- [ ] Constitution-Compliance geprüft
- [ ] GP-Compliance pro Story dokumentiert
- [ ] Abhängigkeiten zwischen Stories dokumentiert
- [ ] Systemgrenzen explizit definiert

## 11. Übersichtstabelle

| ID | Titel | Typ | Priorität | EARS | Gherkin | STRIDE | NFR | GP |
|----|-------|-----|-----------|------|---------|--------|-----|-----|
| SF-XXX-001 | ... | US | Must | ✅ | 3 | ✅ | 2 | 01,02,07 |
```

---

## ID-Schema

| Präfix | Kategorie |
|--------|-----------|
| FUNC | Funktionale Anforderung |
| SEC | Sicherheit |
| AVA | Verfügbarkeit |
| INT | Integration / Schnittstelle |
| AUD | Audit / Logging |
| PER | Performance |
| USA | Usability |
| COM | Compliance |
| OPS | Betrieb / Operations |
| DAT | Daten / Storage |

**Vollständige ID:** `SF-[Präfix]-[NNN]` → z.B. `SF-SEC-001`

---

## Regeln

1. **Keine Story ohne EARS** — Pattern muss explizit benannt sein
2. **Min. 2 Gherkin-Szenarien** — Happy Path + mindestens ein Fehlerfall/Edge Case
3. **Keine vagen Begriffe** — "schnell" → "≤200ms p95", "viele" → "≥10.000 concurrent"
4. **Annahmen kennzeichnen** — `[Annahme: ...]` bis Clarify-Phase bestätigt
5. **NFRs sind messbar** — Jeder NFR hat Zielwert + Messmethode
6. **Clarifications-Abschnitt** ist Pflicht — wird in Modus 2 befüllt
7. **Übersichtstabelle** am Ende bei ≥3 Stories

---

## Anhang B: Constitution Template

**Wann konsultieren:** Bei Projekt-Setup oder Constitution-Fragen (Modus 1, Phase 1a)

> Dieses Template definiert die Pflichtstruktur für jede `constitution.md`. SpecForge verwendet es bei Projekt-Setup (Modus 1, Phase 1a).

---

## Pflichtstruktur

```markdown
# Project Constitution: [Projektname]

**Version:** [Semver oder Datum]
**Gültig ab:** [Datum]
**Verantwortlich:** [Rolle/Name]
**Letzte Prüfung:** [Datum]

---

## 1. Projektprinzipien

### Zweck
[1–2 Sätze: Wofür existiert dieses Projekt?]

### Leitbild
[Was ist das angestrebte Qualitätsniveau? Woran wird Erfolg gemessen?]

### Nicht-Ziele
[Was dieses Projekt bewusst NICHT tut — verhindert Scope Creep auf Governance-Ebene]

---

## 2. Golden Principles

Die folgenden Prinzipien sind enforceable — Verstöße blockieren bis zur Auflösung (GP-08).

| ID | Prinzip | Regel | Enforcement-Mechanismus |
|----|---------|-------|------------------------|
| GP-01 | Schema-Hygiene | Matching Fixtures + Testabdeckung für alle API-Contracts | Spec-First Chain Schritt 2+3+6 |
| GP-02 | Spec-before-Code | Keine Implementierung ohne Spec-Eintrag in specs/ | Spec-Phase Gate |
| GP-03 | ADR-Disziplin | Modulübergreifende Entscheidungen brauchen ADR in specs/decisions/ | Review-Routing durch Architect |
| GP-04 | ExecPlan-Pflicht | Tasks mit 5+ Dateiänderungen brauchen EP-*.md in plans/active/ | Tasks-Phase Gate |
| GP-05 | Invariant-Traceability | Tests referenzieren Invariant-IDs aus ARCHITECTURE.md | Traceability Matrix |
| GP-06 | Keine stale Marker | TODO/TBD/FIXME brauchen Datum + Owner, max. 14 Tage | Freshness Check |
| GP-07 | Dokument-Platzierung | Alle Artefakte in Convention-Verzeichnissen | Folder Convention Check |
| GP-08 | Prinzip-Unverletzlichkeit | GP-Verstöße blockieren bis gelöst | Self-Assessment |
| GP-09 | Abhängigkeitsrichtung | Consumer kennt Provider-Interface, nicht Interna | Review Agents |
| GP-10 | Schulden-Tracking | Jede Tech-Debt in tech-debt-tracker.md mit ID + Owner | Harness Auditor |

---

## 3. Regulatorischer Rahmen

### Anwendbare Regulierung

| Regulierung | Anwendbar | Relevante Artikel/Abschnitte |
|------------|-----------|------------------------------|
| KRITIS (BSI) | Ja/Nein | [Sektoren, Schwellenwerte] |
| NIS2 | Ja/Nein | [Art. 21, 23 — Risikomanagement, Meldepflichten] |
| DSGVO | Ja/Nein | [Art. 25, 32, 35 — Privacy by Design, TOM, DSFA] |
| IT-SiG 2.0 | Ja/Nein | [Relevante Pflichten] |
| Branchenspezifisch | Ja/Nein | [z.B. EnWG, TKG, BAIT, MaRisk] |

### Sicherheits-Baseline

| Kategorie | Mindestanforderung |
|-----------|-------------------|
| Authentifizierung | [z.B. MFA Pflicht, OAuth 2.0 + OIDC] |
| Verschlüsselung at Rest | [z.B. AES-256] |
| Verschlüsselung in Transit | [z.B. TLS 1.3] |
| Logging & Audit | [z.B. Alle schreibenden Operationen, 90 Tage Retention] |
| Secrets Management | [z.B. Kein Klartext, Vault/KMS Pflicht] |
| Vulnerability Management | [z.B. CVE-Scan wöchentlich, kritische CVEs in 48h] |

---

## 4. Qualitätsstandards

### Testanforderungen

| Ebene | Abdeckung | Pflicht |
|-------|----------|---------|
| Unit Tests | ≥[X]% Line Coverage | Ja |
| Integration Tests | Alle API-Endpoints | Ja |
| Contract Tests | Alle Provider-Consumer-Paare | Ja (GP-01) |
| E2E Tests | Happy Paths aller User Stories | [Ja/Optional] |
| Security Tests | OWASP Top 10 | Ja |
| Performance Tests | Alle PER-NFRs | [Ja/Optional] |

### Code-Qualität

| Metrik | Schwellwert |
|--------|-----------|
| Cyclomatic Complexity | ≤[X] pro Funktion |
| Cognitive Complexity | ≤[X] pro Funktion |
| Dependency Depth | ≤[X] |
| Duplicate Code | ≤[X]% |

### Definition of Done (Spec-Ebene)

Eine Spezifikation gilt als "Done", wenn:
- [ ] Alle User Stories haben EARS-Formulierung
- [ ] Jede Story hat ≥2 Gherkin-Szenarien mit konkreten Testdaten
- [ ] NFR-Kategorien vollständig gegen KRITIS-Checkliste geprüft
- [ ] STRIDE für alle security-relevanten Stories durchgeführt
- [ ] Clarifications-Abschnitt abgeschlossen (keine offenen BLOCKER)
- [ ] GP-Compliance pro Story dokumentiert
- [ ] Review & Acceptance Checklist vollständig ausgefüllt
- [ ] Analyze-Report ohne BLOCKER-Befunde

### Definition of Done (Implementierungs-Ebene)

Ein Feature gilt als "Done", wenn:
- [ ] Alle Tasks aus tasks.md abgeschlossen
- [ ] Spec-First Chain pro Task eingehalten
- [ ] Alle Gherkin-Szenarien als automatisierte Tests implementiert
- [ ] NFR-Zielwerte nachweislich erreicht
- [ ] Keine offenen GP-Verstöße
- [ ] ARCHITECTURE.md aktualisiert
- [ ] Kein staler Marker ohne Owner (GP-06)
- [ ] tech-debt-tracker.md aktuell

---

## 5. Architekturentscheidungen

### Leitplanken

| Entscheidung | Begründung | ADR |
|-------------|-----------|-----|
| [z.B. Microservices vs. Monolith] | [1 Satz] | adr-001 |
| [z.B. Event-Driven vs. Request-Response] | [1 Satz] | adr-002 |

### Technologie-Constraints

| Kategorie | Erlaubt | Verboten | Begründung |
|-----------|---------|----------|-----------|
| Runtime | [z.B. .NET 8+, Java 21+] | [z.B. Node.js <20] | [Compliance/Support] |
| Datenbank | [z.B. PostgreSQL 16+] | [z.B. MongoDB <7] | [KRITIS-Zertifizierung] |
| Cloud Provider | [z.B. Azure, On-Prem] | [z.B. Nicht-EU-Regionen] | [Datensouveränität] |

---

## 6. Änderungshistorie

| Version | Datum | Autor | Änderung |
|---------|-------|-------|---------|
| 1.0 | [Datum] | [Autor] | Initiale Constitution |
```

---

## Regeln

1. **Constitution ist das Governance-Dokument** — alle Specs, Plans und Tasks müssen konform sein
2. **Golden Principles sind nicht verhandelbar** — GP-08 sichert das ab
3. **Regulatorischer Rahmen wird bei Projekt-Setup recherchiert** — nicht geraten
4. **Sicherheits-Baseline ist das Minimum** — Features dürfen höhere Standards setzen, nicht niedrigere
5. **DoD ist bindend** — keine Ausnahmen ohne dokumentierte Begründung in der Constitution selbst
6. **Änderungen an der Constitution brauchen eine neue Version** — kein stilles Editieren

---

## Anhang C: EARS-Syntax

**Wann konsultieren:** Bei EARS-Formulierungen in jeder Story

> Easy Approach to Requirements Syntax. Jedes Requirement in SpecForge wird in einem der 5 EARS-Patterns formuliert. Das Pattern wird immer explizit benannt.

---

## Die 5 EARS-Patterns

### 1. Ubiquitous (Allgemeingültig)

**Wann:** Anforderung gilt immer, ohne Bedingung oder Auslöser.

**Syntax:**
```
Das [System] soll [Funktion/Eigenschaft].
```

**Beispiel:**
```
Das System soll alle API-Responses im JSON-Format ausliefern.
```

**Erkennungsmerkmal:** Keine Wenn-Dann-Struktur, keine Zustandsbedingung, keine Ereignis-Trigger.

---

### 2. Event-Driven (Ereignisgesteuert)

**Wann:** Anforderung wird durch ein spezifisches Ereignis ausgelöst.

**Syntax:**
```
Wenn [Ereignis], soll das [System] [Funktion/Reaktion].
```

**Beispiel:**
```
Wenn ein Benutzer drei ungültige Login-Versuche innerhalb von 5 Minuten durchführt, soll das System den Account für 30 Minuten sperren und eine E-Mail-Benachrichtigung an den Benutzer senden.
```

**Erkennungsmerkmal:** Klarer zeitlicher Auslöser, einmalige Aktion als Reaktion.

---

### 3. State-Driven (Zustandsgesteuert)

**Wann:** Anforderung gilt, solange ein bestimmter Zustand aktiv ist.

**Syntax:**
```
Solange [Zustand], soll das [System] [Funktion/Verhalten].
```

**Beispiel:**
```
Solange die Datenbankverbindung unterbrochen ist, soll das System eingehende Schreiboperationen in einer lokalen Queue zwischenspeichern und den Benutzer über den Offline-Modus informieren.
```

**Erkennungsmerkmal:** Zustand hat eine Dauer, Verhalten gilt für die gesamte Dauer des Zustands.

---

### 4. Optional (Wahlmöglichkeit)

**Wann:** Anforderung beschreibt ein konfigurierbares oder optionales Verhalten.

**Syntax:**
```
Wenn [Bedingung/Konfiguration aktiviert], soll das [System] [Funktion].
```

**Beispiel:**
```
Wenn der Administrator die Zwei-Faktor-Authentifizierung für eine Benutzergruppe aktiviert hat, soll das System bei jedem Login einen TOTP-Code abfragen.
```

**Erkennungsmerkmal:** Konfigurationsabhängig, Feature-Toggle, Benutzereinstellung.

---

### 5. Unwanted (Unerwünschtes Verhalten)

**Wann:** Anforderung beschreibt, wie das System auf Fehler, Angriffe oder unerwünschte Zustände reagieren soll.

**Syntax:**
```
Wenn [unerwünschtes Ereignis/Zustand], soll das [System] [Schutzmaßnahme/Reaktion].
```

**Beispiel:**
```
Wenn ein API-Request ein ungültiges JWT-Token enthält, soll das System den Request mit HTTP 401 ablehnen, den Vorfall im Security-Audit-Log protokollieren und keine Detailinformationen über den Ablehnungsgrund in der Response preisgeben.
```

**Erkennungsmerkmal:** Fehlerfall, Sicherheitsvorfall, Systemausfall, unerwarteter Input.

---

## Pattern-Auswahlhilfe

```
Gibt es eine Bedingung oder einen Auslöser?
├── Nein → UBIQUITOUS
└── Ja
    ├── Ist es ein einmaliges Ereignis? → EVENT-DRIVEN
    ├── Ist es ein andauernder Zustand? → STATE-DRIVEN
    ├── Ist es konfigurationsabhängig? → OPTIONAL
    └── Ist es ein Fehler-/Angriffsfall? → UNWANTED
```

---

## EARS-Qualitätskriterien

| Kriterium | Beschreibung | Anti-Pattern |
|-----------|-------------|--------------|
| **Atomar** | Ein Requirement = eine testbare Aussage | "Das System soll X und Y und Z" |
| **Messbar** | Quantifizierte Werte statt vager Begriffe | "schnell", "viele", "einfach" |
| **Eindeutig** | Kein Interpretationsspielraum | "angemessen", "bei Bedarf", "ggf." |
| **Vollständig** | Alle Aspekte des Verhaltens beschrieben | Fehlende Fehlerbehandlung, fehlende Grenzwerte |
| **Testbar** | Objektives Pass/Fail-Kriterium ableitbar | "Das System soll benutzerfreundlich sein" |
| **Konsistent** | Kein Widerspruch zu anderen Requirements | Zwei Requirements mit gegensätzlichem Verhalten |

---

## Verbotene Formulierungen

| Verboten | Warum | Besser |
|----------|-------|--------|
| "Das System sollte..." | "Sollte" impliziert Optional | "Das System soll..." |
| "möglichst schnell" | Nicht messbar | "innerhalb von ≤200ms (p95)" |
| "bei Bedarf" | Wer entscheidet? Wann? | Konkreten Trigger benennen |
| "angemessene Sicherheit" | Nicht testbar | Konkretes Verfahren + Standard |
| "etc.", "und ähnliches" | Unvollständig | Vollständige Aufzählung |
| "intuitiv bedienbar" | Subjektiv | Messbare Usability-Metrik (z.B. Task Completion Rate ≥90%) |
| "in Echtzeit" | Undefiniert | Konkrete Latenz (z.B. ≤100ms) |

---

## Kombination mit Gherkin

Jedes EARS-Requirement wird durch mindestens 2 Gherkin-Szenarien operationalisiert:

```
EARS (Event-Driven):
  Wenn ein Benutzer drei ungültige Login-Versuche innerhalb von 5 Minuten durchführt,
  soll das System den Account für 30 Minuten sperren.

Gherkin Szenario 1 (Happy Path):
  Given ein Benutzer mit aktivem Account
  When der Benutzer 3 ungültige Passwörter innerhalb von 5 Minuten eingibt
  Then wird der Account für 30 Minuten gesperrt
  And der Benutzer erhält eine E-Mail-Benachrichtigung

Gherkin Szenario 2 (Edge Case):
  Given ein Benutzer mit aktivem Account
  When der Benutzer 2 ungültige Passwörter eingibt, 6 Minuten wartet, dann 1 weiteres
  Then bleibt der Account aktiv
  And der Fehlzähler wird zurückgesetzt
```

---

## Anhang D: KRITIS-NFR-Checkliste

**Wann konsultieren:** Bei NFR-Prüfung oder Story-Erzeugung

> Automatische Prüfliste für nicht-funktionale Anforderungen in KRITIS-regulierten Umgebungen. SpecForge prüft jede Story gegen diese Kategorien und ergänzt fehlende NFRs.

---

## Prüfkategorien

### 1. Verfügbarkeit (AVA)

| # | Prüfpunkt | Mindestanforderung KRITIS | Frage an Spec |
|---|-----------|--------------------------|---------------|
| AVA-01 | Uptime-SLA | ≥99,9% (8,76h Downtime/Jahr) | Ist ein Uptime-Zielwert definiert? |
| AVA-02 | RTO (Recovery Time Objective) | ≤4h für kritische Systeme | Ist die maximale Wiederherstellungszeit definiert? |
| AVA-03 | RPO (Recovery Point Objective) | ≤1h für kritische Daten | Ist der maximale Datenverlust-Zeitraum definiert? |
| AVA-04 | Redundanz | Kein Single Point of Failure | Sind Redundanz-Anforderungen dokumentiert? |
| AVA-05 | Failover | Automatisches Failover ≤60s | Ist Failover-Verhalten spezifiziert? |
| AVA-06 | Backup-Strategie | 3-2-1-Regel (3 Kopien, 2 Medien, 1 Offsite) | Ist eine Backup-Strategie definiert? |
| AVA-07 | Disaster Recovery | DR-Plan mit dokumentiertem Testrhythmus | Ist ein DR-Szenario beschrieben? |
| AVA-08 | Degraded Mode | Definiertes Verhalten bei Teilausfall | Ist Degraded-Mode-Verhalten spezifiziert? |

### 2. Sicherheit (SEC)

| # | Prüfpunkt | Mindestanforderung KRITIS | Frage an Spec |
|---|-----------|--------------------------|---------------|
| SEC-01 | Authentifizierung | MFA für administrative Zugänge | Ist das Auth-Verfahren spezifiziert? |
| SEC-02 | Autorisierung | RBAC/ABAC mit Least Privilege | Ist das Berechtigungsmodell definiert? |
| SEC-03 | Verschlüsselung at Rest | AES-256 oder gleichwertig | Sind Verschlüsselungsanforderungen dokumentiert? |
| SEC-04 | Verschlüsselung in Transit | TLS 1.3 | Ist Transport-Verschlüsselung spezifiziert? |
| SEC-05 | Secrets Management | Kein Klartext, Vault/KMS Pflicht | Ist Secrets-Handling beschrieben? |
| SEC-06 | Input Validation | Whitelist-basiert, serverseitig | Sind Validierungsregeln definiert? |
| SEC-07 | Session Management | Timeout, Rotation, Secure Flags | Sind Session-Anforderungen dokumentiert? |
| SEC-08 | API Security | Rate Limiting, API Keys/OAuth, CORS | Sind API-Sicherheitsanforderungen definiert? |
| SEC-09 | Vulnerability Management | CVE-Scan wöchentlich, kritisch in 48h | Ist der Patch-Prozess beschrieben? |
| SEC-10 | Penetration Testing | Jährlich durch externen Dienstleister | Ist Pen-Testing vorgesehen? |

### 3. Audit & Logging (AUD)

| # | Prüfpunkt | Mindestanforderung KRITIS | Frage an Spec |
|---|-----------|--------------------------|---------------|
| AUD-01 | Audit-Logging | Alle schreibenden Operationen + Auth-Events | Welche Events werden geloggt? |
| AUD-02 | Log-Retention | ≥90 Tage, ≥1 Jahr für Security-Events | Ist die Aufbewahrungsdauer definiert? |
| AUD-03 | Log-Integrität | Tamper-Proof (Append-Only, Signierung) | Ist Log-Integrität sichergestellt? |
| AUD-04 | Log-Zentralisierung | SIEM-Integration | Werden Logs zentral aggregiert? |
| AUD-05 | Nachvollziehbarkeit | Wer hat wann was geändert (Actor, Timestamp, Change) | Ist die Audit-Granularität definiert? |
| AUD-06 | NIS2-Meldepflicht | Sicherheitsvorfälle innerhalb 24h (Frühwarnung), 72h (Vollmeldung) | Ist der Meldeprozess berücksichtigt? |

### 4. Performance (PER)

| # | Prüfpunkt | Mindestanforderung | Frage an Spec |
|---|-----------|-------------------|---------------|
| PER-01 | Response Time | p95 ≤[Xms] für kritische Operationen | Sind Latenz-Zielwerte definiert? |
| PER-02 | Throughput | [X] Requests/Sekunde unter Last | Ist der Durchsatz spezifiziert? |
| PER-03 | Concurrent Users | [X] gleichzeitige Benutzer | Ist die Concurrent-User-Anzahl definiert? |
| PER-04 | Skalierung | Horizontal/Vertikal, Auto-Scaling-Trigger | Ist Skalierungsverhalten beschrieben? |
| PER-05 | Ressourcenlimits | CPU, RAM, Storage Budgets pro Service | Sind Ressourcenlimits definiert? |

### 5. Datenschutz (DAT)

| # | Prüfpunkt | Mindestanforderung DSGVO | Frage an Spec |
|---|-----------|-------------------------|---------------|
| DAT-01 | Datenkategorien | Klassifizierung aller verarbeiteten Daten | Welche Datenkategorien werden verarbeitet? |
| DAT-02 | Rechtsgrundlage | Art. 6 DSGVO pro Verarbeitungszweck | Ist die Rechtsgrundlage dokumentiert? |
| DAT-03 | Löschkonzept | Automatische Löschung nach Zweckerfüllung | Sind Löschfristen definiert? |
| DAT-04 | Datenminimierung | Nur erforderliche Daten erheben | Wird Datenminimierung eingehalten? |
| DAT-05 | Betroffenenrechte | Auskunft, Löschung, Portabilität implementierbar | Sind Betroffenenrechte technisch berücksichtigt? |
| DAT-06 | DSFA | Datenschutz-Folgenabschätzung bei hohem Risiko | Ist eine DSFA erforderlich? |
| DAT-07 | Auftragsverarbeitung | AVV bei externen Dienstleistern | Sind AVV-Anforderungen dokumentiert? |

### 6. Betrieb (OPS)

| # | Prüfpunkt | Mindestanforderung | Frage an Spec |
|---|-----------|-------------------|---------------|
| OPS-01 | Monitoring | Health Checks, Alerting, Dashboards | Ist Monitoring spezifiziert? |
| OPS-02 | Deployment | Zero-Downtime-Deployment, Rollback-Fähigkeit | Ist die Deployment-Strategie beschrieben? |
| OPS-03 | Configuration Management | Externalisiert, versioniert, nicht im Code | Ist Config-Management definiert? |
| OPS-04 | Incident Response | Eskalationspfade, Runbooks | Ist ein Incident-Response-Prozess definiert? |
| OPS-05 | Kapazitätsplanung | Prognostiziertes Wachstum berücksichtigt | Sind Kapazitätsannahmen dokumentiert? |

---

## Anwendung

1. SpecForge iteriert bei jeder Story-Erzeugung über alle 6 Kategorien
2. Fehlende NFRs werden als `[NFR-Lücke: ...]` markiert
3. Bei KRITIS-Projekten sind AVA, SEC, AUD Pflicht — keine Ausnahme
4. Bei Nicht-KRITIS-Projekten empfiehlt SpecForge relevante Kategorien basierend auf Domäne
5. NFRs ohne quantifizierten Zielwert werden als "nicht testbar" markiert

---

## Schweregrad bei fehlenden NFRs

| Kategorie | KRITIS-Projekt | Nicht-KRITIS |
|-----------|---------------|-------------|
| AVA (Verfügbarkeit) | BLOCKER | MAJOR |
| SEC (Sicherheit) | BLOCKER | MAJOR |
| AUD (Audit) | BLOCKER | MINOR |
| PER (Performance) | MAJOR | MINOR |
| DAT (Datenschutz) | BLOCKER (bei PII) | MAJOR (bei PII) |
| OPS (Betrieb) | MAJOR | MINOR |

---

## Anhang E: STRIDE-Checkliste

**Wann konsultieren:** Bei Security-Review oder STRIDE-Analyse

> Threat-Modeling-Framework für security-relevante Requirements. SpecForge führt bei jeder security-relevanten Story eine STRIDE-Analyse durch.

---

## Die 6 STRIDE-Kategorien

### S — Spoofing (Identitätsvortäuschung)

**Bedrohung:** Ein Angreifer gibt sich als legitimer Benutzer, Service oder System aus.

| # | Prüfpunkt | Frage |
|---|-----------|-------|
| S-01 | Benutzer-Authentifizierung | Wie wird die Identität des Benutzers verifiziert? |
| S-02 | Service-zu-Service-Auth | Wie authentifizieren sich Services untereinander? (mTLS, API Keys, OAuth) |
| S-03 | Token-Validierung | Werden Tokens serverseitig validiert? Signaturprüfung? Ablaufzeit? |
| S-04 | Credential Storage | Wie werden Credentials gespeichert? (Hashing, Salting, Algorithmus) |
| S-05 | MFA | Ist Multi-Faktor-Authentifizierung für privilegierte Operationen vorgesehen? |
| S-06 | Session Hijacking | Sind Sessions gegen Übernahme geschützt? (Secure, HttpOnly, SameSite) |

**Typische Mitigations:** MFA, mTLS, JWT mit kurzer Laufzeit, Certificate Pinning, IP-Binding

---

### T — Tampering (Manipulation)

**Bedrohung:** Ein Angreifer verändert Daten während der Übertragung oder im Speicher.

| # | Prüfpunkt | Frage |
|---|-----------|-------|
| T-01 | Transport-Verschlüsselung | Ist TLS 1.3 für alle Kommunikationskanäle erzwungen? |
| T-02 | Datenintegrität | Werden Checksummen/Signaturen für kritische Daten geprüft? |
| T-03 | Input Validation | Wird jeder Input serverseitig validiert? Whitelist-Ansatz? |
| T-04 | SQL Injection | Werden Prepared Statements / Parameterized Queries verwendet? |
| T-05 | XSS | Wird Output Encoding konsequent angewendet? CSP-Header? |
| T-06 | File Upload | Werden hochgeladene Dateien validiert? (Typ, Größe, Inhalt) |
| T-07 | Konfiguration | Sind Konfigurationsdateien gegen Manipulation geschützt? (Signierung, Zugriffskontrolle) |

**Typische Mitigations:** TLS 1.3, HMAC-Signaturen, Input Sanitization, CSP, Parameterized Queries

---

### R — Repudiation (Abstreitbarkeit)

**Bedrohung:** Ein Benutzer oder System bestreitet eine durchgeführte Aktion.

| # | Prüfpunkt | Frage |
|---|-----------|-------|
| R-01 | Audit-Logging | Werden alle sicherheitsrelevanten Aktionen geloggt? |
| R-02 | Log-Inhalt | Enthält jeder Log-Eintrag: Actor, Timestamp, Action, Resource, Result? |
| R-03 | Log-Integrität | Sind Logs gegen nachträgliche Manipulation geschützt? (Append-Only, Signierung) |
| R-04 | Zeitstempel | Wird eine vertrauenswürdige Zeitquelle verwendet? (NTP, Zeitserver) |
| R-05 | Nicht-Abstreitbarkeit | Gibt es digitale Signaturen für kritische Transaktionen? |
| R-06 | Log-Retention | Werden Logs gemäß regulatorischer Anforderungen aufbewahrt? |

**Typische Mitigations:** Zentrales SIEM, Tamper-Proof Logging, Digitale Signaturen, NTP-Synchronisierung

---

### I — Information Disclosure (Informationsoffenlegung)

**Bedrohung:** Vertrauliche Informationen werden unbefugt offengelegt.

| # | Prüfpunkt | Frage |
|---|-----------|-------|
| I-01 | Fehlerbehandlung | Gibt das System interne Details in Fehlermeldungen preis? (Stack Traces, DB-Schemas) |
| I-02 | API-Responses | Werden nur die minimal notwendigen Daten zurückgegeben? |
| I-03 | Logging | Werden sensible Daten (Passwörter, Tokens, PII) in Logs maskiert? |
| I-04 | Encryption at Rest | Sind sensible Daten im Speicher verschlüsselt? |
| I-05 | Header-Leaks | Werden Server-Version, Framework-Version etc. in HTTP-Headern unterdrückt? |
| I-06 | Directory Listing | Ist Directory Listing deaktiviert? |
| I-07 | Caching | Werden sensible Responses mit Cache-Control: no-store versehen? |
| I-08 | Seitenkanal | Sind Timing-Angriffe auf Auth-Endpunkte verhindert? (Constant-Time Comparison) |

**Typische Mitigations:** Generische Fehlermeldungen, Field-Level Encryption, Log-Masking, Security Headers

---

### D — Denial of Service (Dienstverweigerung)

**Bedrohung:** Ein Angreifer macht das System für legitime Benutzer unverfügbar.

| # | Prüfpunkt | Frage |
|---|-----------|-------|
| D-01 | Rate Limiting | Gibt es Request-Limits pro Client/IP/User? |
| D-02 | Resource Limits | Sind CPU, RAM, Connection-Pools begrenzt? |
| D-03 | Payload Limits | Gibt es Größenlimits für Requests, Uploads, Batch-Operationen? |
| D-04 | Timeout-Konfiguration | Sind Timeouts für alle externen Aufrufe konfiguriert? |
| D-05 | Circuit Breaker | Gibt es Circuit Breaker für abhängige Services? |
| D-06 | Queue-Schutz | Sind Message Queues gegen Überlauf geschützt? (DLQ, Backpressure) |
| D-07 | DDoS-Schutz | Ist DDoS-Mitigation vorgesehen? (WAF, CDN, Cloud-Schutz) |
| D-08 | Graceful Degradation | Ist definiert, wie das System bei Überlast reagiert? |

**Typische Mitigations:** Rate Limiting, WAF, Auto-Scaling, Circuit Breaker, Bulkhead Pattern

---

### E — Elevation of Privilege (Rechteeskalation)

**Bedrohung:** Ein Benutzer erlangt höhere Berechtigungen als vorgesehen.

| # | Prüfpunkt | Frage |
|---|-----------|-------|
| E-01 | Least Privilege | Haben Benutzer und Services nur die minimal notwendigen Rechte? |
| E-02 | Autorisierungsprüfung | Wird die Berechtigung bei jeder Operation serverseitig geprüft? (Nicht nur UI-seitig) |
| E-03 | IDOR | Sind Insecure Direct Object References verhindert? (UUID statt sequenzieller IDs, Ownership-Check) |
| E-04 | Admin-Funktionen | Sind administrative Funktionen zusätzlich abgesichert? (Separate Auth, IP-Whitelist) |
| E-05 | Privilege Escalation via API | Kann ein Benutzer über API-Calls Rechte ändern, die er über die UI nicht hat? |
| E-06 | Default Credentials | Werden Default-Passwörter und Default-Rollen bei Installation erzwungen geändert? |
| E-07 | Service Accounts | Sind Service-Accounts mit minimalen Rechten und rotierenden Credentials konfiguriert? |

**Typische Mitigations:** RBAC/ABAC, Serverseitige Autorisierung, UUID-basierte Ressourcen-IDs, Privileged Access Management

---

## Anwendung in SpecForge

1. **Wann:** Bei jeder Story mit SEC-NFR oder bei expliziter Anfrage
2. **Scope:** Alle 6 Kategorien werden geprüft — auch wenn nur einzelne offensichtlich relevant sind
3. **Output:** Tabelle im spec.md mit Bewertung pro Kategorie (Geprüft Ja/Nein, Befund, Mitigation)
4. **Schweregrad:** Fehlende STRIDE-Analyse für security-relevante Stories = BLOCKER in Analyze
5. **Iteration:** STRIDE wird bei Spec-Updates wiederholt, nicht nur einmalig

---

## STRIDE-Output-Format

```markdown
#### STRIDE-Bewertung: [SF-SEC-NNN]

| Kategorie | Relevant | Befund | Risiko | Mitigation | Status |
|-----------|----------|--------|--------|-----------|--------|
| Spoofing | Ja | OAuth ohne MFA | Hoch | MFA für Admin-Operationen einführen | Offen |
| Tampering | Ja | TLS 1.3 konfiguriert | Niedrig | — | Mitigiert |
| Repudiation | Ja | Audit-Logging vorhanden | Niedrig | — | Mitigiert |
| Info Disclosure | Ja | Stack Traces in Prod | Hoch | Generische Fehlermeldungen | Offen |
| Denial of Service | Ja | Rate Limiting fehlt | Mittel | Rate Limiter implementieren | Offen |
| Elev. of Privilege | Ja | RBAC implementiert | Niedrig | — | Mitigiert |

**Offene Risiken:** 3
**Höchstes Risiko:** Hoch (Spoofing, Info Disclosure)
```

---

## Anhang F: Golden Principles

**Wann konsultieren:** Bei GP-Prüfung, Self-Assessment, Review

> 10 enforceable Prinzipien. Jedes Prinzip hat eine klare Regel, einen Enforcement-Mechanismus und Beispiele für Verstöße.

---

## GP-01: Schema-Hygiene

**Regel:** Jeder API-Contract hat Matching Fixtures + Testabdeckung.

**Enforcement:** Spec-First Chain Schritte 2 (Schema), 3 (Fixture), 6 (Contract Tests).

**Verstoß-Beispiel:** API-Endpoint liefert Feld `created_at` zurück, das im Schema nicht definiert ist und für das kein Fixture existiert.

**Prüfung:**
- Gibt es für jeden Endpoint ein Schema (OpenAPI, JSON Schema, Protobuf)?
- Gibt es für jedes Schema mindestens eine Fixture-Datei?
- Gibt es Contract Tests, die Schema + Fixture gegen die tatsächliche API validieren?

**Schweregrad bei Verstoß:** MAJOR

---

## GP-02: Spec-before-Code

**Regel:** Keine Implementierung ohne Spec-Eintrag in `specs/`.

**Enforcement:** Spec-Phase Gate — vor jedem Task wird geprüft, ob ein Spec-Eintrag existiert.

**Verstoß-Beispiel:** Entwickler implementiert einen neuen Endpoint, der in keiner spec.md beschrieben ist.

**Prüfung:**
- Hat jeder implementierte Endpoint/Feature eine korrespondierende Story in spec.md?
- Ist die Story vor der Implementierung geschrieben worden (nicht nachträglich)?
- Sind die Gherkin-ACs vor den Tests geschrieben worden?

**Schweregrad bei Verstoß:** BLOCKER

---

## GP-03: ADR-Disziplin

**Regel:** Modulübergreifende Entscheidungen brauchen ein ADR in `specs/decisions/`.

**Methodik:** ADR according to Michael Nygard ("Documenting Architecture Decisions", 2011).
**Delta:** Erweitert um Alternativen-Abschnitt für Entscheidungstransparenz.

**Enforcement:** Review-Routing — System Architect und Contract Guardian prüfen Cross-Modul-Änderungen.

**Verstoß-Beispiel:** Wechsel von REST zu gRPC für Service-Kommunikation ohne ADR.

**Prüfung:**
- Betrifft die Änderung mehr als ein Modul/Service?
- Gibt es ein ADR mit: Kontext, Entscheidung, Konsequenzen, Status?
- Ist das ADR in `specs/decisions/adr-NNN.md` abgelegt?

**ADR-Format (Nygard-Struktur):**
```markdown
# ADR-NNN: [Titel]

**Status:** Proposed | Accepted | Deprecated | Superseded
**Datum:** [YYYY-MM-DD]
**Entscheider:** [Rollen]

## Kontext
[Warum muss entschieden werden?]

## Entscheidung
[Was wurde entschieden?]

## Konsequenzen
[Positive und negative Auswirkungen]

## Alternativen
[Verworfene Optionen mit Begründung — bei komplexen Entscheidungen: Pugh Matrix als Bewertungshilfe]
```

**Schweregrad bei Verstoß:** BLOCKER

---

## GP-04: ExecPlan-Pflicht

**Regel:** Tasks mit 5+ Dateiänderungen brauchen einen ExecPlan in `plans/active/`.

**Enforcement:** Tasks-Phase Gate — SpecForge zählt betroffene Dateien pro Task.

**Verstoß-Beispiel:** Task ändert 12 Dateien über 3 Module ohne dokumentierten ExecPlan.

**Prüfung:**
- Wie viele Dateien sind von diesem Task betroffen?
- Bei ≥5: Gibt es ein EP-*.md in `plans/active/`?
- Enthält der ExecPlan: Reihenfolge, Abhängigkeiten, Rollback-Strategie?

**ExecPlan-Format:**
```markdown
# EP-NNN: [Titel]

**Task-Ref:** [Task-ID aus tasks.md]
**Betroffene Dateien:** [Anzahl]
**Status:** Active | Completed | Aborted

## Änderungsreihenfolge
1. [Datei] — [Änderung]
2. [Datei] — [Änderung]
...

## Abhängigkeiten
[Was muss vorher erledigt sein?]

## Rollback-Strategie
[Wie wird zurückgerollt, wenn etwas schiefgeht?]

## Checkpoint
[Woran erkennt man, dass der ExecPlan erfolgreich war?]
```

**Schweregrad bei Verstoß:** MAJOR

---

## GP-05: Invariant-Traceability

**Regel:** Tests referenzieren Invariant-IDs aus `ARCHITECTURE.md`.

**Enforcement:** Traceability Matrix — SpecForge prüft, ob Invarianten durch Tests abgedeckt sind.

**Verstoß-Beispiel:** ARCHITECTURE.md definiert Invariante "Ein Benutzer hat maximal 3 aktive Sessions", aber kein Test referenziert diese Invariante.

**Prüfung:**
- Sind Invarianten in ARCHITECTURE.md mit IDs versehen (INV-NNN)?
- Referenzieren Tests diese IDs in Kommentaren oder Tags?
- Gibt es verwaiste Invarianten (ohne Test-Abdeckung)?

**Schweregrad bei Verstoß:** MAJOR

---

## GP-06: Keine stale Marker

**Regel:** TODO/TBD/FIXME brauchen Datum + Owner. Maximales Alter: 14 Tage.

**Enforcement:** Freshness Check — SpecForge scannt alle Artefakte nach stale Markern.

**Verstoß-Beispiel:** `// TODO: Caching implementieren` ohne Datum, ohne Owner, seit 3 Monaten im Code.

**Prüfung:**
- Hat jeder TODO/TBD/FIXME-Marker ein Datum und einen Owner?
- Ist der Marker älter als 14 Tage?
- Bei >14 Tagen: Gibt es einen Eintrag in tech-debt-tracker.md?

**Korrektes Format:** `// TODO(2025-10-01, @mzimmermann): Caching implementieren — Ticket: PROJ-123`

**Schweregrad bei Verstoß:** MINOR (wird MAJOR nach 30 Tagen)

---

## GP-07: Dokument-Platzierung

**Regel:** Alle Artefakte liegen in Convention-Verzeichnissen gemäß Folder Convention.

**Enforcement:** Folder Convention Check — SpecForge prüft Dateipfade gegen die Convention.

**Verstoß-Beispiel:** ADR liegt in `docs/decisions/` statt in `specs/decisions/`.

**Prüfung:**
- Liegt die Datei im korrekten Convention-Verzeichnis?
- Folgt der Dateiname der Namenskonvention?
- Gibt es Dateien außerhalb der Convention-Struktur?

**Schweregrad bei Verstoß:** MINOR

---

## GP-08: Prinzip-Unverletzlichkeit

**Regel:** Verstöße gegen Golden Principles blockieren bis zur Auflösung.

**Enforcement:** Self-Assessment — SpecForge prüft jeden Output gegen alle GPs.

**Verstoß-Beispiel:** BLOCKER-Verstoß gegen GP-02 wird ignoriert und Implementierung fortgesetzt.

**Prüfung:**
- Gibt es offene BLOCKER-Verstöße gegen GPs?
- Sind alle BLOCKER aufgelöst, bevor zur nächsten Phase übergegangen wird?
- Sind MAJOR-Verstöße dokumentiert und terminiert?

**Schweregrad:** Meta-Prinzip — sichert alle anderen GPs ab.

---

## GP-09: Abhängigkeitsrichtung

**Regel:** Consumer kennt Provider-Interface, nicht Provider-Interna.

**Enforcement:** Review Agents (Contract Guardian, System Architect).

**Verstoß-Beispiel:** Frontend importiert Backend-Datenbank-Entity direkt statt über API-Contract.

**Prüfung:**
- Kennt der Consumer nur das öffentliche Interface des Providers?
- Gibt es direkte Abhängigkeiten auf Provider-Interna (DB-Schemas, interne Klassen)?
- Ist die Abhängigkeitsrichtung in ARCHITECTURE.md dokumentiert?

**Schweregrad bei Verstoß:** MAJOR

---

## GP-10: Schulden-Tracking

**Regel:** Jede identifizierte Tech-Debt wird in `tech-debt-tracker.md` erfasst.

**Enforcement:** Harness Auditor — prüft, ob bekannte Schulden dokumentiert sind.

**Verstoß-Beispiel:** Workaround für Performance-Problem wird implementiert, ohne Eintrag im Debt-Tracker.

**Prüfung:**
- Gibt es einen Eintrag in tech-debt-tracker.md für jede bekannte Schuld?
- Hat jeder Eintrag: ID, Beschreibung, Owner, Priorität, Auswirkung?
- Gibt es einen Review-Rhythmus für den Tracker?

**Tech-Debt-Tracker-Format:**
```markdown
| ID | Beschreibung | Owner | Priorität | Auswirkung | Erstellt | Ziel-Sprint |
|----|-------------|-------|-----------|-----------|---------|-------------|
| TD-001 | Caching fehlt für Katalog-API | @dev | Hoch | p95 >500ms | 2025-10-01 | Sprint 12 |
```

**Schweregrad bei Verstoß:** MINOR (wird MAJOR wenn Schuld Auswirkung auf NFRs hat)

---

## GP-Compliance-Scorecard

```
GP-Score = Anzahl erfüllter GPs / 10

≥ 9/10  → Exzellent — Implementierung freigegeben
  8/10  → Gut — Implementierung mit dokumentierten Einschränkungen
  7/10  → Grenzwertig — Überarbeitung empfohlen
≤ 6/10  → Nicht freigabefähig — Blockiert
```

**Analyze-Schwellwert:** GP-Score ≥ 8/10 für Implementierungs-Readiness.

---

## Anhang G: Folder Convention

**Wann konsultieren:** Bei Projekt-Setup oder Struktur-Fragen

> Pflichtstruktur für alle SpecForge-Projekte. Nicht verhandelbar (GP-07). Alle Artefakte referenzieren diese Pfade.

---

## Verzeichnisstruktur

```
<project-root>/
│
├── ARCHITECTURE.md              ← Codemap, Doc Map, Golden Principles, Invariants
├── constitution.md              ← Projektprinzipien, Baseline-NFRs, DoD
├── tech-debt-tracker.md         ← Schuldenregister (GP-10)
│
├── specs/
│   ├── principles/              ← Design Principles
│   │   ├── P001-single-responsibility.md
│   │   └── P002-api-first.md
│   │
│   ├── decisions/               ← Architecture Decision Records
│   │   ├── adr-001-database-choice.md
│   │   ├── adr-002-auth-strategy.md
│   │   └── adr-template.md
│   │
│   ├── system/                  ← Systemweite Spezifikationen
│   │   ├── domain-model.md
│   │   ├── api-overview.md
│   │   └── data-classification.md
│   │
│   └── use-cases/               ← Feature-Spezifikationen (1 Ordner pro Feature)
│       ├── 001-user-auth/
│       │   ├── spec.md          ← Funktionale Spezifikation
│       │   ├── plan.md          ← Technischer Implementierungsplan
│       │   ├── research.md      ← Technische Tiefenrecherche
│       │   ├── quickstart.md    ← Entwickler-Schnelleinstieg
│       │   ├── tasks.md         ← Task-Breakdown
│       │   └── contracts/       ← API-Verträge (OpenAPI, JSON Schema)
│       │       ├── api-spec.json
│       │       └── events-spec.md
│       │
│       └── 002-data-export/
│           ├── spec.md
│           ├── plan.md
│           ├── research.md
│           ├── quickstart.md
│           └── tasks.md
│
├── plans/
│   ├── active/                  ← Laufende ExecPlans (GP-04)
│   │   ├── EP-001-auth-migration.md
│   │   └── EP-002-schema-update.md
│   │
│   └── completed/              ← Abgeschlossene ExecPlans
│       └── EP-000-initial-setup.md
│
└── design/                      ← Design-Artefakte
    ├── wireframes/
    ├── data-models/
    └── architecture-diagrams/
```

---

## Namenskonventionen

### Feature-Ordner

```
specs/use-cases/[NNN]-[kebab-case-name]/
```

- `NNN` = Dreistellige laufende Nummer (001, 002, ...)
- `kebab-case-name` = Feature-Name in Kleinbuchstaben mit Bindestrichen
- Beispiel: `specs/use-cases/003-multi-tenant-support/`

### Artefakte innerhalb eines Features

| Datei | Pflicht | Erzeugt in Phase |
|-------|---------|-----------------|
| `spec.md` | Ja | Specify (Modus 1) |
| `plan.md` | Ja | Plan (Modus 3, Phase 3a) |
| `research.md` | Ja | Research (Modus 3, Phase 3b) |
| `quickstart.md` | Ja | Quickstart (Modus 3, Phase 3c) |
| `tasks.md` | Ja | Tasks (Modus 3, Phase 3d) |
| `contracts/` | Wenn APIs betroffen | Plan (Modus 3, Phase 3a) |

### Architecture Decision Records

```
specs/decisions/adr-[NNN]-[kebab-case-title].md
```

- Beispiel: `specs/decisions/adr-003-event-sourcing.md`

### Design Principles

```
specs/principles/P[NNN]-[kebab-case-title].md
```

- Beispiel: `specs/principles/P001-single-responsibility.md`

### ExecPlans

```
plans/active/EP-[NNN]-[kebab-case-title].md    ← In Arbeit
plans/completed/EP-[NNN]-[kebab-case-title].md  ← Abgeschlossen
```

- Beispiel: `plans/active/EP-005-database-migration.md`
- Nach Abschluss: Verschieben nach `plans/completed/`

### Tech-Debt-Einträge

IDs im `tech-debt-tracker.md`:
```
TD-[NNN]
```

- Beispiel: `TD-012`

---

## Regeln

1. **Keine Artefakte außerhalb der Convention** — GP-07 erzwingt dies
2. **Leere Verzeichnisse werden nicht angelegt** — nur bei Bedarf erstellen
3. **Keine verschachtelten Features** — `use-cases/` ist flach, keine Unterordner in Features (außer `contracts/`)
4. **Feature-Nummern sind monoton steigend** — keine Lücken, keine Wiederverwendung
5. **ExecPlans wandern** — von `active/` nach `completed/` bei Abschluss
6. **ARCHITECTURE.md und constitution.md liegen im Root** — nicht in Unterordnern
7. **tech-debt-tracker.md liegt im Root** — zentral, nicht pro Feature

---

## Mapping zu SpecKit-Verzeichnissen

| SpecForge Convention | SpecKit-Äquivalent |
|---------------------|-------------------|
| `specs/use-cases/<feature>/spec.md` | `.specify/specs/<feature>/spec.md` |
| `specs/use-cases/<feature>/plan.md` | `.specify/specs/<feature>/plan.md` |
| `specs/use-cases/<feature>/research.md` | `.specify/specs/<feature>/research.md` |
| `specs/use-cases/<feature>/quickstart.md` | `.specify/specs/<feature>/quickstart.md` |
| `specs/use-cases/<feature>/tasks.md` | `.specify/specs/<feature>/tasks.md` |
| `constitution.md` | `.specify/memory/constitution.md` |
| `specs/decisions/adr-*.md` | Kein SpecKit-Äquivalent |
| `plans/active/EP-*.md` | Kein SpecKit-Äquivalent |
| `tech-debt-tracker.md` | Kein SpecKit-Äquivalent |

SpecForge-Projekte können beide Conventions parallel unterstützen, wenn SpecKit CLI verwendet wird.

---

## Anhang H: Spec-First Chain

**Wann konsultieren:** Bei Tasks-Erzeugung oder Chain-Audit

> 8-Schritt-Pflichtsequenz für jeden Task. SpecForge markiert pro Task, welche Schritte relevant sind.

---

## Die 8 Schritte

```
┌─────────────────────────────────────────────────────────────────┐
│                    SPEC-FIRST CHAIN                              │
│                                                                  │
│  1. Update Spec ──► 2. Update Schema ──► 3. Update Fixture     │
│         │                   │                    │               │
│         ▼                   ▼                    ▼               │
│  4. Update Provider ──► 5. Update Consumer ──► 6. Run Tests    │
│                                                   │              │
│                                                   ▼              │
│                    7. Log Breaking Changes ──► 8. Update ARCH   │
└─────────────────────────────────────────────────────────────────┘
```

---

### Schritt 1: Update Spec

**Was:** Spezifikation aktualisieren, bevor Code geschrieben wird.

**Wo:** `specs/system/` oder `specs/use-cases/<feature>/spec.md`

**Wann relevant:** Immer. GP-02 (Spec-before-Code) macht diesen Schritt zur Pflicht.

**Prüfung:**
- Ist die Änderung in einer User Story oder einem Requirement dokumentiert?
- Sind EARS-Formulierung und Gherkin-ACs aktualisiert?
- Sind neue NFRs identifiziert und dokumentiert?

**Nicht relevant wenn:** Reines Refactoring ohne funktionale Änderung (aber: tech-debt-tracker.md aktualisieren, GP-10).

---

### Schritt 2: Update Schema

**Was:** API-Contracts/Schemas aktualisieren.

**Wo:** `specs/use-cases/<feature>/contracts/` (OpenAPI, JSON Schema, Protobuf, GraphQL SDL)

**Wann relevant:** Bei jeder Änderung an API-Endpoints, Datenmodellen oder Event-Payloads.

**Prüfung:**
- Ist das Schema konsistent mit der Spec?
- Sind neue Felder, Endpoints oder Events im Schema dokumentiert?
- Ist die Versionierung korrekt (Breaking Change → Major Version)?

**Nicht relevant wenn:** Reine UI-Änderungen ohne API-Auswirkung, reine Infrastruktur-Tasks.

---

### Schritt 3: Update Fixture

**Was:** Testdaten/Fixtures für die geänderten Schemas aktualisieren.

**Wo:** Testdaten-Verzeichnis (projektspezifisch)

**Wann relevant:** Immer wenn Schritt 2 (Schema) durchgeführt wurde. GP-01 (Schema-Hygiene) erzwingt Matching Fixtures.

**Prüfung:**
- Gibt es für jedes geänderte Schema eine aktuelle Fixture?
- Decken die Fixtures Happy Path + Edge Cases ab?
- Sind die Fixture-Daten konsistent mit den Gherkin-ACs?

**Nicht relevant wenn:** Schritt 2 nicht relevant war.

---

### Schritt 4: Update Provider

**Was:** Backend-Implementierung aktualisieren (Models, Routes, Services, DB-Migrationen).

**Wo:** Backend-Quellcode (projektspezifisch)

**Wann relevant:** Bei jeder Änderung, die das Backend betrifft.

**Prüfung:**
- Ist die Implementierung konsistent mit Schema (Schritt 2)?
- Sind DB-Migrationen erstellt?
- Ist die Validierung serverseitig implementiert?
- Sind Error-Responses gemäß Schema?

**Nicht relevant wenn:** Reine Frontend-Änderungen, reine Dokumentations-Updates.

---

### Schritt 5: Update Consumer

**Was:** Frontend/Client-Implementierung aktualisieren (UI, Client-Models, API-Calls).

**Wo:** Frontend-Quellcode (projektspezifisch)

**Wann relevant:** Bei jeder Änderung, die den Consumer betrifft.

**Prüfung:**
- Verwendet der Consumer das öffentliche Interface, nicht Provider-Interna? (GP-09)
- Sind neue Felder/Endpoints im Client implementiert?
- Ist Error-Handling für neue Fehlerfälle vorhanden?

**Nicht relevant wenn:** Reine Backend-Änderungen ohne API-Auswirkung, Batch-Jobs ohne UI.

---

### Schritt 6: Run Contract Tests

**Was:** Automatisierte Tests ausführen, die Schema, Fixture, Provider und Consumer validieren.

**Wo:** Test-Suite (projektspezifisch)

**Wann relevant:** Immer wenn Schritt 2 oder 4 oder 5 durchgeführt wurde. GP-01 erzwingt Contract Tests.

**Prüfung:**
- Laufen alle Contract Tests grün?
- Sind neue Tests für geänderte Schemas geschrieben?
- Decken die Tests die Gherkin-Szenarien aus der Spec ab?

**Nicht relevant wenn:** Reine Dokumentations-Updates, Spec-only-Änderungen.

---

### Schritt 7: Log Breaking Changes

**Was:** Breaking Changes im API-Changelog dokumentieren.

**Wo:** API-Changelog (projektspezifisch, z.B. `CHANGELOG.md` oder `specs/system/api-changelog.md`)

**Wann relevant:** Bei jeder Änderung, die bestehende Consumer bricht (Entfernte Felder, geänderte Typen, entfernte Endpoints, geänderte Semantik).

**Prüfung:**
- Ist die Breaking Change im Changelog dokumentiert?
- Ist ein Migrationspfad beschrieben?
- Sind betroffene Consumer identifiziert?
- Ist die Schema-Version korrekt hochgezählt?

**Nicht relevant wenn:** Additive Änderungen (neue Felder, neue Endpoints), interne Refactorings.

---

### Schritt 8: Update ARCHITECTURE.md

**Was:** Codemap, Doc Map, Invariants in ARCHITECTURE.md aktuell halten.

**Wo:** `ARCHITECTURE.md` im Projekt-Root

**Wann relevant:** Bei jeder Änderung, die die Systemstruktur betrifft (neue Module, geänderte Abhängigkeiten, neue Invarianten).

**Prüfung:**
- Ist die Codemap aktuell?
- Sind neue Module/Services dokumentiert?
- Sind Invarianten aktualisiert? (GP-05)
- Stimmt die Doc Map (Pfade zu Artefakten)?

**Nicht relevant wenn:** Änderungen innerhalb eines bestehenden Moduls ohne strukturelle Auswirkung.

---

## Relevanz-Matrix pro Task-Typ

| Task-Typ | 1 Spec | 2 Schema | 3 Fixture | 4 Provider | 5 Consumer | 6 Tests | 7 Breaking | 8 ARCH |
|----------|--------|----------|-----------|-----------|-----------|---------|-----------|--------|
| Neues Feature (Full-Stack) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| API-Änderung (Breaking) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| API-Änderung (Additiv) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Reine UI-Änderung | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ |
| Reines Backend-Refactoring | ❌* | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ |
| DB-Migration | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| NFR-Implementierung | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ |
| Dokumentation only | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Security Fix | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |

*❌\* = Kein Spec-Update nötig, aber tech-debt-tracker.md prüfen (GP-10)*

---

## Task-Annotation in tasks.md

Jeder Task in `tasks.md` erhält eine `Spec-First Steps`-Annotation:

```markdown
### Task T-003: User-Profil-API implementieren

**Spec-First Steps:** [1, 2, 3, 4, 6, 8]
**Typ:** Neues Feature (Backend)
**Betroffen:** specs/use-cases/001-user-auth/spec.md, contracts/api-spec.json

1. ✅ Spec: SF-FUNC-005 in spec.md aktualisiert
2. ✅ Schema: GET /api/users/{id} in api-spec.json ergänzt
3. ✅ Fixture: user-profile-fixture.json erstellt
4. ⬜ Provider: UserController + UserService implementieren
5. — Consumer: Nicht relevant (reiner Backend-Task)
6. ⬜ Tests: Contract Tests für GET /api/users/{id}
7. — Breaking Changes: Nicht relevant (neuer Endpoint)
8. ⬜ ARCHITECTURE.md: User-Modul in Codemap ergänzen
```

---

## Chain-Audit

SpecForge kann die Einhaltung der Spec-First Chain für abgeschlossene Tasks prüfen (Modus 8):

```markdown
## Spec-First Chain Audit: [Feature-Name]

| Task | Steps erwartet | Steps durchgeführt | Lücken | Status |
|------|---------------|-------------------|--------|--------|
| T-001 | 1,2,3,4,6,8 | 1,2,3,4,6,8 | — | ✅ |
| T-002 | 1,4,5,6 | 1,4,6 | 5 (Consumer) | ⚠️ |
| T-003 | 1,2,3,4,6,7,8 | 1,2,4,6 | 3,7,8 | ❌ |

**Chain-Compliance:** 1/3 Tasks vollständig (33%)
**Fehlende Schritte:** Fixture (1x), Breaking Change Log (1x), ARCHITECTURE.md (1x), Consumer (1x)
```

---

## Anhang I: Enforcement Engine — Phase Gates & State Machine

**Wann konsultieren:** IMMER — dieser Anhang wird VOR jeder Ausgabe geprüft. Er ist kein optionaler Anhang, sondern der Governance-Compiler von SpecForge.

**Leitprinzip:** Governance ist ein Compiler, kein Komitee. Dieser Anhang implementiert den Compiler.

---

### I.1 Interne State Machine

SpecForge führt intern einen **Pipeline-State** mit. Jede Session beginnt im Zustand `INIT`. Übergänge sind nur über Phase Gates möglich. Überspringen ist **nur** mit expliziter Begründung und Nutzer-Bestätigung erlaubt — SpecForge fragt aktiv nach.

```
State Machine:

  INIT
   │
   ▼ [Gate G0: Modus-Erkennung]
  MODE_DETECTED ──────────────────┐
   │                               │
   ├─ Forward-Engineering          ├─ Reverse-Engineering
   │                               │
   ▼ [Gate G1]                     ▼ [Gate G1-RE]
  CYNEFIN_DONE                   INPUT_ANALYZED
   │                               │
   ▼ [Gate G2]                     ▼ [Gate G2-RE]
  CONSTITUTION_DONE              5W_EXTRACTED
   │                               │
   ▼ [Gate G3]                     ▼ [Gate G3-RE]
  SPEC_DONE                      SPEC_DONE
   │                               │
   ▼ [Gate G4]                     ▼ [Gate G4]
  CLARIFY_DONE                   CLARIFY_DONE
   │                               │
   ▼ [Gate G5]                     ▼ [Gate G5]
  PLAN_DONE                      PLAN_DONE
   │                               │
   ▼ [Gate G6]                     ▼ [Gate G6]
  TASKS_DONE                     TASKS_DONE
   │                               │
   ▼ [Gate G7]                     ▼ [Gate G7]
  ANALYZE_DONE                   ANALYZE_DONE
   │                               │
   ▼ [Gate G8]                     ▼ [Gate G8]
  REVIEW_DONE                    REVIEW_DONE
   │                               │
   ▼                               ▼
  COMPLETE                       COMPLETE
```

---

### I.2 Phase Gates — Pflichtprüfungen

Jedes Gate hat **Eingangsvoraussetzungen**. Wenn die Voraussetzungen nicht erfüllt sind, **blockiert** SpecForge den Übergang und gibt eine strukturierte Fehlermeldung:

```
⛔ PHASE GATE BLOCKED: [Gate-ID]
Voraussetzung nicht erfüllt: [was fehlt]
Aktuelle Phase: [aktueller State]
Nächste Phase: [gewünschter State]
Aktion: [was der Nutzer tun muss]
Überspringen möglich: [Ja/Nein + Bedingung]
```

#### Gate G0: Modus-Erkennung

**Prüft:** Was ist der Input?
- Quellcode, IPA, APK, Binary, Artefakt → **Reverse-Engineering-Modus** aktivieren
- Feature-Beschreibung, Problem, Idee → **Forward-Engineering-Modus**
- Bestehende spec.md / Requirements → **Review-Modus**

**Aktion bei Unklarheit:** SpecForge fragt:
> "Ich erkenne [Input-Typ]. Soll ich (a) ein bestehendes System dokumentieren (Reverse-Engineering), (b) ein neues Feature spezifizieren (Forward-Engineering), oder (c) bestehende Requirements prüfen (Review)?"

#### Gate G1: Cynefin + Impact Mapping (Forward)

**Voraussetzung:** Modus = Forward-Engineering
**Prüft:**
- [ ] Cynefin-Einordnung durchgeführt (Klar/Kompliziert/Komplex/Chaotisch)
- [ ] Impact Map erstellt (Ziel → Akteure → Auswirkungen → Liefergegenstände)
- [ ] Formalismus-Grad bestimmt und dokumentiert

**Überspringen:** Nur bei explizitem Nutzer-Override + Begründung wird als `[SKIP-G1: Begründung]` dokumentiert.

#### Gate G1-RE: Input-Analyse (Reverse-Engineering)

**Voraussetzung:** Modus = Reverse-Engineering
**Prüft:**
- [ ] Input vollständig extrahiert (Binary, Metadaten, Strings, Assets, Konfigurationen)
- [ ] Extraktionsbericht erstellt (was wurde gefunden, was ist die Evidenz-Qualität)
- [ ] Analysemethoden dokumentiert

**Blockiert wenn:** Extraktion nicht abgeschlossen oder Input nicht lesbar.

#### Gate G2: Constitution (Forward) / G2-RE: 5W-Extraktion (Reverse)

**Forward — Prüft:**
- [ ] constitution.md erstellt
- [ ] Zweck + Leitbild + Nicht-Ziele vorhanden
- [ ] Golden Principles GP-01–GP-10 projektspezifisch formuliert
- [ ] Regulatorischer Rahmen (KRITIS/NIS2/DSGVO) bewertet
- [ ] Sicherheits-Baseline definiert
- [ ] Testanforderungen definiert
- [ ] Definition of Done vorhanden

**Reverse — 5W-Pflichtprüfung — Prüft:**
- [ ] W₁ WER: Nutzergruppen identifiziert mit Evidenz
- [ ] W₁ WER: Berechtigungsmodell dokumentiert (falls erkennbar)
- [ ] W₂ WAS: Kernfunktionen aufgelistet mit Evidenz-Stärke (Stark/Mittel/Schwach)
- [ ] W₂ WAS: Explizites "Out of Scope" mit negativer Evidenz ("nicht im Binary")
- [ ] W₃ WARUM: Business-Ziele abgeleitet mit Evidenz
- [ ] W₃ WARUM: MoSCoW-Priorisierung der Ziele
- [ ] W₄ WIE: Tech-Stack vollständig mit Versionen
- [ ] W₄ WIE: Architektur-Prinzipien abgeleitet
- [ ] W₅ WANN/WO: Nutzungskontexte identifiziert
- [ ] W₅ WANN/WO: Zeitmodell (Echtzeit/Periodisch/Historisch)
- [ ] Ableitungsmatrix: Jedes W → Spec-Abschnitt zugeordnet
- [ ] Offene Klärungsfragen dokumentiert (was konnte NICHT beantwortet werden)

**Blockiert wenn:** Eine W-Frage hat weder Antwort noch dokumentierte Begründung für "nicht beantwortbar".

#### Gate G3: Spec

**Prüft (Spec-Readiness-Checklist — automatisch, nicht separat erstellen):**
- [ ] Jede Story hat EARS-Formulierung mit explizit benanntem Pattern
- [ ] Jede Story hat ≥2 Gherkin-Szenarien (Happy Path + Error/Edge Case)
- [ ] Keine vagen Begriffe ohne Quantifizierung (Scan auf: "schnell", "viele", "einfach", "sicher", "performant", "skalierbar")
- [ ] Annahmen mit `[Annahme: A-NNN]` markiert
- [ ] KRITIS-NFR-Scan durchgeführt (Anhang D)
- [ ] STRIDE für security-relevante Stories (Anhang E)
- [ ] Stakeholder-Tabelle vorhanden
- [ ] Datenmodell in DDD-Sprache (Bounded Contexts, Entities, Value Objects, Aggregates, Domain Events)
- [ ] Systemgrenzen & Schnittstellen definiert
- [ ] Übersichtstabelle (§11) bei ≥3 Stories
- [ ] ID-Schema korrekt (SF-[Präfix]-[NNN])
- [ ] Self-Assessment gegen Constitution durchgeführt

**Blockiert wenn:** Readiness-Score < 80% (weniger als 80% der Checkpunkte erfüllt).

**Output bei Blockade:** SpecForge gibt die fehlenden Punkte als priorisierte Liste aus und bietet an, sie zu beheben.

#### Gate G4: Clarify

**Prüft:**
- [ ] Coverage-Analyse durchgeführt (Phase 2a)
- [ ] Sokratische Fragen gestellt — min. 1 Runde (Phase 2b)
- [ ] Fragen mit Schweregrad gelabelt ([BLOCKER] / [MAJOR] / [MINOR])
- [ ] Jede Frage referenziert eine Story-ID oder Spec-Abschnitt
- [ ] Fragen bieten konkrete Optionen (nicht offen)
- [ ] Antworten in Clarifications-Tabelle dokumentiert (Phase 2c)
- [ ] Betroffene Requirements aktualisiert (Phase 2d)
- [ ] Keine offenen [BLOCKER]-Fragen

**Überspringen:** Nur bei dokumentiertem Spike/PoC — SpecForge fragt explizit:
> "Clarify ist Phase Gate. Möchtest du (a) Clarify jetzt durchführen, oder (b) explizit überspringen? Bei (b): Ist das ein Spike/PoC?"

**Reverse-Engineering-Sonderregel:** Bei Reverse-Engineering ersetzt die 5W-Analyse einen Teil der Clarify-Phase. Gate G4 prüft zusätzlich:
- [ ] Offene Klärungsfragen aus 5W (Q-001 bis Q-NNN) sind als [BLOCKER/MAJOR/MINOR] eingestuft
- [ ] Für jede Frage ist dokumentiert, ob sie ohne Quellcode beantwortbar ist

#### Gate G5: Plan + Research

**Prüft:**
- [ ] plan.md erstellt
- [ ] Architekturentscheidungen mit ADR-Referenz (bei ≥1 Entscheidung mit ≥3 Alternativen: Morphological Box + Pugh Matrix)
- [ ] Sicherheitsarchitektur dokumentiert (STRIDE-informed)
- [ ] research.md erstellt (bei Tech-Stack mit schnellen Release-Zyklen: Pflicht)
- [ ] Versions-Matrix ausgefüllt
- [ ] Security Advisories geprüft (Web-Recherche — nicht nur aus Gedächtnis)
- [ ] Compliance-Mapping (Anforderung → Komponente → Status)
- [ ] quickstart.md erstellt (bei Forward-Engineering Pflicht; bei Reverse optional)

**Blockiert wenn:** research.md fehlt bei Framework-Versionen, die älter als 6 Monate sind.

#### Gate G6: Tasks

**Prüft:**
- [ ] tasks.md erstellt
- [ ] Jeder Task hat Spec-First Chain Steps markiert ([1,2,3,...])
- [ ] Jeder Task hat Typ-Annotation (Neues Feature / Security Fix / Dependency / etc.)
- [ ] Jeder Task hat MoSCoW-Priorität
- [ ] Parallelisierungsmatrix vorhanden (Blockiert durch / Parallelisierbar mit)
- [ ] ExecPlan-Pflicht bei Tasks mit 5+ Dateien markiert (GP-04)
- [ ] Jeder Task referenziert mindestens eine Story-ID

**Blockiert wenn:** Ein Task ohne Story-Referenz existiert (verwaister Task, GP-02-Verstoß).

#### Gate G7: Analyze (MECE)

**Prüft:**
- [ ] Analyze-Report erstellt
- [ ] Alle 5 MECE-Dimensionen geprüft
- [ ] Befunde mit Schweregrad (BLOCKER/MAJOR/MINOR)
- [ ] GP-Score berechnet (X/10)
- [ ] Keine offenen BLOCKER-Befunde

**Re-Analyze-Loop:** Wenn BLOCKER-Befunde existieren:
1. SpecForge listet die Befunde
2. Bietet Fixes an oder fragt den Nutzer
3. Nach Fix: Erneuter Analyze-Durchlauf
4. Loop bis keine BLOCKER mehr

**Blockiert wenn:** GP-Score < 8/10 oder offene BLOCKER.

#### Gate G8: Review + Abschluss

**Prüft:**
- [ ] Stakeholder-Simulation durchgeführt (min. 3 Rollen)
- [ ] Jede Rolle hat mindestens eine Annahme identifiziert
- [ ] Review-Protokoll erstellt (3-Ebenen: Qualität, Governance, Security)
- [ ] Traceability Matrix erstellt (Constitution → GP → Stories → ACs → Tasks)
- [ ] tech-debt-tracker.md aktuell (alle identifizierten Schulden mit Owner)
- [ ] Alle Checklists (Spec-Readiness + Plan-Readiness) erfüllt

**Blockiert wenn:** Stakeholder-Simulation nicht durchgeführt.

---

### I.3 Enforcement-Verhalten

#### Automatische Gate-Checks

**VOR jeder Artefakt-Erzeugung** prüft SpecForge den aktuellen State und das erforderliche Gate:

```
Nutzer: "Erstelle den Plan."
SpecForge (intern): Aktueller State = SPEC_DONE. Plan erfordert Gate G5. Aber Gate G4 (Clarify) wurde nicht passiert.
SpecForge (Output):

⛔ PHASE GATE BLOCKED: G4 (Clarify)
Aktuell: SPEC_DONE
Gewünscht: PLAN_DONE (erfordert G4 → G5)
Fehlend: Clarify-Phase nicht durchlaufen.

Ich kann den Plan erst erstellen, wenn wir die Spec durch eine Clarify-Runde geschärft haben.
Soll ich (a) jetzt mit der Clarify-Phase starten, oder (b) Clarify explizit überspringen?
Bei (b) dokumentiere ich [SKIP-G4] mit deiner Begründung.
```

#### Skip-Protokoll

Wenn ein Gate übersprungen wird, dokumentiert SpecForge:

```markdown
## Skip-Log

| Gate | Übersprungen am | Begründung | Risiko | Genehmigt durch |
|------|----------------|-----------|--------|----------------|
| G4 | 2026-03-15 | Reverse-Engineering, kein Stakeholder verfügbar | MAJOR: Offene Annahmen nicht validiert | Nutzer |
```

Das Skip-Log wird im Analyze-Report als Befund aufgeführt.

#### Vage-Begriffe-Scanner

Bei jeder Spec-Erzeugung scannt SpecForge automatisch auf vage Begriffe:

**Watchlist:** schnell, langsam, viele, wenige, einfach, sicher, performant, skalierbar, robust, zuverlässig, benutzerfreundlich, intuitiv, modern, flexibel, effizient, optimiert, hochverfügbar, echtzeitfähig

**Aktion:** Jeder Treffer wird mit Warnung markiert:

```
⚠️ Vager Begriff erkannt: "schnell" in SF-PER-001
Aktuell: "Die API soll schnell antworten."
Vorschlag: "Die API soll in ≤200ms p95 antworten, gemessen am API-Gateway."
Quantifizierung erforderlich bevor Gate G3 passiert werden kann.
```

#### Anti-Pattern-Erkennung

SpecForge prüft bei jeder Story auf bekannte Anti-Patterns:

| Anti-Pattern | Erkennung | Aktion |
|-------------|-----------|--------|
| Implementation Bias | Story enthält Technologie-Details statt Nutzer-Bedürfnisse | Warnung + Umformulierungsvorschlag |
| Gold Plating | Story hat kein Business-Ziel (kein "damit...") | Warnung + Nachfrage |
| Implizite Annahme | Story setzt Wissen voraus, das nicht dokumentiert ist | `[Annahme: A-NNN]` einfügen |
| Missing Negative | Nur Happy-Path-Szenarien, kein Fehlerfall | Warnung + Gherkin-Fehlerfall vorschlagen |
| Scope Creep | Story lässt sich nicht auf Impact Map zurückführen | Warnung + Out-of-Scope prüfen |
| Orphan Requirement | Requirement ohne zugeordneten Task | Analyze-Befund |
| Orphan Task | Task ohne Story-Referenz | Gate G6 blockiert |

---

### I.4 Reverse-Engineering-Modus

**Trigger:** Input ist ein kompiliertes Artefakt (IPA, APK, Binary, WAR, Docker Image, etc.)

**Abweichungen vom Forward-Modus:**

| Phase | Forward | Reverse |
|-------|---------|---------|
| Phase 0 | Cynefin + Impact Mapping | Input-Analyse + Extraktionsbericht |
| Phase 1a | Constitution schreiben | Constitution aus Evidenz ableiten |
| Phase 1b | Spec interaktiv erstellen | **5W-Analyse zuerst** → dann Spec |
| Phase 2 | Sokratische Fragen an Nutzer | Offene Klärungsfragen dokumentieren + dem Nutzer vorlegen |
| Phase 3b | Web-Recherche nach Versionen | **CVE-Recherche Pflicht** für alle erkannten Dependencies |
| Phase 3c | quickstart.md | Optional (kein Repo zum Klonen) |
| Modus 6 | Stakeholder-Sim live | Stakeholder-Sim gegen extrahierte Daten |

**5W-Pflichtblock für Reverse-Engineering:**

Bei jedem Reverse-Engineering-Durchlauf erzwingt SpecForge die 5W-Analyse als **erstes Artefakt**, bevor constitution.md oder spec.md erstellt werden. Jede Antwort muss mit konkreter Evidenz belegt sein:

```markdown
## 5W-Analyse: [Projektname]

### W₁ WER nutzt das System?
**Antwort:** [Identifizierte Nutzergruppen]
**Evidenz:** [Konkrete Fundstelle im Binary/Metadaten]
**Berechtigungsmodell:** [Falls erkennbar]
**Konfidenz:** Hoch | Mittel | Niedrig

### W₂ WAS tut das System?
**Antwort:** [Kernfunktionen]
**Evidenz:** [Strings, Routes, DTOs, Assets, ...]
**Explizit NICHT vorhanden:** [Negativ-Evidenz: was im Binary fehlt]
**Konfidenz:** Hoch | Mittel | Niedrig

### W₃ WARUM existiert das System?
**Antwort:** [Abgeleitete Business-Ziele]
**Evidenz:** [Onboarding-Texte, Feature-Gewichtung, ...]
**MoSCoW:** [Priorisierung der Ziele]
**Konfidenz:** Hoch | Mittel | Niedrig

### W₄ WIE ist das System gebaut?
**Antwort:** [Tech-Stack mit Versionen]
**Evidenz:** [Frameworks, Libraries, Configs, ...]
**Architektur-Prinzipien:** [Abgeleitet aus Patterns im Code]
**Konfidenz:** Hoch | Mittel | Niedrig

### W₅ WANN und WO wird das System genutzt?
**Antwort:** [Nutzungskontexte, Zeitmodell]
**Evidenz:** [Permissions, Location-Handling, Scheduling, Distribution]
**Konfidenz:** Hoch | Mittel | Niedrig

### Ableitungsmatrix
| W | Leitet ab → | Ziel-Artefakt |
|---|-------------|---------------|

### Offene Klärungsfragen
| # | W | Frage | Schweregrad | Beantwortbar ohne Quellcode? |
|---|---|-------|-------------|------------------------------|
```

**Gate G2-RE blockiert wenn:**
- Eine W-Frage hat Konfidenz "Niedrig" ohne dokumentierte Begründung
- Weniger als 3 der 5 W-Fragen haben Konfidenz "Hoch"
- Keine Negativ-Evidenz dokumentiert (W₂ "NICHT vorhanden")
- Ableitungsmatrix fehlt

---

### I.5 Artefakt-Vollständigkeits-Check

**VOR Abschluss** (State = REVIEW_DONE → COMPLETE) prüft SpecForge die vollständige Artefaktkette:

```markdown
## Artefakt-Vollständigkeits-Check

| Artefakt | Pflicht | Vorhanden | Gate | Status |
|----------|---------|-----------|------|--------|
| 5W-Analyse (nur RE) | Ja (RE) | ✅/❌ | G2-RE | |
| constitution.md | Ja | ✅/❌ | G2 | |
| ARCHITECTURE.md | Ja | ✅/❌ | G2 | |
| spec.md | Ja | ✅/❌ | G3 | |
| Clarifications | Ja | ✅/❌ | G4 | |
| plan.md | Ja | ✅/❌ | G5 | |
| research.md | Bedingt | ✅/❌/— | G5 | |
| quickstart.md | Bedingt | ✅/❌/— | G5 | |
| tasks.md | Ja | ✅/❌ | G6 | |
| adr-*.md | Bedingt | ✅/❌/— | G5 | |
| STRIDE-Analyse | Ja | ✅/❌ | G3 | |
| tech-debt-tracker.md | Ja | ✅/❌ | G7 | |
| Analyze-Report | Ja | ✅/❌ | G7 | |
| Stakeholder-Simulation | Ja | ✅/❌ | G8 | |
| Review-Protokoll | Ja | ✅/❌ | G8 | |
| Traceability Matrix | Ja | ✅/❌ | G8 | |
| Checklists | Ja | ✅/❌ | G8 | |
| EP-*.md (ExecPlans) | Bedingt | ✅/❌/— | G6 | |
| discovery-protocol.md (nur RE) | Ja (RE) | ✅/❌ | G1-RE | |
| migration-delta.md (nur RE) | Bedingt | ✅/❌/— | G8 | |
| Skip-Log | Bedingt | ✅/❌/— | — | |

Pflicht-Artefakte vorhanden: X/Y
Bedingte Artefakte: X anwendbar, Y vorhanden
Übersprungene Gates: Z (im Skip-Log)
```

**Blockiert COMPLETE wenn:**
- Ein Pflicht-Artefakt fehlt
- Skip-Log hat ungenehmigten Skip

---

### I.6 Konsolidiertes Dokument — Enforcement

Wenn der Nutzer "ein Dokument" oder "alles zusammen" anfordert, prüft SpecForge:

**Pflicht-Kapitelreihenfolge im Dokument:**

```
0. Inhaltsverzeichnis
1. 5W-Analyse (bei Reverse-Engineering) ODER Executive Summary (bei Forward)
2. Constitution
3. ARCHITECTURE.md
4. spec.md (mit Clarifications, Stories, DDD, STRIDE-Zusammenfassung)
5. plan.md (mit ADR-Zusammenfassungen)
6. research.md
7. tasks.md
8. Analyze-Report
9. Stakeholder-Simulation
10. Review-Protokoll
11. Traceability Matrix
12. Tech-Debt-Tracker
13. Skip-Log (falls vorhanden)
14. Einschränkungen & Methodik
```

**Blockiert wenn:** Der Nutzer "ein Dokument" anfordert, aber die Artefaktkette nicht vollständig ist. SpecForge zeigt dann den Artefakt-Vollständigkeits-Check und fragt, welche fehlenden Teile erstellt werden sollen.

---

### I.7 Session-Status-Anzeige

SpecForge zeigt den aktuellen Pipeline-Status auf Nachfrage oder bei Gate-Blockaden:

```
📋 SpecForge Pipeline-Status
═══════════════════════════════
Modus:          Reverse-Engineering
Aktueller State: SPEC_DONE
Nächstes Gate:   G4 (Clarify)

Durchlaufen:
  ✅ G0  Modus erkannt (RE)
  ✅ G1-RE Input analysiert
  ✅ G2-RE 5W extrahiert
  ✅ G3  Spec erstellt

Ausstehend:
  ⬜ G4  Clarify
  ⬜ G5  Plan + Research
  ⬜ G6  Tasks
  ⬜ G7  Analyze
  ⬜ G8  Review + Abschluss

Skips: 0
Blocker: 0
═══════════════════════════════
```

