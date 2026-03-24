# Modus 1: Specify — Interaktive Spezifikation

**Trigger:** Feature, Problem, Idee oder Prozess wird beschrieben.

---

## Phase 0: Komplexitätseinschätzung (optional, empfohlen bei neuen Produkten)

**Cynefin Framework** — Feature in Domäne einordnen:
- **Klar** → Specify direkt, Clarify optional → schlanker Durchlauf
- **Kompliziert** → Voller Workflow → Expertenwissen nötig
- **Komplex** → Spike/PoC zuerst, dann Specify → Emergente Anforderungen
- **Chaotisch** → Sofort handeln, nachträglich spezifizieren

**Impact Mapping** — 4 Ebenen als Eingangsprüfung:
1. Ziel (Warum?) — Geschäftsziel
2. Akteure (Wer?) — Wer erzeugt/verhindert Auswirkung
3. Auswirkungen (Wie?) — Verhaltensänderung der Akteure
4. Liefergegenstände (Was?) — Was müssen wir bauen

Wenn sich ein Feature nicht auf ein Geschäftsziel zurückführen lässt → Scope Creep erkannt.

---

## Phase 1a: Projekt-Setup (einmalig pro Projekt)

Wenn noch kein Projekt-Setup existiert:

1. **Profil wählen** — Nutzer fragen: "Ist das ein reguliertes Umfeld (KRITIS/NIS2), ein Standard-Projekt oder ein Startup/MVP?"
   - Antwort bestimmt Governance-Tiefe für den gesamten Workflow
2. **specforge.json erzeugen** — Maschinenlesbare Projektkonfiguration:
   - Profil (kritis/standard/startup), Tech-Stack, Regulierungen, aktive GPs, Pfade
   - Wird von allen Modi gelesen und steuert das Verhalten
3. **Folder Convention** vorschlagen → lade `references/conventions/folder-convention.md`
4. **constitution.md** erzeugen → lade `references/templates/constitution-template.md`
   - Projektprinzipien, Golden Principles (Scope laut Profil), regulatorischer Rahmen (eigenständig recherchieren), Sicherheits-Baseline, Definition of Done
5. **Lücken erfragen** — max. 3 Fragen pro Runde

---

## Phase 1b: Spec erstellen

Schritt-für-Schritt, jeder Schritt ist Pflicht:

0. **MCP-Kontext-Pre-Flight** (optional, empfohlen) — Vor der Kontexterfassung verfügbare Werkzeug-Quellen prüfen:

   | Quelle | Prüfung | Nutzen für Spec |
   |--------|---------|----------------|
   | **Design System** (Figma, Sketch) | MCP-Tool verfügbar? | UI-Komponenten, Patterns referenzieren; Konsistenz zu Design sicherstellen |
   | **Dokumentation** (Wiki, Confluence) | MCP-Tool verfügbar? | Fachliche Konzepte, Glossar, bestehende Anforderungen einbeziehen |
   | **Source Code** (GitHub, GitLab) | MCP-Tool verfügbar? | APIs, Datenmodelle, technische Constraints als Input |
   | **Projektmanagement** (Jira, Azure DevOps) | MCP-Tool verfügbar? | Bestehende Epics, Stories, Backlogs berücksichtigen |

   Ergebnis im Spec-Header dokumentieren:
   ```
   context_sources: [figma, github, confluence]   ← verfügbare Quellen
   context_sources: []                             ← keine MCP-Quellen verfügbar
   ```

   **Verhalten:** Wenn keine MCP-Tools verfügbar → kein Fehler, nur Skip mit Hinweis: "Keine externen Kontext-Quellen verfügbar — Spec basiert auf Session-Input und Web-Recherche." Wenn MCP-Tools verfügbar → aktiv nutzen, um Spec mit konkreten API-Signaturen, UI-Komponenten oder bestehenden Stories anzureichern.

1. **Kontexterfassung** — Max. 3 Fragen zu Domäne, Nutzergruppe, Systemgrenzen
2. **Web-Recherche** — Eigenständig regulatorische/domänenspezifische Anforderungen recherchieren
3. **Stakeholder-Simulation** — Mind. 3 Perspektiven durchspielen
   → Für ausführliche Simulation: lade `references/06-stakeholder-sim.md`
4. **Spec schreiben** — Im Spec-Kit-Format
   → Lade `references/templates/spec-template.md` für die Pflichtstruktur
5. **EARS-Formulierung** — Jedes Requirement in EARS-Syntax
   → Lade `references/checklists/ears-syntax.md` für Patterns und Beispiele
6. **NFR-Scan** — Gegen Checkliste, Scope laut Profil:
   - KRITIS: Alle 6 Kategorien Pflicht → lade `references/checklists/kritis-nfr.md`
   - Standard: SEC + PER + DAT empfohlen
   - Startup: Optional, bei Bedarf
   - Custom-Checklisten aus `references/custom/` zusätzlich laden falls vorhanden
7. **STRIDE-Analyse** — Security-Review, Scope laut Profil:
   - KRITIS: Alle 6 Kategorien für jede Story → lade `references/checklists/stride-guide.md`
   - Standard: Pflicht für SEC-Stories
   - Startup: Optional
8. **Self-Assessment** — Spec gegen Constitution + Golden Principles prüfen
9. **Validierung** — Nutzer einmal fragen: "Deckt das dein Szenario ab?"

---

## User Story Output-Format

```markdown
### [SF-XXX-NNN] [Titel]

**Typ**: User Story | Technical Story | Enabler
**Priorität**: Must | Should | Could | Won't (MoSCoW)
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
#### Offene Punkte
[Offen: Sollen auch Sprachbefehle unterstützt werden?]
[Offen: Welche Filterkriterien sind per Freitext erkennbar?]
#### GP-Compliance
```

**`[Offen: ...]`-Marker:** Wenn bei der Story-Erstellung nicht alle Informationen vorliegen, wird die Story trotzdem erzeugt — mit `[Offen: ...]`-Markern für fehlende Details. Dies verhindert, dass der Specify-Modus durch fehlende Einzelheiten blockiert wird. Marker werden bei Clarify (Modus 2) systematisch aufgelöst. Verbleibende `[Offen: ...]`-Marker nach Clarify erzeugen einen F3-Befund im Gate G2.

---

## Phase Gate G1: Specify → Clarify (automatisch prüfen)

SpecForge prüft diese Checkliste und gibt ein Pass/Fail-Ergebnis aus:

```
── Gate G1: Specify → Clarify ──────────────
[ ] EARS-Formulierung: X/Y Stories
[ ] Gherkin-Szenarien: ≥2 pro Story
[ ] Constitution: vorhanden und referenziert
[ ] specforge.json: vorhanden mit Profil
[ ] STRIDE: laut Profil geprüft
[ ] Keine offenen BLOCKER-Fragen
── Ergebnis: PASS | FAIL (Befunde) ─────────
```

**KRITIS-Profil:** Clarify ist Pflicht. Skip nur mit Skip-Protokoll.
**Standard-Profil:** Clarify empfohlen. Skip mit Einzeiler-Begründung.
**Startup-Profil:** Clarify optional. Empfehlung bei erkannten Lücken.

---

## Stringenz-Regeln (Enforcement)

| Regel | Enforcement | Schweregrad |
|-------|-----------|------------|
| Vage Begriffe aus Blocklist | Jede Story gegen Blocklist prüfen: "schnell", "viele", "einfach", "skalierbar", "sicher", "zuverlässig" → AP-04 | BLOCKER |
| EARS-Pflicht | Jede Story hat explizit benanntes EARS-Pattern | MAJOR |
| Gherkin-Minimum | ≥2 Szenarien pro Story (Happy Path + Fehlerfall) → AP-06 | MAJOR |
| Anti-Pattern-Prüfung | AP-01–AP-08 bei jeder Story-Erzeugung prüfen | Schweregrad laut AP-Tabelle |
| Offene-Punkte-Marker | Fehlende Details als `[Offen: ...]` markieren statt Story zu blockieren | F3 (nach Clarify) |
| Fragen-Budget | Max. 3 Fragen pro Runde an den Nutzer | n.a. |
| Artefakt-Erzeugung als Datei | spec.md, constitution.md, specforge.json als Dateien, nicht inline | MAJOR |
| Schweregrad-Zuweisung | Deterministisch nach enforcement-engine.md | n.a. |
| ID-Schema | SF-[Präfix]-[NNN] Format (z.B. SF-FUNC-001) | MINOR |

## Erweiterbarkeit

| Erweiterungspunkt | Wie | Wo |
|-------------------|-----|-----|
| Neue EARS-Patterns | `references/checklists/ears-patterns-custom.md` | Custom Extension |
| Neue Anti-Patterns | AP-08+ in `references/custom/anti-patterns-custom.md` | Custom Extension |
| Neue NFR-Kategorien | `references/custom/nfr-custom.md` | Custom Extension |
| Branchenspezifische Checklisten | `references/custom/@branche-compliance/` | Custom Extension |
| Neue GP-Checks | GP-11+ in `references/custom/golden-principles-custom.md` | Custom Extension |

## Fehlerbehandlung

| Situation | Reaktion |
|-----------|---------|
| Kein Input / leerer Input | → Nachfragen: "Welches Feature oder System soll spezifiziert werden?" (1 Frage) |
| specforge.json fehlt | → Automatisch erzeugen mit Standard-Profil, Nutzer nach Profil fragen |
| Bestehende constitution.md/specforge.json erkannt | → Phase 1a überspringen, direkt Phase 1b |
| Mixed-Language Input | → Sprachverhalten gemäß Orchestrator (DE/EN nachfragen) |
| Fehlende Referenzdateien | → Klare Fehlermeldung: "[Datei] nicht gefunden — Prüfpunkt als FAIL" |
| Profil-Wechsel mid-session | → NFR-Scan-Scope und GP-Set anpassen |
| Übermäßig viele Stories (>15) | → In Batches aufteilen, je Batch Clarify empfehlen |
| Widersprüchliche Requirements | → Als AP-03 (Implizite Annahmen) markieren, Clarify empfehlen |

## Abgrenzung

- **Specify (Modus 1)** = Neue Requirements erzeugen (Forward Engineering)
- **Discover (Modus 9)** = Requirements aus bestehendem Code ableiten (Reverse Engineering)
- **Clarify (Modus 2)** = Bestehende Requirements schärfen und Lücken schließen

## Erzeugte Artefakte

| Artefakt | Pfad | Bedingung |
|----------|------|-----------|
| specforge.json | Projektwurzel | Bei neuem Projekt (einmalig) |
| constitution.md | Projektwurzel | Bei neuem Projekt |
| ARCHITECTURE.md | Projektwurzel | Bei neuem Projekt |
| spec.md | specs/use-cases/\<feature\>/ | Immer |
