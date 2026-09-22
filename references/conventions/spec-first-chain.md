# Spec-First Chain

8-Schritt-Pflichtsequenz für jeden Task. SpecForge markiert pro Task, welche Schritte relevant sind.

## Die 8 Schritte

```
1. Update Spec → 2. Update Schema → 3. Update Fixture → 4. Update Provider
→ 5. Update Consumer → 6. Run Contract Tests → 7. Log Breaking Changes
→ 8. Update ARCHITECTURE.md
```

### Schritt 1: Update Spec
**Was:** Spezifikation aktualisieren, bevor Code geschrieben wird.
**Wo:** `specs/system/` oder `specs/use-cases/<feature>/spec.md`
**Wann:** Immer. GP-02 (Spec-before-Code) macht diesen Schritt zur Pflicht.
**Nicht relevant:** Reines Refactoring ohne funktionale Änderung (aber: tech-debt-tracker.md, GP-10).

### Schritt 2: Update Schema
**Was:** API-Contracts/Schemas aktualisieren.
**Wo:** `specs/use-cases/<feature>/contracts/` (OpenAPI, JSON Schema, Protobuf, GraphQL SDL)
**Wann:** Bei jeder Änderung an API-Endpoints, Datenmodellen oder Event-Payloads.
**Nicht relevant:** Reine UI-Änderungen, reine Infrastruktur-Tasks.

### Schritt 3: Update Fixture
**Was:** Testdaten/Fixtures für geänderte Schemas aktualisieren.
**Wann:** Immer wenn Schritt 2 durchgeführt wurde. GP-01 erzwingt Matching Fixtures.
**Nicht relevant:** Wenn Schritt 2 nicht relevant war.

### Schritt 4: Update Provider
**Was:** Backend-Implementierung aktualisieren (Models, Routes, Services, DB-Migrationen).
**Wann:** Bei jeder Änderung, die das Backend betrifft.
**Nicht relevant:** Reine Frontend-Änderungen, reine Dokumentation.

### Schritt 5: Update Consumer
**Was:** Frontend/Client-Implementierung aktualisieren.
**Wann:** Bei jeder Änderung, die den Consumer betrifft.
**Prüfung:** Consumer nutzt öffentliches Interface, nicht Provider-Interna (GP-09).
**Nicht relevant:** Reine Backend-Änderungen, Batch-Jobs ohne UI.

### Schritt 6: Run Contract Tests
**Was:** Automatisierte Tests ausführen (Schema + Fixture + Provider + Consumer).
**Wann:** Immer wenn Schritt 2, 4 oder 5 durchgeführt wurde. GP-01 erzwingt Contract Tests.
**Nicht relevant:** Reine Dokumentation, Spec-only-Änderungen.

### Schritt 7: Log Breaking Changes
**Was:** Breaking Changes im API-Changelog dokumentieren.
**Wann:** Bei Änderungen die bestehende Consumer brechen (entfernte Felder, geänderte Typen etc.).
**Nicht relevant:** Additive Änderungen, interne Refactorings.

### Schritt 8: Update ARCHITECTURE.md
**Was:** Codemap, Doc Map, Invariants aktuell halten.
**Wann:** Bei Änderungen an der Systemstruktur (neue Module, geänderte Abhängigkeiten).
**Nicht relevant:** Änderungen innerhalb eines Moduls ohne strukturelle Auswirkung.

## Relevanz-Matrix pro Task-Typ

| Task-Typ | 1 Spec | 2 Schema | 3 Fixture | 4 Provider | 5 Consumer | 6 Tests | 7 Breaking | 8 ARCH |
|----------|--------|----------|-----------|-----------|-----------|---------|-----------|--------|
| Neues Feature (Full-Stack) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| API-Änderung (Breaking) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| API-Änderung (Additiv) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Reine UI-Änderung | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ |
| Backend-Refactoring | ❌* | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ |
| DB-Migration | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| NFR-Implementierung | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ |
| Dokumentation only | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Security Fix | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |

*❌\* = Kein Spec-Update, aber tech-debt-tracker.md prüfen (GP-10)*

## Task-Annotation in tasks.md

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

## Beleg pro Schritt (Enforcement)

Das ✅ in der Task-Annotation ist eine Behauptung, kein Beleg. Für den Chain-Audit zählt ein Schritt
nur als durchgeführt, wenn das zugehörige Artefakt vorliegt:

| Schritt | Beleg | Kein Beleg |
|---------|-------|-----------|
| 1 Spec | Requirement-ID existiert in spec.md und deckt die Änderung ab | Task nennt eine ID, die es in spec.md nicht gibt |
| 2 Schema | Endpoint/Feld/Event steht im Contract unter `contracts/` | Schema-Datei unverändert |
| 3 Fixture | Fixture existiert und passt zum aktuellen Schema (GP-01) | Fixture aus einer älteren Schema-Version |
| 4 Provider | Benannte Provider-Dateien existieren mit der beschriebenen Änderung | Nur eine Absichtserklärung im Task |
| 5 Consumer | Consumer nutzt das öffentliche Interface (GP-09) | Consumer greift weiter auf Provider-Interna zu |
| 6 Tests | Auffindbarer CI-Lauf oder Testreport mit Datum, Umfang und Befund | „Tests laufen grün“ ohne auffindbaren Lauf |
| 7 Breaking Changes | Eintrag im API-Changelog mit Migrationshinweis | Breaking Change nur in der Commit-Message |
| 8 ARCHITECTURE.md | Codemap/Invariants zeigen den neuen Stand | Datei unverändert (Gate G5, F3) |

**Regeln:**
- Jeder Task wird geprüft, auch ein vollständig abgehakter. Abgehakt heißt nicht belegt.
- Lässt sich ein Beleg nicht prüfen (kein Zugriff, Artefakt außerhalb des Repos), gilt der Schritt als
  **offen** und wird als Lücke geführt — nie als durchgeführt. In der Lücken-Spalte steht dann
  `nicht prüfbar` mit dem Grund, damit ein fehlender Zugriff nicht wie ein übersprungener Schritt gelesen
  wird (gleiche Absicht wie die `[Annahme: ...]`-Markierung in Clarify).
- Ein nachgezogener Beleg (Spec erst nach dem Code aktualisiert) schließt die Lücke inhaltlich, bleibt
  aber ein SFC-01-Verstoß (GP-02).

## Chain-Audit (Modus 8)

```markdown
## Spec-First Chain Audit: [Feature-Name]

| Task | Steps erwartet | Steps belegt | Lücken | Status |
|------|---------------|-------------|--------|--------|
| T-001 | 1,2,3,4,6,8 | 1,2,3,4,6,8 | — | ✅ |
| T-002 | 1,4,5,6 | 1,4,6 | 5 (Consumer) | ⚠️ |
| T-003 | 1,2,3,4,6,8 | 1,2,3 | 4,6,8 (abgehakt, ohne Beleg) | ⚠️ |
| T-004 | 1,4,6 | 1,4 | 6 (nicht prüfbar: CI außerhalb des Repos) | ⚠️ |

**Chain-Compliance:** X/Y Tasks vollständig
```
