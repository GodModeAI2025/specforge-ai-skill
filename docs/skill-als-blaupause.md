# SpecForge als Blaupause für eigene Skills

Ausgelagert aus dem README. Die Methodik hinter SpecForge, falls du einen
eigenen Claude-Skill nach demselben Muster bauen willst.

Zurück zum [README](../README.md).

---

SpecForge kann als Blaupause für eigene Skills dienen. Hier die Methodik:

## 1. Frontmatter definieren
```yaml
---
name: MeinSkill
description: Kurzbeschreibung mit Trigger-Keywords. Verwende diesen Skill
  IMMER bei: keyword1, keyword2, keyword3. Auch bei "natürlichsprachlicher
  Trigger", "weiterer Trigger".
---
```

**Regeln für gute Trigger:**
- Technische Begriffe UND natürlichsprachliche Formulierungen
- "Verwende diesen Skill IMMER bei:" signalisiert Claude den Aktivierungszeitpunkt
- "Auch bei:" für indirekte Trigger ("prüfe meine X", "was fehlt bei Y")

## 2. Session-Isolation festlegen

Entscheide: Darf der Skill auf Memories/Vorwissen zugreifen oder ist jede Session ein Blank Slate?

```markdown
## Wissensquellen
MeinSkill arbeitet ausschließlich mit:
1. Session-Kontext
2. Eigenrecherche via Web Search
3. Skill-eigene Referenzen
```

## 3. Modi definieren

Jeder Modus hat:
- **Trigger:** Woran erkennt der Skill, dass dieser Modus gemeint ist?
- **Phasen:** Welche Schritte werden durchlaufen?
- **Artefakte:** Was wird erzeugt?
- **Abschlusskriterium:** Wann ist der Modus fertig?

```markdown
### Modus N: [Name]
**Trigger:** [Beschreibung]
**Phase Na: [Schritt]**
1. ...
2. ...
**Erzeugte Artefakte:**
- ...
```

## 4. Output-Formate als Templates definieren

Gib Claude exakte Templates mit Platzhaltern:

```markdown
## Output-Format: [Artefakt-Typ]
\```markdown
### [ID] [Titel]
**Typ**: ...
**Priorität**: ...
#### Abschnitt
[Inhalt]
\```
```

## 5. Qualitätsregeln als enforceable Constraints

Nicht "versuche X" sondern "X ist Pflicht":

```markdown
## Qualitätsregeln (immer aktiv)
1. **Regel** — Enforcement-Beschreibung
2. **Regel** — Enforcement-Beschreibung
```

## 6. Interaktionsregeln für Gesprächsführung

```markdown
## Interaktionsregeln
1. Max. N Fragen pro Runde
2. Nach [Aktion] einmal validieren
3. Smarte Annahmen mit `[Annahme: ...]` kennzeichnen
```

## 7. Referenzen als separate Dateien

Statt alles inline: Module in `references/` auslagern und per Dispatch-Tabelle referenzieren:

```markdown
## Dispatch-Tabelle
| Modus | Modul | Laden |
|-------|-------|-------|
| 1: Specify | references/01-specify.md | Bei Modus-Aktivierung |
```

## 8. Standardisierte Modul-Sektionen

Jedes Modul sollte enthalten: Profil-Steuerung, Ablauf, Output-Template, Stringenz-Regeln, Erweiterbarkeit, Fehlerbehandlung, GP-Mapping, Erzeugte Artefakte.

## 9. Skill testen

Teste jeden Modus mit:
- Minimalem Input (erkennt der Skill den Modus?)
- Komplexem Input (erzeugt er alle Artefakte?)
- Edge Cases (was passiert bei fehlendem Kontext?)
- Sprachtest (Deutsch → Deutsch, Englisch → Englisch?)
