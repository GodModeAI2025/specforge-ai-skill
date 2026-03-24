# BAIT-NFR-Checkliste (Stub)

Automatische Prüfliste für nicht-funktionale Anforderungen nach BAIT (BaFin-Rundschreiben 10/2017 (BA) i.d.F. 10/2021 (BA)). SpecForge prüft jede Story gegen diese Kategorien und ergänzt fehlende NFRs.

> **Hinweis:** Dies ist ein Stub mit 8 Prüfpunkten als Proof-of-Concept. Eine vollständige BAIT-Checkliste erfordert die Abdeckung aller 12 BAIT-Kapitel.

> **Perspektive vorab klären:** Vor Anwendung dieser Checkliste muss die Perspektive bestimmt werden:
> - **A) Kreditinstitut** (direkt reguliert durch BaFin)
> - **B) IT-Dienstleister** (Auslagerungsunternehmen)
> - **C) Beratung/Prüfung** (Wirtschaftsprüfer, IT-Berater)

---

## 1. IT-Strategie (ITS)

*BAIT Tz. 1–5*

| # | Prüfpunkt | Mindestanforderung BAIT | Rechtsquelle | Frage an Spec |
|---|-----------|------------------------|--------------|---------------|
| ITS-01 | IT-Strategie dokumentiert | Konsistente, vom Vorstand verabschiedete IT-Strategie | BAIT Tz. 1, 2 | Ist eine IT-Strategie dokumentiert und vom Vorstand verabschiedet? |
| ITS-02 | IT-Strategie-Inhalte | Mindestinhalte: strategische Entwicklung der IT-Aufbau-/Ablauforganisation, Auslagerungsstrategie, IT-Architektur, IT-Notfallmanagement, Informationssicherheit | BAIT Tz. 3 | Enthält die IT-Strategie alle BAIT-Pflichtinhalte? |

**Perspektive B:** IT-Dienstleister müssen nachweisen, dass ihre eigene IT-Strategie die Anforderungen der auslagernden Institute berücksichtigt.
**Perspektive C:** IT-Strategie-Review und Gap-Assessment als typische Beratungsleistung.

---

## 2. Informationsrisikomanagement (IRM)

*BAIT Tz. 6–14*

| # | Prüfpunkt | Mindestanforderung BAIT | Rechtsquelle | Frage an Spec |
|---|-----------|------------------------|--------------|---------------|
| IRM-01 | Informationsverbund | Vollständige Erfassung aller Komponenten des Informationsverbunds (Geschäftsprozesse, IT-Systeme, Netzwerke, Räumlichkeiten) | BAIT Tz. 6, 7 | Ist der Informationsverbund vollständig erfasst und dokumentiert? |
| IRM-02 | Schutzbedarf | Schutzbedarfsfeststellung für alle Bestandteile des Informationsverbunds | BAIT Tz. 8 | Ist eine Schutzbedarfsfeststellung durchgeführt? |

**Perspektive B:** Schutzbedarfsfeststellung muss die vom Institut übertragenen Daten und Prozesse einbeziehen.
**Perspektive C:** Schutzbedarfsanalyse und Risikoassessment als Deliverable.

---

## 3. Informationssicherheitsmanagement (ISM)

*BAIT Tz. 15–24*

| # | Prüfpunkt | Mindestanforderung BAIT | Rechtsquelle | Frage an Spec |
|---|-----------|------------------------|--------------|---------------|
| ISM-01 | Informationssicherheitsleitlinie | Vom Vorstand verabschiedete Informationssicherheitsleitlinie | BAIT Tz. 15 | Ist eine Informationssicherheitsleitlinie vorhanden und vom Vorstand verabschiedet? |
| ISM-02 | Informationssicherheitsbeauftragter | Bestellung eines ISB mit direktem Berichtsweg an die Geschäftsleitung | BAIT Tz. 16, 17 | Ist ein Informationssicherheitsbeauftragter bestellt? |

**Perspektive B:** ISM muss die Sicherheitsanforderungen der auslagernden Institute erfüllen.
**Perspektive C:** ISM-Audit und Reifegradanalyse als typische Beratungsleistung.

---

## 4. Benutzerberechtigungsmanagement (BBM)

*BAIT Tz. 25–31*

| # | Prüfpunkt | Mindestanforderung BAIT | Rechtsquelle | Frage an Spec |
|---|-----------|------------------------|--------------|---------------|
| BBM-01 | Berechtigungskonzept | Sparsamkeitsprinzip (Least Privilege), Funktionstrennung (Segregation of Duties) | BAIT Tz. 25 | Ist ein Berechtigungskonzept mit Least Privilege und Funktionstrennung definiert? |
| BBM-02 | Rezertifizierung | Regelmäßige Überprüfung der Berechtigungen (mindestens jährlich) | BAIT Tz. 27 | Ist ein Rezertifizierungsprozess für Berechtigungen definiert? |

**Perspektive B:** Berechtigungsmanagement muss die vertraglichen Vorgaben des Instituts einhalten.
**Perspektive C:** Berechtigungs-Audit und SoD-Analyse als Deliverable.

---

## Anwendung

1. Perspektive klären: Vor der ersten Prüfung die Perspektive (A/B/C) abfragen
2. SpecForge iteriert bei jeder Story-Erzeugung über alle 4 Kategorien
3. Fehlende NFRs werden als `[NFR-Lücke F{n}: BAIT ...]` markiert
4. Pflicht-Kategorien: IRM, ISM (keine Ausnahme für regulierte Institute)
5. Querschnitts-Kategorien: ITS, BBM (werden immer mitgeprüft)
6. NFRs ohne quantifizierten Zielwert werden als "nicht testbar" markiert

## F-Stufen bei fehlenden NFRs

| Kategorie | regulated_entity | ict_provider | advisory | _default |
|-----------|-----------------|--------------|----------|----------|
| **ITS** (IT-Strategie) | F4 | F2 | F1 | F3 |
| **IRM** (Informationsrisikomanagement) | F4 | F3 | F2 | F4 |
| **ISM** (Informationssicherheitsmanagement) | F4 | F4 | F2 | F4 |
| **BBM** (Benutzerberechtigungsmanagement) | F4 | F3 | F1 | F3 |
