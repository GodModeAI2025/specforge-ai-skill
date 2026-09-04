# Feature-Spezifikation: Fixture fuer den Extension-Tippfehler

**ID:** SF-EXT
**Version:** 2026.09.05.1
**Status:** Draft

## 5. User Stories & Requirements

### [SF-COM-001] Auslagerungsvertrag im Informationsregister führen

**Typ**: Technical Story

#### EARS-Requirement
**Pattern:** Ubiquitous
Das Vertragsregister führt zu jedem IKT-Dienstleistungsvertrag Anbieter, Leistung, Kritikalität
und Kündigungsfrist.

#### Acceptance Criteria (Gherkin, min. 2)

Scenario: Neuer Vertrag wird aufgenommen
  Given ein unterzeichneter IKT-Dienstleistungsvertrag
  When der Auslagerungsbeauftragte ihn erfasst
  Then enthält das Register alle Pflichtfelder

Scenario: Vertrag ohne Kritikalitätseinstufung
  Given ein erfasster Vertrag ohne Kritikalitätseinstufung
  When der Auslagerungsbeauftragte das Register abschließen will
  Then verweigert das Register den Abschluss
