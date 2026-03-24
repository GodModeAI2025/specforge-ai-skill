# @dora — DORA-NFR-Extension für SpecForge

## Scope

Digital Operational Resilience Act (EU 2022/2554).
Zielgruppe: Finanzunternehmen, IKT-Drittdienstleister, Beratungen im Finanzsektor.

## Trigger-Begriffe

DORA, EU 2022/2554, Digital Operational Resilience, Finanzunternehmen,
IKT-Drittdienstleister, BaFin, PrüfbV, TLPT, Register of Information

## Trigger-Modi

- Modus 1 (Specify): NFR-Scan gegen alle 6 DORA-Kategorien
- Modus 4 (Analyze): DORA-Compliance als 6. Dimension (Custom Checker)
- Modus 5 (Checklist): DORA-Readiness-Checkliste erzeugen (Typ D — Domain)
- Modus 6 (Stakeholder-Sim): Rolle "DORA Compliance Officer" verfügbar
- Modus 7 (Review): DORA-Compliance-Prüfung bestehender Stories

## Pflicht-Abfrage bei Aktivierung

Vor der ersten Prüfung MUSS die Perspektive abgefragt werden:

- **A) Finanzunternehmen** (Bank, Versicherung, Zahlungsinstitut etc.)
- **B) IKT-Drittdienstleister** (Cloud/SaaS/Infrastruktur für Finanzsektor)
- **C) Beratung/Implementierung** für Finanzunternehmen

Die Perspektive bestimmt, welche Prüfpunkte Pflicht sind und welche
F-Stufe ein fehlender NFR erhält.

## Perspektiven-Mapping

| Perspective-Wert | DORA-Rolle | Beschreibung |
|------------------|------------|-------------|
| `regulated_entity` | Perspektive A | Finanzunternehmen (Bank, Versicherung, Wertpapierfirma, Zahlungsinstitut) |
| `ict_provider` | Perspektive B | IKT-Drittdienstleister (Cloud/SaaS/Infrastruktur für Finanzsektor) |
| `advisory` | Perspektive C | Beratung/Implementierung für Finanzunternehmen |

## F-Stufen-Zuordnung nach Perspektive

| Kategorie | regulated_entity | ict_provider | advisory | _default |
|-----------|-----------------|--------------|----------|----------|
| **IRM** (IKT-Risikomanagement) | F4 | F4 (CTPP) / F3 | F2 | F4 |
| **INC** (Incident Reporting) | F4 | F4 | F2 | F4 |
| **TST** (Resilience Testing) | F4 (TLPT) / F3 | F3 | F1 | F3 |
| **TPR** (Drittparteirisiko) | F4 | F4 | F2 | F4 |
| **DAT** (Daten & Integrität) | F4 (PII) / F3 | F4 (PII) / F3 | F2 (PII) | F3 |
| **GOV** (Governance) | F4 | F3 | F1 | F3 |

## Enthaltene Checklisten

- `checklisten/dora-nfr.md` — 58 Prüfpunkte in 6 Kategorien (IRM, INC, TST, TPR, DAT, GOV)

## Überschneidungen mit anderen Regulierungen

- **NIS2:** DORA ist lex specialis zu NIS2 für den Finanzsektor. Bei gleichzeitiger Aktivierung gilt DORA vorrangig für IKT-Risikomanagement, NIS2 ergänzend für allgemeine Cybersecurity.
- **DSGVO:** DAT-Kategorie überschneidet sich mit DSGVO-Anforderungen. DORA-Meldepflichten (Art. 19) müssen mit DSGVO Art. 33 (72h) koordiniert werden.
- **KRITIS:** KRITIS-NFR-Checkliste (Core) bleibt aktiv. DORA ergänzt um finanzsektor-spezifische Anforderungen.
