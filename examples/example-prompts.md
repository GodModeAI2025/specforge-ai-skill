# SpecForge — Beispiel-Prompts

Kopiere diese Prompts in eine Claude-Session mit geladenem SpecForge-Skill.

---

## Modus 1: Specify

### Neues Projekt aufsetzen (Constitution + Spec)

```
Ich starte ein neues Projekt: Ein Self-Service-Portal für Versicherungskunden.
Kunden sollen Verträge einsehen, Schadensmeldungen einreichen und persönliche
Daten ändern können. Das System verarbeitet personenbezogene Daten und muss
DSGVO-konform sein. Erstelle die Constitution und eine erste Spezifikation.
```

### Feature zu bestehendem Projekt hinzufügen

```
Wir haben ein bestehendes Kundenportal. Ich brauche eine Spezifikation für
eine neue Zwei-Faktor-Authentifizierung. Benutzer sollen zwischen TOTP (App)
und SMS wählen können. Admins können MFA für Benutzergruppen erzwingen.
```

---

## Modus 2: Clarify

```
Kläre die offenen Fragen in meiner Spec. Fokussiere auf Blocker, die die
Planung verhindern würden.
```

---

## Modus 3: Plan & Tasks

```
Erstelle einen technischen Plan für die MFA-Spezifikation.
Tech-Stack: Python 3.12, FastAPI, PostgreSQL 16, Redis für Sessions.
Frontend: React 18 mit TypeScript.
Dann generiere die Tasks.
```

---

## Modus 4: Analyze

```
Prüfe die Konsistenz zwischen spec.md, plan.md und tasks.md.
Gibt es Lücken oder Widersprüche?
```

---

## Modus 5: Checklist

```
Erstelle eine Spec-Readiness-Checklist für mein MFA-Feature.
```

```
Erstelle eine DSGVO-Compliance-Checklist für das Kundenportal.
```

---

## Modus 6: Stakeholder-Simulation

```
Simuliere einen Security Reviewer und einen Datenschutzbeauftragten
für meine MFA-Spezifikation. Welche Lücken sehen die?
```

---

## Modus 7: Review

```
Prüfe diese User Story auf Qualität und Compliance:

Als Kunde möchte ich mich mit MFA einloggen können,
damit mein Konto besser geschützt ist.

Akzeptanzkriterien:
- Login mit Passwort + TOTP funktioniert
- SMS-Fallback ist verfügbar
- Admin kann MFA erzwingen
```

---

## Modus 8: Traceability

```
Erstelle eine Traceability Matrix für das MFA-Feature:
Von der Constitution über die Spec bis zu den Tasks.
```
