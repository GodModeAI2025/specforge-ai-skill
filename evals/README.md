# Eval-Suite

Sieben Golden Specs und ihre erwarteten Befunde. Sie sind zugleich die ersten echten
Spezifikationen im Repo: bis hierher lagen nur Templates und Eingabe-Prompts, an denen sich kein
Ergebnis messen ließ.

## Aufbau

```
evals/golden/<fall>/
  spec.md          die Spezifikation
  tasks.md         optional, für die Traceability-Prüfung
  specforge.json   optional, für Profil, Perspektive und checks_config
  expected.json    Exit-Code und die erwarteten Befunde
```

`expected.json` nennt neben der Erwartung auch, was der Fall belegt. Ein Golden-Fall, dessen
Zweck sich nicht in einem Satz sagen lässt, prüft meist nichts.

## Ausführen

```bash
python3 evals/run_static.py              # alle Fälle
python3 evals/run_static.py 04           # nur passende Fälle
python3 evals/run_static.py --ausgabe    # mit der vollen Gate-Ausgabe
```

Exit 0, wenn alle Fälle bestehen. Die CI fährt das Skript bei jedem Lauf.

## Die Fälle

| Fall | Perspektive | Exit | Belegt |
|------|-------------|------|--------|
| 01-kritis-valide | keine | 0 | Der Forward-Path läuft ohne Befund durch |
| 02-gherkin-fehlt | keine | 1 | Gherkin-Minimum ist F4, nicht F3 |
| 03-dora-regulated-ohne-irm01 | regulated_entity | 1 | Fehlender IRM-01-NFR blockiert das Gate |
| 04-dora-advisory-ohne-irm01 | advisory | 0 | Dieselbe Lücke, F2 statt F4, Gate passierbar |
| 05-orphan-task | keine | 2 | AP-07 ist F3: passierbar mit Risiko-Akzeptanz |
| 06-dora-falsche-f-stufe | advisory | 1 | Eine zu hart eingestufte Lücke ist selbst ein Befund |
| 07-spec-ohne-story | keine | 1 | Ein Lauf ohne erkannte Story ist kein bestandener Lauf |

Die Fälle 03 und 04 sind das Paar, an dem die Schweregrad-Vereinheitlichung hängt. Das frühere,
dreistufige Vokabular konnte den Unterschied nicht abbilden: seine mittlere Stufe übersetzt sich
in beiden Fällen zu F3 und hätte damit auch dem Beratungsprojekt eine Risiko-Akzeptanz durch das
Leitungsorgan abverlangt. Hergeleitet ist das in
[../docs/f-stufen-entscheidung.md](../docs/f-stufen-entscheidung.md).

## Was hier nicht steht

Eine Ebene 2, die dieselben Fälle durch die Claude-API schickt und die Gate-Ausgabe der Session
mit `expected.json` vergleicht. Das wäre der Beleg, dass Skill-Prosa und Linter dasselbe sagen.
Sie fehlt bewusst: ein Lauf gegen ein Sprachmodell ist nicht reproduzierbar, kostet Budget und
braucht ein Secret. Er gehört in einen eigenen Workflow, nicht in die Pipeline, die bei jedem
Push läuft.
