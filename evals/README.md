# Eval-Suite

Acht Golden Specs und ihre erwarteten Befunde. Sie sind zugleich die ersten echten
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
| 03-dora-regulated-ohne-irm01 | regulated_entity | 1 | F4 ist für diese Perspektive die richtige Stufe |
| 04-dora-advisory-ohne-irm01 | advisory | 0 | F2 passt zur Perspektive: WARNING statt Risiko-Akzeptanz |
| 05-orphan-task | keine | 2 | AP-07 ist F3: passierbar mit Risiko-Akzeptanz |
| 06-dora-falsche-f-stufe | advisory | 1 | Dieselbe Spec wie 03, andere Perspektive, ein Befund mehr |
| 07-spec-ohne-story | keine | 1 | Ein Lauf ohne erkannte Story ist kein bestandener Lauf |
| 08-dora-luecke-undokumentiert | regulated_entity | 0 | Grenze: eine nicht markierte Lücke sieht der Linter nicht |

## Das Perspektiven-Paar

Die Fälle 03 und 06 sind das Paar, an dem die F-Stufen-Zuordnung der Extension hängt: die
`spec.md` ist in beiden Byte für Byte dieselbe, die `specforge.json` unterscheidet sich in einem
einzigen Feld, der Perspektive. Für `regulated_entity` ist die F4-Einstufung der Lücke richtig
und es bleibt beim `nfr_gap` (Fall 03); für `advisory` sieht `@dora` F2 vor, und derselbe Marker
erzeugt zusätzlich den Befund `nfr_severity` (Fall 06). Das ist der einzige Unterschied, den die
Perspektive im Linter macht, und damit der Beleg dafür, dass die Perspektiven-Spalten des
Manifests wirken.

Fall 04 gehört nicht zu diesem Paar. Er zeigt die zur Perspektive passende, mildere
Selbsteinstufung: F2 ergibt WARNING und einen Pflicht-Task vor Go-Live statt einer
Risiko-Akzeptanz durch das Leitungsorgan. Genau diesen Unterschied konnte das frühere,
dreistufige Vokabular nicht abbilden, dessen mittlere Stufe sich in beiden Fällen zu F3
übersetzt. Hergeleitet ist das in
[../docs/f-stufen-entscheidung.md](../docs/f-stufen-entscheidung.md).

Was der Linter dabei tut und was nicht: Er liest die F-Stufe, die der Autor in den Marker
`[NFR-Lücke F{n}: ...]` geschrieben hat, und vergleicht sie mit der F-Stufen-Zuordnung der
aktiven Extension. Er leitet die Stufe nicht aus der Perspektive ab, und er bemerkt keine
Anforderung, die niemand als fehlend markiert hat. Fall 08 hält das fest: dieselbe Spec ohne
Marker läuft mit PASS durch. Der NFR-Scan gegen die Checkliste bleibt Sache der Session.

## Was hier nicht steht

Eine Ebene 2, die dieselben Fälle durch die Claude-API schickt und die Gate-Ausgabe der Session
mit `expected.json` vergleicht. Das wäre der Beleg, dass Skill-Prosa und Linter dasselbe sagen.
Sie fehlt bewusst: ein Lauf gegen ein Sprachmodell ist nicht reproduzierbar, kostet Budget und
braucht ein Secret. Er gehört in einen eigenen Workflow, nicht in die Pipeline, die bei jedem
Push läuft.
