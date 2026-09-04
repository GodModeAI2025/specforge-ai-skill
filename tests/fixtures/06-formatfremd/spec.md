# Feature-Spezifikation: Rollenverwaltung

**ID:** SF-ROLLEN
**Version:** 2026.09.04.1
**Status:** Draft

## 5. User Stories & Requirements

### SF-SEC-001 Anmeldung mit zweitem Faktor

Der Story-Kopf steht hier ohne eckige Klammern und wird deshalb nicht als
Story erkannt. Die Datei sieht vollstaendig aus, hat fuer den Checker aber
keinen pruefbaren Inhalt.

**Pattern:** Event-Driven

Scenario: Anmeldung mit gueltigem zweitem Faktor
  Given ein Konto mit aktivierter Zwei-Faktor-Authentisierung
  When der Nutzer einen gueltigen TOTP-Code eingibt
  Then gewaehrt der Auth-Service Zugriff
