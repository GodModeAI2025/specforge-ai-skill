# Folder Convention

Pflichtstruktur für alle SpecForge-Projekte. Nicht verhandelbar (GP-07). Alle Artefakte referenzieren diese Pfade.

## Verzeichnisstruktur

```
<project-root>/
│
├── specforge.json               ← Projektkonfiguration (Profil, Stack, Pfade)
├── ARCHITECTURE.md              ← Codemap, Doc Map, Golden Principles, Invariants
├── constitution.md              ← Projektprinzipien, Baseline-NFRs, DoD
├── tech-debt-tracker.md         ← Schuldenregister (GP-10)
│
├── specs/
│   ├── principles/              ← Design Principles
│   │   ├── P001-single-responsibility.md
│   │   └── P002-api-first.md
│   │
│   ├── decisions/               ← Architecture Decision Records
│   │   ├── adr-001-database-choice.md
│   │   └── adr-template.md
│   │
│   ├── system/                  ← Systemweite Spezifikationen
│   │   ├── domain-model.md
│   │   ├── api-overview.md
│   │   └── data-classification.md
│   │
│   └── use-cases/               ← Feature-Spezifikationen (1 Ordner pro Feature)
│       ├── 001-user-auth/
│       │   ├── spec.md
│       │   ├── plan.md
│       │   ├── research.md
│       │   ├── quickstart.md
│       │   ├── tasks.md
│       │   └── contracts/
│       │       ├── api-spec.json
│       │       └── events-spec.md
│       │
│       └── 002-data-export/
│           ├── spec.md
│           ├── plan.md
│           ├── research.md
│           ├── quickstart.md
│           └── tasks.md
│
├── plans/
│   ├── active/                  ← Laufende ExecPlans (GP-04)
│   │   └── EP-001-auth-migration.md
│   └── completed/              ← Abgeschlossene ExecPlans
│       └── EP-000-initial-setup.md
│
├── references/custom/           ← Projektspezifische Checklisten (nie überschrieben)
│
└── design/                      ← Design-Artefakte
    ├── wireframes/
    ├── data-models/
    └── architecture-diagrams/
```

## Namenskonventionen

### Feature-Ordner
```
specs/use-cases/[NNN]-[kebab-case-name]/
```
- `NNN` = Dreistellige laufende Nummer (001, 002, ...)
- `kebab-case-name` = Feature-Name in Kleinbuchstaben mit Bindestrichen
- Beispiel: `specs/use-cases/003-multi-tenant-support/`

### Artefakte innerhalb eines Features

| Datei | Pflicht | Erzeugt in Phase |
|-------|---------|-----------------|
| `spec.md` | Ja | Specify (Modus 1) |
| `plan.md` | Ja | Plan (Modus 3a) |
| `research.md` | Ja | Research (Modus 3b) |
| `quickstart.md` | Ja | Quickstart (Modus 3c) |
| `tasks.md` | Ja | Tasks (Modus 3d) |
| `contracts/` | Wenn APIs betroffen | Plan (Modus 3a) |

### ADRs: `specs/decisions/adr-[NNN]-[kebab-case-title].md`
### Principles: `specs/principles/P[NNN]-[kebab-case-title].md`
### ExecPlans: `plans/active/EP-[NNN]-[kebab-case-title].md`
### Tech-Debt: `TD-[NNN]` in tech-debt-tracker.md

## Regeln

1. **Keine Artefakte außerhalb der Convention** — GP-07 erzwingt dies
2. **Leere Verzeichnisse werden nicht angelegt** — nur bei Bedarf
3. **Keine verschachtelten Features** — `use-cases/` ist flach
4. **Feature-Nummern sind monoton steigend** — keine Lücken, keine Wiederverwendung
5. **ExecPlans wandern** — von `active/` nach `completed/` bei Abschluss
6. **ARCHITECTURE.md und constitution.md liegen im Root**
7. **tech-debt-tracker.md liegt im Root** — zentral, nicht pro Feature
8. **Custom-Referenzen** in `references/custom/` werden bei Core-Updates nie überschrieben

## Mapping zu SpecKit

| SpecForge Convention | SpecKit-Äquivalent |
|---------------------|-------------------|
| `specs/use-cases/<feature>/spec.md` | `.specify/specs/<feature>/spec.md` |
| `constitution.md` | `.specify/memory/constitution.md` |
| `specs/decisions/adr-*.md` | Kein SpecKit-Äquivalent |
| `plans/active/EP-*.md` | Kein SpecKit-Äquivalent |
