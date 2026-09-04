# Feature-Spezifikation: Zweiter Faktor am Leitsystem-Gateway

**ID:** SF-AUTH
**Version:** 2026.09.04.1
**Status:** Draft
**Profil:** kritis

## 5. User Stories & Requirements

### [SF-SEC-001] Anmeldung mit zweitem Faktor

**Typ**: User Story
**Priorität**: MoSCoW: Must

#### EARS-Requirement
**Pattern:** Event-Driven
Wenn ein Betriebsführer sich am Leitsystem-Gateway anmeldet, dann fordert der
Auth-Service einen TOTP-Code nach RFC 6238 an.

#### Acceptance Criteria (Gherkin, min. 2)

Scenario: Anmeldung mit gültigem TOTP-Code
  Given ein Konto mit hinterlegtem TOTP-Geheimnis
  When der Betriebsführer einen zum Zeitfenster passenden Code eingibt
  Then gewährt der Auth-Service Zugriff auf das Leitsystem-Gateway

Scenario: Anmeldung mit abgelaufenem TOTP-Code
  Given ein Konto mit hinterlegtem TOTP-Geheimnis
  When der Betriebsführer einen Code aus einem vergangenen Zeitfenster eingibt
  Then verweigert der Auth-Service den Zugriff und schreibt einen Audit-Eintrag

### [SF-AVA-001] Wiederanlauf nach Ausfall des Auth-Service

**Typ**: Technical Story
**Priorität**: MoSCoW: Must

#### EARS-Requirement
**Pattern:** State-Driven
Solange der Auth-Service nicht erreichbar ist, hält das Leitsystem-Gateway
bestehende Sitzungen für höchstens 15 Minuten aufrecht.

#### Acceptance Criteria (Gherkin, min. 2)

Scenario: Bestehende Sitzung überdauert einen Ausfall von 10 Minuten
  Given eine aktive Sitzung am Leitsystem-Gateway
  When der Auth-Service für 10 Minuten nicht antwortet
  Then bleibt die Sitzung gültig

Scenario: Sitzung endet nach 15 Minuten ohne Auth-Service
  Given eine aktive Sitzung am Leitsystem-Gateway
  When der Auth-Service für 16 Minuten nicht antwortet
  Then beendet das Leitsystem-Gateway die Sitzung und verlangt eine Neuanmeldung
