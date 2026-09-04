# Sicherheitsrichtlinie

## Unterstützte Versionen

Das Repo hat keine Tags und keine Releases, nur `main`. Die Version 3.2 steht in der README-Versionstabelle (Z. 473) und im JSON-LD von `index.html` (Z. 34), sie ist kein veröffentlichtes Artefakt. Unterstützt wird nur der aktuelle Stand von `main`.

Installation heißt laut README ab Z. 41 Ordner kopieren. Wer das getan hat, arbeitet mit einem Snapshot ohne Update-Kanal und muss selbst nachziehen.

## Schwachstelle melden

Meldeweg über GitHub Security Advisories:

https://github.com/GodModeAI2025/specforge-ai-skill/security/advisories/new

Kein öffentliches Issue für Schwachstellen, auch nicht für Verdachtsfälle. Falls das Formular nicht erreichbar ist, ist Private Vulnerability Reporting im Repo nicht aktiviert. Dann bitte ein Issue eröffnen, das nur nach einem privaten Kanal fragt und nichts zum Fund selbst enthält.

Es gibt keine zugesagte Reaktionszeit, kein SLA und kein Bug-Bounty. Das Repo hat einen Maintainer und keinen Bereitschaftsdienst. Betrifft der Fund einen Client oder einen MCP-Server statt dieses Repo, melde ihn bitte auch dort.

## Bedrohungsmodell

Der Skill ist Markdown. Ausführbarer Code steckt allein in `course.html`: ein Inline-Script ab Z. 1291 und Inline-Handler an Buttons, kein externes JavaScript. `index.html` enthält einen JSON-LD-Block (Z. 24) und sonst keinen Code. Die Angriffsfläche ist der Prompt-Text: was in `SKILL.md` und unter `references/` steht, liest ein Modell als Anweisung.

**1. Untergeschobene Extension unter `references/custom/`**

`SKILL.md` Z. 192 beschreibt Manifest-Auto-Detection. Beim Modus-Start werden alle `references/custom/@*/manifest.md` gescannt und ihre Trigger-Begriffe gegen den Nutzer-Input abgeglichen. Ein Treffer lädt die Extension, ohne Eintrag in `specforge.json` und ohne Rückfrage. Sichtbar wird das nur als Marker `[Extension geladen: @{name}]`.

Für die Trigger-Begriffe gibt es keine Regel. Weder Z. 192 noch `CONTRIBUTING-CHECKLISTS.md` ab Z. 20 schränken ein, was dort stehen darf. Die mitgelieferten Manifeste nutzen bereits generische Begriffe wie `Kreditinstitut`, `IT-Strategie` und `Finanzunternehmen`. Ein Manifest mit breit gewählten Triggern lädt bei fast jedem Input.

Der Custom Checker lädt laut Z. 379 über `references/custom/@*/**/*.md`, also rekursiv. Was in einem `@`-Paket liegt, wird gelesen, unabhängig davon, ob das Manifest es aufzählt.

Dazu kommt die `Pflicht-Abfrage bei Aktivierung` (`@dora/manifest.md` Z. 21, `@bait/manifest.md` Z. 24). Eine Extension darf Fragen definieren, die vor der ersten Prüfung gestellt werden. Sie erscheinen dem Nutzer in der Stimme des Skills.

Z. 186 sagt zu, dass Dateien in `references/custom/` bei Core-Updates nie überschrieben werden. Eine dort platzierte Datei überlebt jedes Update.

**2. `specforge.json` als zweiter Steuerpfad**

Die Datei liegt im Projekt des Nutzers, nicht in diesem Repo, steuert laut `SKILL.md` Z. 35 aber das Verhalten aller Modi. `custom_checklists` steht im Beispiel auf dem Glob `references/custom/*.md` (Z. 46). `severity_model.gate_mapping` (Z. 50 ff.) legt fest, welche F-Stufe zu FAIL wird. Über die Dispatch-Tabelle lassen sich neue Modi als `references/custom/mode-NN-name.md` registrieren (Z. 215). Wer diese eine Datei ändert, verschiebt Gate-Ergebnisse und hängt neue Anweisungsdateien ein.

**3. Dokumentierte Ladepfade als Zielliste**

Die Tabelle der Erweiterungspunkte (Z. 205 bis 218) nennt konkrete Pfade: `anti-patterns-custom.md`, `golden-principles-custom.md`, `nfr-custom.md`, `ears-patterns-custom.md`. Keiner davon liegt im Repo. Ihr Fehlen ist kein Defekt, Z. 222 bis 238 regelt das: optionale Referenzen werden mit dokumentierter Warnung übersprungen, nur vier als KRITISCH geführte Dateien erzwingen ein Gate FAIL, und die existieren alle. Sicherheitsrelevant ist die Gegenrichtung. Wer Schreibzugriff auf den Skill-Ordner erlangt, muss die Namen der Ladepfade nicht raten, sie stehen in `SKILL.md`.

**4. Fremdtext aus Web-Recherche und MCP**

`SKILL.md` Z. 481 verlangt, Web-Recherche "automatisch und ohne Ankündigung" durchzuführen, Z. 25 führt Web Search als reguläre Quelle. `references/01-specify.md` Z. 45 bis 60 beschreibt einen MCP-Kontext-Pre-Flight für Figma, Confluence, GitHub/GitLab und Jira, markiert als "optional, empfohlen". Sind die Tools verfügbar, sollen sie laut Z. 60 aktiv genutzt werden. Bedingung ist die Werkzeug-Verfügbarkeit, nicht eine Zustimmung des Nutzers. Ticket-Texte, Wiki-Seiten und Suchergebnisse landen damit im selben Kontext wie die Anweisungen des Skills. Angreifer ist, wer einen solchen Text verfasst, ohne je Zugriff auf dieses Repo gehabt zu haben.

**5. Ausgabe wird zur Eingabe**

`SKILL.md` Z. 449 schreibt alle Artefakte als Dateien ins Projekt. Die Liste enthält `specforge.json` (Z. 452) und `references/custom/@<scope>/manifest.md` samt `checklisten/*.md` (Z. 464 bis 466). Der Skill erzeugt also Dateien in genau den beiden Pfaden, die er beim nächsten Lauf als Steuerung liest. Ein Manifest aus Modellausgabe trägt Trigger-Begriffe und kann eine Pflicht-Abfrage enthalten. Fremdtext aus Punkt 4 und die Ladepfade aus Punkt 1 hängen darüber zusammen.

**6. Projektinhalte und Fremdtext in derselben Session**

`references/09-discover.md` Z. 17 lässt Module, APIs, Datenmodelle, Konfigurationen und Dependencies analysieren. Lesen von Projektinterna und Zufluss von Fremdtext treffen im selben Lauf zusammen. Was davon in eine externe Anfrage gerät, entscheidet der Client, nicht dieser Skill.

## Vertrauensgrenzen

Als vertrauenswürdig behandelt werden dürfen `SKILL.md` und `references/` aus diesem Repo in dem Zustand, den man selbst gelesen hat, sowie eine Kopie, deren Herkunft bekannt ist.

Nicht vertrauenswürdig, auch wenn die Dateien im selben Ordner liegen:

- alles unter `references/custom/`, das nicht selbst geschrieben wurde. Mitgeliefert sind nur `@dora` und `@bait`
- `specforge.json` aus einem fremden Projekt oder aus einem PR
- Suchergebnisse, MCP-Antworten, Ticket- und Wiki-Inhalte
- die erzeugten Artefakte, `specforge-audit.md` eingeschlossen. Sie sind Modellausgabe, kein Prüfergebnis

Der Abschnitt "Session-Isolation (KRITISCH)" in `SKILL.md` Z. 21 bis 29 ist keine Sicherheitsgrenze. Er verbietet Memories und Vorwissen über Nutzer und Projekte (Z. 29). Web Search (Z. 25) und `specforge.json` (Z. 27) stehen in derselben Liste als erlaubte Quellen. Technische Isolation gibt es nicht.

Die Grenze verläuft dort, wo eine Datei in den Skill-Ordner oder ins Projekt gelangt. Danach prüft sie niemand mehr.

## Bekannte Lücken

- **Keine Laufzeit-Isolation.** Der Skill läuft im Kontext des Clients mit dessen Rechten. Was der Client darf, darf der Skill.
- **Signatur und Prüfsumme fehlen.** Nichts im Repo erlaubt es, eine lokale Kopie gegen den Repo-Stand zu prüfen. Ohne Tags und Releases fehlt auch der Bezugspunkt.
- **Manipulierte Extensions fallen nicht auf.** Auto-Detection gleicht Trigger-Begriffe ab, sonst nichts. Es gibt keine Allowlist und keine Herkunftsprüfung. Woher eine `manifest.md` stammt und was in ihr steht, prüft niemand.
- **Beiträge laufen durch keine maschinelle Prüfung.** Es gibt kein `.github/` und keine CI. `CONTRIBUTING-CHECKLISTS.md` prüft ab Z. 20 und in der Checkliste Z. 140, ob Pflichtabschnitte vorhanden sind, nicht, was darin steht. Commit `bc09323` aus dem externen PR #2 hat `references/templates/spec-template.md` geändert, eine der vier in Z. 224 bis 228 als KRITISCH geführten Dateien, dazu `index.html` und `course.html`, also die veröffentlichte Seite.
- **Die Checklisten tragen kein Datum.** Weder `references/checklists/kritis-nfr.md` noch `references/custom/@dora/checklisten/dora-nfr.md` nennen einen Stand. Ob die zitierten Rechtsquellen aktuell sind, ist nicht zugesichert.
- **Die Kursseite lädt Schriften von Google.** `course.html` Z. 7 bis 9 bindet `fonts.googleapis.com` und `fonts.gstatic.com` ein. Wer die Seite unter der in `index.html` Z. 11 hinterlegten Adresse `godmodeai2025.github.io/specforge-ai-skill/` aufruft, verbindet sich zu Google.
- **Ungeprüft:** ob Private Vulnerability Reporting, Branch Protection und Review-Pflicht auf `main` aktiv sind. Aus dem Checkout ist das nicht sichtbar.

## Was dieses Projekt nicht leistet

- **Kein Prüfurteil.** F-Stufen und Gate-Ergebnisse (PASS, CONDITIONAL, FAIL) sind Ausgaben eines Sprachmodells. `references/enforcement/enforcement-engine.md` Z. 31 lehnt die Klassifikation an Anlage 6 zu § 27 PrüfbV an. Die Begriffe stammen aus der Aufsichtspraxis, das Ergebnis nicht.
- **Keinen Nachweis einer Risiko-Akzeptanz.** Bei CONDITIONAL fragt der Skill laut `SKILL.md` Z. 293 nur ab, ob sie dokumentiert ist. `enforcement-engine.md` Z. 24 stellt selbst klar, dass die Bestätigung keine Dokumentation ist. Nachprüfen kann der Skill das nicht.
- **Enforcement greift nur in der Session.** Jede Regel wirkt, solange das Modell ihr folgt. Einen Linter oder ein PR-Gate gibt es nicht, maschinell nachprüfbar ist davon nichts.
- **Aufsicht, interne Revision und Wirtschaftsprüfer** urteilen unabhängig von jedem Gate-Ergebnis aus diesem Skill. Der Skill ersetzt keine Prüfung.
- **Keine Rechtsberatung.** Die Checklisten zu KRITIS, NIS2, DORA und BAIT sind Arbeitsmaterial. `@bait` ist im Repo als Stub gekennzeichnet und deckt 8 Prüfpunkte ab, nach eigener Angabe von rund 80.
- **Es gilt der Haftungsausschluss der MIT-Lizenz** aus `LICENSE`. Eine Gewährleistung gibt es nicht.
