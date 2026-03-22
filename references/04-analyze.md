# Modus 4: Analyze — MECE-Konsistenzprüfung

**Methode:** MECE Principle — Mutually Exclusive, Collectively Exhaustive.
**Trigger:** tasks.md existiert. Empfohlen: immer nach Tasks und vor Implementierung.

## Profil-Steuerung

- **KRITIS:** Analyze Pflicht; Loop bis Blocker-frei UND GP-Score ≥ 9/10; Alle 5+1 Dimensionen; Custom Checks falls konfiguriert
- **Standard:** Analyze empfohlen; Loop bis GP-Score ≥ 8/10; Dimensionen 1–5; Custom optional
- **Startup:** Analyze optional; GP-Score ≥ 6/10; Dimensionen 1–3 Pflicht, 4–5 empfohlen

## Parallele Prüf-Agenten

Die Analyze-Phase nutzt spezialisierte Checker-Perspektiven, die unabhängig und parallel arbeiten. Jeder Checker hat einen klar begrenzten Scope.

| Checker | Prüft | Dimensionen | Referenzen laden |
|---------|-------|-------------|-----------------|
| **Consistency Checker** | Spec ↔ Plan ↔ Tasks Traceability | 1, 2, 3 | spec.md, plan.md, tasks.md |
| **GP Auditor** | Golden Principles Compliance | 4 | `references/checklists/golden-principles.md` |
| **Security Checker** | STRIDE + NFRs + NIS2/DSGVO | 5 | `references/checklists/stride-guide.md`, `references/checklists/kritis-nfr.md` |
| **Custom Checker** | Projektspezifische Checklisten | 6 (optional) | `references/custom/*.md` + `references/custom/@*/**/*.md` |

## Prüfkatalog (5+1 MECE-Dimensionen)

| # | Dimension | Prüft | Schweregrad bei Lücke |
|---|-----------|-------|-----------------------|
| 1 | Spec ↔ Plan | Jedes Requirement hat Entsprechung im Plan; ADRs vorhanden (GP-03) | MAJOR |
| 2 | Plan ↔ Tasks | Jede Plan-Komponente hat Task; Reihenfolge respektiert Abhängigkeiten | MAJOR |
| 3 | Spec ↔ Tasks | Jede Story durch Task abgedeckt; keine verwaisten Tasks/Requirements (AP-05, AP-07) | BLOCKER |
| 4 | Governance | GP-Compliance laut Profil; ExecPlans (GP-04); Folder Convention (GP-07); stale Marker (GP-06) | Schweregrad laut GP |
| 5 | Security & Compliance | STRIDE; NFRs; NIS2; DSGVO — Scope laut Profil | MAJOR (KRITIS: BLOCKER) |
| 6 | Custom | Projektspezifische Prüfregeln (nur wenn `custom_checklists` in specforge.json) | Konfigurierbar |

## Ablauf (deterministisch)

### Phase 4a: Vorbereitung
1. Profil aus specforge.json lesen
2. Scope bestimmen (welche Dimensionen Pflicht, welche optional)
3. Referenzdateien laden (siehe Checker-Tabelle oben)

### Phase 4b: Parallele Prüfung
Alle Checker arbeiten unabhängig. Jeder Checker erzeugt einen eigenständigen Befund-Report.

### Phase 4c: Konsolidierung
1. Checker-Reports zusammenführen
2. Bei Widersprüchen zwischen Checkern: höherer Schweregrad gewinnt
3. GP-Score berechnen: `Erfüllte GPs / Aktive GPs laut Profil`
4. Sortierung: BLOCKER → MAJOR → MINOR

## Output: Konsolidierter Analyze-Report (deterministisch)

```markdown
## Analyze-Report: [Feature-Name]
**Profil:** [KRITIS / Standard / Startup]
**Scope:** Dimensionen [1–6] / [1–5] / [1–3]

### Checker-Ergebnisse
| Checker | Status | Befunde (B/M/m) | Blocker |
|---------|--------|-----------------|---------|
| Consistency | ✅/⚠️/❌ | X/Y/Z | [Anzahl] |
| GP Auditor | [Score]/10 | X/Y/Z | [Anzahl] |
| Security | ✅/⚠️/❌ | X/Y/Z | [Anzahl] |
| Custom | ✅/n.a. | X/Y/Z | — |

### Detailbefunde
| # | Checker | Schweregrad | Befund | Betroffene Artefakte | Empfohlene Aktion |
|---|---------|------------|--------|---------------------|------------------|
| A-001 | Consistency | BLOCKER | Orphan Task T-005 | tasks.md | Spec-Referenz ergänzen |

### Gesamtbewertung
**Implementierungs-Readiness:** [Bereit / Überarbeitung nötig / Nicht bereit]
**GP-Score:** [X/10] (Schwelle: [Y/10])
**BLOCKER:** [Anzahl] | **MAJOR:** [Anzahl] | **MINOR:** [Anzahl]
```

## Phase Gate G4: Analyze → Implement (automatisch prüfen)

```
── Gate G4: Analyze → Implement ────────────
[ ] Keine BLOCKER-Befunde offen
[ ] GP-Score ≥ Profil-Schwelle (KRITIS: 9, Standard: 8, Startup: 6)
[ ] STRIDE vollständig (laut Profil)
[ ] Custom-Checks bestanden (falls vorhanden)
── Ergebnis: PASS | FAIL (Befunde) ─────────
```

## Re-Analyze-Loop (automatisch)

Nach Fixes erneut ausführen. Der Loop ist **automatisch** — nicht optional:

1. Analyze ausführen → Report erzeugen
2. Wenn FAIL: Findings beheben (Nutzer oder automatisch)
3. Erneut Analyze ausführen
4. Loop bis Gate G4 PASS

**Loop-Begrenzung:**
- Max. 5 Iterationen. Danach: Verbleibende Findings als KNOWN-ISSUES dokumentieren, Nutzer entscheidet
- Jede Iteration wird in der Analyze-Historie (Modus 8) protokolliert

**Re-Analyze-Trigger:**
- Automatisch nach Spec-Änderungen (GP-02)
- Automatisch nach Plan/Task-Änderungen
- Manuell durch Nutzer ("prüf nochmal", "analyze")

## Fehlerbehandlung

| Situation | Reaktion |
|-----------|---------|
| tasks.md fehlt | → Fehlermeldung: "tasks.md nicht gefunden — Plan (Modus 3) zuerst ausführen" |
| specforge.json fehlt | → Standard-Profil anwenden, Hinweis ausgeben |
| Referenzdateien fehlen | → Klare Fehlermeldung mit Pfad, betroffener Checker als FAIL |
| Profil-Wechsel mid-session | → Scope (Dimensionen, Schwellwerte) neu evaluieren |
| Widersprüchliche Checker-Ergebnisse | → Höherer Schweregrad gewinnt, Widerspruch dokumentieren |
| Mixed-Language Input | → Sprachverhalten gemäß Orchestrator |
| Loop terminiert nicht (>5 Iterationen) | → KNOWN-ISSUES dokumentieren, Nutzer informieren |

## GP-Mapping

| GP | Relevanz in Modus 4 |
|----|---------------------|
| GP-01 | Security Checker: Schema-Hygiene |
| GP-02 | Consistency Checker: Spec-before-Code |
| GP-03 | Consistency Checker: ADR-Vollständigkeit |
| GP-04 | GP Auditor: ExecPlan bei 5+ Dateien |
| GP-05 | GP Auditor: Invariant-Traceability |
| GP-06 | GP Auditor: Stale Marker |
| GP-07 | GP Auditor: Folder Convention |
| GP-08 | Meta: GP-Verstöße blockieren Gate G4 |
| GP-09 | Consistency Checker: Abhängigkeitsrichtung |
| GP-10 | GP Auditor: Tech-Debt dokumentiert |

## Abgrenzung zu Review (Modus 7)

- **Analyze** = Cross-Artefakt-Konsistenz (System als Ganzes)
- **Review** = Einzelne Requirements/Stories prüfen (Qualität einzelner Artefakte)

## Erzeugte Artefakte

| Artefakt | Pfad |
|----------|------|
| analyze-report.md | specs/use-cases/\<feature\>/ |
