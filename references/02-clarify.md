# Modus 2: Clarify — Sokratische Spezifikationsklärung

**Methode:** Socratic Method — geführte Entdeckung durch Fragen statt direkter Instruktion.
**Delta:** Fokus auf Stakeholder-Konflikte, implizite Annahmen, Systemgrenzen. Max. 5 Fragen/Runde. Schweregrade steuern Priorisierung.

**Trigger:** spec.md existiert, offene Fragen oder unterspezifizierte Bereiche vorhanden.

---

## Wann Pflicht vs. Optional (profilabhängig)

**KRITIS-Profil:** Pflicht vor jeder Plan-Phase. Skip nur mit Skip-Protokoll.
**Standard-Profil:** Empfohlen. Skip mit Einzeiler-Begründung.
**Startup-Profil:** Optional. Empfehlung bei erkannten Lücken.

---

## Phase 2a: Coverage-Analyse

Spec systematisch nach Lücken scannen (MECE-vollständig):

- Anforderungen ohne/mit unvollständiger EARS-Formulierung
- User Stories ohne/mit unvollständigen Gherkin-ACs
- Vage Begriffe ohne Quantifizierung ("schnell", "viele", "einfach")
- Fehlende NFR-Kategorien (gegen KRITIS-Checkliste)
- Unbeantwortete `[Annahme: ...]`-Marker
- TBD/TODO/FIXME ohne Owner (GP-06)
- Lücken in STRIDE-Abdeckung
- Fehlende Abhängigkeitsdeklarationen zwischen Stories
- Implizite Annahmen über Systemgrenzen/Schnittstellen

---

## Phase 2b: Sokratische Befragung

Für jede Lücke gezielte Fragen nach Hierarchie:

1. **Klärende Fragen** — "Was genau meinst du mit ...?" (Vage Begriffe auflösen)
2. **Annahmen hinterfragen** — "Welche Annahme steckt hinter ...?" (Implizites explizit machen)
3. **Implikationen erforschen** — "Was passiert, wenn ...?" (Grenzfälle und Fehlerszenarien)

### Regeln

- Max. 5 Fragen pro Runde (priorisiert nach Schweregrad)
- Jede Frage referenziert die betroffene Story-ID oder Spec-Abschnitt
- Fragen bieten konkrete Optionen — keine offenen "was meinen Sie"-Fragen
- Schweregrad pro Frage: `[BLOCKER]` | `[MAJOR]` | `[MINOR]`

### Bei BLOCKER: Five Whys anwenden

Max. 5 Iterationen. Stopp bei handlungsfähiger Grundursache. Fokus auf Prozess-/Architekturlücken, nicht Schuldzuweisung.

### Frageformat

```markdown
**[BLOCKER] SF-SEC-001 — Authentifizierung**
Sokratische Ebene: Annahme hinterfragen
Die Spec definiert "sichere Authentifizierung" ohne konkretes Verfahren.
Implizite Annahme: "Sicher" ist selbsterklärend.
Optionen: (a) OAuth 2.0 + OIDC, (b) mTLS Client-Zertifikate, (c) SAML 2.0, (d) Kombination
Auswirkung bei Nicht-Klärung: Plan-Phase kann Sicherheitsarchitektur nicht ableiten.
```

---

## Phase 2c: Dokumentation

Antworten in dediziertem Clarifications-Abschnitt der spec.md:

```markdown
## Clarifications

| # | Frage-Ref | Antwort | Datum | Auswirkung auf |
|---|-----------|---------|-------|----------------|
| C-001 | SF-SEC-001 Auth-Verfahren | OAuth 2.0 + OIDC via Keycloak | 2025-10-01 | plan.md Sicherheitsarchitektur |
| C-002 | SF-AVA-003 RTO/RPO | RTO 4h, RPO 1h | 2025-10-01 | KRITIS-NFRs, Infrastruktur |
```

---

## Phase 2d: Spec-Update

Nach Klärung betroffene Requirements aktualisieren:
- EARS-Formulierungen konkretisieren
- Gherkin-Szenarien ergänzen/schärfen
- Vage Begriffe durch quantifizierte Werte ersetzen
- `[Annahme: ...]` in bestätigte Anforderungen umwandeln
- TBD-Marker auflösen oder mit Owner versehen (GP-06)

---

## Abschlusskriterium

Clarify ist abgeschlossen wenn:
- Keine `[BLOCKER]`-Fragen mehr offen
- `[MAJOR]`-Fragen dürfen mit dokumentierter Begründung in Plan-Phase mitgenommen werden
- `[MINOR]`-Fragen als bekannte Lücken dokumentiert

---

## Phase Gate G2: Clarify → Plan (automatisch prüfen)

```
── Gate G2: Clarify → Plan ────────────────
[ ] Keine offenen [BLOCKER]-Fragen
[ ] Clarifications-Abschnitt in spec.md vorhanden
[ ] [MAJOR]-Fragen mit Begründung dokumentiert oder gelöst
[ ] Vage Begriffe durch quantifizierte Werte ersetzt
[ ] [Annahme: ...]-Marker bestätigt oder verworfen
── Ergebnis: PASS | FAIL (Befunde) ─────────
```

---

## Stringenz-Regeln (Enforcement)

| Regel | Enforcement | Schweregrad |
|-------|-----------|------------|
| Vage Begriffe aus Blocklist | Jede Clarification gegen Blocklist prüfen: "schnell", "viele", "einfach", "skalierbar", "sicher", "zuverlässig" → AP-04 | BLOCKER |
| Fragen-Budget | Max. 5 Fragen pro Runde (Clarify-spezifisch, sonst 3) | n.a. |
| BLOCKER-Fragen vor Plan lösen | Offene BLOCKER-Fragen blockieren Gate G2 | BLOCKER |
| Anti-Pattern-Prüfung | AP-01–AP-08 bei jeder Reformulierung | Schweregrad laut AP-Tabelle |
| Artefakt-Aktualisierung als Datei | Clarifications in spec.md als Datei, nicht inline | MAJOR |
| Schweregrad-Zuweisung | Deterministisch: Fragen mit Architektur-Impact = BLOCKER, Fragen zu Details = MAJOR, Verständnisfragen = MINOR | n.a. |

## Erweiterbarkeit

| Erweiterungspunkt | Wie | Wo |
|-------------------|-----|-----|
| Neue Clarify-Techniken | `references/custom/clarify-techniques-custom.md` | Custom Extension |
| Branchenspezifische Fragen-Templates | `references/custom/@branche-compliance/clarify-templates.md` | Custom Extension |
| Neue Anti-Patterns | AP-08+ in `references/custom/anti-patterns-custom.md` | Custom Extension |
| Custom Fragen-Kataloge | `references/custom/clarify-katalog.md` | Custom Extension |

## Fehlerbehandlung

| Situation | Reaktion |
|-----------|---------|
| Keine spec.md vorhanden | → Fehlermeldung: "spec.md nicht gefunden — Specify (Modus 1) zuerst ausführen" |
| specforge.json fehlt | → Standard-Profil anwenden, Hinweis ausgeben |
| Leere/triviale Antworten vom Nutzer | → Frage reformulieren mit konkreterem Fokus |
| Mixed-Language Input | → Sprachverhalten gemäß Orchestrator |
| Profil-Wechsel mid-session | → Clarify-Tiefe anpassen (KRITIS=tiefere Fragen) |
| Widersprüchliche Antworten | → Widerspruch explizit benennen, Entscheidung einfordern |
| Fragen-Budget erschöpft | → Verbleibende Fragen als [Annahme: ...] markieren, nächste Runde |
| Nutzer will Clarify überspringen | → Gate G2 prüfen; bei KRITIS: Skip nur mit Protokoll |

## Abgrenzung

- **Clarify (Modus 2)** = Bestehende Requirements schärfen und Lücken schließen (iterativ)
- **Specify (Modus 1)** = Neue Requirements erzeugen (Forward Engineering)
- **Stakeholder-Sim (Modus 6)** = Blindspot-Analyse durch Rollen-Perspektiven
- **Review (Modus 7)** = Qualitätsprüfung bestehender Requirements

## Erzeugte/aktualisierte Artefakte

| Artefakt | Pfad |
|----------|------|
| spec.md (aktualisiert) | specs/use-cases/\<feature\>/ — Clarifications-Abschnitt + aktualisierte Requirements |
