# EARS-Syntax — Easy Approach to Requirements Syntax

Jedes Requirement wird in einem der 5 Patterns formuliert. Das Pattern wird immer explizit benannt.

## Die 5 Patterns

### 1. Ubiquitous (Allgemeingültig)
Anforderung gilt immer, ohne Bedingung.
```
Das [System] soll [Funktion/Eigenschaft].
```
Beispiel: "Das System soll alle API-Responses im JSON-Format ausliefern."

### 2. Event-Driven (Ereignisgesteuert)
Anforderung wird durch ein spezifisches Ereignis ausgelöst.
```
Wenn [Ereignis], soll das [System] [Funktion/Reaktion].
```
Beispiel: "Wenn ein Benutzer drei ungültige Login-Versuche innerhalb von 5 Minuten durchführt, soll das System den Account für 30 Minuten sperren."

### 3. State-Driven (Zustandsgesteuert)
Anforderung gilt, solange ein Zustand aktiv ist.
```
Solange [Zustand], soll das [System] [Funktion/Verhalten].
```
Beispiel: "Solange die Datenbankverbindung unterbrochen ist, soll das System eingehende Schreiboperationen in einer lokalen Queue zwischenspeichern."

### 4. Optional (Wahlmöglichkeit)
Konfigurierbares oder optionales Verhalten.
```
Wenn [Bedingung/Konfiguration aktiviert], soll das [System] [Funktion].
```
Beispiel: "Wenn der Administrator die 2FA für eine Benutzergruppe aktiviert hat, soll das System bei jedem Login einen TOTP-Code abfragen."

### 5. Unwanted (Unerwünschtes Verhalten)
Reaktion auf Fehler, Angriffe, unerwünschte Zustände.
```
Wenn [unerwünschtes Ereignis/Zustand], soll das [System] [Schutzmaßnahme].
```
Beispiel: "Wenn ein API-Request ein ungültiges JWT-Token enthält, soll das System den Request mit HTTP 401 ablehnen und den Vorfall im Security-Audit-Log protokollieren."

## Pattern-Auswahl

```
Gibt es eine Bedingung oder einen Auslöser?
├── Nein → UBIQUITOUS
└── Ja
    ├── Einmaliges Ereignis? → EVENT-DRIVEN
    ├── Andauernder Zustand? → STATE-DRIVEN
    ├── Konfigurationsabhängig? → OPTIONAL
    └── Fehler-/Angriffsfall? → UNWANTED
```

## Qualitätskriterien

| Kriterium | Anti-Pattern |
|-----------|-------------|
| **Atomar** — ein Req = eine testbare Aussage | "soll X und Y und Z" |
| **Messbar** — quantifizierte Werte | "schnell", "viele", "einfach" |
| **Eindeutig** — kein Interpretationsspielraum | "angemessen", "bei Bedarf" |
| **Vollständig** — alle Aspekte beschrieben | Fehlende Fehlerbehandlung |
| **Testbar** — objektives Pass/Fail | "soll benutzerfreundlich sein" |
| **Konsistent** — kein Widerspruch | Gegensätzliche Requirements |

## Verbotene Formulierungen

| Verboten | Besser |
|----------|--------|
| "sollte" | "soll" |
| "möglichst schnell" | "≤200ms (p95)" |
| "bei Bedarf" | Konkreten Trigger benennen |
| "angemessene Sicherheit" | Konkretes Verfahren + Standard |
| "etc.", "und ähnliches" | Vollständige Aufzählung |
| "intuitiv bedienbar" | Task Completion Rate ≥90% |
| "in Echtzeit" | Konkrete Latenz (z.B. ≤100ms) |

## Kombination mit Gherkin

Jedes EARS-Requirement wird durch ≥2 Gherkin-Szenarien operationalisiert (Happy Path + Edge Case/Fehlerfall).
