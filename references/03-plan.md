# Modus 3: Plan & Tasks — Von Spec zu Backlog

**Trigger:** spec.md existiert und Clarify ist abgeschlossen (oder bewusst übersprungen).

---

## Profil-Steuerung

- **KRITIS:** Research Pflicht bei jeder Tech-Entscheidung; ExecPlan-Enforcement strikt (GP-04); ADRs Pflicht (GP-03); Explore bei Komplexität empfohlen
- **Standard:** Research empfohlen bei schnelllebigen Stacks; ExecPlan bei 5+ Dateien; ADRs für modulübergreifende Entscheidungen
- **Startup:** Research optional; ExecPlans empfohlen; ADRs bei Bedarf; Speed vor Evaluation

## Brownfield vs. Greenfield

| Aspekt | Greenfield | Brownfield |
|--------|-----------|------------|
| Explore-Phase | Empfohlen bei Komplexität | Nur bei grundlegender Architektur-Änderung |
| Architektur-Varianten | 2–3 Varianten bewerten | Bestehende Architektur als Referenz in Pugh Matrix |
| research.md | Neuer Stack vollständig recherchieren | Delta-Research: Was ändert sich? |
| ARCHITECTURE.md | Neu erzeugen | Aktualisieren (Codemap, Invarianten) |
| Migration | Nicht relevant | migration-delta.md erzeugen (Ist → Soll) |

## Phase 3-pre: Explore — Parallele Architektur-Varianten (optional)

**Wann einsetzen:**
- Cynefin-Einordnung "Komplex" oder "Kompliziert" mit 3+ realistischen Architektur-Optionen
- Stakeholder-Konflikt über technische Richtung
- Greenfield-Projekt ohne Vorgänger-Architektur

**Wann überspringen:**
- Klar/Trivial — eine offensichtliche Lösung
- Brownfield mit klarer Architektur — bestehende Architektur gibt Richtung vor (aber: ADR für "Architektur beibehalten" dokumentieren)
- Startup-Profil — Speed vor Evaluation

**Ablauf:**

1. **Varianten identifizieren** — Aus spec.md die architekturrelevanten Entscheidungsdimensionen extrahieren (Runtime, Persistenz, Kommunikationsmuster, Hosting). 2–3 realistische Varianten skizzieren.

2. **Skizzen erstellen** — Pro Variante eine kompakte Architektur-Skizze:
   - Komponentendiagramm (ASCII oder Beschreibung)
   - Stärken/Schwächen in Bezug auf die NFRs aus spec.md
   - Bekannte Risiken und offene Fragen
   - Grobe Aufwandsschätzung (T-Shirt-Sizing: S/M/L/XL)

3. **Bewerten** — Morphological Box + Pugh Matrix anwenden:
   - Referenz = einfachste Variante oder Status Quo
   - Kriterien = NFRs aus spec.md + aktive Golden Principles
   - Bewertung: Besser (+) / Gleich (S) / Schlechter (−)

4. **Entscheiden** — Gewählte Variante in ADR dokumentieren. Verworfene Varianten mit Begründung im Alternativen-Abschnitt des ADR festhalten.

**Erzeugt:** `specs/decisions/adr-NNN-architekturwahl.md` mit Explore-Ergebnissen

→ Direkt in Phase 3a (Plan) überleiten mit gewählter Variante als Grundlage.

---

## Phase 3a: Plan

Erzeugt `plan.md` mit:
- Technische Architekturentscheidungen → ADR in `specs/decisions/`
- **Technisches Datenmodell** (WIE — abgeleitet vom fachlichen Modell in spec.md):
  - Persistenz-Strategie (RDBMS, Document Store, Event Store)
  - Datenbankschema, OR-Mapping, Indizes, Partitionierung
  - Aggregate-Root-Patterns, Repository-Schnitte
  - Event-Serialisierung und -Versionierung (falls Event-Driven)
- Sicherheitsarchitektur (STRIDE-informed)
- Integrationen und Schnittstellen
- Compliance-Mapping (NIS2-Artikel ↔ Komponente, laut Profil)

### Technologieentscheidungen

Bei 3+ Alternativen: **Morphological Box + Pugh Matrix** anwenden.

**Morphological Box** — Dimensionen = Architektur-Parameter (Runtime, DB, Auth, Hosting). Pro Parameter 3–5 Varianten. Constraint-Filterung eliminiert nicht-kompatible Kombinationen.

**Pugh Matrix** — Referenz = bestehende Lösung oder einfachste Option. Kriterien = NFRs + Golden Principles. Bewertung: Besser (+), Gleich (S), Schlechter (−). Nettowert entscheidet.

Ergebnis fließt in ADR ein (Alternativen-Abschnitt dokumentiert Pugh-Bewertung).

---

## Phase 3b: Research — Technische Tiefenrecherche

**Profil-Steuerung:**
- KRITIS: Pflicht bei jeder Tech-Entscheidung
- Standard: Empfohlen bei schnelllebigen Tech-Stacks
- Startup: Optional, bei Bedarf

**Trigger für Research:**
- Tech-Stack mit schnellen Release-Zyklen
- Externe APIs mit unbekannten Versionen/Breaking Changes
- KRITIS-/NIS2-Compliance erfordert spezifische Versionsstände

**Ablauf:**
1. Research-Scope identifizieren — nummerierte Research-Fragen aus Plan
2. Gezielte Web-Recherche — offizielle Docs, Changelogs, CVEs, Zertifizierungen
3. `research.md` erzeugen:

```markdown
# Research — [Feature-Name]
**Spec-Referenz:** specs/use-cases/<feature-id>/spec.md
**Stand:** [Datum]

## Research-Fragen
### RQ-001: [Frage]
**Kontext:** [Warum relevant] | **Ergebnis:** [Mit Quellen] | **Auswirkung auf Plan:** [Anpassung]

## Versions-Matrix
| Komponente | Gewählte Version | Aktuelle Stable | EOL-Datum | Kompatibilität |

## Security Advisories
| Komponente | CVE/Advisory | Schweregrad | Mitigation | Status |
```

4. Plan mit Research-Ergebnissen aktualisieren

---

## Phase 3c: Quickstart — Entwickler-Schnelleinstieg

Erzeugt `quickstart.md` mit:
- Voraussetzungen (Tools, Versionen, Installation)
- Projekt-Setup (Schritt-für-Schritt)
- Architektur-Kurzfassung (max. 10 Zeilen + Diagramm)
- Wichtigste Entscheidungen (ADR-Referenzen)
- Erster Task (Verweis auf tasks.md)
- Konventionen (Branch, Commit, Spec-First Chain)
- Häufige Fehler (GP-Verstöße vermeiden)

---

## Phase 3d: Tasks mit Spec-First Chain

Lade `references/conventions/spec-first-chain.md` für die 8 Pflichtschritte.

Erzeugt `tasks.md` — jeder Task folgt der Spec-First Chain:

```
1. Update Spec → 2. Update Schema → 3. Update Fixture → 4. Update Provider
→ 5. Update Consumer → 6. Run Contract Tests → 7. Log Breaking Changes
→ 8. Update ARCHITECTURE.md
```

Nicht jeder Task durchläuft alle 8 Schritte — markieren, welche relevant sind.

### Task-Regeln (Enforcement)
- Parallelisierbare Tasks mit `[P]` markieren
- Jeder Task hat Gherkin ACs (≥2 Szenarien, AP-06)
- Jeder Task hat Spec-Referenz (GP-02, AP-05 Scope Creep)
- NFR-Tasks explizit ausweisen mit Kategorie (AVA/SEC/AUD/PER/DAT/OPS)
- **GP-04: Tasks mit 5+ Dateien → ExecPlan-Pflicht (EP-*.md)** — Verstoß = MAJOR
  - ExecPlan enthält: Änderungsreihenfolge, Abhängigkeiten, Rollback-Strategie, Checkpoint
  - ExecPlan-Pfad: `plans/active/EP-*.md`
- Definition-of-Ready-Prüfung pro Task:
  - Spec-Referenz vorhanden? (GP-02)
  - Gherkin ACs vorhanden? (≥2)
  - Spec-First Steps markiert?
  - ExecPlan vorhanden falls 5+ Dateien? (GP-04)

---

## Phase Gate: Tasks → Analyze

Empfehlung: IMMER Analyze nach Tasks ausführen.

---

## Phase Gate G3: Plan+Tasks → Analyze (automatisch prüfen)

```
── Gate G3: Plan+Tasks → Analyze ──────────
[ ] plan.md erzeugt
[ ] tasks.md erzeugt mit Spec-First Steps pro Task
[ ] research.md vorhanden und aktuell (Pflicht bei KRITIS)
[ ] quickstart.md vorhanden
[ ] ADRs für alle modulübergreifenden Entscheidungen (GP-03)
[ ] ExecPlans für Tasks mit 5+ Dateien (GP-04)
── Ergebnis: PASS | FAIL (Befunde) ─────────
```

---

## Stringenz-Regeln (Enforcement)

| Regel | Enforcement | Schweregrad |
|-------|-----------|------------|
| Vage Begriffe in plan.md/tasks.md | Jedes Artefakt gegen Blocklist: "schnell", "viele", "einfach", "skalierbar", "sicher", "zuverlässig" → AP-04 | BLOCKER |
| Fragen-Budget | Max. 3 Fragen pro Runde an den Nutzer | n.a. |
| ExecPlan-Pflicht (GP-04) | Automatisch bei Tasks mit 5+ Dateien | MAJOR |
| ADR-Pflicht (GP-03) | Automatisch bei modulübergreifenden Entscheidungen | MAJOR (KRITIS: BLOCKER) |
| Anti-Pattern-Prüfung | AP-01–AP-08 bei jedem Task | Schweregrad laut AP-Tabelle |
| Artefakte als Dateien | plan.md, tasks.md, research.md als Dateien, nicht inline | MAJOR |
| Schweregrad-Zuweisung | Deterministisch nach enforcement-engine.md | n.a. |

## Erweiterbarkeit

| Erweiterungspunkt | Wie | Wo |
|-------------------|-----|-----|
| Neue Task-Typen | Relevanz-Matrix in spec-first-chain.md erweitern | Convention |
| Branchenspezifische Plan-Checklisten | `references/custom/@branche-compliance/plan-checks.md` | Custom Extension |
| Neue Anti-Patterns | AP-08+ in `references/custom/anti-patterns-custom.md` | Custom Extension |
| Custom Research-Templates | `references/custom/research-template-custom.md` | Custom Extension |
| Neue Architektur-Bewertungsmethoden | `references/custom/architecture-methods.md` | Custom Extension |

## Fehlerbehandlung

| Situation | Reaktion |
|-----------|---------|
| spec.md fehlt | → Fehlermeldung: "spec.md nicht gefunden — Clarify (Modus 2) oder Specify (Modus 1) zuerst ausführen" |
| specforge.json fehlt | → Standard-Profil anwenden, Hinweis ausgeben |
| Keine ADR-Entscheidungen identifizierbar | → Hinweis: "Keine modulübergreifenden Entscheidungen erkannt — ADR optional" |
| Task mit 5+ Dateien ohne ExecPlan | → MAJOR-Finding, ExecPlan-Erstellung anbieten |
| Research-Quellen nicht erreichbar | → Befund dokumentieren, Konfidenz auf "Niedrig" setzen |
| Profil-Wechsel mid-session | → Plan-Scope anpassen (Research Pflicht/Optional, ADR-Tiefe) |
| Brownfield ohne ARCHITECTURE.md | → ARCHITECTURE.md aus Code ableiten (Discover-Aspekte) |
| Mixed-Language Input | → Sprachverhalten gemäß Orchestrator |
| Übermäßig viele Tasks (>20) | → In Epics aufteilen, je Epic eigene tasks.md |

## GP-Mapping

| GP | Relevanz in Modus 3 |
|----|---------------------|
| GP-02 | Jeder Task hat Spec-Referenz |
| GP-03 | ADRs für modulübergreifende Entscheidungen |
| GP-04 | ExecPlan bei Tasks mit 5+ Dateien |
| GP-05 | Invarianten in ARCHITECTURE.md |
| GP-07 | Artefakte in Convention-Verzeichnissen |
| GP-09 | Consumer/Provider-Richtung in Plan beachten |
| GP-10 | Tech-Debt aus Plan-Phase → tech-debt-tracker.md |

## Erzeugte Artefakte

| Artefakt | Pfad |
|----------|------|
| plan.md | specs/use-cases/\<feature\>/ |
| research.md | specs/use-cases/\<feature\>/ |
| quickstart.md | specs/use-cases/\<feature\>/ |
| tasks.md | specs/use-cases/\<feature\>/ |
| adr-*.md | specs/decisions/ |
| EP-*.md | plans/active/ (bei GP-04) |
| migration-delta.md | specs/use-cases/\<feature\>/ (bei Brownfield) |
