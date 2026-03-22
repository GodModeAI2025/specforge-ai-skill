# Constitution Template

Pflichtstruktur für jede `constitution.md`. Verwende bei Projekt-Setup (Modus 1, Phase 1a).

```markdown
# Project Constitution: [Projektname]

**Version:** [Semver oder Datum]
**Gültig ab:** [Datum]
**Verantwortlich:** [Rolle/Name]
**Letzte Prüfung:** [Datum]
**Profil:** [kritis | standard | startup] ← aus specforge.json

---

## 1. Projektprinzipien

### Zweck
[1–2 Sätze: Wofür existiert dieses Projekt?]

### Leitbild
[Was ist das angestrebte Qualitätsniveau? Woran wird Erfolg gemessen?]

### Nicht-Ziele
[Was dieses Projekt bewusst NICHT tut — verhindert Scope Creep auf Governance-Ebene]

---

## 2. Golden Principles

Die folgenden Prinzipien sind enforceable — Verstöße blockieren bis zur Auflösung (GP-08).

| ID | Prinzip | Regel | Enforcement-Mechanismus |
|----|---------|-------|------------------------|
| GP-01 | Schema-Hygiene | Matching Fixtures + Testabdeckung für alle API-Contracts | Spec-First Chain Schritt 2+3+6 |
| GP-02 | Spec-before-Code | Keine Implementierung ohne Spec-Eintrag in specs/ | Spec-Phase Gate |
| GP-03 | ADR-Disziplin | Modulübergreifende Entscheidungen brauchen ADR in specs/decisions/ | Review-Routing durch Architect |
| GP-04 | ExecPlan-Pflicht | Tasks mit 5+ Dateiänderungen brauchen EP-*.md in plans/active/ | Tasks-Phase Gate |
| GP-05 | Invariant-Traceability | Tests referenzieren Invariant-IDs aus ARCHITECTURE.md | Traceability Matrix |
| GP-06 | Keine stale Marker | TODO/TBD/FIXME brauchen Datum + Owner, max. 14 Tage | Freshness Check |
| GP-07 | Dokument-Platzierung | Alle Artefakte in Convention-Verzeichnissen | Folder Convention Check |
| GP-08 | Prinzip-Unverletzlichkeit | GP-Verstöße blockieren bis gelöst | Self-Assessment |
| GP-09 | Abhängigkeitsrichtung | Consumer kennt Provider-Interface, nicht Interna | Review Agents |
| GP-10 | Schulden-Tracking | Jede Tech-Debt in tech-debt-tracker.md mit ID + Owner | Harness Auditor |

---

## 3. Regulatorischer Rahmen

### Anwendbare Regulierung

| Regulierung | Anwendbar | Relevante Artikel/Abschnitte |
|------------|-----------|------------------------------|
| KRITIS (BSI) | Ja/Nein | [Sektoren, Schwellenwerte] |
| NIS2 | Ja/Nein | [Art. 21, 23 — Risikomanagement, Meldepflichten] |
| DSGVO | Ja/Nein | [Art. 25, 32, 35 — Privacy by Design, TOM, DSFA] |
| IT-SiG 2.0 | Ja/Nein | [Relevante Pflichten] |
| Branchenspezifisch | Ja/Nein | [z.B. EnWG, TKG, BAIT, MaRisk] |

### Sicherheits-Baseline

| Kategorie | Mindestanforderung |
|-----------|-------------------|
| Authentifizierung | [z.B. MFA Pflicht, OAuth 2.0 + OIDC] |
| Verschlüsselung at Rest | [z.B. AES-256] |
| Verschlüsselung in Transit | [z.B. TLS 1.3] |
| Logging & Audit | [z.B. Alle schreibenden Operationen, 90 Tage Retention] |
| Secrets Management | [z.B. Kein Klartext, Vault/KMS Pflicht] |
| Vulnerability Management | [z.B. CVE-Scan wöchentlich, kritische CVEs in 48h] |

---

## 4. Qualitätsstandards

### Testanforderungen

| Ebene | Abdeckung | Pflicht |
|-------|----------|---------|
| Unit Tests | ≥[X]% Line Coverage | Ja |
| Integration Tests | Alle API-Endpoints | Ja |
| Contract Tests | Alle Provider-Consumer-Paare | Ja (GP-01) |
| E2E Tests | Happy Paths aller User Stories | [Ja/Optional] |
| Security Tests | OWASP Top 10 | Ja |
| Performance Tests | Alle PER-NFRs | [Ja/Optional] |

### Code-Qualität

| Metrik | Schwellwert |
|--------|-----------|
| Cyclomatic Complexity | ≤[X] pro Funktion |
| Cognitive Complexity | ≤[X] pro Funktion |
| Dependency Depth | ≤[X] |
| Duplicate Code | ≤[X]% |

### Definition of Done (Spec-Ebene)

Eine Spezifikation gilt als "Done", wenn:
- [ ] Alle User Stories haben EARS-Formulierung
- [ ] Jede Story hat ≥2 Gherkin-Szenarien mit konkreten Testdaten
- [ ] NFR-Kategorien vollständig gegen KRITIS-Checkliste geprüft
- [ ] STRIDE für alle security-relevanten Stories durchgeführt
- [ ] Clarifications-Abschnitt abgeschlossen (keine offenen BLOCKER)
- [ ] GP-Compliance pro Story dokumentiert
- [ ] Review & Acceptance Checklist vollständig ausgefüllt
- [ ] Analyze-Report ohne BLOCKER-Befunde

### Definition of Done (Implementierungs-Ebene)

Ein Feature gilt als "Done", wenn:
- [ ] Alle Tasks aus tasks.md abgeschlossen
- [ ] Spec-First Chain pro Task eingehalten
- [ ] Alle Gherkin-Szenarien als automatisierte Tests implementiert
- [ ] NFR-Zielwerte nachweislich erreicht
- [ ] Keine offenen GP-Verstöße
- [ ] ARCHITECTURE.md aktualisiert
- [ ] Kein staler Marker ohne Owner (GP-06)
- [ ] tech-debt-tracker.md aktuell

---

## 5. Architekturentscheidungen

### Leitplanken

| Entscheidung | Begründung | ADR |
|-------------|-----------|-----|
| [z.B. Microservices vs. Monolith] | [1 Satz] | adr-001 |
| [z.B. Event-Driven vs. Request-Response] | [1 Satz] | adr-002 |

### Technologie-Constraints

| Kategorie | Erlaubt | Verboten | Begründung |
|-----------|---------|----------|-----------|
| Runtime | [z.B. .NET 8+, Java 21+] | [z.B. Node.js <20] | [Compliance/Support] |
| Datenbank | [z.B. PostgreSQL 16+] | [z.B. MongoDB <7] | [KRITIS-Zertifizierung] |
| Cloud Provider | [z.B. Azure, On-Prem] | [z.B. Nicht-EU-Regionen] | [Datensouveränität] |

---

## 6. Änderungshistorie

| Version | Datum | Autor | Änderung |
|---------|-------|-------|---------|
| 1.0 | [Datum] | [Autor] | Initiale Constitution |
```

## Regeln

1. **Constitution ist das Governance-Dokument** — alle Specs, Plans und Tasks müssen konform sein
2. **Golden Principles sind nicht verhandelbar** — GP-08 sichert das ab
3. **Regulatorischer Rahmen wird bei Projekt-Setup recherchiert** — nicht geraten
4. **Sicherheits-Baseline ist das Minimum** — Features dürfen höhere Standards setzen, nicht niedrigere
5. **DoD ist bindend** — keine Ausnahmen ohne dokumentierte Begründung in der Constitution selbst
6. **Änderungen an der Constitution brauchen eine neue Version** — kein stilles Editieren
