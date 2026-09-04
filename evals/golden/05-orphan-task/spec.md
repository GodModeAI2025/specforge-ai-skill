# Feature-Spezifikation: Rollenverwaltung im Meldeportal

**ID:** SF-ROLLEN
**Version:** 2026.09.04.1
**Status:** Draft
**Profil:** standard

## 5. User Stories & Requirements

### [SF-FUNC-001] Rolle einem Konto zuweisen

**Typ**: User Story
**Priorität**: MoSCoW: Must

#### Story
Als Administrator möchte ich einem Konto eine Rolle zuweisen, damit die Berechtigung
nachvollziehbar an der Rolle hängt und nicht am Konto.

#### EARS-Requirement
**Pattern:** Event-Driven
Wenn ein Administrator eine Rolle zuweist, dann protokolliert die Rollenverwaltung Zeitpunkt,
Konto, Rolle und den zuweisenden Administrator.

#### Acceptance Criteria (Gherkin, min. 2)

Scenario: Rolle wird zugewiesen
  Given ein bestehendes Konto ohne Rolle
  When der Administrator die Rolle "Betriebsführer" zuweist
  Then trägt das Konto die Rolle
  And der Vorgang steht mit Zeitpunkt und Administrator im Protokoll

Scenario: Zuweisung einer nicht vergebenen Rollenbezeichnung
  Given ein bestehendes Konto ohne Rolle
  When der Administrator eine nicht vergebene Rollenbezeichnung übermittelt
  Then weist die Rollenverwaltung die Zuweisung zurück und nennt die gültigen Rollen
