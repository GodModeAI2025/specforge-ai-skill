# Ein Schweregrad-Dialekt: F0 bis F5

Bis Version 3.2 liefen zwei Skalen nebeneinander. Die Enforcement Engine, Modus 10 und beide
Regulatorik-Extensions sprachen F-Stufen, fünf Fachmodule sprachen ausschließlich BLOCKER, MAJOR
und MINOR, drei mischten. Dieses Dokument hält fest, wie die Umstellung entschieden wurde, damit
sich einzelne Werte später nachvollziehen lassen, ohne die Diskussion neu zu führen.

## Warum die F-Stufen gewinnen

Das Repo hatte die Frage an drei Stellen selbst beantwortet, ohne die Folge zu ziehen:
`kritis-nfr.md` führte die alten Werte unter "Legacy-Kompatibilität", `enforcement-engine.md` unter
"Abwärtskompatibilität", und die SKILL.md nannte das Verhalten ohne `severity_model` ausdrücklich
Legacy. Dazu kommt der sachliche Grund: die F-Stufen decken sechs Zustände ab, die alten Werte
drei. F0, F2 und F5 sind über das Mapping nicht erreichbar, werden aber gebraucht — F2 als
Pflicht-Task vor Go-Live, F5 als dokumentierter Skip, F0 als Positivbefund im Gate-Ergebnis.

## Warum das kein Suchen-und-Ersetzen war

Das Mapping ist verlustbehaftet. BLOCKER, MAJOR und MINOR treffen nur F4, F3 und F1. MAJOR diente
im Payload als Sammelstufe: es stand für "Gate blockiert bis zur Risiko-Akzeptanz" ebenso wie für
"das Artefakt gehört in eine eigene Datei". Pauschal auf F3 übersetzt, hätte jedes dieser
Formalien-Findings eine Risiko-Akzeptanz durch das Leitungsorgan verlangt. Deshalb wurde jeder
Prüfpunkt einzeln bewertet.

## Die Regel für den Einzelfall

1. Führt ein Gate oder die Anti-Pattern-Tabelle in `enforcement-engine.md` denselben Prüfpunkt,
   gilt deren Wert. Die Engine ist die normative Quelle, das Modul die Wiederholung.
2. Sonst die vier Fragen in dieser Reihenfolge: Blockiert der Befund die Phase (F4)? Braucht er
   eine dokumentierte Risiko-Akzeptanz (F3)? Reicht ein Pflicht-Task vor Go-Live (F2)? Oder ist es
   eine Empfehlung (F1)?
3. Profilabhängige Werte in der Notation `F3 (KRITIS: F4)` schreiben, wie sie der
   Artefakt-Vollständigkeits-Check der Engine schon verwendet.

## Was sich dabei verschoben hat

| Prüfpunkt | vorher | jetzt | Quelle |
|-----------|--------|-------|--------|
| Vage Begriffe aus der Blocklist (AP-04) | BLOCKER | F4 | AP-Tabelle, Gate G2 |
| EARS-Pflicht | MAJOR | F4 | Gate G1 |
| Gherkin-Minimum ≥2 Szenarien | MAJOR | F4 | Gate G1 |
| ADR-Pflicht (GP-03) | MAJOR / BLOCKER bei KRITIS | F3 (KRITIS: F4) | Gate G3, profilabhängig |
| ExecPlan-Pflicht (GP-04) | MAJOR | F2 | Gate G3 |
| Artefakt als Datei statt inline | MAJOR | F2 | Gate G2, Artefakt-Erwartung |
| Stale Marker ohne Datum und Owner (GP-06) | MINOR | F2 | Gate G5 |
| ARCHITECTURE.md nicht aktuell | MINOR | F3 | Gate G5 |
| Constitution ohne aktive GPs (TM-06) | MINOR | F4 | Gate G0 |
| Orphan Task, Orphan Spec (AP-07) | MAJOR | F3 | AP-Tabelle |
| Task ohne Spec-Referenz (AP-05, GP-02) | BLOCKER | F4 | AP-Tabelle |
| Tech-Debt ohne Eintrag (GP-10) | MINOR, MAJOR bei NFR-Wirkung | F1, F2 bei NFR-Wirkung | Artefakt-Check |
| ID-Schema, Atomarität | MINOR | F1 | Einzelbewertung |

Vier Prüfpunkte sind dabei strenger geworden, weil die Engine sie höher führte als die
Modulprosa: TM-06 (Constitution), TM-07 und SFC-06 (ARCHITECTURE.md), FR-04 (Freshness). Sechs
sind milder geworden, weil MAJOR dort als Sammelstufe stand und ein Pflicht-Task vor Go-Live die
Sache trifft.

## Ein Widerspruch, der aufgelöst werden musste

Gate G1 führte "Gherkin-Szenarien ≥2 pro Story" als F4, AP-06 ("Missing Negative") als F3, und die
Module beriefen sich mal auf das eine, mal auf das andere. Aufgelöst ist das jetzt über eine
Trennung: die Mindestanzahl von zwei Szenarien ist der Gate-Prüfpunkt und damit F4. AP-06 greift
eine Stufe darüber — Szenarien sind vorhanden, decken aber nur den Happy Path ab — und bleibt F3.

## Was bleibt

Das Legacy-Mapping in `enforcement-engine.md` bleibt bestehen, mit einem Zweck: eine alte
`specforge.json` ohne `severity_model` einzulesen. Beim Einlesen wird einmal übersetzt, danach
rechnet die Engine ausschließlich mit F-Stufen. `scripts/check-severity-dialect.py` prüft in der
CI, dass die alten Werte nirgendwo sonst auftauchen.
