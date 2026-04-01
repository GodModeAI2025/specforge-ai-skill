# Enforcement Engine

Phase Gates, Anti-Pattern-Erkennung, State Machine und Artefakt-Vollständigkeitsprüfung. Wird bei jedem Phasenübergang automatisch aktiviert. Verhalten skaliert mit dem gewählten Profil und der Perspektive aus `specforge.json`.

---

## I.1 State Machine — Forward Path

```
   G0              G1              G2              G3                G4              G5
[START+PROFIL] → [SPECIFY] → [CLARIFY] → [PLAN+TASKS] → [ANALYZE] → [IMPLEMENT] → [COMPLETE]
                                 ↑                          ↑           │
                                 │                          └── Fix ────┘
                            (Loop bei F4/F3)
```

### Gate-Ausgänge

Jedes Gate hat drei mögliche Ausgänge:

| Ausgang | Bedingung | Verhalten |
|---------|-----------|-----------|
| **PASS** | Nur F0/F1/F2/F5-Befunde | Weiter zur nächsten Phase. F2-Befunde erzeugen Pflicht-Tasks. |
| **CONDITIONAL** | Mindestens 1× F3, kein F4 | Gate blockiert bis Nutzer-Bestätigung. **Voraussetzung:** Die dokumentierte Risiko-Akzeptanz (gemäß CONDITIONAL-Akzeptanz-Protokoll, Abschnitt I.5) muss **vor** der Gate-Bestätigung vorliegen — die Bestätigung selbst ist keine Dokumentation, sondern setzt deren Existenz voraus. Bei Bestätigung → PASS mit Audit-Eintrag `[CONDITIONAL ACCEPTED]`. Bei Ablehnung → Gate bleibt offen. |
| **FAIL** | Mindestens 1× F4 | Gate blockiert. Prüfpunkt muss erfüllt werden, bevor das Gate erneut geprüft wird. |

---

## I.2 Schweregrad-System (F-Stufen)

Das F-Stufen-System ersetzt das bisherige binäre `required: true/false`. Die Klassifikation folgt dem aufsichtlichen Standard der Deutschen Bundesbank (Anlage 6 zu § 27 PrüfbV).

| F-Stufe | Bezeichnung | Gate-Ergebnis | Verhalten |
|---------|-------------|---------------|-----------|
| **F4** | Schwergewichtiger Mangel | ❌ FAIL | Gate blockiert — Prüfpunkt muss erfüllt werden |
| **F3** | Gewichtiger Mangel | ⚠️ CONDITIONAL | Gate passierbar nur mit dokumentierter Risiko-Akzeptanz durch Leitungsorgan |
| **F2** | Mittelschwerer Mangel | ⚠️ WARNING | Gate passierbar — Pflicht-Task vor Go-Live erzeugen |
| **F1** | Geringfügiger Mangel | ℹ️ INFO | Gate passierbar — als Empfehlung dokumentieren |
| **F0** | Kein Mangel | ✅ PASS | Kein Handlungsbedarf |
| **F5** | Nicht anwendbar | ⏭️ SKIP | Prüfpunkt entfällt — Begründung im Audit Trail |

### Abwärtskompatibilität (Legacy-Mapping)

Projekte ohne `severity_model` in specforge.json nutzen weiterhin Boolean-Logik. Die interne Zuordnung:

| Legacy-Wert | F-Stufen-Äquivalent |
|-------------|---------------------|
| `required: true` | F4 |
| `required: false, skip_reason_required: true` | F3 |
| `required: false` | F1 |
| BLOCKER (Anti-Pattern/Schweregrad) | F4 |
| MAJOR | F3 |
| MINOR | F1 |

### Perspektivenabhängige F-Stufen

Die F-Stufe eines Prüfpunkts kann je nach Perspektive variieren. In `checks_config` wird `severity` als String (einheitlich) oder als Objekt (perspektivenabhängig) angegeben:

```json
"stride_complete": {
  "severity": {
    "_default": "F3",
    "regulated_entity": "F4",
    "ict_provider": "F3",
    "advisory": "F1"
  }
}
```

**Resolution:** Perspektive aus `specforge.json → perspective` lesen → Lookup im `severity`-Objekt → bei Treffer: diesen Wert verwenden → bei Fehltreffer: `_default` verwenden → kein `_default`: F3 als Fallback.

### GP-Score-Berechnung mit F-Stufen

| F-Stufe des Befunds | Auswirkung auf GP-Score |
|----------------------|-------------------------|
| F4 | GP gilt als nicht erfüllt |
| F3 (nicht akzeptiert) | GP gilt als nicht erfüllt |
| F3 (akzeptiert) | GP gilt als erfüllt (mit Conditional-Marker) |
| F2 | GP gilt als erfüllt (mit Warning-Marker) |
| F1 | GP gilt als erfüllt |
| F0 | GP gilt als erfüllt |
| F5 | GP wird aus Berechnung entfernt |

**GP-Score-Schwellen nach Profil:** KRITIS ≥ 9/10 · Standard ≥ 8/10 · Startup ≥ 6/10

---

## I.3 Ausführbare Phase Gates

### Gate G0: Start → Specify
```
── Gate G0 ─────────────────────────────────
[ ] specforge.json erzeugt mit Profil           [F4]
[ ] Perspektive abgefragt (wenn Regulierung     [F3]
    mit Pflicht-Abfrage geladen)
[ ] Cynefin-Einordnung (empfohlen)              [F1]
[ ] Folder Convention bestätigt                  [F2]
[ ] constitution.md erzeugt mit GPs laut Profil [F4]
── Ergebnis: PASS | CONDITIONAL | FAIL ─────────
```

### Gate G1: Specify → Clarify
```
── Gate G1 ─────────────────────────────────
[ ] spec.md erzeugt                              [F4]
[ ] EARS-Formulierung: X/Y Stories vollständig   [F4]
[ ] Gherkin-Szenarien: ≥2 pro Story              [F4]
[ ] Constitution referenziert                    [F4]
[ ] STRIDE: laut Profil geprüft                  [profilabhängig]
[ ] NFR-Scan: Core + Extensions                  [profilabhängig]
[ ] Keine offenen F4-Befunde                     [F4]
── Ergebnis: PASS | CONDITIONAL | FAIL ─────────
```

### Gate G2: Clarify → Plan
```
── Gate G2 ─────────────────────────────────
[ ] Keine offenen F4-Befunde                     [F4]
[ ] Clarifications dokumentiert in spec.md       [F4]
[ ] Vage Begriffe aufgelöst                      [F4]
[ ] [Annahme: ...]-Marker bestätigt/verworfen    [F3]
[ ] Artefakt-Erwartung erfüllt                   [F2]
── Ergebnis: PASS | CONDITIONAL | FAIL ─────────
```

### Gate G3: Plan+Tasks → Analyze
```
── Gate G3 ─────────────────────────────────
[ ] plan.md erzeugt                              [F4]
[ ] tasks.md erzeugt mit Spec-First Steps        [F4]
[ ] ADRs für Cross-Modul-Entscheidungen (GP-03)  [profilabhängig]
[ ] research.md vorhanden                        [profilabhängig]
[ ] quickstart.md vorhanden                      [F2]
[ ] ExecPlans für Tasks mit 5+ Dateien (GP-04)   [F2]
── Ergebnis: PASS | CONDITIONAL | FAIL ─────────
```

### Gate G4: Analyze → Implement
```
── Gate G4 ─────────────────────────────────
[ ] Keine F4-Befunde offen                       [F4]
[ ] GP-Score ≥ Profil-Schwelle                   [F4]
[ ] STRIDE vollständig (laut Profil)             [profilabhängig]
[ ] NFR-Scan bestanden (Core + Extensions)       [profilabhängig]
[ ] Custom-Checks bestanden (falls vorhanden)    [konfigurierbar]
── Ergebnis: PASS | CONDITIONAL | FAIL ─────────
```

### Gate G5: Implement → Complete
```
── Gate G5 ─────────────────────────────────
[ ] Artefakt-Vollständigkeits-Check (siehe I.6)  [F4]
[ ] Plan Fidelity Check (Diff vs plan.md)        [F3]
[ ] Alle Tasks aus tasks.md abgeschlossen        [F4]
[ ] Spec-First Chain Compliance geprüft          [F4]
[ ] ARCHITECTURE.md aktuell                      [F3]
[ ] Kein staler Marker ohne Owner (GP-06)        [F2]
[ ] Alle F2-WARNING-Tasks abgearbeitet           [F4]
── Ergebnis: PASS | CONDITIONAL | FAIL ─────────
```

### Gate-Ergebnis-Format

```
── Gate G4: Analyze → Implement ──────────────
✅ [F0] EARS-Formulierung: 5/5 Stories
✅ [F0] Gherkin-Szenarien: 12 (min. 10)
✅ [F0] Constitution: vorhanden
⚠️ [F3] STRIDE: 2/5 Stories noch offen — CONDITIONAL
   └─ Risiko-Akzeptanz erforderlich
⚠️ [F2] NFR DAT-03: Transport-Verschlüsselung — WARNING
   └─ Pflicht-Task vor Go-Live: DAT-03-FIX
ℹ️ [F1] NFR GOV-03: Informationsaustausch — INFO
── Ergebnis: CONDITIONAL — Risiko-Akzeptanz? ──
```

### NFR-Lücken-Format

```
[NFR-Lücke F4: IRM-01 — IKT-Risikomanagement-Framework fehlt — Gate: FAIL]
[NFR-Lücke F3: TST-06 — TLPT-Zyklus nicht geplant — Gate: CONDITIONAL]
[NFR-Lücke F2: DAT-03 — Transport-Verschlüsselung nicht spezifiziert — Gate: WARNING]
[NFR-Lücke F1: GOV-03 — Informationsaustausch nicht vorgesehen — Gate: INFO]
```

### Skip-Protokoll (F5-Dokumentation)

Jeder F5-Befund (nicht anwendbar) erfordert eine dokumentierte Begründung. Bei KRITIS-Profil ist das vollständige Skip-Protokoll Pflicht, bei Standard reicht ein Einzeiler, bei Startup entfällt die Dokumentationspflicht.

```markdown
## Skip-Protokoll: [Gate-ID] — [Prüfpunkt-ID]

**Gate:** [z.B. G4 — Analyze → Implement]
**Prüfpunkt:** [z.B. TST-06 — TLPT-Zyklus]
**F-Stufe:** F5 (nicht anwendbar)
**Begründung:** [z.B. Entität ist nicht für TLPT designiert (Art. 26(1) DORA)]
**Risiko:** [Was wird durch Überspringen nicht geprüft?]
**Kompensation:** [Welche Maßnahmen reduzieren das Risiko?]
**Entscheider:** [Wer hat zugestimmt?]
**Datum:** [YYYY-MM-DD]
```

### CONDITIONAL-Akzeptanz-Protokoll (F3-Dokumentation)

```markdown
## Risiko-Akzeptanz: [Prüfpunkt-ID]

**Gate:** [z.B. G4 — Analyze → Implement]
**Prüfpunkt:** [z.B. TST-06 — TLPT-Zyklus nicht geplant]
**F-Stufe:** F3 (gewichtiger Mangel)
**Risiko:** [Beschreibung des Risikos bei Akzeptanz]
**Akzeptiert durch:** [Name/Rolle des Leitungsorgans]
**Kompensation:** [Geplante Maßnahmen zur Risikoreduktion]
**Frist:** [Bis wann muss der Mangel behoben sein?]
**Datum:** [YYYY-MM-DD]
```

---

## I.4 Anti-Pattern-Erkennung (8 Patterns)

Bei jeder Story-Erzeugung und jedem Review automatisch prüfen:

| # | Anti-Pattern | Beschreibung | Erkennung | F-Stufe |
|---|-------------|-------------|-----------|---------|
| AP-01 | Implementation Bias | Requirement beschreibt HOW statt WHAT | Technologie-Begriffe in Story-Text | F3 |
| AP-02 | Gold Plating | Überflüssige Features ohne Business Value | Story ohne Impact-Mapping-Referenz | F1 |
| AP-03 | Implizite Annahmen | Unausgesprochene Voraussetzungen | Fehlende `[Annahme: ...]`-Marker | F3 |
| AP-04 | Vage Quantifizierung | Nicht messbare Anforderungen | "schnell", "viele", "einfach" etc. | F4 |
| AP-05 | Scope Creep | Schleichende Erweiterung ohne Spec-Update | Tasks ohne Spec-Referenz (GP-02) | F4 |
| AP-06 | Missing Negative | Nur Happy Path, keine Fehlerfälle | <2 Gherkin-Szenarien, kein Unwanted-Pattern | F3 |
| AP-07 | Orphan Artifact | Artefakt ohne Bezug zum Workflow | Task ohne Story, Story ohne Spec | F3 |
| AP-08 | SOPHIST-Verletzung | Sprachliche Mehrdeutigkeit oder Unvollständigkeit | Passiv ohne Akteur, Negation statt Positivaussage, optionale Formulierung ohne Bedingung, generische Begriffe ("das System", "der Nutzer") | F3 |

### SOPHIST-Blocklist (Erweiterung zu AP-04 Vage-Begriffe-Blocklist)

AP-08 erkennt sprachliche Anti-Patterns, die über vage Quantifizierung (AP-04) hinausgehen. Prüfung erfolgt bei jeder Story-Erzeugung und jedem Review.

| Kategorie | Trigger-Muster | Korrektur |
|-----------|---------------|-----------|
| **Passiv ohne Akteur** | "Es wird angezeigt", "wird verarbeitet", "ist sichtbar" | Akteur benennen: "Die Mobile App zeigt an" |
| **Negation statt Positivaussage** | "nicht langsamer als", "nicht weniger als" | Positiv formulieren: "mindestens so schnell wie", "mindestens" |
| **Optionale Formulierung ohne Bedingung** | "ggf.", "evtl.", "normalerweise", "in der Regel", "falls möglich" | Konkrete Bedingung: "Wenn [Bedingung], dann [Verhalten]" |
| **Generische Begriffe** | "das System", "der Nutzer", "der Service" (ohne vorherige Definition) | Konkret benennen: "die Mobile App", "der E-Mobility Fahrer", "der Auth-Service" |
| **Unvollständige Aufzählung** | "etc.", "usw.", "und so weiter", "u.a.", "z.B." (als einzige Spezifikation) | Vollständige Aufzählung oder explizit abgrenzen: "ausschließlich: X, Y, Z" |
| **Implizite Zeitangabe** | "zeitnah", "umgehend", "bald", "regelmäßig" | Konkret: "innerhalb von 24h", "alle 5 Minuten" |

**Abgrenzung AP-04 vs. AP-08:** AP-04 erkennt nicht messbare Quantifizierungen ("schnell", "viele"). AP-08 erkennt sprachliche Strukturprobleme (Passiv, Negation, Generik). Beide können gleichzeitig zutreffen — ein und dasselbe Requirement kann sowohl AP-04 als auch AP-08 verletzen.

**Legacy-Mapping:** BLOCKER → F4, MAJOR → F3, MINOR → F1

---

## I.5 5W-Pflichtblock (Reverse Engineering)

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

## I.6 Artefakt-Vollständigkeits-Check (vor G5 COMPLETE)

Vor Abschluss eines Features prüft die Enforcement Engine die gesamte Artefaktkette:

| Artefakt | Pflicht | Prüfung | Default-F-Stufe |
|----------|---------|---------|-----------------|
| specforge.json | Ja (einmal) | Existiert? Profil gesetzt? Perspektive gesetzt (wenn Regulierung)? | F4 |
| constitution.md | Ja (einmal) | Existiert? GPs laut Profil enthalten? DoD definiert? | F4 |
| ARCHITECTURE.md | Ja (einmal) | Existiert? Codemap aktuell? Invarianten mit IDs? | F4 |
| spec.md | Ja | EARS vollständig? Gherkin ≥2? STRIDE laut Profil? NFRs? Clarifications? | F4 |
| plan.md | Ja | Architektur dokumentiert? ADRs vorhanden (GP-03)? | F4 |
| research.md | KRITIS/Standard | Research-Fragen beantwortet? Versions-Matrix? | F3 (KRITIS: F4) |
| quickstart.md | Ja | Setup-Anleitung? Konventionen? Erster Task? | F2 |
| tasks.md | Ja | Spec-First Steps markiert? ExecPlans bei 5+ Dateien (GP-04)? | F4 |
| tech-debt-tracker.md | Wenn Debt | Alle bekannten Schulden erfasst (GP-10)? | F2 |
| specforge-audit.md | KRITIS: Pflicht | Gate-Checks dokumentiert? F-Stufen + Perspektive enthalten? | F4 (KRITIS), F1 (sonst) |

**Ergebnis:**
```
COMPLETE-Readiness: [Ja / Nein]
Fehlende Artefakte: [Liste mit F-Stufe]
Unvollständige Artefakte: [Liste mit Befund und F-Stufe]
GP-Score: [X/10]
Offene Warnings (F2): [Anzahl — müssen vor Go-Live abgearbeitet sein]
Offene Conditionals (F3): [Anzahl — mit Akzeptanz-Verweis]
```

---

## I.7 Reverse-Engineering Path (State Machine)

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
