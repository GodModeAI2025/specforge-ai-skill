# @bait — BAIT-NFR-Extension für SpecForge (Stub)

> **Hinweis:** Dies ist ein Stub mit 8 Prüfpunkten als Proof-of-Concept für das Checklisten-Schema. Für eine vollständige BAIT-Checkliste müssen alle Anforderungen der BaFin-Rundschreiben 10/2017 (BA) und 10/2021 (BA) abgedeckt werden.

## Scope

Bankaufsichtliche Anforderungen an die IT (BAIT).
Rechtsquelle: BaFin-Rundschreiben 10/2017 (BA) i.d.F. 10/2021 (BA).
Zielgruppe: Kreditinstitute und Finanzdienstleistungsinstitute in Deutschland.

## Trigger-Begriffe

BAIT, Bankaufsichtliche Anforderungen an die IT, BaFin Rundschreiben 10/2017,
Kreditinstitut, IT-Strategie, Informationsrisikomanagement, Informationssicherheitsmanagement,
Benutzerberechtigungsmanagement, Auslagerung IT

## Trigger-Modi

- Modus 1 (Specify): NFR-Scan gegen BAIT-Kategorien
- Modus 4 (Analyze): BAIT-Compliance als Dimension im Custom Checker
- Modus 5 (Checklist): BAIT-Readiness-Checkliste erzeugen (Typ D — Domain)
- Modus 7 (Review): BAIT-Compliance-Prüfung bestehender Stories

## Pflicht-Abfrage bei Aktivierung

Vor der ersten Prüfung muss die **Perspektive** abgefragt werden:

1. **Sind Sie ein direkt durch die BaFin reguliertes Kreditinstitut/Finanzdienstleister?** → `regulated_entity`
2. **Sind Sie IT-Dienstleister/Auslagerungsunternehmen für ein reguliertes Institut?** → `ict_provider`
3. **Sind Sie in beratender/prüfender Funktion tätig (z.B. Wirtschaftsprüfer, IT-Berater)?** → `advisory`

> **Stub-Hinweis:** Diese Extension enthält nur 8 von ca. 80+ BAIT-Prüfpunkten. Ergebnisse sind nicht vollständig und dienen als Proof-of-Concept für das Checklisten-Schema.

## Perspektiven-Mapping

| Perspective-Wert | BAIT-Rolle |
|------------------|------------|
| `regulated_entity` | Kreditinstitut / Finanzdienstleister (direkt reguliert) |
| `ict_provider` | IT-Dienstleister / Auslagerungsunternehmen |
| `advisory` | Beratung / Prüfung (z.B. Wirtschaftsprüfer, IT-Berater) |

## F-Stufen-Zuordnung nach Perspektive

| Kategorie | regulated_entity | ict_provider | advisory | _default |
|-----------|-----------------|--------------|----------|----------|
| **ITS** (IT-Strategie) | F4 | F2 | F1 | F3 |
| **IRM** (Informationsrisikomanagement) | F4 | F3 | F2 | F4 |
| **ISM** (Informationssicherheitsmanagement) | F4 | F4 | F2 | F4 |
| **BBM** (Benutzerberechtigungsmanagement) | F4 | F3 | F1 | F3 |

## Enthaltene Checklisten

- `checklisten/bait-nfr.md` — 8 Prüfpunkte in 4 Kategorien (Stub)
  (ITS, IRM, ISM, BBM)

## Überschneidungen mit anderen Regulierungen

- **MaRisk:** BAIT konkretisiert die IT-Anforderungen der MaRisk (AT 7.2). Bei gleichzeitiger Aktivierung ergänzen sich beide.
- **DORA:** Ab 2025 überlagert DORA Teile der BAIT für den Bereich IKT-Risikomanagement. BAIT bleibt für nicht-DORA-erfasste Bereiche relevant.
- **KRITIS:** Kreditinstitute ab Schwellenwert sind KRITIS-Betreiber. BAIT ergänzt KRITIS-NFRs um bankspezifische Anforderungen.
