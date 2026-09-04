# Feature-Spezifikation: Störungsmeldung an die Leitstelle

**ID:** SF-OPS
**Version:** 2026.09.04.1
**Status:** Draft
**Profil:** standard

## 5. User Stories & Requirements

### [SF-OPS-001] Störungsmeldung absetzen

**Typ**: User Story
**Priorität**: MoSCoW: Must

#### EARS-Requirement
**Pattern:** Event-Driven
Wenn ein Betriebsführer eine Störung erfasst, dann übermittelt das
Meldeportal den Vorgang innerhalb von 60 Sekunden an die Leitstelle.

#### Acceptance Criteria (Gherkin, min. 2)

Scenario: Störungsmeldung erreicht die Leitstelle
  Given ein angemeldeter Betriebsführer
  When er eine Störung mit Anlagenkennung erfasst
  Then liegt der Vorgang binnen 60 Sekunden in der Leitstelle vor
