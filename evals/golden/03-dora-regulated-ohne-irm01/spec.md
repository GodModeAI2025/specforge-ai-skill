# Feature-Spezifikation: Auslagerung der Kontoführung an einen Cloud-Betreiber

**ID:** SF-OUTSOURCING
**Version:** 2026.09.04.1
**Status:** Draft
**Profil:** kritis

## 5. User Stories & Requirements

### [SF-COM-001] Auslagerungsvertrag im Informationsregister führen

**Typ**: Technical Story
**Priorität**: MoSCoW: Must

#### Story
Als Auslagerungsbeauftragter möchte ich jeden IKT-Dienstleistungsvertrag im Informationsregister
führen, damit die Aufsicht ihn ohne Nachfrage einsehen kann.

#### EARS-Requirement
**Pattern:** Ubiquitous
Das Vertragsregister führt zu jedem IKT-Dienstleistungsvertrag Anbieter, Leistung, Kritikalität
und Kündigungsfrist.

#### Acceptance Criteria (Gherkin, min. 2)

Scenario: Neuer Vertrag wird aufgenommen
  Given ein unterzeichneter IKT-Dienstleistungsvertrag
  When der Auslagerungsbeauftragte ihn erfasst
  Then enthält das Register Anbieter, Leistung, Kritikalität und Kündigungsfrist

Scenario: Vertrag ohne Kritikalitätseinstufung
  Given ein erfasster Vertrag ohne Kritikalitätseinstufung
  When der Auslagerungsbeauftragte das Register abschließen will
  Then verweigert das Register den Abschluss und benennt das fehlende Feld

#### DORA-NFRs
[NFR-Lücke F4: IRM-01 — IKT-Risikomanagement-Framework nicht spezifiziert — Gate: FAIL]
