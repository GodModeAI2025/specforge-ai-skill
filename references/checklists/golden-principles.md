# Golden Principles (GP-01 bis GP-10)

Jede constitution.md enthält diese Prinzipien als enforceable Regeln. SpecForge prüft jede Spezifikation dagegen.

| ID | Prinzip | Regel | Enforcement |
|----|---------|-------|-------------|
| GP-01 | Schema-Hygiene | Matching Fixtures + Testabdeckung für alle API-Contracts | Spec-First Chain Schritt 2+3+6 |
| GP-02 | Spec-before-Code | Keine Implementierung ohne Spec-Eintrag in specs/ | Spec-Phase Gate |
| GP-03 | ADR-Disziplin | Modulübergreifende Entscheidungen brauchen ADR in specs/decisions/ | Review-Routing |
| GP-04 | ExecPlan-Pflicht | Tasks mit 5+ Dateiänderungen brauchen EP-*.md in plans/active/ | Tasks-Phase Gate |
| GP-05 | Invariant-Traceability | Tests referenzieren Invariant-IDs aus ARCHITECTURE.md | Traceability Matrix |
| GP-06 | Keine stale Marker | TODO/TBD/FIXME brauchen Datum + Owner, max. 14 Tage | Freshness Check |
| GP-07 | Dokument-Platzierung | Alle Artefakte in Convention-Verzeichnissen | Folder Convention Check |
| GP-08 | Prinzip-Unverletzlichkeit | GP-Verstöße blockieren bis gelöst | Self-Assessment |
| GP-09 | Abhängigkeitsrichtung | Consumer kennt Provider-Interface, nicht Interna | Review Agents |
| GP-10 | Schulden-Tracking | Jede Tech-Debt in tech-debt-tracker.md mit ID + Owner | Harness Auditor |

---

## GP-01: Schema-Hygiene
**Regel:** Jeder API-Contract hat Matching Fixtures + Testabdeckung.
**Enforcement:** Spec-First Chain Schritte 2+3+6.
**Verstoß-Beispiel:** API liefert Feld `created_at` zurück, das im Schema nicht definiert ist.
**Prüfung:** Schema vorhanden? Fixture vorhanden? Contract Tests validieren Schema + Fixture?
**Schweregrad:** MAJOR

## GP-02: Spec-before-Code
**Regel:** Keine Implementierung ohne Spec-Eintrag in `specs/`.
**Enforcement:** Spec-Phase Gate.
**Verstoß-Beispiel:** Neuer Endpoint implementiert, der in keiner spec.md beschrieben ist.
**Prüfung:** Korrespondierende Story? Story vor Implementierung geschrieben? ACs vor Tests?
**Schweregrad:** BLOCKER

## GP-03: ADR-Disziplin
**Regel:** Modulübergreifende Entscheidungen brauchen ADR in `specs/decisions/`.
**Enforcement:** Review-Routing durch Architect + Contract Guardian.
**Verstoß-Beispiel:** Wechsel von REST zu gRPC ohne ADR.
**ADR-Format (Nygard):**
```markdown
# ADR-NNN: [Titel]
**Status:** Proposed | Accepted | Deprecated | Superseded
**Datum:** [YYYY-MM-DD]
## Kontext — ## Entscheidung — ## Konsequenzen — ## Alternativen
```
**Schweregrad:** BLOCKER

## GP-04: ExecPlan-Pflicht
**Regel:** Tasks mit 5+ Dateiänderungen brauchen EP-*.md in `plans/active/`.
**Enforcement:** Tasks-Phase Gate — Dateizählung pro Task.
**Verstoß-Beispiel:** Task ändert 12 Dateien über 3 Module ohne ExecPlan.
**ExecPlan-Format:** Änderungsreihenfolge, Abhängigkeiten, Rollback-Strategie, Checkpoint.
**Schweregrad:** MAJOR

## GP-05: Invariant-Traceability
**Regel:** Tests referenzieren Invariant-IDs aus `ARCHITECTURE.md`.
**Enforcement:** Traceability Matrix.
**Verstoß-Beispiel:** Invariante "max. 3 aktive Sessions" ohne Test-Referenz.
**Schweregrad:** MAJOR

## GP-06: Keine stale Marker
**Regel:** TODO/TBD/FIXME brauchen Datum + Owner. Max. 14 Tage.
**Korrektes Format:** `// TODO(2025-10-01, @owner): Beschreibung — Ticket: PROJ-123`
**Verstoß-Beispiel:** `// TODO: Caching implementieren` seit 3 Monaten.
**Schweregrad:** MINOR (wird MAJOR nach 30 Tagen)

## GP-07: Dokument-Platzierung
**Regel:** Alle Artefakte in Convention-Verzeichnissen (→ folder-convention.md).
**Verstoß-Beispiel:** ADR in `docs/decisions/` statt `specs/decisions/`.
**Schweregrad:** MINOR

## GP-08: Prinzip-Unverletzlichkeit
**Regel:** Verstöße gegen Golden Principles blockieren bis zur Auflösung.
**Meta-Prinzip:** Sichert alle anderen GPs ab.
**Verstoß-Beispiel:** BLOCKER-Verstoß gegen GP-02 wird ignoriert.
**Schweregrad:** Meta — sichert alle anderen GPs ab.

## GP-09: Abhängigkeitsrichtung
**Regel:** Consumer kennt Provider-Interface, nicht Provider-Interna.
**Verstoß-Beispiel:** Frontend importiert Backend-DB-Entity direkt statt über API-Contract.
**Schweregrad:** MAJOR

## GP-10: Schulden-Tracking
**Regel:** Jede Tech-Debt in `tech-debt-tracker.md` mit ID + Owner.
**Format:** `| TD-NNN | Beschreibung | Owner | Priorität | Auswirkung | Erstellt | Ziel-Sprint |`
**Schweregrad:** MINOR (wird MAJOR wenn Debt auf NFRs wirkt)

---

## GP-Compliance-Scorecard

```
GP-Score = Anzahl erfüllter GPs / 10

≥ 9/10  → Exzellent — Implementierung freigegeben
  8/10  → Gut — mit dokumentierten Einschränkungen
  7/10  → Grenzwertig — Überarbeitung empfohlen
≤ 6/10  → Nicht freigabefähig — Blockiert
```

**Analyze-Schwellwert:** GP-Score ≥ 8/10 für Implementierungs-Readiness.
