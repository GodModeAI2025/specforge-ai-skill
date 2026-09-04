# Das maschinenlesbare Format der spec.md

`references/templates/spec-template.md` beschreibt, was in einer Spezifikation stehen muss. Was es
bisher nicht beschrieb: woran ein Programm die Teile wiedererkennt. Dieses Dokument schließt die
Lücke. Es ist die Grundlage für `specforge check` und ändert das Template nicht, es liest es
genauer.

Das Format ist bewusst dasselbe Markdown, das Claude ohnehin erzeugt. Kein Frontmatter-Zwang, kein
zweites Dateiformat, keine Code-Fences um die Gherkin-Blöcke.

## Story-Kopf

Eine Story beginnt mit einer H3-Überschrift, die mit der ID in eckigen Klammern anfängt:

```markdown
### [SF-SEC-001] Anmeldung mit zweitem Faktor
```

Die ID folgt dem Schema `SF-{Präfix}-{NNN}`. Gültige Präfixe stehen in `spec-template.md`,
Abschnitt ID-Schema: FUNC, SEC, AVA, INT, AUD, PER, USA, COM, OPS, DAT. Drei Ziffern, führende
Nullen inklusive. Eine Story endet, wo die nächste H3-Überschrift oder eine H2-Überschrift beginnt.

## EARS-Pattern

Innerhalb der Story steht das Pattern als Fettdruck-Feld am Zeilenanfang:

```markdown
**Pattern:** Event-Driven
```

Erlaubt sind genau die fünf Werte aus `references/checklists/ears-syntax.md`: Ubiquitous,
Event-Driven, State-Driven, Optional, Unwanted. Groß- und Kleinschreibung ist egal, der Bindestrich
nicht.

Dieselbe Schreibweise gilt für die übrigen Kopffelder der Story (`**Typ**:`, `**Priorität**:`,
`**REQ-ID**:`). Der Doppelpunkt darf innerhalb oder außerhalb der Fettung stehen, beide Formen
kommen im Template vor.

## Gherkin-Szenarien

Ein Szenario beginnt mit `Scenario:` am Zeilenanfang, ohne Code-Fence, und läuft bis zum nächsten
`Scenario:`, zur nächsten Überschrift oder zum Ende der Story. Die Zeilen dazwischen beginnen mit
Given, When, Then, And oder But.

```markdown
Scenario: Anmeldung mit gültigem zweitem Faktor
  Given ein Konto mit aktivierter Zwei-Faktor-Authentisierung
  When der Nutzer einen gültigen TOTP-Code eingibt
  Then gewährt der Auth-Service Zugriff
```

Zwei Szenarien je Story sind Pflicht, eines davon ein Fehlerfall. Die Zählung prüft die Anzahl,
nicht den Inhalt: ob das zweite Szenario wirklich einen Fehlerfall beschreibt, entscheidet weiterhin
ein Mensch oder die Session.

## Marker

Drei Marker sind maschinenlesbar und stehen irgendwo im Story-Text:

| Marker | Bedeutung | Auflösung |
|--------|-----------|-----------|
| `[Annahme: ...]` | unbestätigte Voraussetzung | Clarify (Modus 2) |
| `[Offen: ...]` | fehlende Information, Story trotzdem erzeugt | Clarify (Modus 2) |
| `[NFR-Lücke F{n}: ...]` | fehlender NFR mit F-Stufe | Plan oder Analyze |

Nach Clarify dürfen `[Annahme: ...]` und `[Offen: ...]` nicht mehr offenstehen. `specforge check`
prüft das nur mit `--nach-clarify`, weil eine Spec vor Clarify beide legitim trägt.

## Verweis auf Tasks

`tasks.md` referenziert Stories über die Story-ID im Klartext, in beliebiger Zeile des Tasks:

```markdown
- [ ] T-004 Auth-Service um TOTP-Prüfung erweitern (SF-SEC-001)
```

Ein Task beginnt mit einer Zeile, die eine Task-ID im Format `T-NNN` enthält. Ein Task ohne
Story-ID ist ein Orphan Task (AP-07), eine Story ohne Task ein Orphan Spec.

## Was der Checker nicht liest

Alles, was Bedeutung statt Struktur ist. Ob die EARS-Formulierung inhaltlich zum genannten Pattern
passt, ob ein NFR-Zielwert realistisch ist, ob die STRIDE-Bewertung vollständig gedacht wurde: das
bleibt in der Session. Der Checker prüft, was ohne Modell entscheidbar ist, und meldet den Rest
nicht als bestanden, sondern gar nicht.
