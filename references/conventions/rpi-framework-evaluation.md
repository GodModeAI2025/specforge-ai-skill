# RPI Framework Evaluation (Dexter Horthy Methodik)

Dieses Dokument definiert, wie SpecForge die Wirksamkeit der integrierten RPI-Prinzipien (Research -> Plan -> Implement) misst, evaluiert und daraus lernt.

## 1. Getestete Hypothesen

Mit der Integration des RPI-Frameworks testen wir kontinuierlich folgende vier Kernhypothesen:

* **Hypothese 1 (Grounding durch Research Summary):** Wenn der Ist-Zustand explizit am Anfang der `plan.md` (ohne Feature-Ticket-Bias) zusammengefasst wird, sinkt die Rate an "confident garbage" (Halluzinationen von APIs/Modulen), da der Kontext im Kontextfenster frisch aktiviert wurde.
* **Hypothese 2 (Alignment durch Outline):** Wenn vor dem Detailplan zwingend eine High-Level-Outline zur Freigabe präsentiert wird, reduzieren wir Token-Verschwendung und Frustration, da Architektur-Irrwege frühzeitig korrigiert werden ("Back-and-Forth").
* **Hypothese 3 (Prompt-Diet & Execution Rules):** Wenn strikt verboten ist, mehr als 40 Instruktionen auf einmal auszuführen (sequenzielle Stopps erzwungen), steigt die Regeleinhaltung (Compliance) bei komplexen Checklisten (Gate-Checks, EARS), da das "Context Overflow"-Problem umgangen wird.
* **Hypothese 4 (Plan Fidelity / Anti-Drift):** Wenn im Review und Gate G5 ein expliziter Abgleich zwischen Code (Diff) und `plan.md` verlangt wird (Abweichungen = F3 CONDITIONAL), verhindern wir eigenmächtiges "Vibe-Coding" während der Ausführung.

## 2. Zu überwachende Risiken (Monitoring)

Während der Nutzung (insbesondere in der Session-Retro) müssen folgende Aspekte kritisch im Auge behalten werden:

* **Respektiert das LLM die "Prompt Diet"?** (Gefahr der "Eager Execution")
  Stoppt der Agent wirklich und wartet auf das Back-and-Forth, oder ignoriert er die Stopp-Anweisungen und generiert den Plan samt Outline in einem Rutsch?
* **False-Positives beim Plan Fidelity Check:**
  Bewertet das System "Drift" zu streng? Wenn sinnvolles Refactoring betrieben wird (z.B. Auslagern einer Helper-Funktion), das nicht im Plan stand – nervt der F3-Befund den Nutzer durch Alert Fatigue?
* **Friction vs. Safety (Outline-Overhead):**
  Ist der Zwang zur Outline bei trivialen Tasks (z.B. "Tippfehler fixen") zu viel Overhead? Sind Nutzer genervt von ständigen Freigabe-Schleifen?
* **Loop-Gefahr beim Iterativen Research:**
  Erkennt der Agent präzise, wann Kontext fehlt, um in Modus 9 (Discover) zurückzuspringen, oder verfängt er sich in Endlosschleifen zwischen Plan und Research?

## 3. Lern- & Feedback-Schleifen (Skill-Improvement)

Um den Skill weiter zu verbessern, nutzen wir folgende mechanische Metriken und Feedback-Kanäle:

* **Auswertung der `specforge-audit.md` (Lokal & Global):**
  Dieses Audit-Log protokolliert alle Gate-Checks. Scheitert Gate G5 (Implementierung) extrem oft an "Plan Fidelity" (F3), wissen wir: Entweder sind die Pläne nicht detailliert genug, oder das LLM ignoriert sie systematisch.
* **Erweiterte `session-retro.md`:**
  Am Ende von Sessions müssen die Nutzer/Agenten explizit dokumentieren, ob die RPI-Grenzen durchbrochen wurden (z.B. `[IMPROVEMENT: Agent hat ungefragt Code generiert]`). Dies dient als primäre Datenquelle für Prompt-Anpassungen.
* **Skill-Forge Auto-Modus (Overnight-Runs):**
  Durch autonome Testläufe über Nacht (Spezifikation + Implementierung von Testprojekten) messen wir den Erfolg. Metriken: **GP-Score** und die **Assertion Pass Rate** der Unit-Tests. Bei funktionierendem RPI muss die Architektur stabiler und der Code fehlerfreier sein als ohne RPI.

## 4. Langfristige Strategie: Harte Plugins (Hooks) statt Skill-Prompts

Ein LLM-Prompt (Skill) ist ein "weicher" Vertrag – der Agent kann ihn im Eifer des Gefechts "vergessen". Die wichtigsten Erkenntnisse aus dem Dexter-Horthy-Vortrag und dem SpecForge-Design sind so geschäftskritisch, dass sie künftig auf die Plattform-Ebene (als Plugin/Code-Hook) gehoben werden sollten:

1. **Der Plan Fidelity Diff-Checker:**
   * *Warum:* LLMs sind schlecht darin, exakte Datei-Diffs gegen eine Markdown-Liste zu validieren.
   * *Plugin-Idee:* Ein Hook in der Ausführungs-Engine. Bevor eine Datei via `Write/Edit` geschrieben wird, prüft ein hart codiertes Plugin (AST-Parser oder Regex), ob diese Datei explizit in der `plan.md` freigegeben wurde. Wenn nicht → harter System-Blocker.
2. **State Machine für die "Prompt Diet" (Phasen-Orchestrierung):**
   * *Warum:* Dem LLM zu sagen "Bitte stoppe hier und warte auf den User" ist extrem fehleranfällig.
   * *Plugin-Idee:* Ein SpecForge-Plugin orchestriert die Phasen (Research → Outline → Plan → Implement). Das Plugin injiziert dem Agenten jeweils *nur* den Prompt für die aktuelle Phase. Der Agent kann technisch gar nicht in die nächste Phase springen, bis der Nutzer "Approve Outline" klickt.
3. **Harte Gate-Checks (Enforcement Engine):**
   * *Warum:* Aktuell bittet der Skill den Agenten, sich selbst zu bewerten ("Prüfe, ob du vage Wörter wie *schnell* genutzt hast"). Das führt zu Halluzinationen ("Ich habe keine vagen Wörter genutzt" – obwohl er es tat).
   * *Plugin-Idee:* Ein Linter-Plugin (ähnlich wie ESLint), das bei jedem Speichern der `spec.md` lokal läuft und deterministisch auf die Blocklist-Wörter, EARS-Syntax und SOPHIST-Regeln prüft. Erst wenn der Linter "Grün" gibt, darf das Phase Gate passiert werden.
4. **Isoliertes Research (Kontext-Maskierung):**
   * *Warum:* Selbst wenn wir dem Agenten sagen "Ignoriere das Feature-Ticket für einen Moment", liegt es im Chat-Kontext und erzeugt einen unbewussten Bias im LLM.
   * *Plugin-Idee:* Ein Hook, der für die Discover/Research-Phase einen temporären Sub-Agenten spawnt (`spawn_session`), dem das ursprüngliche Feature-Ticket **nicht** übergeben wird. Er bekommt nur den Auftrag: "Lies das Repo und dokumentiere es". Erst wenn sein Report fertig ist, wird er mit dem Ticket im Haupt-Thread zusammengeführt.
