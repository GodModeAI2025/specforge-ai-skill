# SpecForge v3.0 — Beispiel-Prompts

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

### Mit KRITIS-Profil starten

```
Erstelle eine Spezifikation für ein Leitsystem-Gateway im Stromnetz.
Das System ist KRITIS-relevant. Profil: KRITIS.
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

### Brownfield-Projekt

```
Erstelle einen Plan für die Integration von MFA in unser bestehendes
Spring-Boot-Backend. Es gibt bereits eine User-Tabelle und Session-Handling.
Berücksichtige die Brownfield-Situation.
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

```
Erstelle eine Security-Checklist für die API-Endpunkte.
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

## Modus 8: Management & Traceability

### Traceability Matrix

```
Erstelle eine Traceability Matrix für das MFA-Feature:
Von der Constitution über die Spec bis zu den Tasks.
```

### Spec-First Chain Audit

```
Führe einen Spec-First Chain Audit durch.
Gibt es Implementierungen ohne zugehörige Spec-Einträge?
```

### Freshness-Check

```
Prüfe auf stale Marker in allen Artefakten.
Welche TODOs, TBDs oder FIXMEs sind überfällig?
```

### Spec-Diff

```
Vergleiche den aktuellen Stand von spec.md mit der letzten Version.
Was hat sich geändert?
```

---

## Modus 9: Discover — Bestandsdokumentation

### Reverse Spec aus Code

```
Dokumentiere den Bestand dieses Systems.
Erstelle eine Spec aus dem vorhandenen Code.
```

### Bestandsdokumentation mit Migration

```
Reverse-engineer die Anforderungen dieses Legacy-Systems.
Erstelle auch ein migration-delta.md mit Ist/Soll-Abweichungen.
```

### Fremdes Repo analysieren

```
Analysiere dieses Repository und erstelle eine vollständige
Bestandsdokumentation. Welche Module gibt es, wie hängen sie
zusammen, welche Business Rules sind implementiert?
```

---

## Kombinierte Workflows

### Kompletter Durchlauf (Specify → Analyze)

```
Ich brauche ein Benachrichtigungssystem für unsere Plattform.
Nutzer sollen Push, E-Mail und In-App-Benachrichtigungen erhalten.
Erstelle die komplette Spezifikation, kläre offene Fragen,
erstelle den Plan und prüfe am Ende die Konsistenz.
```

### Discover → Specify (Legacy-Modernisierung)

```
Dokumentiere zuerst den Bestand des vorhandenen Authentifizierungsmoduls.
Erstelle dann basierend auf der Bestandsaufnahme eine neue Spezifikation
für ein modernisiertes OAuth2/OIDC-System.
```
