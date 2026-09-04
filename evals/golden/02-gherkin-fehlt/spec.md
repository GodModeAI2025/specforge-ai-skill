# Feature-Spezifikation: Störungsmeldung an die Netzleitstelle

**ID:** SF-MELDUNG
**Version:** 2026.09.04.1
**Status:** Draft
**Profil:** standard

## 5. User Stories & Requirements

### [SF-OPS-001] Störungsmeldung absetzen

**Typ**: User Story
**Priorität**: MoSCoW: Must

#### Story
Als Betriebsführer möchte ich eine Störung im Meldeportal erfassen, damit die Netzleitstelle den
Vorgang ohne Telefonat übernimmt.

#### EARS-Requirement
**Pattern:** Event-Driven
Wenn ein Betriebsführer eine Störung erfasst, dann übermittelt das Meldeportal den Vorgang
innerhalb von 60 Sekunden an die Netzleitstelle.

#### Acceptance Criteria (Gherkin, min. 2)

Scenario: Störungsmeldung erreicht die Netzleitstelle
  Given ein angemeldeter Betriebsführer
  When er eine Störung mit Anlagenkennung erfasst
  Then liegt der Vorgang binnen 60 Sekunden in der Netzleitstelle vor
