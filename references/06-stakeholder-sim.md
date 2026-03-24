# Modus 6: Stakeholder- & Reviewer-Simulation

**Methode:** Devil's Advocate + Steelmanning — stärkste Gegenposition, kein Strohmann.
**Trigger:** Blinde Flecken aufdecken oder explizit Perspektiven simulieren.

## Profil-Steuerung

- **KRITIS:** Security Reviewer + Datenschutzbeauftragter immer dabei; min. 4 Rollen; STRIDE-Findings Pflicht
- **Standard:** Rollenauswahl nach Relevanz; Security Reviewer bei SEC-Stories; min. 3 Rollen
- **Startup:** Fokus auf Product Owner + Endnutzer; min. 3 Rollen; Security optional

## Verfügbare Rollen

| Rolle | Fokus | Methodik | Pflicht-Fragen |
|-------|-------|----------|---------------|
| Product Owner | Business Value, ROI, MVP-Scope | MoSCoW, Value/Effort | "Welcher Business Value rechtfertigt den Aufwand?" |
| System Architect | API-Design, Modulstruktur, ADR-Compliance | FLEX + ARCEVAL | "Welche Architektur-Entscheidungen fehlen als ADR?" |
| Contract Guardian | Spec→Schema-Chain, Fixture-Validität | iSAQB-Governance | "Sind alle API-Contracts durch Fixtures abgedeckt?" |
| Security Reviewer | OWASP Top 10, STRIDE, Auth, Secrets | STRIDE (alle 6 Kat.) | "Welche STRIDE-Kategorie ist unzureichend mitigiert?" |
| Data Engineer | Storage, Datenfluss, Retention, Concurrency | Retention Policy | "Gibt es Datenflüsse ohne Retention-Regelung?" |
| Harness Auditor | Golden Principles, Datei-Platzierung, ExecPlan | GP-01–GP-10 | "Welche GPs werden verletzt?" |
| Endnutzer | Usability, Verständlichkeit, Fehlertoleranz | Persona-basiert | "Kann ein Nicht-Techniker den Fehlerfall verstehen?" |
| Datenschutzbeauftragter | DSGVO, Datenkategorien, Löschkonzepte | DSGVO Art. 25, 35 | "Sind alle PII-Felder mit Löschkonzept versehen?" |

## Regeln (Enforcement)

1. **Rollenanzahl:** Min. 3, max. 5 Rollen pro Simulation — Unterschreitung = BLOCKER
2. **Pflicht-Rollen nach Profil:** Siehe Profil-Steuerung oben — fehlende Pflicht-Rolle = BLOCKER
3. **Steelmanning-Pflicht:** Jede Rolle muss mindestens eine Annahme explizit in Frage stellen und die stärkste Version der Gegenposition formulieren (kein Strohmann)
4. **Findings-Pflicht:** Jede Rolle muss mindestens ein Finding mit Schweregrad liefern
5. **Schweregrad-Zuweisung:** Jedes Finding wird klassifiziert: BLOCKER / MAJOR / MINOR — Zuordnung ist deterministisch nach denselben Regeln wie enforcement-engine.md
6. **Anti-Pattern-Prüfung:** AP-01–AP-08 werden von jeder Rolle mitgeprüft; Findings bei Erkennung sind Pflicht
7. **GP-Referenz:** Jedes Finding referenziert den betroffenen GP (z.B. "Verstoß gegen GP-03: ADR fehlt")

## Ablauf (deterministisch)

### Phase 6a: Rollenauswahl
1. Profil aus specforge.json lesen
2. Pflicht-Rollen gemäß Profil-Steuerung auswählen
3. Verbleibende Rollen nach deterministischen Regeln ergänzen (bis max. 5):
   - Input enthält API/Schema-Begriffe → Contract Guardian
   - Input enthält Datenbank/Storage-Begriffe → Data Engineer
   - Input enthält Auth/STRIDE-Begriffe → Security Reviewer (falls nicht schon Pflicht)
   - Input enthält UI/UX-Begriffe → Endnutzer
   - Input enthält Architektur/Modul-Begriffe → System Architect
   - Default-Fallback: Product Owner + Endnutzer (breiteste Abdeckung)
4. Rollenauswahl dem Nutzer anzeigen — Nutzer kann überschreiben (aber nicht unter Profil-Minimum)

**Simulations-Limit:** Max. 1 Durchlauf pro Rollenset. Falls Nutzer erneute Simulation wünscht, neues Rollenset oder neue Input-Version erforderlich.

### Phase 6b: Simulation
Jede Rolle durchläuft denselben 4-Schritt-Prozess:

1. **Kontext-Analyse:** Input (spec.md / Requirements) aus Rollenperspektive lesen
2. **Annahmen-Challenge:** Mindestens eine explizite Annahme identifizieren und hinterfragen
3. **Findings erzeugen:** Mindestens ein Finding mit Schweregrad + betroffener GP-Referenz
4. **Empfehlung:** Konkrete Aktion zur Behebung vorschlagen

### Phase 6c: Konsolidierung
1. Alle Findings zusammenführen, Duplikate mit höherem Schweregrad gewinnt
2. Sortierung: BLOCKER → MAJOR → MINOR
3. Konsolidiertes Protokoll erzeugen als Datei `stakeholder-sim-protocol.md`

**Gate-Integration:** Stakeholder-Sim-Findings fließen in Gate G4 (Analyze → Implement) ein. BLOCKER-Findings aus der Simulation blockieren den Gate-Übergang, bis sie gelöst sind.

### Phase 6d: Integration (optional)
- Nutzer entscheidet: Findings direkt in spec.md einarbeiten oder als Backlog-Items dokumentieren
- Bei Einarbeitung: Betroffene Stories aktualisieren, neue Gherkin-Szenarien für identifizierte Lücken

## Output: Stakeholder-Sim-Protokoll (deterministisch)

```markdown
## Stakeholder-Simulation: [Feature-Name / Spec-Referenz]
**Profil:** [KRITIS / Standard / Startup]
**Rollen:** [Liste der aktivierten Rollen]
**Input:** [spec.md / Requirements-Quelle]

### Rollen-Findings

#### [Rolle 1: Name]
| # | Finding | Schweregrad | Betroffener GP | Annahme hinterfragt | Empfehlung |
|---|---------|------------|---------------|---------------------|------------|
| F-01 | [Befund] | BLOCKER/MAJOR/MINOR | GP-XX | [Annahme] | [Aktion] |

#### [Rolle 2: Name]
...

### Konsolidierte Findings
| # | Finding | Schweregrad | Quelle (Rolle) | GP | Status |
|---|---------|------------|----------------|-------|--------|
| CF-01 | [Befund] | BLOCKER | Security Reviewer | GP-03 | Offen |

### Zusammenfassung
**BLOCKER:** [Anzahl] | **MAJOR:** [Anzahl] | **MINOR:** [Anzahl]
**Empfehlung:** [Freigabefähig / Überarbeitung empfohlen / Nicht freigabefähig]
```

## Stringenz-Regeln (Enforcement)

Folgende Regeln werden **automatisch** bei jeder Simulation durchgesetzt:

| Regel | Enforcement | Schweregrad bei Verstoß |
|-------|-----------|------------------------|
| Min. 3 Rollen aktiviert | Automatischer Check vor Simulation | BLOCKER |
| Pflicht-Rollen laut Profil anwesend | Automatischer Check nach Rollenauswahl | BLOCKER |
| Jede Rolle liefert ≥1 Finding mit Schweregrad | Automatischer Check nach Simulation | MAJOR |
| Jede Rolle hinterfragt ≥1 Annahme | Automatischer Check nach Simulation | MAJOR |
| Vage Begriffe aus Blocklist erkannt | Jedes Finding gegen Blocklist prüfen: "schnell", "viele", "einfach", "skalierbar", "sicher", "zuverlässig" → AP-04 | BLOCKER |
| Fragen-Budget | Max. 3 Fragen pro Runde an den Nutzer; Stakeholder-Fragen intern unbegrenzt | n.a. (Budget-Überschreitung = Skip) |
| Anti-Pattern-Prüfung | AP-01–AP-08 + custom APs aus `references/custom/anti-patterns-custom.md` | Schweregrad laut AP-Tabelle |
| Spec-Artefakt als Datei | Output als stakeholder-sim-protocol.md, nicht inline | MAJOR (AP-09) |

## Erweiterbarkeit

| Erweiterungspunkt | Wie | Wo |
|-------------------|-----|-----|
| Neue Rollen | `references/custom/@team-review-rollen/rollen/*.md` mit Rolle, Fokus, Methodik, Pflicht-Frage | Custom Extension |
| Neue Anti-Patterns | `references/custom/anti-patterns-custom.md` (AP-08+) | Custom Extension |
| Branchenspezifische Prüfaspekte | `references/custom/@branche-compliance/checklisten/*.md` — werden als Zusatz-Prüfpunkte jeder Rolle mitgegeben | Custom Extension |
| Profil-spezifische Rollen-Defaults | Konfigurierbar über `specforge.json → extensions` | specforge.json |

## Fehlerbehandlung

| Situation | Reaktion |
|-----------|---------|
| Kein Input / leerer Input | → Fehlermeldung: "Bitte spec.md oder Requirements übergeben" |
| specforge.json fehlt | → Standard-Profil anwenden, Hinweis ausgeben |
| Weniger als 3 relevante Rollen identifizierbar | → Pflicht-Rollen + Endnutzer als Fallback |
| Profil-Wechsel mid-session | → Rollenauswahl neu evaluieren, Pflicht-Rollen anpassen |
| Widersprüchliche Findings zwischen Rollen | → Beide dokumentieren, höherer Schweregrad gewinnt |
| Mixed-Language Input | → Sprachverhalten gemäß Orchestrator (DE/EN nachfragen) |
| Fehlende Referenzdateien | → Klare Fehlermeldung mit Dateipfad; betroffene Prüfpunkte als FAIL |
| Übermäßig viele Stories (>20) | → Rollen auf Top-5-kritischste Stories fokussieren; Hinweis ausgeben |

## GP-Mapping

| GP | Relevanz in Modus 6 |
|----|---------------------|
| GP-01 | Contract Guardian prüft Schema-Hygiene |
| GP-02 | Alle Rollen: Spec-Referenz vorhanden? |
| GP-03 | System Architect: ADR-Vollständigkeit |
| GP-04 | Harness Auditor: ExecPlan bei 5+ Dateien |
| GP-05 | System Architect: Invariant-Traceability |
| GP-06 | Harness Auditor: Stale Marker |
| GP-07 | Harness Auditor: Folder Convention |
| GP-08 | Alle: GP-Verstöße als BLOCKER |
| GP-09 | Contract Guardian: Abhängigkeitsrichtung |
| GP-10 | Harness Auditor: Tech-Debt dokumentiert |

## Erzeugte Artefakte

| Artefakt | Pfad |
|----------|------|
| stakeholder-sim-protocol.md | specs/use-cases/\<feature\>/ |
| Aktualisierte spec.md (optional) | specs/use-cases/\<feature\>/ |
