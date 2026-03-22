# Modus 5: Checklist — Custom Quality Checklists

**Trigger:** "Checklist", "DoR", "Quality Gate", "Prüfliste", "Unit Tests für Prosa"
**Methode:** Profilabhängige Checklisten-Generierung mit deterministischer Struktur.

## Profil-Steuerung

- **KRITIS:** Alle Prüfpunkte inkl. regulatorischer Compliance (NIS2, DSGVO, KRITIS-NFRs); Custom-Checklisten Pflicht falls vorhanden
- **Standard:** Kernprüfpunkte; regulatorisches optional; Custom-Checklisten empfohlen
- **Startup:** Nur funktionale Kernprüfpunkte; regulatorisches nur bei expliziter Anfrage

## Checklist-Typen

| Typ | Zweck | Prüft gegen | Pflicht-Referenzen |
|-----|-------|-------------|-------------------|
| **A — Spec-Readiness** | Ist spec.md bereit für Plan-Phase? | Gate G1 Checks | ears-syntax.md, golden-principles.md |
| **B — Plan-Readiness** | Sind plan.md + tasks.md bereit für Implementierung? | Gate G3 Checks | spec-first-chain.md, golden-principles.md |
| **C — Custom** | Nutzer definiert Prüfaspekt | Kontext-abhängig | Nutzer-Input + Constitution |
| **D — Domain** | Branchenspezifische Compliance | Regulatorische Checklisten | references/custom/*.md |

### Domain-Checklist-Mapping

| Domäne/Kontext | Checklist-Quellen | Auto-Trigger |
|---------------|-------------------|-------------|
| KRITIS/Energie | kritis-nfr.md + NIS2-Mapping | Profil = KRITIS |
| PII/Datenschutz | DSGVO Art. 25, 35 | PII-Felder in spec.md erkannt |
| Security | stride-guide.md | SEC-Stories in spec.md |
| Branchenspezifisch | references/custom/@*/ | custom_checklists in specforge.json |
| API-Compliance | Schema-Hygiene (GP-01) | API-Contracts in spec.md |

## Ablauf (deterministisch)

### Phase 5a: Typ-Erkennung
1. Nutzer benennt Prüfaspekt oder wählt Typ explizit
2. Falls kein Typ gewählt: Automatische Erkennung:
   - spec.md vorhanden, plan.md nicht → **Typ A**
   - plan.md + tasks.md vorhanden → **Typ B**
   - Regulatorischer Kontext erkannt → **Typ D**
   - Sonst → Nachfragen (max. 1 Frage)

### Phase 5b: Checklist-Generierung
1. Profil aus specforge.json lesen
2. Referenzen laden:
   → `references/checklists/golden-principles.md`
   → `references/checklists/ears-syntax.md` (bei Typ A)
   → `references/conventions/spec-first-chain.md` (bei Typ B)
   → `references/custom/*.md` (falls vorhanden)
   → Domänen-spezifische Checklisten (bei Typ D)
3. Checklist generieren basierend auf Constitution, Spec, Golden Principles und Profil
4. Optional: Web-Recherche für domänenspezifische Kriterien (automatisch bei KRITIS)

### Phase 5c: Profilabhängige Filterung
Checklist-Tiefe skaliert mit Profil:

| Prüfpunkt-Kategorie | KRITIS | Standard | Startup |
|---------------------|--------|----------|---------|
| Funktionale Kernprüfpunkte | ✅ | ✅ | ✅ |
| GP-Compliance (alle aktiven GPs) | ✅ | ✅ | GP-02 + GP-07 |
| EARS/Gherkin-Qualität | ✅ | ✅ | Empfohlen |
| Regulatorische Compliance | ✅ | Optional | — |
| STRIDE/Security | ✅ | SEC-Stories | — |
| Custom Checks | ✅ | Empfohlen | — |

### Phase 5d: Output erzeugen

## Output: Checklist (deterministisch)

```markdown
## Checklist: [Typ] — [Prüfaspekt / Feature-Name]
**Profil:** [KRITIS / Standard / Startup]
**Typ:** [A Spec-Readiness / B Plan-Readiness / C Custom / D Domain]
**Generiert:** [YYYY-MM-DD]
**Referenzen:** [Geladene Referenzdateien]

### Funktionale Prüfpunkte
- [ ] [Prüfpunkt 1] — Quelle: [GP-XX / Gate GY / Custom]
- [ ] [Prüfpunkt 2] — Quelle: [ears-syntax.md]

### Governance-Prüfpunkte (laut Profil)
- [ ] GP-02: Spec-Eintrag vorhanden?
- [ ] GP-07: Folder Convention eingehalten?
- [ ] ... (weitere laut Profil)

### Regulatorische Prüfpunkte (falls Profil = KRITIS oder Typ D)
- [ ] NIS2 Art. X: [Prüfpunkt]
- [ ] DSGVO Art. 25: [Prüfpunkt]

### Custom-Prüfpunkte (falls vorhanden)
- [ ] [Custom Check aus references/custom/]

### Ergebnis
**Bestanden:** [X/Y] Prüfpunkte ([Z%])
**Offene Punkte:** [Liste mit Schweregrad]
**Empfehlung:** [Bereit / Nacharbeit nötig]
```

## Fehlerbehandlung

| Situation | Reaktion |
|-----------|---------|
| Kein Input / unklarer Prüfaspekt | → Nachfragen: "Was soll geprüft werden?" (1 Frage) |
| specforge.json fehlt | → Standard-Profil anwenden, Hinweis ausgeben |
| Referenzdateien fehlen | → Klare Fehlermeldung, Checklist ohne diese Quelle erzeugen |
| Profil-Wechsel mid-session | → Checklist-Tiefe anpassen |
| Typ A aber spec.md fehlt | → Fehlermeldung: "spec.md nicht gefunden — Specify (Modus 1) zuerst" |
| Typ B aber tasks.md fehlt | → Fehlermeldung: "tasks.md nicht gefunden — Plan (Modus 3) zuerst" |
| Mixed-Language Input | → Sprachverhalten gemäß Orchestrator |

## GP-Mapping

| GP | Relevanz in Modus 5 |
|----|---------------------|
| GP-01 | Typ B: Schema-Hygiene-Prüfpunkte |
| GP-02 | Typ A + B: Spec-before-Code |
| GP-03 | Typ B: ADR-Vollständigkeit |
| GP-04 | Typ B: ExecPlan bei 5+ Dateien |
| GP-06 | Typ A + B: Stale Marker prüfen |
| GP-07 | Typ A + B: Folder Convention |
| GP-08 | Meta: GP-Verstöße als offene Prüfpunkte |
| GP-10 | Typ B: Tech-Debt dokumentiert |

## Abgrenzung

- **Checklist (Modus 5)** = Erzeugt wiederverwendbare Prüflisten für spezifische Qualitätsaspekte, die der Nutzer selbst anwenden kann
- **Analyze (Modus 4)** = Prüft Cross-Artefakt-Konsistenz automatisch (System als Ganzes)
- **Review (Modus 7)** = Prüft einzelne Requirements/Stories auf Qualität

## Erzeugte Artefakte

| Artefakt | Pfad |
|----------|------|
| checklist-[typ]-[name].md | specs/use-cases/\<feature\>/ |
