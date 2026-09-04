# Feature-Spezifikation: Rollenverwaltung

**ID:** SF-FUNC
**Version:** 2026.09.04.1
**Status:** Draft
**Profil:** standard

## 5. User Stories & Requirements

### [SF-FUNC-001] Rolle einem Konto zuweisen

**Typ**: User Story
**Priorität**: MoSCoW: Must

#### EARS-Requirement
**Pattern:** Event-Driven
Wenn ein Administrator eine Rolle zuweist, dann protokolliert die
Rollenverwaltung Zeitpunkt, Konto und Rolle.

#### Acceptance Criteria (Gherkin, min. 2)

Scenario: Rolle wird zugewiesen
  Given ein bestehendes Konto ohne Rolle
  When der Administrator die Rolle "Betriebsführer" zuweist
  Then trägt das Konto die Rolle und die Zuweisung steht im Protokoll

Scenario: Zuweisung einer unbekannten Rolle
  Given ein bestehendes Konto ohne Rolle
  When der Administrator eine nicht vergebene Rollenbezeichnung übermittelt
  Then weist die Rollenverwaltung die Zuweisung zurück
