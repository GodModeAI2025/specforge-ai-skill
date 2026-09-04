# SpecForge @VERSION@

Spec-Driven Requirements Engineering als Skill für Claude. Dieses Archiv
enthält den Skill und sonst nichts: den Orchestrator `SKILL.md` und die
Referenzdateien unter `references/`, die er lädt.

| | |
|---|---|
| Version | @VERSION@, auch in `VERSION` |
| Herkunft | https://github.com/GodModeAI2025/specforge-ai-skill |
| Lizenz | MIT, siehe `LICENSE` |

## Was hier liegt

```
specforge/
├── SKILL.md        Orchestrator: Dispatch auf die Modi, Phase Gates, Pre-Flight
├── references/     Fachmodule, Checklisten, Templates, Konventionen, Extensions
├── VERSION         Version dieses Pakets
├── LICENSE         MIT
├── TRADEMARK.md    Hinweis zu den genannten Marken
└── README.md       diese Datei
```

Der Skill lädt seine Referenzen über relative Pfade ab `references/`. Wer
einzelne Dateien herauskopiert, muss diese Struktur erhalten, sonst laufen die
Pfadangaben in `SKILL.md` ins Leere.

## Installation

Entpacken ergibt den Ordner `specforge/`. Er wird als Ganzes kopiert.

### Claude.ai, Projekt-Knowledge

1. Claude-Projekt öffnen und **Project Knowledge** aufrufen
2. `SKILL.md` und den Inhalt von `references/` hochladen

### Claude Cowork, Plugin/Skill

1. `specforge/` nach `<dein-plugin>/skills/specforge/` kopieren
2. Den Skill in der `plugin.json` registrieren

### Claude Code, Projekt-Kontext

1. `specforge/` nach `.claude/knowledge/specforge/` legen
2. In der `CLAUDE.md` darauf verweisen:

   ```markdown
   ## Knowledge
   Read .claude/knowledge/specforge/SKILL.md for Requirements Engineering guidance.
   ```

## Womit zu rechnen ist

- **Prompt-Text, kein Programm.** Der Skill steuert eine Claude-Session. Er
  installiert nichts und hat keinen Exit-Code.
- **Enforcement wirkt nur in der Session.** Phase Gates, F-Stufen und
  Anti-Pattern-Erkennung greifen, solange Claude den Skill geladen hat. Eine
  fertige `spec.md` prüft danach niemand mehr automatisch.
- **Kein Updateweg.** Ein kopierter Ordner erfährt nicht, dass es ein neueres
  Paket gibt. Der Abgleich läuft über die Version in `VERSION` gegen die
  Releases im Repository.
- **Keine Rechtsberatung.** Die KRITIS-, DORA- und BAIT-Checklisten sind
  Arbeitshilfen mit Verweis auf die Rechtsquelle und ersetzen keine
  aufsichtsrechtliche Prüfung. `@bait` ist ein Stub.
- **Deutsch als Arbeitssprache.** Auf englische Eingaben antwortet der Skill
  englisch, die Referenzdateien bleiben deutsch.

## Was nicht im Paket ist

Landingpage, Beispiel-Prompts, Prüfskripte und die Repo-Dokumentation gehören
nicht zum Skill und sind deshalb nicht enthalten. Sie stehen im Repository.
Dort laufen auch Issues und Pull Requests.
