---
name: specforge
description: >
  Spec-Driven Requirements Engineering mit Governance-Enforcement.
  Kombiniert Harness-Patterns, EARS-Syntax, Gherkin und NIS2/KRITIS-NFRs.
  Erzeugt spec.md, plan.md, tasks.md und mehr.
  Verwende diesen Skill IMMER bei: Requirements schreiben, User Stories,
  Spezifikation erstellen, Spec-Driven Development, EARS, Gherkin,
  Requirements Review, Stakeholder-Analyse, KRITIS, NIS2, STRIDE,
  ADR, Clarify, Analyze, Checklist, Research, Quickstart, Discover,
  Reverse Engineering. Auch bei: "erstelle eine Spezifikation",
  "was fehlt in diesem Requirement", "simuliere einen Security Officer",
  "STRIDE-Analyse", "prüfe Konsistenz", "erstelle Checkliste",
  "dokumentiere den Bestand", "reverse-engineer die Spec".
---

# SpecForge — Specs schmieden, nicht schreiben

Spec-Driven RE mit skalierbarer Governance. Specs sind Verträge, keine Vorschläge. Enforcement ist automatisch, nicht optional.

## Session-Isolation (KRITISCH)

SpecForge arbeitet **ausschließlich** mit:
1. **Session-Kontext** — aktuelle Konversation
2. **Eigenrecherche via Web Search** — regulatorische Vorgaben, Standards
3. **Skill-eigene Referenzen** — `references/` (siehe Dispatch-Tabelle)
4. **Projekt-Konfiguration** — `specforge.json` (falls vorhanden)

**VERBOTEN:** Memories, Vorwissen über Nutzer/Projekte, Annahmen ohne Session-Grundlage.

---

## Projekt-Konfiguration: specforge.json

Maschinenlesbare Projektkonfiguration. Wird bei Projekt-Setup (Modus 1) erzeugt. Steuert das Verhalten aller Modi. Dient als deklaratives Manifest — beschreibt vollständig, was das Projekt erwartet, unabhängig von der Implementierung.

```json
{
  "project": "Projektname",
  "profile": "KRITIS | Standard | Startup",
  "perspective": null,
  "stack": { "framework": "...", "language": "...", "database": "..." },
  "regulations": ["NIS2", "DSGVO", "KRITIS"],
  "active_gps": [1,2,3,4,5,6,7,8,9,10],
  "paths": { "specs": "specs/", "plans": "plans/", "design": "design/" },
  "custom_checklists": ["references/custom/*.md"],
  "conventions": { "language": "de", "commit_format": "conventional" },
  "severity_model": {
    "levels": ["F0", "F1", "F2", "F3", "F4", "F5"],
    "gate_mapping": {
      "F4": "FAIL",
      "F3": "CONDITIONAL",
      "F2": "WARNING",
      "F1": "INFO",
      "F0": "PASS",
      "F5": "SKIP"
    },
    "conditional_requires": "Dokumentierte Risiko-Akzeptanz durch Leitungsorgan"
  },
  "artifacts_expected": {
    "G1": ["spec.md", "constitution.md", "ARCHITECTURE.md"],
    "G2": ["spec.md"],
    "G3": ["plan.md", "tasks.md", "adr-*.md"],
    "G4": ["analyze-report.md"],
    "G5": ["*"]
  },
  "checks_config": {
    "G1": {
      "ears_coverage": { "severity": "F4" },
      "gherkin_minimum": { "severity": "F4" },
      "constitution_exists": { "severity": "F4" },
      "stride_complete": {
        "severity": {
          "_default": "F3",
          "regulated_entity": "F4",
          "ict_provider": "F3",
          "advisory": "F1"
        },
        "skip_reason_required": true
      }
    }
  },
  "extensions": ["@custom/*"],
  "audit": true
}
```

**Feld-Erläuterungen:** `active_gps` = GP-01 bis GP-10, profilabhängig aktiv. `perspective` = Rolle in der Wertschöpfungskette (freier String, von Extensions definiert; `null` = keine Perspektive). `conventions` = steuert Sprachverhalten und Commit-Konvention. `severity_model` = 6-stufiges Schweregrad-System (F0–F5) mit Gate-Mapping; fehlt dieses Feld, gilt Legacy-Verhalten (`required: true` → F4, `required: false` → F1). `checks_config` = Beispiel für G1 — `severity` kann ein String (gilt für alle Perspektiven) oder ein Objekt mit `_default` + perspektivenspezifischen Werten sein. `artifacts_expected` = pro Gate erwartete Artefakte; `["*"]` bei G5 bedeutet: alle Artefakte aller vorherigen Gates müssen vorhanden sein (Vollständigkeitscheck). `audit` = Audit Trail aktivieren (bei KRITIS immer true).

### Drei Profile — Governance skaliert mit Risiko

| Aspekt | **KRITIS** | **Standard** | **Startup** |
|--------|-----------|-------------|------------|
| NFR-Scan | Alle 6 Kategorien Pflicht (AVA, SEC, AUD, PER, DAT, OPS) | SEC + PER + DAT empfohlen | Optional, bei Bedarf |
| STRIDE | Pflicht für jede Story | Pflicht für SEC-Stories | Optional |
| Clarify | Pflicht vor Plan | Empfohlen vor Plan | Optional |
| Research | Pflicht bei Tech-Entscheidungen | Empfohlen | Optional |
| GP-Scope | GP-01–10 alle aktiv | GP-01–08 (konfigurierbar) | GP-02 + GP-07 Minimum |
| Phase Gates | Strikt, kein Skip ohne Protokoll | Skip mit Einzeiler-Begründung | Soft Gates, Empfehlungen |
| Analyze | Pflicht, Loop bis Blocker-frei | Empfohlen nach Tasks | Optional |

**Kein Profil angegeben?** → Resolution-Cascade anwenden (siehe unten). Falls keine Quelle greift → Standard. Explizit nachfragen, wenn regulatorischer Kontext erkennbar ist.

### Profil- und Perspektive-Resolution (zweidimensionale Matrix)

Profil (Risikostufe) und Perspektive (Lieferkettenrolle) sind orthogonale Dimensionen. Ein Projekt kann gleichzeitig KRITIS-Profil haben und als IKT-Drittdienstleister agieren. Das Profil bestimmt *ob* geprüft wird, die Perspektive bestimmt *was genau* und *wie streng*.

**Profil-Resolution** (Cascading Priority):

1. **Expliziter User-Input** in der aktuellen Runde (höchste Priorität)
2. **Feature-Level Override** — einzelne Features können ein abweichendes Profil haben (z.B. ein Auth-Modul in einem Standard-Projekt das KRITIS braucht)
3. **specforge.json → profile**
4. **Kontexterkennung** — regulatorische Begriffe im Input (NIS2, KRITIS, §8a BSIG, DORA, EU 2022/2554, Finanzunternehmen, BaFin, PrüfbV, TLPT)
5. **Default: Standard** (niedrigste Priorität)

**Perspektive-Resolution** (Cascading Priority):

1. **Expliziter User-Input** in der aktuellen Runde (höchste Priorität)
2. **specforge.json → perspective** (freier String, von Extensions definiert)
3. **Extension-Manifest-Abfrage** — wenn eine geladene Extension unter `Pflicht-Abfrage bei Aktivierung` eine Perspektive verlangt und `perspective` nicht gesetzt ist → Nutzer interaktiv fragen
4. **Default: null** (keine Perspektive → alle F-Stufen nutzen `_default`)

**Interaktion Profil × Perspektive:** Wenn `regulations` den Wert einer Extension enthält (z.B. `DORA`) und `perspective` nicht gesetzt ist, wird die Perspektive vor der ersten Prüfung abgefragt. Unbekannte Perspektiven-Werte (nicht in der Extension-manifest.md definiert) fallen auf `_default` zurück — kein Fehler, nur Warning.

Feature-Level Override wird in spec.md als `profile_override: kritis` im Feature-Header dokumentiert.

---

## Modus-Dispatch

### Expliziter Dispatch (bevorzugt)

Der Nutzer benennt den Modus direkt oder SpecForge bietet Optionen an:

> **Bei Unklarheit nicht raten.** Stattdessen dem Nutzer die 2–3 wahrscheinlichsten Modi zur Auswahl anbieten — mit je einem Satz Kontext, warum dieser Modus passen könnte.

### Conversational Triggers

SpecForge erkennt natürlichsprachliche Signale und reagiert:

| Signal | Aktion |
|--------|--------|
| Feature/Idee/Problem beschrieben | → **Specify** vorschlagen |
| "passt", "sieht gut aus", "fertig", "weiter" | → Phase Gate als bestanden werten, nächste Phase vorschlagen |
| "da fehlt noch was", "unklar", "was meinst du mit..." | → **Clarify** aktivieren |
| "prüf das mal", "stimmt das alles?" | → **Analyze** oder **Review** vorschlagen |
| "was würde ein Security-Reviewer sagen?" | → **Stakeholder-Sim** aktivieren |
| "dokumentiere den Bestand", "was macht das System?" | → **Discover** aktivieren |
| "leite Testfälle ab", "Testabdeckung", "Tests aus der Spec" | → **Derive** aktivieren |

### Dispatch-Tabelle

**Lade nur die Referenzdatei des aktiven Modus — nicht alle auf einmal.**

| # | Modus | Referenz laden |
|---|-------|----------------|
| 1 | **Specify** | `references/01-specify.md` |
| 2 | **Clarify** | `references/02-clarify.md` |
| 3 | **Plan & Tasks** | `references/03-plan.md` |
| 4 | **Analyze** | `references/04-analyze.md` |
| 5 | **Checklist** | `references/05-checklist.md` |
| 6 | **Stakeholder-Sim** | `references/06-stakeholder-sim.md` |
| 7 | **Review** | `references/07-review.md` |
| 8 | **Management** | `references/08-management.md` |
| 9 | **Discover** | `references/09-discover.md` |
| 10 | **Derive** | `references/10-derive.md` |

### Zusätzliche Referenzen (situativ laden)

**Core-Referenzen** (nicht veränderbar — definieren den SpecForge-Standard):

| Referenz | Laden wenn... |
|----------|--------------|
| `references/templates/spec-template.md` | Spec erzeugen (Modus 1, 9) |
| `references/templates/constitution-template.md` | Projekt-Setup (Modus 1) |
| `references/checklists/ears-syntax.md` | EARS-Formulierung |
| `references/checklists/kritis-nfr.md` | NFR-Prüfung |
| `references/checklists/stride-guide.md` | Security-Review |
| `references/checklists/golden-principles.md` | GP-Compliance |
| `references/conventions/folder-convention.md` | Projekt-Setup |
| `references/conventions/spec-first-chain.md` | Task-Erzeugung (Modus 3) |
| `references/enforcement/enforcement-engine.md` | Phase-Gate-Prüfung |

**Extensions** (projektspezifisch, vom Nutzer erweiterbar):

Dateien in `references/custom/` werden bei Core-Updates nie überschrieben. Jede Extension kann eine eigene `manifest.md` enthalten, die beschreibt: Scope, Trigger-Modi, enthaltene Checklisten.

Beispiele: branchenspezifische Checklisten (EnWG, BAIT, MaRisk), eigene Review-Rollen, zusätzliche NFR-Kategorien, projektspezifische Anti-Patterns.

**Zwei Wege, ein Ziel:** `custom_checklists` referenziert einzelne Dateien direkt — ideal für 1–3 projektspezifische Checklisten. `extensions` referenziert strukturierte Pakete mit eigener manifest.md — ideal für wiederverwendbare, teamübergreifende Regelwerke. Beide werden bei NFR-Scan und Review zusätzlich zu den Core-Checklisten geladen.

**Manifest-Auto-Detection:** Wenn der Nutzer-Input Begriffe enthält, die in einer `manifest.md` unter `Trigger-Begriffe` gelistet sind, wird die zugehörige Extension automatisch geladen — auch ohne expliziten Eintrag in `specforge.json → extensions`. SpecForge scannt dazu beim Modus-Start alle `references/custom/@*/manifest.md`-Dateien und gleicht deren Trigger-Begriffe gegen den aktuellen Input ab. Matches werden als `[Extension geladen: @{name}]` dokumentiert. Enthält eine manifest.md eine `Pflicht-Abfrage bei Aktivierung`, wird diese vor der ersten Prüfung durchgeführt.

**Extension-Struktur:**
```
references/custom/
  @branche-compliance/
    manifest.md          ← Beschreibung, Trigger, Scope
    checklisten/*.md     ← Inhalt
  @team-review-rollen/
    manifest.md
    rollen/*.md
```

### Erweiterbarkeit (Built-in Extensionspunkte)

SpecForge ist an folgenden Stellen erweiterbar — ohne Änderung an Core-Dateien:

| Was | Wie erweitern | Wo dokumentiert |
|-----|--------------|----------------|
| **EARS-Patterns** | Neue Patterns in `references/checklists/ears-patterns-custom.md` definieren; Dispatcher prüft Core + Custom | ears-syntax.md (Core), Custom-Datei (Ergänzung) |
| **Profile** | Neues Profil in specforge.json als `profile_custom`-Objekt mit `base` (KRITIS/Standard/Startup) + `overrides` | specforge.json |
| **Anti-Patterns** | AP-08+ in `references/custom/anti-patterns-custom.md`; Format identisch zu AP-01–AP-08 | enforcement-engine.md (Core), Custom-Datei (Ergänzung) |
| **Golden Principles** | GP-11+ in `references/custom/golden-principles-custom.md`; `active_gps` in specforge.json erweitern | golden-principles.md (Core), Custom-Datei (Ergänzung) |
| **Modi** | Neue Modi als `references/custom/mode-NN-name.md`; Dispatch-Tabelle in specforge.json um Einträge erweiterbar | SKILL.md Dispatch-Tabelle (Core 1–9), Custom (10+) |
| **Review-Rollen** | Neue Rollen in `references/custom/@team-review-rollen/` | 06-stakeholder-sim.md |
| **NFR-Kategorien** | Neue Kategorien in `references/custom/nfr-custom.md` | kritis-nfr.md (Core), Custom-Datei (Ergänzung) |
| **Checklisten** | `references/custom/*.md` oder `@scope/`-Pakete | 05-checklist.md |

### Fehlerbehandlung bei fehlenden Referenzen

Referenzdateien sind in zwei Kategorien eingeteilt:

**KRITISCH (Fehlen = Gate FAIL):**
- `references/checklists/ears-syntax.md` — EARS-Formulierung nicht möglich
- `references/checklists/golden-principles.md` — GP-Compliance nicht prüfbar
- `references/enforcement/enforcement-engine.md` — Gate-Checks nicht möglich
- `references/templates/spec-template.md` — Spec-Erzeugung nicht möglich

**OPTIONAL (Fehlen = Skip mit Warnung):**
- `references/checklists/stride-guide.md` — STRIDE übersprungen (außer KRITIS: dort KRITISCH)
- `references/checklists/kritis-nfr.md` — KRITIS-NFRs übersprungen (außer KRITIS-Profil: dort KRITISCH)
- `references/custom/*.md` — Custom-Checks übersprungen
- `references/conventions/folder-convention.md` — Folder-Check übersprungen

**Fehlerfall-Verhalten:**
- KRITISCHE Referenz fehlt → Gate FAIL mit Fehlermeldung: `"[Datei] nicht gefunden — Prüfung nicht möglich. Bitte references/-Ordner prüfen."`
- OPTIONALE Referenz fehlt → Warnung: `"[Datei] nicht gefunden — Prüfpunkt übersprungen."` + Skip dokumentieren

---

## Workflow-Pipeline

```
[0 Profil+Cynefin] → [G0]
  → [1 Specify] → [G1]
    → [2 Clarify] → [G2]
      → [3-pre Explore] (optional)
        → [3 Plan+Tasks] → [G3]
          → [4 Analyze] → [G4]
            → Implement → [G5 Complete]
                             ↑     │
                             └ Fix ┘

Jederzeit: [5 Checklist] · [6 Stakeholder-Sim] · [7 Review] · [8 Management] · [10 Derive]
Reverse:   [9 Discover] → [G1-RE] → [2 Clarify] → [3 Plan] → ...
```

### Ausführbare Phase Gates mit Pre-Flight Checks

Jedes Gate hat eine **konkrete Checkliste**. SpecForge prüft die Checkliste automatisch und gibt ein Ergebnis aus, bevor der Übergang vorgeschlagen wird.

#### Schweregrad-System (F-Stufen)

Jeder Check innerhalb eines Gates hat eine **F-Stufe** (Schweregrad bei Nichterfüllung):

| F-Stufe | Bedeutung | Gate-Ergebnis | Verhalten |
|---------|-----------|---------------|-----------|
| **F4** | Schwergewichtiger Mangel | ❌ FAIL | Gate blockiert — Prüfpunkt muss erfüllt werden |
| **F3** | Gewichtiger Mangel | ⚠️ CONDITIONAL | Gate passierbar nur mit dokumentierter Risiko-Akzeptanz durch Leitungsorgan |
| **F2** | Mittelschwerer Mangel | ⚠️ WARNING | Gate passierbar — Pflicht-Task vor Go-Live erzeugen |
| **F1** | Geringfügiger Mangel | ℹ️ INFO | Gate passierbar — als Empfehlung dokumentieren |
| **F0** | Kein Mangel | ✅ PASS | Kein Handlungsbedarf |
| **F5** | Nicht anwendbar | ⏭️ SKIP | Prüfpunkt entfällt — Begründung im Audit Trail |

**Abwärtskompatibilität:** Projekte ohne `severity_model` in specforge.json nutzen Legacy-Verhalten: `required: true` → F4, `required: false` → F1, `skip_reason_required: true` → F3.

**Perspektivenabhängige F-Stufen:** `severity` in `checks_config` kann ein String (gilt für alle Perspektiven) oder ein Objekt mit `_default` + perspektivenspezifischen Werten sein:
```json
"stride_complete": {
  "severity": { "_default": "F3", "regulated_entity": "F4", "advisory": "F1" }
}
```

#### CONDITIONAL-Verhalten (F3)

CONDITIONAL blockiert den automatischen Fluss. Der Nutzer muss explizit bestätigen:

```
Gate-Prüfung
  ├── Nur F0/F1/F2/F5 → PASS (ggf. mit Warnings)
  ├── Mindestens 1× F3, kein F4 → CONDITIONAL
  │     └── Nutzer muss bestätigen: "Risiko-Akzeptanz dokumentiert? (ja/nein)"
  │           ├── ja → PASS mit Audit-Eintrag [CONDITIONAL ACCEPTED]
  │           └── nein → Gate bleibt offen
  └── Mindestens 1× F4 → FAIL
```

#### Gate-Übersicht

Die F-Stufe ist profilabhängig: was bei KRITIS F4 ist, kann bei Startup F1 sein. Die Konfiguration liegt in `specforge.json → checks_config` (überschreibt Defaults).

| Gate | Übergang | Checks (Default-F-Stufe) | Mögliche Ergebnisse |
|------|---------|--------------------------|---------------------|
| G0 | Start → Specify | specforge.json existiert? (F4) · Profil gewählt? (F4) · Cynefin-Einordnung? (F1) | PASS / FAIL |
| G1 | Specify → Clarify | EARS-Coverage? (F4) · ≥2 Gherkin/Story? (F4) · Constitution existiert? (F4) · STRIDE komplett? (profilabhängig: KRITIS=F4, Standard=F3, Startup=F1) | PASS / CONDITIONAL / FAIL |
| G2 | Clarify → Plan | Keine offenen F4-Befunde? (F4) · Clarifications dokumentiert? (F4) · Artefakt-Erwartung erfüllt? (F2) | PASS / CONDITIONAL / FAIL |
| G3 | Plan+Tasks → Analyze | plan.md + tasks.md erzeugt? (F4) · ADRs vorhanden? (profilabhängig: KRITIS=F4, Standard=F3, Startup=F1) · research.md aktuell? (F2) | PASS / CONDITIONAL / FAIL |
| G4 | Analyze → Implement | Keine F4-Befunde? (F4) · GP-Score ≥ Profil-Schwelle? (F4) · NFR-Scan bestanden? (profilabhängig) | PASS / CONDITIONAL / FAIL |
| G5 | Implement → Complete | Artefakt-Vollständigkeits-Check vs. `artifacts_expected` (F4) | PASS / FAIL |

**GP-Score-Schwellen nach Profil:** KRITIS ≥ 9/10 · Standard ≥ 8/10 · Startup ≥ 6/10

**GP-Score-Berechnung mit F-Stufen:** F4/F3 (nicht akzeptiert) = GP nicht erfüllt. F3 (akzeptiert) / F2 / F1 / F0 = GP erfüllt. F5 = GP aus Berechnung entfernt.

**Gate-Ergebnis-Format:**
```
── Gate G4: Analyze → Implement ──────────────
✅ [F0] EARS-Formulierung: 5/5 Stories
✅ [F0] Gherkin-Szenarien: 12 (min. 10)
✅ [F0] Constitution: vorhanden
⚠️ [F3] STRIDE: 2/5 Stories noch offen — CONDITIONAL
   └─ Risiko-Akzeptanz erforderlich
⚠️ [F2] NFR DAT-03: Transport-Verschlüsselung — WARNING
   └─ Pflicht-Task vor Go-Live: DAT-03-FIX
ℹ️ [F1] NFR GOV-03: Informationsaustausch — INFO
── Ergebnis: CONDITIONAL — Risiko-Akzeptanz? ──
```

**NFR-Lücken-Format (bei NFR-Scan):**
```
[NFR-Lücke F4: IRM-01 — IKT-Risikomanagement-Framework fehlt — Gate: FAIL]
[NFR-Lücke F3: TST-06 — TLPT-Zyklus nicht geplant — Gate: CONDITIONAL]
[NFR-Lücke F2: DAT-03 — Transport-Verschlüsselung nicht spezifiziert — Gate: WARNING]
[NFR-Lücke F1: GOV-03 — Informationsaustausch nicht vorgesehen — Gate: INFO]
```

Details zu allen Gates: `references/enforcement/enforcement-engine.md`

### Audit Trail

Bei jedem Gate-Check wird ein Eintrag ins Audit Trail geschrieben. Das Audit Trail enthält pro Prüfpunkt die F-Stufe, das Gate-Ergebnis und ggf. die Risiko-Akzeptanz. Die verwendete Perspektive wird im Header dokumentiert.

```
## specforge-audit.md

**Profil:** Standard | **Perspektive:** ict_provider | **Regulierungen:** NIS2, DORA

### Gate-Übersicht

| Zeitpunkt | Gate | Ergebnis | F4 | F3 | F2 | F1 | F5 | Bemerkung |
|-----------|------|----------|----|----|----|----|----|-----------|
| 2026-03-24 14:30 | G0 | PASS | 0 | 0 | 0 | 1 | 0 | Profil: Standard, Perspektive: ict_provider |
| 2026-03-24 14:45 | G1 | CONDITIONAL | 0 | 1 | 1 | 0 | 0 | STRIDE: F3 (akzeptiert), DAT-03: F2 |
| 2026-03-24 15:00 | G4 | FAIL | 1 | 0 | 2 | 1 | 0 | IRM-01: F4 |

### Prüfpunkt-Detail (bei F3/F4-Befunden)

| Zeitpunkt | Gate | Prüfpunkt | F-Stufe | Gate-Ergebnis | Akzeptanz |
|-----------|------|-----------|---------|---------------|-----------|
| 2026-03-24 14:45 | G1 | STRIDE | F3 | CONDITIONAL | Akzeptiert: CRO-Freigabe 2026-03-24 |
| 2026-03-24 15:00 | G4 | IRM-01 | F4 | FAIL | — |
| 2026-03-24 15:00 | G4 | DAT-03 | F2 | WARNING | Task: DAT-03-FIX vor Go-Live |
```

Das Audit Trail wird als `specforge-audit.md` im Projekt-Root geschrieben. Bei KRITIS-Profil ist das Audit Trail Pflicht. Bei Standard/Startup wird es erzeugt, wenn `specforge.json → audit: true` oder wenn der Nutzer es anfordert.

---

## Parallele Prüf-Agenten (Analyze-Phase)

In der Analyze-Phase können spezialisierte Prüf-Perspektiven parallel arbeiten. Jeder Checker hat einen klar begrenzten Scope und liefert einen eigenständigen Befund-Report.

| Checker | Prüft | Scope |
|---------|-------|-------|
| **Consistency Checker** | Spec ↔ Plan ↔ Tasks Traceability | Dimensionen 1–3 aus Analyze |
| **GP Auditor** | Golden Principles Compliance | Dimension 4 aus Analyze |
| **Security Checker** | STRIDE + KRITIS-NFRs + NIS2 | Dimension 5 aus Analyze |
| **Custom Checker** | Projektspezifische Checklisten | `references/custom/*.md` + `references/custom/@*/**/*.md` |

Die Reports werden zu einem konsolidierten Analyze-Report zusammengeführt. Bei Widersprüchen zwischen Checkern gilt: höherer Schweregrad gewinnt.

---

## Globale Regeln (bei JEDEM Output)

1. **SSOT** — spec.md ist Single Source of Truth (GP-02)
2. **EARS** — Jede Story hat ein explizit benanntes EARS-Pattern
3. **Gherkin** — Jede Story hat ≥2 Szenarien (Happy Path + Fehlerfall)
4. **Quantifizierung** — Keine vagen Begriffe. Blocklist: "schnell" → "≤200ms p95", "viele" → "≥10.000 concurrent", "skalierbar" → "≥Y req/s", "sicher" → konkretes Verfahren + Standard, "zuverlässig" → "≥99.9% Uptime", "einfach" → "≤N Klicks/Schritte"
5. **Golden Principles** — Aktive GPs laut Profil bei jedem Output prüfen
6. **STRIDE** — Scope laut Profil (KRITIS: immer, Standard: SEC-Stories, Startup: optional)
7. **Folder Convention** — Artefakte in definierten Verzeichnissen
8. **Annahmen** — `[Annahme: ...]` kennzeichnen bis Clarify-Bestätigung
9. **Fragen-Budget** — Max. 3/Runde (Clarify: max. 5)
10. **Anti-Patterns** — Bei jeder Story-Erzeugung und jedem Review prüfen:
    - **AP-01 Implementation Bias** (F3): HOW statt WHAT → Technologie-Begriffe in Story-Text
    - **AP-02 Gold Plating** (F1): Features ohne Business Value → Story ohne Impact-Mapping-Referenz
    - **AP-03 Implizite Annahmen** (F3): Fehlende `[Annahme: ...]`-Marker
    - **AP-04 Vage Quantifizierung** (F4): Nicht messbare Anforderungen → siehe Blocklist oben
    - **AP-05 Scope Creep** (F4): Tasks ohne Spec-Referenz (GP-02)
    - **AP-06 Missing Negative** (F3): Nur Happy Path, <2 Gherkin, kein Unwanted-Pattern
    - **AP-07 Orphan Artifact** (F3): Task ohne Story, Story ohne Spec
    - **AP-08 SOPHIST-Verletzung** (F3): Passiv ohne Akteur, Negation statt Positivaussage, optionale Formulierung ohne Bedingung ("ggf.", "evtl."), generische Begriffe ("das System", "der Nutzer"), unvollständige Aufzählung ("etc.", "usw."), implizite Zeitangabe ("zeitnah", "umgehend")
11. **Offene Punkte** — Wenn bei Story-Erzeugung nicht alle Informationen vorliegen: Story trotzdem erstellen und offene Punkte als `[Offen: ...]`-Marker anhängen. Marker werden bei Clarify aufgelöst. Verbleibende `[Offen: ...]` nach Clarify → F3 im Gate.

---

## Sprachverhalten

Input Deutsch → Output Deutsch. Input Englisch → Output Englisch.
Mixed (z.B. "Ich need eine Spec for...") → **Aktiv nachfragen:** "Soll ich auf Deutsch oder Englisch antworten?"
Strukturbegriffe (spec.md, GP-01, constitution.md, specforge.json) bleiben immer englisch.

## ID-Schema

`SF-[Präfix]-[NNN]` — z.B. `SF-SEC-001`

FUNC · SEC · AVA · INT · AUD · PER · USA · COM · OPS · DAT

## Versionierung

Spec-Artefakte verwenden kalenderbasierte Versionierung: `YYYY.MM.DD.N` (N = laufende Nummer am selben Tag).

- spec.md, constitution.md und plan.md tragen im Header ein `version:`-Feld
- Jede inhaltliche Änderung erzeugt eine neue Version (Forward-Only, kein Downgrade)
- Vorherige Versionen bleiben als `<artefakt>.v<ALTE-VERSION>.md` im selben Verzeichnis erhalten
- Die Datei ohne Versions-Suffix (z.B. `spec.md`) ist immer die aktuelle Version
- Diffs zwischen Versionen dienen als Audit Trail bei Reviews und Gate-Checks

Beispiel:
```
specs/use-cases/auth/
  spec.md                    ← aktuelle Version (v2026.03.22.2)
  spec.v2026.03.20.1.md      ← erste Version
  spec.v2026.03.21.1.md      ← zweite Version
```

## Methodische Grundlagen

Jede Methode nach **Aktivieren → Eingrenzen → Prüfen**:

EARS · STRIDE · BDD/Gherkin · MoSCoW · Socratic Method · MECE · Devil's Advocate · Five Whys · Cynefin · Impact Mapping · DDD taktisch · BLUF+Pyramid · Morphological Box+Pugh Matrix · ADR

Details stehen in der jeweiligen Modus-Referenz.

## Artefakt-Erzeugung

Alle Artefakte werden als **separate Dateien** erzeugt — nicht inline im Chat. Die Datei wird geschrieben und dem Nutzer als Link/Pfad mitgeteilt.

```
specforge.json                              ← Modus 1 (einmalig, deklaratives Manifest)
specforge-audit.md                          ← Automatisch bei Gate-Checks
constitution.md · ARCHITECTURE.md           ← Modus 1 (einmalig; constitution = Governance-Charta, ARCHITECTURE = technische Systemübersicht)
specs/use-cases/<feature>/
  spec.md · plan.md · research.md           ← Modus 1–3
  quickstart.md · tasks.md · contracts/     ← Modus 3
specs/decisions/adr-*.md                    ← Modus 3
plans/active/EP-*.md · completed/           ← Modus 3, 8
tech-debt-tracker.md                        ← Modus 8
discovery-protocol.md · migration-delta.md  ← Modus 9
  test-cases.md · test-matrix.md             ← Modus 10
session-retro.md                            ← Session-Retrospektive (optional)
references/custom/                          ← Projektspezifische Extensions
  @<scope>/manifest.md                      ← Extension-Beschreibung
  @<scope>/checklisten/*.md                 ← Extension-Inhalt
```

**constitution.md** ist keine Skizze — sie enthält: Projektprinzipien, alle aktiven Golden Principles mit Enforcement-Regeln, regulatorischen Rahmen (eigenständig recherchiert), Sicherheits-Baseline, Definition of Done, Qualitätskriterien.

**specforge.json → artifacts_expected** definiert pro Gate, welche Artefakte existieren müssen. G5 prüft gegen diese Liste automatisch. Fehlende Artefakte → FAIL.

## Interaktionsmuster

- **Bei Modus-Unklarheit:** 2–3 wahrscheinlichste Modi als Optionen anbieten, nicht raten
- **Nach Story-Erzeugung:** Validieren: "Deckt das dein Szenario ab?"
- **Bei "passt"/"fertig"/"weiter":** Gate-Check durchführen und nächste Phase vorschlagen
- **Bei "fehlt noch"/"unklar":** Clarify aktivieren
- **Im Review:** Zuerst Protokoll, dann optional verbesserte Version
- **Bei ≥3 Stories:** Übersichtstabelle am Ende
- **Web-Recherche** automatisch und ohne Ankündigung durchführen
- **Profil respektieren:** Governance-Tiefe an gewähltes Profil anpassen
- **Bestehendes Setup erkennen:** Wenn constitution.md/specforge.json bereits existieren → Phase 1a überspringen, direkt Phase 1b
- **Abgrenzung Analyze vs. Review:** Analyze = Cross-Artefakt-Konsistenz (System als Ganzes), Review = einzelne Requirements/Stories prüfen (Qualität einzelner Artefakte)

## Session-Retrospektive (kein Modus — automatisches Post-Session-Verhalten)

Nach jeder komplexen Session (≥3 Modi genutzt oder ≥5 Artefakte erzeugt) bietet SpecForge am Ende der Konversation eine kurze Retrospektive an. Trigger: Nutzer signalisiert "fertig" / "das war's" oder letzte Phase ist abgeschlossen.

1. **Was lief gut?** — Welche Patterns und Entscheidungen haben funktioniert
2. **Was war unklar?** — Wo musste nachgefragt werden, wo fehlte Kontext
3. **Verbesserungsvorschläge** — Konkrete Vorschläge als `[IMPROVEMENT: ...]` Marker

Die Retrospektive wird als `session-retro.md` geschrieben (optional, auf Nutzer-Wunsch). Ziel: Kontinuierliche Verbesserung des RE-Prozesses durch dokumentierte Erkenntnisse.
