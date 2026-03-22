# Spec Template

Pflichtstruktur für jede `spec.md`. Verwende bei Spec-Erzeugung (Modus 1, Phase 1b) und Discover (Modus 9).

```markdown
# Feature-Spezifikation: [Feature-Name]

**ID:** [Feature-Kürzel, z.B. SF-AUTH]
**Version:** [Semver oder Datum]
**Status:** Draft | In Review | Approved | Superseded
**Autor:** [Name/Rolle]
**Erstellt:** [Datum]
**Letzte Änderung:** [Datum]
**Constitution-Ref:** constitution.md v[X]
**Profil:** [kritis | standard | startup] ← aus specforge.json

---

## 1. Zusammenfassung (BLUF + Pyramid Principle)

**Format:** BLUF — Ein Satz: Was wird gebaut, für wen, welches Problem wird gelöst.
Danach: Pyramid Principle — max. 3 Schlüsselargumente als Stützen. Kein Tech-Stack.

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
**Priorität**: MoSCoW: Must | Should | Could | Won't
**Spec-First Steps**: [1,2,3,4,6,7]

#### Story
Als [Rolle] möchte ich [Funktion], damit [Nutzen].

#### EARS-Requirement
**Pattern:** [Ubiquitous | Event-Driven | State-Driven | Optional | Unwanted]
[EARS-Formulierung gemäß checklists/ears-syntax.md]

#### Acceptance Criteria (Gherkin, min. 2)

Scenario: [Happy Path]
  Given [Vorbedingung]
  When [Aktion]
  Then [Erwartetes Ergebnis]

Scenario: [Edge Case / Fehlerfall]
  Given [Vorbedingung]
  When [Aktion]
  Then [Erwartetes Ergebnis]

#### KRITIS-NFRs
[Relevante Kategorien aus checklists/kritis-nfr.md]

#### STRIDE-Bewertung
[Falls security-relevant — alle 6 Kategorien, siehe checklists/stride-guide.md]

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

## 7. Fachliches Datenmodell (WAS — konzeptionell, kein Tech-Stack)

Dieses Modell beschreibt die Fachdomäne in der Sprache der Stakeholder. Technische Entscheidungen (Persistenz-Strategie, Event-Sourcing, Serialisierung) gehören in plan.md.

- **Bounded Contexts** und deren Grenzen (Wo endet ein Modell?)
- **Entities** (identitätsbasiert — z.B. Benutzer, Auftrag)
- **Value Objects** (attributbasiert, unveränderlich — z.B. Adresse, Geldbetrag)
- **Aggregates** mit fachlichen Invarianten (Konsistenzregeln der Domäne)
- **Domain Events** (fachliche Vorkommnisse — z.B. "AuftragAngenommen")
- **Datenklassifizierung** (PII, sensibel, öffentlich — DSGVO-relevant)

**Abgrenzung:** Technisches Datenbankschema, OR-Mapping, Indizes, Partitionierung → plan.md

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

## Regeln

1. **Keine Story ohne EARS** — Pattern muss explizit benannt sein
2. **Min. 2 Gherkin-Szenarien** — Happy Path + mindestens ein Fehlerfall/Edge Case
3. **Keine vagen Begriffe** — "schnell" → "≤200ms p95", "viele" → "≥10.000 concurrent"
4. **Annahmen kennzeichnen** — `[Annahme: ...]` bis Clarify-Phase bestätigt
5. **NFRs sind messbar** — Jeder NFR hat Zielwert + Messmethode
6. **Clarifications-Abschnitt** ist Pflicht — wird in Modus 2 befüllt
7. **Übersichtstabelle** am Ende bei ≥3 Stories
