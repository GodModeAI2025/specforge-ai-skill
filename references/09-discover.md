# Modus 9: Discover — Bestandsdokumentation & Reverse Spec

**Methode:** Reverse Engineering + Domain Analysis.
**Trigger:** Bestehender Code/System, Bestandsdokumentation, Reverse-Engineer-Anfrage.

**Prompt Diet & Execution Rules (RPI Framework):**
- **Isoliertes Research:** Ignoriere zu Beginn (Phase 9a-9e) jegliche Feature-Tickets oder Soll-Zustände des Nutzers. Dokumentiere den Ist-Zustand absolut wertfrei und objektiv.
- **Delta ganz am Schluss:** Wende das Feature-Ticket erst ganz am Ende an, um den Confirmation Bias zu umgehen.
- Gehe in kleinen Schritten vor (Back-and-Forth). Max. 40 Instruktionen pro Interaktion.

## Profil-Steuerung

- **KRITIS:** Beide QS-Schleifen Pflicht (keine Ausnahme); STRIDE + KRITIS-NFRs in generierter Spec; Keine offenen BLOCKER/MAJOR nach QS-2
- **Standard:** Beide QS-Schleifen Pflicht; STRIDE für SEC-relevante Stories; MAJOR darf dokumentiert mitgenommen werden
- **Startup:** QS-Schleife 1 (Vollständigkeit) Pflicht; QS-Schleife 2 (Stringenz) empfohlen; Soft-Findings statt Blocker

## Ablauf (deterministisch)

### Phase 9a: Bestandsaufnahme (Discovery)

**Schritte:**
1. **Code-Analyse:** Module, APIs, Datenmodelle, Konfigurationen, Tests, TODOs, Dependencies
2. **Dokumentations-Analyse:** READMEs, Wikis, API-Docs, Runbooks, Inline-Kommentare
3. **Stakeholder-Befragung:** Sokratisch, max. 5 Fragen/Runde (Fragen-Budget beachten)
4. **Discovery-Protokoll erzeugen** mit Vollständigkeitsampel:

```markdown
## Discovery-Protokoll: [Systemname]
**Datum:** [YYYY-MM-DD]
**Quellen:** [Code, Doku, Stakeholder]

| Aspekt | Status | Quellen | Konfidenz |
|--------|--------|---------|-----------|
| Module/Komponenten | 🟢/🟡/🔴 | [Quellen] | Hoch/Mittel/Niedrig |
| APIs/Schnittstellen | 🟢/🟡/🔴 | [Quellen] | Hoch/Mittel/Niedrig |
| Datenmodell | 🟢/🟡/🔴 | [Quellen] | Hoch/Mittel/Niedrig |
| Security-Aspekte | 🟢/🟡/🔴 | [Quellen] | Hoch/Mittel/Niedrig |
| Business-Logik | 🟢/🟡/🔴 | [Quellen] | Hoch/Mittel/Niedrig |

**Vollständigkeits-Score:** [X/5 Aspekte ≥ 🟡]
```

### Phase 9b: 5W-Analyse (Pflicht-Artefakt vor spec.md)

→ Lade `references/enforcement/enforcement-engine.md` Abschnitt I.4 für 5W-Pflichtblock.

Die 5W-Analyse ist das **erste Pflicht-Artefakt** — vor constitution.md und spec.md:

| Dimension | Fragestellung | Quellen |
|-----------|--------------|---------|
| **WER** | Akteure und Rollen | Auth-Code, User-Management, Stakeholder |
| **WAS** | Kernfunktionen | API-Endpoints, Service-Layer, Business Logic |
| **WARUM** | Geschäftszweck | README, Stakeholder, Product-Docs |
| **WIE** | Technische Umsetzung | Stack, Frameworks, Dependencies |
| **WANN** | Zeitliche Aspekte | Git-Historie, Cron-Jobs, Logs |

**Abschlusskriterium:** Alle 5 Dimensionen bearbeitet. Konfidenz-Bewertung pro Dimension. Offene Fragen als Input für Clarify-Phase dokumentiert.

**Output:** 5W-Analyse gemäß dem Template in enforcement-engine.md I.4 (mit Konfidenz + Evidenz pro Dimension).

### Phase 9c: Spec-Generierung

Vollwertige spec.md mit **identischem Qualitätsanspruch** wie Modus 1 (Specify):

**Pflichtschritte:**
1. → Lade `references/templates/spec-template.md` für Pflichtstruktur
2. → Lade `references/checklists/ears-syntax.md` für EARS-Formulierung
3. EARS-Requirements formulieren (jedes mit explizit benanntem Pattern)
4. Gherkin-ACs erzeugen (≥2 pro Story: Happy Path + Fehlerfall)
5. DDD-Datenmodell aus Code ableiten
6. NFR-Scan durchführen (Scope laut Profil):
   - KRITIS: Alle 6 Kategorien (AVA, SEC, AUD, PER, DAT, OPS)
   - Standard: SEC + PER + DAT empfohlen
   - Startup: Optional
7. STRIDE-Analyse (Scope laut Profil)
8. Wissenslücken als `[DISCOVERY-GAP]`-Marker kennzeichnen

**Anti-Pattern-Prüfung:** AP-01–AP-08 bei jeder Story-Erzeugung prüfen (identisch zu Modus 1).

### Phase 9d: QS-Schleife 1 — Vollständigkeit

**Ziel:** Jede Funktion/Endpunkt/Business Rule im Code muss in einer Story in spec.md abgebildet sein.

**Prüfung (deterministisch):**

| Prüfpunkt | Was wird geprüft | Schweregrad |
|-----------|-----------------|------------|
| QS1-01 | Jeder API-Endpoint hat Story | MAJOR |
| QS1-02 | Jede Business Rule hat Story | MAJOR |
| QS1-03 | Jeder Datenfluss ist dokumentiert | MINOR |
| QS1-04 | Alle Auth/Authz-Pfade abgebildet | MAJOR (bei KRITIS: BLOCKER) |
| QS1-05 | Error-Handling-Pfade als Unwanted-Stories | MAJOR (AP-06) |

**Loop:** Wiederholen bis keine FEHLT-Einträge mehr vorhanden.

**Output pro Iteration:**
```markdown
## QS-1 Vollständigkeit: Iteration [N]
| Code-Element | Story vorhanden? | Status | Aktion |
|-------------|-----------------|--------|--------|
| POST /api/users | SF-FUNC-001 | ✅ | — |
| DELETE /api/users/{id} | — | ❌ FEHLT | Story erzeugen |

**Abdeckung:** [X/Y] Elemente abgebildet ([Z%])
**Status:** [Vollständig / Lücken vorhanden → nächste Iteration]
```

### Phase 9e: QS-Schleife 2 — Konsistenz & Stringenz

**Ziel:** MECE-Konsistenzprüfung (wie Modus 4 Analyze) + Begriffskonsistenz + Ist/Soll-Delta.

**Prüfung:**

| Prüfpunkt | Was wird geprüft | Schweregrad |
|-----------|-----------------|------------|
| QS2-01 | Begriffe konsistent (gleicher Begriff = gleiche Bedeutung überall) | MAJOR |
| QS2-02 | Keine widersprüchlichen Requirements | BLOCKER |
| QS2-03 | Ist/Soll-Delta dokumentiert (was ist im Code, was fehlt) | MAJOR |
| QS2-04 | GP-Compliance laut Profil | Schweregrad laut GP |
| QS2-05 | EARS-Pattern korrekt gewählt (deterministisch nach Entscheidungsbaum) | MINOR |
| QS2-06 | Keine verwaisten Stories (Story ohne Code-Evidenz = Soll, kennzeichnen) | MINOR |

**Loop:** Wiederholen bis keine BLOCKER/MAJOR-Findings (KRITIS/Standard) bzw. keine BLOCKER (Startup).

**Output pro Iteration:**
```markdown
## QS-2 Konsistenz: Iteration [N]
| # | Prüfpunkt | Status | Schweregrad | Befund | Fix |
|---|-----------|--------|------------|--------|-----|
| QS2-01 | Begriffskonsistenz | ✅/❌ | — / MAJOR | [Befund] | [Fix] |

**Offene Findings:** BLOCKER: [X] | MAJOR: [Y] | MINOR: [Z]
**Status:** [PASS / Nächste Iteration nötig]
```

### Phase 9f: Finalisierung

1. spec.md vollständig und konsistent (QS-1 + QS-2 bestanden)
2. Ist/Soll-Delta dokumentiert (was existiert vs. was spec.md beschreibt)
3. `[DISCOVERY-GAP]`-Marker für verbleibende Wissenslücken
4. Optional: Direkt in Modus 2 (Clarify) oder Modus 3 (Plan) überleiten

## Phase Gates — Reverse-Engineering Path

→ Siehe `references/enforcement/enforcement-engine.md` Abschnitt I.6

| Gate | Prüfung | Schweregrad bei Fail |
|------|---------|---------------------|
| G0-RE | Discovery-Protokoll erzeugt? Quellen dokumentiert? | BLOCKER |
| G1-RE | 5W-Analyse komplett? Alle 5 Dimensionen mit Konfidenz? | BLOCKER |
| G2-RE | spec.md erzeugt? EARS + Gherkin? Qualität = Forward-Path? | BLOCKER |
| G3-RE | QS-1 bestanden (Vollständigkeit)? QS-2 bestanden (Konsistenz)? | BLOCKER |
| G4-RE | Finalisierung — spec.md konsistent, Ist/Soll-Delta dokumentiert? | BLOCKER |

Nach G4-RE: Übergang in Forward-Path ab G2 (Clarify) oder G3 (Plan).

## Stringenz-Regeln (Enforcement)

| Regel | Enforcement | Schweregrad |
|-------|-----------|------------|
| Vage Begriffe aus Blocklist | Jede erzeugte Story gegen Blocklist prüfen: "schnell", "viele", "einfach", "skalierbar", "sicher", "zuverlässig" → AP-04 | BLOCKER |
| Fragen-Budget | Stakeholder-Befragung: max. 5 Fragen/Runde; sonstige Interaktion: max. 3 Fragen/Runde | n.a. |
| Anti-Pattern-Prüfung | AP-01–AP-08 + custom APs bei jeder Story-Erzeugung in Phase 9c | Schweregrad laut AP-Tabelle |
| EARS-Pflicht | Jede Story hat explizit benanntes Pattern (wie Forward-Path) | MAJOR |
| Gherkin-Minimum | ≥2 Szenarien pro Story (Happy Path + Fehlerfall) | MAJOR (AP-06) |
| QS-Schleifen nicht überspringbar | KRITIS: beide Pflicht; Standard: beide Pflicht; Startup: QS-1 Pflicht | BLOCKER bei Skip |
| Artefakt-Erzeugung als Datei | Alle Artefakte als separate .md-Dateien, nicht inline | MAJOR |
| Schweregrad-Zuweisung | Deterministisch nach enforcement-engine.md | n.a. |

## Erweiterbarkeit

| Erweiterungspunkt | Wie | Wo |
|-------------------|-----|-----|
| Neue QS-Prüfpunkte | QS1-06+ / QS2-07+ in `references/custom/discover-qs-custom.md` | Custom Extension |
| Neue Anti-Patterns | AP-08+ in `references/custom/anti-patterns-custom.md` | Custom Extension |
| Branchenspezifische Discovery-Checklisten | `references/custom/@branche-compliance/discovery-checks.md` | Custom Extension |
| Neue 5W-Dimensionen | 6W+ in `references/custom/5w-custom.md` (z.B. WIEVIEL für Skalierung) | Custom Extension |
| Neue EARS-Patterns | `references/checklists/ears-patterns-custom.md` | Custom Extension |
| Custom NFR-Kategorien | `references/custom/nfr-custom.md` | Custom Extension |

## Fehlerbehandlung

| Situation | Reaktion |
|-----------|---------|
| Kein Code / leeres Repository | → Fehlermeldung: "Kein analysierbarer Code gefunden" |
| specforge.json fehlt | → Standard-Profil anwenden, Hinweis ausgeben |
| Code ohne Tests / ohne Doku | → Konfidenz auf "Niedrig" setzen, [DISCOVERY-GAP] markieren |
| Profil-Wechsel mid-session | → QS-Schleifen-Intensität anpassen, Pflicht-Rollen neu evaluieren |
| Übermäßig großes System (>20 Module) | → Modular aufteilen, je Modul eigene 5W + spec.md |
| Mixed-Language-Code | → Sprachverhalten: Fachbegriffe in Originalsprache, Rest gemäß Orchestrator |
| Fehlende Referenzdateien | → Klare Fehlermeldung mit Pfad, Schritt als FAIL werten |
| QS-Loop terminiert nicht (>5 Iterationen) | → Verbleibende Findings als [DISCOVERY-GAP] markieren, Nutzer informieren |

## GP-Mapping

| GP | Relevanz in Modus 9 |
|----|---------------------|
| GP-01 | Spec-Gen: Schema-Hygiene für entdeckte APIs |
| GP-02 | Spec-Gen: Jede entdeckte Funktion → Story |
| GP-03 | Spec-Gen: ADR für Architektur-Entscheidungen |
| GP-06 | Discovery: Stale Marker im Code identifizieren |
| GP-07 | Finalisierung: Folder Convention einhalten |
| GP-08 | QS-Schleifen: GP-Verstöße blockieren |
| GP-10 | Discovery: Tech-Debt im Code → tech-debt-tracker.md |

## Erzeugte Artefakte

| Artefakt | Pfad |
|----------|------|
| discovery-protocol.md | specs/use-cases/\<feature\>/ |
| 5w-analyse.md | specs/use-cases/\<feature\>/ |
| spec.md | specs/use-cases/\<feature\>/ |
| migration-delta.md (optional) | specs/use-cases/\<feature\>/ |

## Pflicht: Beide QS-Schleifen durchlaufen — kein Abkürzen.

QS-Schleifen-Intensität richtet sich nach Profil:
- **KRITIS:** Beide Schleifen strikt, keine offenen BLOCKER/MAJOR nach Abschluss
- **Standard:** Beide Schleifen, MAJOR darf dokumentiert mitgenommen werden
- **Startup:** Schleife 1 (Vollständigkeit) Pflicht, Schleife 2 (Stringenz) empfohlen
