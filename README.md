# SpecForge — Specs schmieden, nicht schreiben

[![CI](https://github.com/GodModeAI2025/specforge-ai-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/GodModeAI2025/specforge-ai-skill/actions/workflows/ci.yml)

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

- **Anti-Vibe-Coding (RPI Framework)** — Striktes Enforcement des Research -> Plan -> Implement Workflows nach Dexter Horthy (HumanLayer):
  - *Isolated Research:* Ist-Analyse ohne Feature-Ticket-Bias (verhindert Halluzinationen)
  - *Outline-Alignment:* Zwingende High-Level Outline vor der Detaillierungsphase
  - *Plan Fidelity Check (Anti-Drift):* Code-Änderungen werden strikt gegen die `plan.md` geprüft. Ungeplante Änderungen erzeugen einen F3-Befund.
  - *Prompt Diet:* Phasen werden strikt sequenziell orchestriert (Context Overflow Prävention)
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

Der Skill ist ein Ordner. Es gibt zwei Wege, an ihn zu kommen; ab dann sind die
drei Varianten gleich.

**Aus dem Release-Archiv:**

```bash
curl -L -O https://github.com/GodModeAI2025/specforge-ai-skill/releases/latest/download/specforge-skill.zip
unzip specforge-skill.zip
```

Das ergibt den Ordner `specforge/` mit `SKILL.md`, `references/`, `LICENSE`,
`TRADEMARK.md`, einer `VERSION` und einem README, das ohne das Repo auskommt.
Der Dateiname bleibt über Releases hinweg gleich, `releases/latest/download/`
zeigt also immer auf das aktuelle Paket. Der Link greift ab dem ersten
veröffentlichten Tag; solange keiner gesetzt ist, antwortet GitHub mit 404.
Gebaut wird das Archiv von `scripts/package-skill.py`, das auch lokal läuft.

**Aus dem Repository:** klonen und `SKILL.md` samt `references/` als Ordner
verwenden. Diesen Weg nimmt, wer am Skill selbst arbeitet.

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

SpecForge scannt die spec.md nach Lücken, vagen Begriffen und unbestätigten Annahmen. Fragen werden mit F-Stufe (F4 bis F1) priorisiert.

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

5-Dimensionen-Check: Spec↔Plan, Plan↔Tasks, Spec↔Tasks, GP-Compliance, Security/Compliance. Re-Analyze-Loop (max. 5 Iterationen) bis kein F4-Befund mehr offen ist.

### Modus 5: Checklist — Quality Gates

```
"Erstelle eine Spec-Readiness-Checklist."
"Erstelle eine DSGVO-Compliance-Checklist."
```

4 Checklist-Typen: Spec-Readiness (Typ A), Plan-Readiness (Typ B), Custom (Typ C), Domain (Typ D). Wiederverwendbare Prüflisten — "Unit Tests für Prosa".

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

### Modus 10: Derive — Testfälle aus Acceptance Criteria

```
"Leite Testfälle aus den Gherkin-Szenarien ab."
"Erstelle die Testabdeckungsmatrix für dieses Feature."
```

Aus jedem Gherkin-Szenario wird ein Testfall `[Story-ID]-TC[NNN]` mit Vorbedingung, Aktion, erwartetem Ergebnis und Testdaten. Dazu die Testabdeckungsmatrix und eine Traceability-Prüfung Story zu Testfall. 6 Testfall-Typen, Pflicht-Scope je Profil.

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

SpecForge ist als **Multi-File-Skill** aufgebaut: ein Orchestrator (`SKILL.md`) dispatcht zu 10 Fachmodulen und den Support-Dateien unter `references/`.

```
specforge/
├── SKILL.md                          Orchestrator: Dispatch, Gates, Pre-Flight
└── references/
    ├── 01-specify.md                 Modus 1: Specify
    ├── 02-clarify.md                 Modus 2: Clarify
    ├── 03-plan.md                    Modus 3: Plan & Tasks
    ├── 04-analyze.md                 Modus 4: Analyze
    ├── 05-checklist.md               Modus 5: Checklist
    ├── 06-stakeholder-sim.md         Modus 6: Stakeholder-Simulation
    ├── 07-review.md                  Modus 7: Review
    ├── 08-management.md              Modus 8: Management & Traceability
    ├── 09-discover.md                Modus 9: Discover
    ├── 10-derive.md                  Modus 10: Derive
    ├── checklists/
    │   ├── ears-syntax.md
    │   ├── golden-principles.md
    │   ├── kritis-nfr.md             41 Prüfpunkte, KRITIS/NIS2
    │   └── stride-guide.md
    ├── templates/
    │   ├── spec-template.md
    │   └── constitution-template.md
    ├── conventions/
    │   ├── folder-convention.md
    │   └── spec-first-chain.md
    ├── enforcement/
    │   └── enforcement-engine.md
    └── custom/
        ├── @dora/                    manifest.md + 58 Prüfpunkte
        └── @bait/                    manifest.md + 8 Prüfpunkte, Stub
```

**Skill-Payload:** Orchestrator plus 10 Fachmodule und die Support-Dateien unter `references/`. Die Zahl der Fachmodule und die Prüfpunktzahlen prüft die CI gegen den Verzeichnisbaum, siehe `scripts/check-docs-numbers.py`.

### Warum Multi-File?

- **Separation of Concerns** — Orchestrator bleibt kompakt, Module werden nur bei Bedarf geladen
- **Wartbarkeit** — einzelne Module unabhängig aktualisierbar
- **Erweiterbarkeit** — neue Modi, Checklisten oder Profile über `references/custom/` hinzufügbar
- **Audit-freundlich** — jede Datei unabhängig bewertbar und testbar
- **Context-Window-effizient** — Claude lädt Orchestrator plus benötigtes Modul, nicht den ganzen Payload

### Was die Fachmodule enthalten (Standard-Sektionen)

Die 10 Fachmodule folgen weitgehend derselben Struktur. Wo eine Sektion fehlt oder anders heißt, sagt es die Tabelle:

| Sektion | Beschreibung |
|---------|-------------|
| Profil-Steuerung | KRITIS/Standard/Startup-spezifisches Verhalten. Eigene Sektion in acht Modulen; `01-specify.md` behandelt die Profilwahl als Ablaufschritt, `02-clarify.md` unter „Wann Pflicht vs. Optional (profilabhängig)“ |
| Ablauf (deterministisch) | Nummerierte Phasen mit konkreten Schritten. Eigene Überschrift in fünf Modulen; `01-specify.md`, `02-clarify.md`, `03-plan.md` und `10-derive.md` gliedern direkt nach Phasen, `08-management.md` nach Funktionen |
| Output-Template | Markdown-Template für erzeugte Artefakte, in allen zehn Modulen vorhanden. Eigene Sektion „Output: …“ nur in `04-analyze.md`, `05-checklist.md`, `06-stakeholder-sim.md` und `07-review.md` |
| Stringenz-Regeln (Enforcement) | Tabellarische Regeln mit Schweregraden. Fehlt in `04-analyze.md` und `05-checklist.md` |
| Erweiterbarkeit | Custom-Extension-Punkte mit Pfaden. Fehlt in `04-analyze.md` und `05-checklist.md` |
| Fehlerbehandlung | Tabellarische Edge-Case-Behandlung, vier bis neun Fälle je nach Modul |
| GP-Mapping | Zuordnung relevanter Golden Principles. Fehlt in `01-specify.md`, `02-clarify.md` und `07-review.md` |
| Erzeugte Artefakte | Artefakt-Tabelle mit Pfaden. In `02-clarify.md` heißt die Sektion „Erzeugte/aktualisierte Artefakte“ |

### Orchestrator-Features (SKILL.md)

| Feature | Beschreibung |
|---------|-------------|
| Pre-Flight Checks | specforge.json laden, Profil-Resolution, Referenz-Verfügbarkeit |
| Dispatch-Tabelle | Modus → Modul-Mapping mit Trigger-Keywords |
| Profil-Resolution Cascade | CLI-Flag → specforge.json → Nutzer-Frage → Standard |
| Artefakt-Versionierung | `YYYY.MM.DD.N` im `version:`-Feld jedes erzeugten Artefakts |
| Session-Retrospektive | Automatische Zusammenfassung am Session-Ende |
| Erweiterbarkeit | 8 Built-in Extension Points (EARS, Profile, APs, GPs, Modi, ...) |
| Fehlerbehandlung | KRITISCH vs. OPTIONAL Referenzen mit spezifischem Verhalten |
| Audit Trail | Jede Enforcement-Entscheidung wird protokolliert |

---

## Grenzen

SpecForge ist Prompt-Text, kein Programm. Daraus folgen Grenzen, die keine Version wegräumt:

- **Die CI prüft den Skill, nicht die Ergebnisse.** Der Workflow in `.github/workflows/ci.yml` hält Referenzpfade, Frontmatter, Checklisten, Zahlen- und Versionsangaben konsistent und baut das Release-Paket bei jedem Lauf, damit ein kaputtes Paket vor dem Tag auffällt. Ob eine damit erzeugte Spezifikation fachlich taugt, beurteilt weiterhin ein Mensch.
- **Der Linter prüft Struktur, nicht Bedeutung.** `specforge check` erkennt fehlende EARS-Pattern, zu wenige Gherkin-Szenarien, Begriffe aus der Blocklist und Traceability-Lücken. Ob die EARS-Formulierung inhaltlich zum Pattern passt, ob ein NFR-Zielwert realistisch ist und ob die STRIDE-Bewertung zu Ende gedacht wurde, entscheidet weiterhin die Session oder ein Mensch. Der Linter meldet solche Punkte nicht als bestanden, sondern gar nicht.
- **F-Stufen sind Konvention, nicht Typprüfung.** Alle Module, Checklisten und Templates sprechen F0 bis F5; `scripts/check-severity-dialect.py` hält das in der CI fest. Ob Claude im Einzelfall die richtige Stufe vergibt, prüft das Skript nicht. Es prüft nur, dass keine zweite Skala danebensteht.
- **Keine Rechtsberatung.** Die KRITIS-, DORA- und BAIT-Checklisten sind Arbeitshilfen mit Verweis auf die Rechtsquelle. Sie ersetzen keine aufsichtsrechtliche Prüfung. `@bait` ist ausdrücklich ein Stub.
- **Das Paket ist ein Archiv aus Markdown.** Es installiert nichts und aktualisiert sich nicht. Ein kopierter Ordner erfährt nicht, dass es ein neueres Release gibt; der Abgleich läuft über die `VERSION` im Paket gegen die Releases im Repository.
- **Deutsch als Arbeitssprache.** Der Skill antwortet englisch auf englische Eingaben, die Referenzdateien und Checklisten bleiben deutsch.

---

## Roadmap

Offen, in dieser Reihenfolge:

1. **`@bait` vervollständigen:** vom Stub auf die Kapitel der BaFin-Rundschreiben 10/2017 (BA) und 10/2021 (BA).
2. **Weitere Regulierungen:** MaRisk, PCI-DSS 4.0, EnWG/IT-Sicherheitskatalog. Priorisierung in [CONTRIBUTING-CHECKLISTS.md](CONTRIBUTING-CHECKLISTS.md), Abschnitt 5.
3. **Composite Action ausliefern:** `.github/actions/specforge-check/` liegt im Repo, ist aber erst über ein Tag ab dem nächsten Release als `uses:` erreichbar. Bis dahin ruft ein fremdes Repository den Linter über einen eigenen Checkout auf.
4. **Englische Fassung** des Payloads.

---

## `specforge check`: Enforcement außerhalb der Session

Die Phase Gates greifen, solange Claude den Skill geladen hat. Für alles danach, also Pull
Request, Pipeline und Pre-Commit-Hook, liegt derselbe Regelsatz als Linter im Repo. Er braucht
Python 3.8 oder neuer und sonst nichts: keine Installation, keine Abhängigkeit.

```bash
python3 cli/specforge check specs/mein-feature/spec.md
```

Liegt eine `tasks.md` neben der Spec, prüft der Linter zusätzlich die Traceability. Fehlt sie,
läuft AP-07 nicht, und das steht in der Ausgabe: Gate G4 erscheint mit `SKIP` und nennt die beiden
Prüfpunkte, die niemand angesehen hat; im JSON stehen sie unter `skipped_checks`. Am Exit-Code
ändert das nichts, denn eine Spezifikation vor der Plan-Phase hat legitim noch keine `tasks.md`.
Eine gelöschte oder falsch abgelegte Datei soll aber nicht wie ein bestandener Lauf aussehen. Eine
`specforge.json` wird ab der Spec aufwärts gesucht und ausgewertet; `checks_config` überschreibt
die Default-F-Stufen, perspektivenabhängig wie in der Session.

Das Feld `extensions` nennt die Pakete unter `references/custom/`, die gelten sollen. Die
Schreibweise des Namens spielt keine Rolle (`@dora`, `@DORA`, `dora`), ein unbekannter Name ist ein
Aufrufproblem mit Exit 3 statt einer stillschweigend übergangenen Prüfung. Fehlt das Feld, gelten
alle vorhandenen Pakete; `[]` heißt ausdrücklich: keine Extension.

| Prüfpunkt | F-Stufe | Herkunft |
|-----------|---------|----------|
| Keine Story im erkannten Format (leere oder formatfremde Datei) | F4 | [docs/spec-format.md](docs/spec-format.md) |
| EARS-Pattern fehlt oder ist unbekannt | F4 | Gate G1 |
| Weniger als 2 Gherkin-Szenarien je Story | F4 | Gate G1 |
| Begriff aus der AP-04-Blocklist | F4 | Anti-Pattern AP-04 |
| SOPHIST-Trigger (`ggf.`, `zeitnah`, `etc.`) | F3 | Anti-Pattern AP-08 |
| Offene `[Annahme:]`- oder `[Offen:]`-Marker (nur mit `--nach-clarify`) | F3 | SKILL.md, globale Regel 11 |
| Task ohne Story-Referenz, Story ohne Task | F3 | Anti-Pattern AP-07 |
| ID folgt nicht `SF-{Präfix}-{NNN}` | F1 | Modus 1 und 7 |
| Doppelt vergebene Story-ID | F4 | Nachverfolgbarkeit |

Exit-Codes: `0` sauber, `1` mindestens ein F4-Befund, `2` ein F3-Befund ohne dokumentierte
Risiko-Akzeptanz, `3` Aufrufproblem. Eine Akzeptanz nach dem CONDITIONAL-Protokoll wird mit
`--risiko-akzeptanz datei.md` übergeben und hebt Exit 2 auf.

Der Linter liest die Datei als Protokoll, nicht als Fließtext. Ein Block hebt einen F3-Befund nur
auf, wenn seine Überschrift `## Risiko-Akzeptanz: <Betreff>` den Betreff des Befunds als eigenes
Wort nennt, alle Pflichtfelder aus
[enforcement-engine.md I.5](references/enforcement/enforcement-engine.md) ausgefüllt sind (Gate,
Prüfpunkt, F-Stufe, Risiko, Akzeptiert durch, Kompensation, Frist, Datum), die F-Stufe zum Befund
passt und die Frist als Datum `YYYY-MM-DD` in der Zukunft liegt. Was daran fehlt, steht als eigene
Zeile unter `Risiko-Akzeptanz:` in der Ausgabe. Eine Datei, die den Prüfpunkt nur erwähnt, ist
keine Freigabe.

Das gelesene Format ist in [docs/spec-format.md](docs/spec-format.md) beschrieben. Für fremde
Repositories liegt eine Composite Action unter `.github/actions/specforge-check/`, ein
Beispiel-Workflow in [docs/ci-example.yml](docs/ci-example.yml). Die Action ist erst ab dem
nächsten Release über ein Tag erreichbar; im aktuellen Release `v3.2.0` gibt es sie noch nicht.

### Golden Specs

Unter `evals/golden/` liegen acht vollständige Spezifikationen mit ihrem erwarteten Ergebnis.
Sie sind zugleich die ersten echten Specs im Repo, denn bis dahin gab es nur Templates, und der
Regressionstest für den Linter:

```bash
python3 evals/run_static.py
```

Das Paar aus Fall 03 und 06 zeigt, was die Perspektive im Linter bewirkt: identische `spec.md`,
zwei `specforge.json`, die sich nur in der Perspektive unterscheiden. Die als F4 markierte
DORA-Lücke ist für ein Finanzunternehmen richtig eingestuft und bleibt ein einzelner Befund; für
ein Beratungsprojekt sieht `@dora` F2 vor, und die zu harte Einstufung kommt als zweiter Befund
`nfr_severity` dazu. Fall 04 zeigt die dazu passende mildere Einstufung, die das Gate mit einem
Pflicht-Task vor Go-Live passiert. Das frühere, dreistufige Vokabular konnte diesen Unterschied
nicht abbilden; die Umstellung ist in
[docs/f-stufen-entscheidung.md](docs/f-stufen-entscheidung.md) begründet.

Was der Linter dabei prüft, ist die Selbsteinstufung des Autors gegen das Manifest der Extension.
Die F-Stufe einer Lücke liest er aus dem Marker `[NFR-Lücke F{n}: ...]`; eine Anforderung, die
niemand als fehlend markiert hat, bemerkt er nicht. Fall 08 hält diese Grenze fest. Details in
[evals/README.md](evals/README.md).

---

## Weiterführende Dokumente

| Dokument | Inhalt |
|----------|--------|
| [docs/skill-als-blaupause.md](docs/skill-als-blaupause.md) | SpecForge als Muster für eigene Claude-Skills: Frontmatter, Modi, Output-Templates, Qualitätsregeln |
| [docs/quellen-und-einfluesse.md](docs/quellen-und-einfluesse.md) | Herkunft der Methoden: Spec Kit, EARS, Gherkin, STRIDE, Cynefin und die übrigen |
| [docs/spec-format.md](docs/spec-format.md) | Das maschinenlesbare Format der `spec.md`: Story-Kopf, Pattern-Feld, Scenario-Blöcke, Marker |
| [docs/f-stufen-entscheidung.md](docs/f-stufen-entscheidung.md) | Warum F0 bis F5 der einzige Schweregrad-Dialekt ist und welcher Prüfpunkt sich dabei verschoben hat |
| [CONTRIBUTING-CHECKLISTS.md](CONTRIBUTING-CHECKLISTS.md) | Schema, Validierung und Kandidatenliste für eigene Regulierungs-Checklisten |

---

## Versionierung

SpecForge führt zwei Versionen, dazu den Tag, unter dem eine davon veröffentlicht wird:

| Gegenstand | Schema | Ort |
|------------|--------|-----|
| Skill-Version | `MAJOR.MINOR`, aktuell 3.2 | [CHANGELOG.md](CHANGELOG.md), Abschnitt Aktuelles Release; Badge auf der Landingpage |
| Release-Tag | `v{MAJOR}.{MINOR}.{PATCH}`, aktuell `v3.2.0` | derselbe Abschnitt; darauf reagiert `.github/workflows/release.yml` |
| Artefakt-Version | `YYYY.MM.DD.N`, N = laufende Nummer am selben Tag | `version:`-Feld im Header jeder erzeugten `spec.md`, `constitution.md` und `plan.md` |

Der Tag ist keine dritte Version, sondern die Skill-Version mit einer
Patch-Stelle. Sie zählt Korrekturen, die den Funktionsumfang nicht verändern.
Ein Funktionsschritt erhöht die Skill-Version, nicht die Patch-Stelle.

Gepflegt wird die Version an genau einer Stelle: in der Tabelle unter
"Aktuelles Release" in [CHANGELOG.md](CHANGELOG.md). Packaging-Skript und
Release-Workflow lesen sie dort, `scripts/check-version.py` prüft dieses README,
die Landingpage und den Artefaktnamen dagegen.

Verbindlich ist die Artefakt-Versionierung in [SKILL.md](SKILL.md), Abschnitt Versionierung. Die Templates unter `references/templates/` geben dasselbe Schema vor. Die früher genannte Schreibweise `v<YYMM>-green` war ein Audit-Status, keine Version, und wird nicht mehr verwendet.

Die Versionsgeschichte von 1.0 bis 3.2 steht in [CHANGELOG.md](CHANGELOG.md).

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
