# Feature-Spezifikation: Fernzugriff auf das Leitsystem-Gateway

**ID:** SF-GATEWAY
**Version:** 2026.09.04.1
**Status:** Draft
**Autor:** Requirements Engineering
**Erstellt:** 2026-09-04
**Letzte Änderung:** 2026-09-04
**Constitution-Ref:** constitution.md v1
**Profil:** kritis

---

## 1. Zusammenfassung (BLUF + Pyramid Principle)

Betriebsführer eines Verteilnetzbetreibers erreichen das Leitsystem-Gateway künftig auch von
außerhalb des Betriebsgeländes, ohne dass ein Zugang ohne zweiten Faktor entsteht.

Drei Stützen: der Fernzugriff verkürzt die Zeit bis zum Eingriff bei einer Störung; die
Zwei-Faktor-Pflicht hält die Anforderung aus dem IT-Sicherheitskatalog ein; jeder Zugriff
hinterlässt einen Audit-Eintrag, der über die gesetzliche Aufbewahrungsfrist erhalten bleibt.

## 2. Kontext & Problemstellung

Heute ist das Leitsystem-Gateway nur aus dem Betriebsnetz erreichbar. Bei einer Störung außerhalb
der Regelarbeitszeit muss ein Betriebsführer erst anfahren. Ohne Änderung bleibt die Zeit bis zum
Eingriff an die Fahrzeit gebunden.

## 3. Scope

### In Scope
- Anmeldung am Leitsystem-Gateway über das Internet mit zweitem Faktor
- Aufrechterhaltung bestehender Sitzungen bei Ausfall des Auth-Service
- Audit-Eintrag je Anmeldeversuch

### Out of Scope
- Steuerbefehle über den Fernzugriff. Lesen ja, Schalten nein.
- Zugriff für externe Dienstleister

### Annahmen
- [Annahme: Der Auth-Service läuft in derselben Sicherheitszone wie das Gateway]

## 4. Stakeholder

| Rolle | Interesse | Einfluss |
|-------|----------|---------|
| Betriebsführer | Eingriff ohne Anfahrt | Hoch |
| Informationssicherheitsbeauftragter | Einhaltung des IT-Sicherheitskatalogs | Hoch |
| Netzleitstelle | Nachvollziehbarkeit jedes Zugriffs | Mittel |

## 5. User Stories & Requirements

### [SF-SEC-001] Anmeldung mit zweitem Faktor

**Typ**: User Story
**Priorität**: MoSCoW: Must
**REQ-ID**: [REQ-001]
**Spec-First Steps**: [1,2,3,4,6,8]

#### Story
Als Betriebsführer möchte ich mich von außerhalb des Betriebsgeländes am Leitsystem-Gateway
anmelden, damit ich eine Störung ohne Anfahrt bewerten kann.

#### EARS-Requirement
**Pattern:** Event-Driven
Wenn ein Betriebsführer sich am Leitsystem-Gateway anmeldet, dann fordert der Auth-Service einen
TOTP-Code nach RFC 6238 an und gibt den Zugang erst nach dessen Prüfung frei.

#### Acceptance Criteria (Gherkin, min. 2)

Scenario: Anmeldung mit gültigem TOTP-Code
  Given ein Konto mit hinterlegtem TOTP-Geheimnis
  When der Betriebsführer einen zum aktuellen Zeitfenster passenden Code eingibt
  Then gewährt der Auth-Service Zugriff auf das Leitsystem-Gateway
  And schreibt einen Audit-Eintrag mit Konto, Zeitpunkt und Quell-IP

Scenario: Anmeldung mit abgelaufenem TOTP-Code
  Given ein Konto mit hinterlegtem TOTP-Geheimnis
  When der Betriebsführer einen Code aus einem vergangenen Zeitfenster eingibt
  Then verweigert der Auth-Service den Zugriff
  And schreibt einen Audit-Eintrag mit dem Ablehnungsgrund

Scenario: Fünf Fehlversuche hintereinander
  Given ein Konto mit vier fehlgeschlagenen Anmeldeversuchen in den letzten 15 Minuten
  When ein fünfter Versuch fehlschlägt
  Then sperrt der Auth-Service das Konto für 30 Minuten
  And benachrichtigt die Netzleitstelle

#### Execution Context (Für GSD & TaskPulse)
- **Files/Components affected**: auth-service/totp.py, gateway/session.py
- **Execution Action**: TOTP-Prüfung vor der Sitzungserzeugung einhängen
- **Verification Command**: `pytest tests/test_totp.py -k SF_SEC_001`

#### KRITIS-NFRs & Governance
**ITIL/CMDB Impact:** High (betroffen: Auth-Service und Leitsystem-Gateway)
- SEC-01 Authentisierung: TOTP nach RFC 6238, Geheimnis im HSM
- AUD-01 Protokollierung: Konto, Zeitpunkt, Quell-IP, Ergebnis je Versuch

#### STRIDE-Bewertung
- **Spoofing:** Zweiter Faktor verhindert die Übernahme mit gestohlenem Kennwort
- **Tampering:** TLS 1.3 zwischen Client und Gateway
- **Repudiation:** Audit-Eintrag je Versuch, Aufbewahrung 24 Monate
- **Information Disclosure:** Kein Klartext-Geheimnis in Logs
- **Denial of Service:** Sperre nach fünf Fehlversuchen begrenzt Rateversuche
- **Elevation of Privilege:** Der Fernzugriff vergibt keine Schaltberechtigung

#### Abhängigkeiten
- Blockiert: SF-AVA-001

#### GP-Compliance
- GP-02 erfüllt: Story vor Implementierung
- GP-05 erfüllt: Test referenziert Invariante INV-03 aus ARCHITECTURE.md

---

### [SF-AVA-001] Sitzungen überdauern einen Ausfall des Auth-Service

**Typ**: Technical Story
**Priorität**: MoSCoW: Must
**REQ-ID**: [REQ-002]
**Spec-First Steps**: [1,4,6,8]

#### Story
Als Betriebsführer möchte ich, dass eine laufende Sitzung einen kurzen Ausfall des Auth-Service
übersteht, damit ein Wartungsfenster keine Störungsbearbeitung abbricht.

#### EARS-Requirement
**Pattern:** State-Driven
Solange der Auth-Service nicht antwortet, hält das Leitsystem-Gateway bestehende Sitzungen für
höchstens 15 Minuten aufrecht.

#### Acceptance Criteria (Gherkin, min. 2)

Scenario: Sitzung überdauert einen Ausfall von 10 Minuten
  Given eine aktive Sitzung am Leitsystem-Gateway
  When der Auth-Service 10 Minuten lang nicht antwortet
  Then bleibt die Sitzung gültig
  And das Gateway zeigt einen Hinweis auf den eingeschränkten Betrieb

Scenario: Sitzung endet nach 15 Minuten ohne Auth-Service
  Given eine aktive Sitzung am Leitsystem-Gateway
  When der Auth-Service 16 Minuten lang nicht antwortet
  Then beendet das Gateway die Sitzung und verlangt eine Neuanmeldung

#### Execution Context (Für GSD & TaskPulse)
- **Files/Components affected**: gateway/session.py
- **Execution Action**: Sitzungs-Timeout auf 15 Minuten setzen, Zustand "degraded" einführen
- **Verification Command**: `pytest tests/test_session.py -k SF_AVA_001`

#### KRITIS-NFRs & Governance
**ITIL/CMDB Impact:** Medium (betroffen: Leitsystem-Gateway)
- AVA-02 Wiederanlauf: RTO 15 Minuten für den Auth-Pfad

#### STRIDE-Bewertung
[Nicht security-kritisch im Sinne der Zugangsentscheidung, da die Sitzung bereits mit zweitem
Faktor erzeugt wurde. Elevation of Privilege ausgeschlossen, da im Zustand "degraded" keine neuen
Berechtigungen vergeben werden.]

#### Abhängigkeiten
- Blockiert durch: SF-SEC-001

#### GP-Compliance
- GP-02 erfüllt
- GP-10 nicht betroffen

---

## 6. Nicht-funktionale Anforderungen (NFRs)

### Performance
| Metrik | Zielwert | Messmethode |
|--------|---------|-------------|
| Anmeldedauer p95 | ≤ 800 ms | Lasttest mit 50 gleichzeitigen Anmeldungen |

### Verfügbarkeit
| Metrik | Zielwert |
|--------|---------|
| Uptime | 99,5 % im Monatsmittel |
| RTO | 15 Minuten |
| RPO | 0 (keine persistenten Sitzungsdaten) |

### Sicherheit
Zweiter Faktor nach RFC 6238, TLS 1.3, TOTP-Geheimnis im HSM. STRIDE je Story dokumentiert.

### Compliance
IT-Sicherheitskatalog nach § 11 Abs. 1a EnWG, Abschnitt Zugriffskontrolle. NIS2: Artikel 21
Absatz 2 Buchstabe i (Multi-Faktor-Authentisierung).

## 7. Fachliches Datenmodell

- **Bounded Context:** Zugang zum Leitsystem
- **Entities:** Konto, Sitzung
- **Value Objects:** TOTP-Geheimnis, Zeitfenster
- **Aggregates:** Konto mit seinen Sitzungen; Invariante: höchstens drei aktive Sitzungen
- **Domain Events:** ZugangGewährt, ZugangVerweigert, KontoGesperrt
- **Datenklassifizierung:** Konto-Kennung ist PII, TOTP-Geheimnis ist Geheimnis

## 8. Systemgrenzen & Schnittstellen

Rein: HTTPS vom Browser des Betriebsführers. Raus: Audit-Einträge an das SIEM per Syslog.
Das Leitsystem selbst bleibt hinter dem Gateway und ist nicht direkt erreichbar.

## 9. Clarifications

| # | Frage-Ref | Antwort | Datum | Auswirkung auf |
|---|-----------|---------|-------|----------------|
| C-001 | SF-SEC-001 Verfahren | TOTP nach RFC 6238, kein SMS-Verfahren | 2026-09-04 | plan.md, STRIDE |
| C-002 | SF-AVA-001 Frist | 15 Minuten, abgeleitet aus RTO | 2026-09-04 | NFR AVA-02 |

## 10. Review & Acceptance Checklist

- [x] Alle User Stories haben EARS-Formulierung
- [x] Jede Story hat ≥2 Gherkin-Szenarien
- [x] Execution Context (Action & Verify Command) ist für GSD/Agents definiert
- [x] REQ-IDs für MissionForge Task-Generierung vergeben
- [x] NFR-Kategorien vollständig geprüft
- [x] STRIDE für security-relevante Stories durchgeführt
- [x] Keine vagen Begriffe ohne Quantifizierung
- [x] Keine offenen F4-Fragen
- [x] Constitution-Compliance geprüft
- [x] GP-Compliance pro Story dokumentiert
- [x] Abhängigkeiten zwischen Stories dokumentiert
- [x] Systemgrenzen explizit definiert

## 11. Übersichtstabelle

| ID | Titel | Typ | Priorität | EARS | Gherkin | STRIDE | NFR | GP |
|----|-------|-----|-----------|------|---------|--------|-----|-----|
| SF-SEC-001 | Anmeldung mit zweitem Faktor | US | Must | ✅ | 3 | ✅ | 2 | 02,05 |
| SF-AVA-001 | Sitzungen überdauern Ausfall | TS | Must | ✅ | 2 | n.a. | 1 | 02 |
