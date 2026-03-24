# Modus 10: Derive — Testfall-Ableitung aus Acceptance Criteria

**Trigger:** spec.md mit Gherkin-Szenarien existiert. Nutzer möchte Testfälle ableiten oder Testabdeckung prüfen.
**Methode:** Systematische Transformation von Gherkin-Szenarien in strukturierte Testfälle mit konkreten Testdaten, Testabdeckungsmatrix und Traceability zur Spec.

## Profil-Steuerung

- **KRITIS:** Derive Pflicht vor Implementierung; alle 5 Testfall-Typen; Testabdeckungsmatrix Pflicht; Automatisierungsgrad dokumentieren
- **Standard:** Derive empfohlen; Happy Path + Fehlerfall Pflicht; Edge Cases empfohlen; Testabdeckungsmatrix empfohlen
- **Startup:** Derive optional; Happy Path Pflicht; Rest optional

---

## Phase 10a: Vorbereitung

1. Profil aus specforge.json lesen
2. spec.md laden — alle Stories mit Gherkin-Szenarien identifizieren
3. Testfall-Scope bestimmen (laut Profil)
4. Referenzen laden:
   → `references/checklists/kritis-nfr.md` (bei KRITIS: NFR-Tests ableiten)
   → `references/checklists/stride-guide.md` (bei KRITIS/SEC-Stories: Security-Tests ableiten)

---

## Phase 10b: Testfall-Ableitung (pro Story)

Für jedes Gherkin-Szenario wird ein strukturierter Testfall erzeugt.

### Testfall-Struktur

```markdown
### [Story-ID]-TC[NNN] — [Szenario-Name]

**Typ:** Happy Path | Fehlerfall | Edge Case | Negativ-Test | Performance | Security
**Priorität:** Hoch | Mittel | Niedrig
**Automatisierbar:** Ja | Nein | Teilweise
**Herkunft:** [Story-ID] → Szenario [N]

#### Vorbedingung (Given)
- [Alle Given-Schritte als konkrete Vorbedingungen]

#### Aktion (When)
- [Alle When-Schritte als ausführbare Aktionen]

#### Erwartetes Ergebnis (Then)
- [Alle Then-Schritte als messbare Ergebnisse]

#### Testdaten
| Parameter | Wert | Begründung |
|-----------|------|-----------|
| [Eingabe] | [Konkreter Wert] | [Warum dieser Wert] |

#### Status
- [ ] Nicht getestet
```

### Testfall-Typen und Pflicht-Scope

| Typ | Beschreibung | KRITIS | Standard | Startup |
|-----|-------------|--------|----------|---------|
| **Happy Path** | Erfolgreicher Standardablauf — direkt aus Gherkin-Szenario 1 | Pflicht | Pflicht | Pflicht |
| **Fehlerfall** | Erwartete Fehlersituationen — aus Gherkin-Fehlerszenario | Pflicht | Pflicht | Empfohlen |
| **Edge Case** | Grenzwerte, Sonderfälle — zusätzlich abgeleitet | Pflicht | Empfohlen | Optional |
| **Negativ-Test** | Ungültige Eingaben, nicht-autorisierte Zugriffe | Pflicht | Empfohlen | Optional |
| **Performance** | Antwortzeiten, Last, Durchsatz — aus NFR-Quantifizierungen | Pflicht | Optional | Optional |
| **Security** | STRIDE-basierte Tests — aus STRIDE-Bewertung der Story | Pflicht | SEC-Stories | Optional |

### Ableitung zusätzlicher Testfälle (über Gherkin hinaus)

SpecForge leitet nicht nur 1:1 aus Gherkin ab, sondern erzeugt zusätzliche Testfälle:

1. **Grenzwert-Tests:** Für jede numerische Bedingung in Given/When/Then → Testfall mit Grenzwert (min, max, min-1, max+1)
2. **Berechtigungs-Tests:** Für jede Rolle im "Als [Rolle]" → Testfall mit und ohne Berechtigung
3. **NFR-Tests:** Für jede quantifizierte NFR → Testfall mit Messung (z.B. "≤200ms p95" → Lasttest)
4. **STRIDE-Tests:** Pro STRIDE-Kategorie in der Story → mindestens 1 Security-Testfall

---

## Phase 10c: Testabdeckungsmatrix

Pro Story eine Übersichtstabelle:

```markdown
## Testabdeckungsmatrix: [Feature-Name]

| Story-ID | Szenario | TC-ID | Typ | Priorität | Automatisiert? | Status |
|----------|----------|-------|-----|-----------|----------------|--------|
| SF-FUNC-001 | Freitext-Suche | TC001 | Happy Path | Hoch | Ja | ☐ |
| SF-FUNC-001 | Keine Ergebnisse | TC002 | Fehlerfall | Hoch | Ja | ☐ |
| SF-FUNC-001 | Leere Eingabe | TC003 | Edge Case | Mittel | Ja | ☐ |
| SF-FUNC-001 | SQL Injection | TC004 | Security | Hoch | Ja | ☐ |
| SF-FUNC-001 | Antwortzeit <200ms | TC005 | Performance | Mittel | Nein | ☐ |

### Abdeckungsübersicht
| Typ | Anzahl | Automatisiert | Manuell |
|-----|--------|--------------|---------|
| Happy Path | [N] | [N] | [N] |
| Fehlerfall | [N] | [N] | [N] |
| Edge Case | [N] | [N] | [N] |
| Negativ-Test | [N] | [N] | [N] |
| Performance | [N] | [N] | [N] |
| Security | [N] | [N] | [N] |
| **Gesamt** | **[N]** | **[N]** | **[N]** |
```

---

## Phase 10d: Traceability-Prüfung

Jeder Testfall muss auf genau ein Gherkin-Szenario oder eine NFR zurückverfolgbar sein:

| Prüfpunkt | Beschreibung | Schweregrad |
|-----------|-------------|------------|
| Jede Story hat ≥1 Testfall | Keine Story ohne Test | F4 |
| Jeder Happy Path hat Testfall | Gherkin-Szenario 1 → TC | F4 |
| Jeder Fehlerfall hat Testfall | Gherkin-Fehlerszenarien → TC | F3 (KRITIS: F4) |
| Testfall referenziert Story-ID | Traceability-Kette intakt | F3 |
| Testdaten sind konkret | Keine Platzhalter ("TODO", "TBD") | F3 (AP-06, GP-06) |
| Erwartete Ergebnisse sind messbar | Kein "funktioniert korrekt" — konkreter Wert | F4 (AP-04) |

---

## Stringenz-Regeln (Enforcement)

| Regel | Enforcement | Schweregrad |
|-------|-----------|------------|
| Testfall-ID eindeutig | Format: [Story-ID]-TC[NNN] | F1 |
| Given/When/Then vollständig | Alle Gherkin-Schritte übernommen + Testdaten ergänzt | F3 |
| Testdaten konkret | Keine Platzhalter, keine generischen Werte | F3 |
| Erwartete Ergebnisse messbar | Konkrete Werte, keine vagen Formulierungen (AP-04, AP-08) | F4 |
| Anti-Pattern-Prüfung | AP-01–AP-08 auch in Testfall-Beschreibungen prüfen | Schweregrad laut AP-Tabelle |
| Testabdeckungsmatrix vollständig | Jede Story abgedeckt (laut Profil-Scope) | F3 (KRITIS: F4) |

## Erweiterbarkeit

| Erweiterungspunkt | Wie | Wo |
|-------------------|-----|-----|
| Neue Testfall-Typen | Zusätzliche Typen in `references/custom/test-types-custom.md` | Custom Extension |
| Branchenspezifische Tests | z.B. DORA-Art.-26-TLPT-Tests in `references/custom/@dora/test-derive-rules.md` | Custom Extension |
| Custom Testdaten-Generatoren | Domänenspezifische Testdaten-Templates | Custom Extension |

## Fehlerbehandlung

| Situation | Reaktion |
|-----------|---------|
| spec.md fehlt | → Fehlermeldung: "spec.md nicht gefunden — Specify (Modus 1) zuerst ausführen" |
| Keine Gherkin-Szenarien in spec.md | → Warnung: "Keine Gherkin-Szenarien gefunden — AP-06 dokumentieren, Spec ergänzen" |
| Story ohne messbare Ergebnisse | → AP-04 dokumentieren, Testfall mit `[Offen: Messbare Ergebnisse definieren]` erzeugen |
| Testdaten nicht definierbar | → Testfall erzeugen, Testdaten als `[Offen: Testdaten definieren]` markieren |

## Abgrenzung

- **Derive (Modus 10)** = Testfälle aus Gherkin-Szenarien ableiten (Forward: Spec → Tests)
- **Review (Modus 7)** = Requirement-Qualität prüfen (Prüfung der Spec selbst)
- **Analyze (Modus 4)** = Cross-Artefakt-Konsistenz (System als Ganzes)

## GP-Mapping

| GP | Relevanz in Modus 10 |
|----|---------------------|
| GP-02 | Jeder Testfall referenziert Story-ID (Spec-before-Code) |
| GP-05 | Testfälle referenzieren Invariant-IDs (KRITIS) |
| GP-06 | Keine stale Marker in Testfällen (TBD/TODO mit Owner) |
| GP-07 | Testfälle in Folder Convention ablegen |

## Erzeugte Artefakte

| Artefakt | Pfad | Bedingung |
|----------|------|-----------|
| test-cases.md | specs/use-cases/\<feature\>/ | Immer |
| test-matrix.md | specs/use-cases/\<feature\>/ | Bei KRITIS/Standard (empfohlen) |
