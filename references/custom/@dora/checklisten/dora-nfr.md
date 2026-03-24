# DORA-NFR-Checkliste

Automatische Prüfliste für nicht-funktionale Anforderungen nach DORA (Regulation (EU) 2022/2554 — Digital Operational Resilience Act). SpecForge prüft jede Story gegen diese Kategorien und ergänzt fehlende NFRs.

> **Perspektive vorab klären:** Vor Anwendung dieser Checkliste muss die Perspektive bestimmt werden:
> - **A) Finanzunternehmen** (Bank, Versicherung, Wertpapierfirma, Zahlungsinstitut etc.)
> - **B) IKT-Drittdienstleister** (Cloud/SaaS/Infrastruktur für den Finanzsektor)
> - **C) Beratung/Implementierung** für Finanzunternehmen
>
> Die Spalte „Mindestanforderung" zeigt den Standard für **Perspektive A**. Abweichungen für B und C sind in den Fußnoten der jeweiligen Kategorie dokumentiert.

---

## 1. IKT-Risikomanagement (IRM)

*Kapitel II DORA, Art. 5–16*

| # | Prüfpunkt | Mindestanforderung DORA | DORA-Artikel | Frage an Spec |
|---|-----------|------------------------|-------------|---------------|
| IRM-01 | IKT-Risikomanagement-Framework | Dokumentiert, jährlich reviewed, Teil des Gesamt-Risikomanagements | Art. 6(1), 6(5) | Ist ein IKT-Risikomanagement-Framework definiert und dokumentiert? |
| IRM-02 | Governance & Verantwortlichkeit | Leitungsorgan trägt Gesamtverantwortung, Kontrollfunktion zugewiesen | Art. 5(1), 5(2), 6(4) | Ist die Verantwortung für IKT-Risikomanagement dem Leitungsorgan zugewiesen? |
| IRM-03 | IKT-Asset-Inventar | Vollständige Identifikation und Klassifikation aller IKT-Assets und -Funktionen | Art. 8(1) | Ist ein vollständiges IKT-Asset-Inventar vorhanden und klassifiziert? |
| IRM-04 | Risikobewertung | Kontinuierliche Identifikation von Risikoquellen, jährliches Szenario-Review | Art. 8(2), 8(3) | Werden IKT-Risiken kontinuierlich bewertet und Szenarien regelmäßig aktualisiert? |
| IRM-05 | Legacy-System-Bewertung | Jährliches Risk Assessment für alle Legacy-IKT-Systeme | Art. 8(7) | Werden Legacy-Systeme separat und regelmäßig bewertet? |
| IRM-06 | Schutzmaßnahmen | Policies, Protokolle und Tools zum Schutz aller IKT-Assets und physischen Infrastrukturen | Art. 6(2), 9(1) | Sind Schutzmaßnahmen für alle IKT-Assets spezifiziert? |
| IRM-07 | Erkennung (Detection) | Mechanismen zur Erkennung anomaler Aktivitäten, inkl. Netzwerk-Performance und IKT-Incidents | Art. 10(1), 10(2) | Sind Erkennungsmechanismen für anomale Aktivitäten definiert? |
| IRM-08 | Business Continuity | IKT-Continuity-Policy mit RTO/RPO, regelmäßig getestet | Art. 11(1), 11(6), 11(7) | Ist eine IKT-Business-Continuity-Strategie mit konkreten RTO/RPO-Werten definiert? |
| IRM-09 | Backup & Wiederherstellung | Backup-Policies, getrennte Systeme, regelmäßige Restore-Tests | Art. 12(1), 12(2) | Ist eine Backup-Strategie mit Restore-Tests dokumentiert? |
| IRM-10 | Kommunikationsstrategie | Kommunikationsplan für IKT-bezogene Incidents (intern + extern) | Art. 14(1), 14(2) | Ist ein Kommunikationsplan für IKT-Incidents spezifiziert? |
| IRM-11 | Lessons Learned | Post-Incident-Reviews, Integration in Risikomanagement-Framework | Art. 13(1), 13(2) | Ist ein Post-Incident-Review-Prozess definiert? |
| IRM-12 | Digital Operational Resilience Strategy | Strategie zur Umsetzung des Frameworks, inkl. Multi-Vendor-Strategie | Art. 6(8), 6(9) | Ist eine Digital Operational Resilience Strategy dokumentiert? |
| IRM-13 | Schulung Leitungsorgan | Regelmäßige IKT-Risiko-Schulungen für das Leitungsorgan | Art. 5(4) | Sind IKT-Schulungen für das Leitungsorgan vorgesehen? |
| IRM-14 | Interne Revision | Regelmäßige IKT-Audits durch unabhängige interne Prüfer | Art. 6(6), 6(7) | Ist ein IKT-Audit-Zyklus durch interne Revision definiert? |

**Perspektive B (IKT-Drittdienstleister):** IRM-01 bis IRM-06 gelten analog für eigene Systeme, die Finanzunternehmen bedienen. Zusätzlich: Nachweispflicht gegenüber Aufsichtsbehörden bei Designation als kritischer Drittdienstleister (Art. 31 ff.).
**Perspektive C (Beratung):** IRM-01 bis IRM-14 als Prüfrahmen für den Kunden anwenden. Empfehlung: Gap-Assessment gegen alle Prüfpunkte.

---

## 2. IKT-Incident-Management & Reporting (INC)

*Kapitel III DORA, Art. 17–23*

| # | Prüfpunkt | Mindestanforderung DORA | DORA-Artikel | Frage an Spec |
|---|-----------|------------------------|-------------|---------------|
| INC-01 | Incident-Management-Prozess | Definierte Prozesse zur Überwachung, zum Management und zur Nachverfolgung von IKT-Incidents | Art. 17(1), 17(2) | Ist ein IKT-Incident-Management-Prozess definiert? |
| INC-02 | Frühwarnindikatoren | Early-Warning-Indicators zur Erkennung von Incidents | Art. 17(1)(a) | Sind Frühwarnindikatoren definiert? |
| INC-03 | Incident-Klassifikation | Klassifikation nach Kritikalität, Anzahl betroffener Kunden, Dauer, Datenverlust, geographische Ausbreitung, wirtschaftliche Auswirkung | Art. 18(1) | Ist ein Klassifikationsschema für IKT-Incidents implementiert? |
| INC-04 | Major-Incident-Meldung — Initial | Initialnotifikation ≤4h nach Klassifikation als Major, max. 24h nach Erkennung | Art. 19(4)(a), RTS | Ist der Meldefluss für Major Incidents mit Fristen definiert? |
| INC-05 | Major-Incident-Meldung — Intermediate | Zwischenbericht ≤72h nach Klassifikation | Art. 19(4)(b), RTS | Ist die Frist für den Zwischenbericht dokumentiert? |
| INC-06 | Major-Incident-Meldung — Final | Abschlussbericht ≤1 Monat nach Klassifikation | Art. 19(4)(c), RTS | Ist die Frist für den Abschlussbericht dokumentiert? |
| INC-07 | Kundenbenachrichtigung | Unverzügliche Information betroffener Kunden bei Auswirkung auf finanzielle Interessen | Art. 19(3) | Ist ein Prozess zur Kundenbenachrichtigung bei Major Incidents definiert? |
| INC-08 | Incident-Logging | Aufzeichnung aller IKT-Incidents mit Zeitstempel, Art, betroffene Systeme | Art. 17(2) | Werden alle IKT-Incidents vollständig protokolliert? |
| INC-09 | Rollen & Verantwortlichkeiten | Klare Zuweisung von Rollen für Incident Response | Art. 17(1)(c) | Sind Rollen und Verantwortlichkeiten für Incident Response dokumentiert? |
| INC-10 | Meldung an Leitungsorgan | Mindestens Major Incidents werden dem Leitungsorgan gemeldet | Art. 17(1)(e) | Ist die Eskalation an das Leitungsorgan für Major Incidents definiert? |
| INC-11 | Freiwillige Cyber-Threat-Meldung | Prozess für freiwillige Meldung signifikanter Cyber-Bedrohungen an Aufsichtsbehörde | Art. 19(2) | Ist ein Prozess für freiwillige Cyber-Threat-Meldungen vorgesehen? |

**Perspektive B:** IKT-Drittdienstleister müssen Incidents an betroffene Finanzunternehmen unverzüglich melden, damit diese ihre eigenen Meldefristen einhalten können. Vertraglich zu verankern (Art. 30(3)).
**Perspektive C:** Incident-Response-Playbooks und Meldevorlagen als Deliverable einplanen.

---

## 3. Digital Operational Resilience Testing (TST)

*Kapitel IV DORA, Art. 24–27*

| # | Prüfpunkt | Mindestanforderung DORA | DORA-Artikel | Frage an Spec |
|---|-----------|------------------------|-------------|---------------|
| TST-01 | Testprogramm | Umfassendes Testprogramm als integraler Bestandteil des IKT-Risikomanagement-Frameworks | Art. 24(1), 24(2) | Ist ein Digital Operational Resilience Testprogramm definiert? |
| TST-02 | Test-Scope | Alle IKT-Systeme und -Anwendungen, die kritische oder wichtige Funktionen unterstützen | Art. 24(1), 25(1) | Ist der Test-Scope auf alle kritischen Funktionen abgestimmt? |
| TST-03 | Basistest-Typen | Vulnerability Assessments, Netzwerksicherheitstests, Gap-Analysen, Source-Code-Reviews, Szenario-Tests, Penetrationstests (jährlich) | Art. 25(1) | Welche Testarten werden durchgeführt und in welchem Rhythmus? |
| TST-04 | Unabhängigkeit der Tester | Tests durch unabhängige interne oder externe Parteien, keine Interessenkonflikte | Art. 24(4), 25(2) | Ist die Unabhängigkeit der Tester sichergestellt? |
| TST-05 | Befund-Management | Priorisierung, Klassifikation und zeitnahe Behebung aller Schwachstellen | Art. 24(5) | Ist ein Prozess für Befund-Management und Remediation definiert? |
| TST-06 | TLPT — Pflicht | Threat-Led Penetration Testing mind. alle 3 Jahre für designierte Entitäten | Art. 26(1), 26(8) | Ist die Entität für TLPT designiert? Wenn ja: Ist ein TLPT-Zyklus geplant? |
| TST-07 | TLPT — Scope | Mehrere oder alle kritischen/wichtigen Funktionen auf Live-Produktionssystemen | Art. 26(1), 26(2) | Ist der TLPT-Scope auf Live-Systeme und kritische Funktionen ausgerichtet? |
| TST-08 | TLPT — Drittanbieter-Einbindung | Vertragliche Verpflichtung von IKT-Drittanbietern zur Teilnahme am TLPT | Art. 26(3), 30(3)(d) | Sind IKT-Drittanbieter vertraglich zur TLPT-Teilnahme verpflichtet? |
| TST-09 | TLPT — Tester-Anforderungen | Zertifizierung, Expertise in Threat Intelligence & Red Teaming, Unabhängigkeit, Versicherungsschutz | Art. 27(1) | Erfüllen die TLPT-Tester die DORA-Anforderungen? |
| TST-10 | Pooled Testing | Bei gemeinsamer Nutzung eines IKT-Dienstleisters: gepooltes TLPT unter Leitung einer designierten Entität | Art. 26(4) | Ist Pooled Testing für gemeinsame IKT-Drittanbieter vorgesehen? |

**Perspektive B:** IKT-Drittdienstleister müssen am TLPT der Finanzunternehmen teilnehmen und kooperieren (Art. 30(3)(d)). Eigenständige Tests als Nachweis der Resilienz empfohlen.
**Perspektive C:** Beratung bei Scope-Definition, Tester-Auswahl und Remediation-Planung als typische Deliverables.

---

## 4. IKT-Drittparteirisiko (TPR)

*Kapitel V DORA, Art. 28–44*

| # | Prüfpunkt | Mindestanforderung DORA | DORA-Artikel | Frage an Spec |
|---|-----------|------------------------|-------------|---------------|
| TPR-01 | Drittparteirisiko im Framework | IKT-Drittparteirisiko als integraler Bestandteil des IKT-Risikomanagements | Art. 28(1) | Ist IKT-Drittparteirisiko in das Risikomanagement-Framework integriert? |
| TPR-02 | Strategie IKT-Drittparteien | Regelmäßig reviewte Strategie zum IKT-Drittparteirisiko, inkl. Multi-Vendor-Policy | Art. 28(2), 6(9) | Ist eine IKT-Drittpartei-Risikostrategie dokumentiert? |
| TPR-03 | Informationsregister | Vollständiges Register aller vertraglichen Vereinbarungen mit IKT-Drittanbietern, jährlich an Aufsicht gemeldet | Art. 28(3) | Wird ein vollständiges Informationsregister (Register of Information) geführt und gemeldet? |
| TPR-04 | Konzentrationsrisiko | Vorab-Bewertung des IKT-Konzentrationsrisikos auf Entitätsebene vor neuen Vereinbarungen | Art. 29(1) | Wird das IKT-Konzentrationsrisiko vor Vertragsabschluss bewertet? |
| TPR-05 | Vertragsklauseln — Pflichtinhalte | SLA, Sicherheitsmaßnahmen, Audit-Rechte, Datenlokalisierung, Mitwirkung bei Incidents, Subcontracting-Regeln, Exit-Strategie | Art. 30(2), 30(3) | Enthalten IKT-Verträge alle DORA-Pflichtklauseln? |
| TPR-06 | Audit- & Zugangsrechte | Uneingeschränkte Audit-, Inspektions- und Zugangsrechte des Finanzunternehmens und der Aufsichtsbehörde | Art. 30(3)(e) | Sind Audit- und Zugangsrechte vertraglich gesichert? |
| TPR-07 | Exit-Strategie | Dokumentierte Exit-Strategie für jeden kritischen IKT-Drittanbieter, Übergangspläne, Datenrückgabe/-löschung | Art. 28(8), 30(3)(f) | Ist eine Exit-Strategie für kritische IKT-Drittanbieter definiert? |
| TPR-08 | Subcontracting-Kette | Monitoring und Risikobewertung der Subcontracting-Kette, Einspruchsrecht bei wesentlichen Änderungen | Art. 30(2)(a), RTS | Wird die IKT-Subcontracting-Kette überwacht und bewertet? |
| TPR-09 | Kritische/wichtige Funktionen | Klassifikation, ob ausgelagerte Funktionen kritisch/wichtig sind — schärfere Anforderungen bei Ja | Art. 28(1)(b), 30(2) | Sind ausgelagerte Funktionen als kritisch/wichtig klassifiziert? |
| TPR-10 | Kündigungsrechte | Definierte Kündigungsrechte bei: schwerwiegendem Vertragsbruch, Sicherheitsmängeln, behördlicher Anordnung | Art. 28(7) | Sind DORA-konforme Kündigungsrechte vertraglich verankert? |
| TPR-11 | Oversight-Regime CTPP | Bei kritischen IKT-Drittanbietern (CTPP): Compliance mit dem EU-Oversight-Framework | Art. 31–37 | Ist der IKT-Drittanbieter als CTPP designiert? Wenn ja: Sind Oversight-Anforderungen berücksichtigt? |
| TPR-12 | Gesamtverantwortung | Finanzunternehmen bleibt auch bei Auslagerung vollständig verantwortlich für DORA-Compliance | Art. 28(1)(a) | Ist dokumentiert, dass die regulatorische Gesamtverantwortung beim Finanzunternehmen verbleibt? |

**Perspektive B:** TPR-03 bis TPR-08 spiegeln sich in vertraglichen Pflichten gegenüber dem Finanzunternehmen. IKT-Drittdienstleister muss alle geforderten Klauseln akzeptieren und umsetzen.
**Perspektive C:** Vertragsreviews, Register-of-Information-Templates und Exit-Strategien als typische Beratungsleistung.

---

## 5. Datenschutz & Datenintegrität (DAT)

*Querschnittsthema — DORA i.V.m. DSGVO*

| # | Prüfpunkt | Mindestanforderung DORA | DORA-Artikel | Frage an Spec |
|---|-----------|------------------------|-------------|---------------|
| DAT-01 | Vertraulichkeit & Integrität | Schutz von Verfügbarkeit, Authentizität, Integrität und Vertraulichkeit der Daten | Art. 6(2), 9(2) | Sind Datenintegrität und Vertraulichkeit als Schutzziele definiert? |
| DAT-02 | Verschlüsselung at Rest | Verschlüsselung aller gespeicherten Daten nach aktuellem Stand der Technik | Art. 9(2) | Sind Verschlüsselungsanforderungen für ruhende Daten spezifiziert? |
| DAT-03 | Verschlüsselung in Transit | Verschlüsselung aller Daten im Transport (TLS 1.2+) | Art. 9(2) | Ist Transport-Verschlüsselung spezifiziert? |
| DAT-04 | Datenlokalisierung | Bei Auslagerung: Speicherort der Daten vertraglich festgelegt | Art. 30(2)(h) | Ist der Speicherort der Daten vertraglich festgelegt? |
| DAT-05 | Datenrückgabe & -löschung | Bei Vertragsende: sichere Rückgabe oder Löschung der Daten durch IKT-Drittanbieter | Art. 30(3)(f) | Ist ein Datenrückgabe- und Löschprozess bei Vertragsende definiert? |
| DAT-06 | DSGVO-Koordination | Abstimmung DORA-Incident-Reporting mit DSGVO-Datenschutz-Meldepflichten (72h) | Art. 19, DSGVO Art. 33 | Sind DORA- und DSGVO-Meldepflichten aufeinander abgestimmt? |

---

## 6. Governance & Compliance (GOV)

*Querschnittsthema — Art. 5, 45, 46 ff.*

| # | Prüfpunkt | Mindestanforderung DORA | DORA-Artikel | Frage an Spec |
|---|-----------|------------------------|-------------|---------------|
| GOV-01 | Leitungsorgan-Verantwortung | Letztverantwortung des Leitungsorgans für IKT-Risikomanagement | Art. 5(1), 5(2) | Ist die DORA-Verantwortung des Leitungsorgans dokumentiert? |
| GOV-02 | Proportionalität | Umsetzung proportional zu Größe, Risikoprofil, Art und Komplexität der Entität | Art. 4(1), 4(2) | Ist die Proportionalität der Maßnahmen nachvollziehbar begründet? |
| GOV-03 | Informationsaustausch | Teilnahme an freiwilligem Informationsaustausch zu Cyber-Bedrohungen zwischen Finanzunternehmen | Art. 45(1) | Ist eine Teilnahme am Informationsaustausch vorgesehen? |
| GOV-04 | Sanktionsregime | Kenntnis und Berücksichtigung der nationalen Sanktionsvorschriften | Art. 50 | Sind die Konsequenzen bei Non-Compliance bekannt und dokumentiert? |
| GOV-05 | Vereinfachtes Framework | Für Mikrounternehmen: vereinfachtes IKT-Risikomanagement-Framework anwenden | Art. 16(1) | Qualifiziert sich die Entität als Mikrounternehmen nach Art. 16? |

---

## Anwendung

1. **Perspektive klären:** Vor der ersten Prüfung die Perspektive (A/B/C) abfragen
2. SpecForge iteriert bei jeder Story-Erzeugung über alle 6 Kategorien
3. Fehlende NFRs werden als `[NFR-Lücke: ...]` markiert
4. Bei DORA-regulierten Projekten sind **IRM, INC, TST, TPR** Pflicht — keine Ausnahme
5. **DAT** und **GOV** sind Querschnittsthemen und werden immer mitgeprüft
6. NFRs ohne quantifizierten Zielwert werden als "nicht testbar" markiert
7. Die Checkliste wird als Extension unter `references/custom/@dora/checklisten/dora-nfr.md` abgelegt

---

## Schweregrad bei fehlenden NFRs (F0–F5 nach § 27 PrüfbV)

Die Klassifizierung folgt dem aufsichtlichen Standard der Deutschen Bundesbank (Anlage 6 zu § 27 PrüfbV). Jeder fehlende NFR wird nach dem Schweregrad des resultierenden Normverstoßes eingestuft.

### F-Klassifizierung — Definitionen

| Stufe | Bezeichnung | Bedeutung (PrüfbV) | Konsequenz im SpecForge-Kontext |
|-------|-------------|--------------------|---------------------------------|
| **F 0** | Keine Mängel | Völliges Fehlen von Normverstößen | NFR vollständig erfüllt — keine Aktion |
| **F 1** | Geringfügige Mängel | Normverstoß mit leichten Auswirkungen auf die Wirksamkeit der Maßnahme | Story kann implementiert werden; NFR als Verbesserung nachziehen |
| **F 2** | Mittelschwere Mängel | Normverstoß mit merklichen Auswirkungen auf die Wirksamkeit der Maßnahme | Story kann implementiert werden; NFR muss vor Go-Live ergänzt werden |
| **F 3** | Gewichtige Mängel | Normverstoß mit deutlichen Auswirkungen auf die Wirksamkeit der Maßnahme | Story darf nur mit dokumentiertem Risiko-Akzeptanz-Beschluss des Leitungsorgans implementiert werden |
| **F 4** | Schwergewichtige Mängel | Normverstoß, der die Wirksamkeit der Maßnahme erheblich beeinträchtigt oder vollständig beseitigt | Story kann nicht implementiert werden, bis NFR ergänzt ist — Aufsichtsbehördliche Maßnahmen drohen (Art. 50 DORA) |
| **F 5** | Nicht anwendbar | Prüfungsgebiet ist auf die Entität nicht anwendbar | NFR entfällt — Begründung dokumentieren |

### Zuordnung Kategorie → F-Stufe bei fehlendem NFR

| Kategorie | Finanzunternehmen (Perspektive A) | IKT-Drittdienstleister (Perspektive B) | Beratung (Perspektive C) |
|-----------|----------------------------------|---------------------------------------|--------------------------|
| **IRM** (IKT-Risikomanagement) | F 4 | F 4 (wenn CTPP), F 3 (sonst) | F 2 (Empfehlung) |
| **INC** (Incident Reporting) | F 4 | F 4 (vertraglich gefordert) | F 2 (Empfehlung) |
| **TST** (Resilience Testing) | F 4 (TLPT-designiert), F 3 (nicht designiert) | F 3 (Mitwirkungspflicht) | F 1 (Empfehlung) |
| **TPR** (Drittparteirisiko) | F 4 | F 4 (Vertragspflichten) | F 2 (Empfehlung) |
| **DAT** (Daten & Integrität) | F 4 (bei PII/Finanzdaten), F 3 (sonst) | F 4 (bei PII/Finanzdaten), F 3 (sonst) | F 2 (bei PII) |
| **GOV** (Governance) | F 4 | F 3 | F 1 |

### Mapping F-Stufe → SpecForge-Gate-Verhalten

| F-Stufe | Gate-Ergebnis | Aktion |
|---------|---------------|--------|
| F 4 | ❌ FAIL | Gate blockiert — Story darf nicht weiter, bis NFR ergänzt |
| F 3 | ⚠️ CONDITIONAL | Gate passierbar nur mit dokumentierter Risiko-Akzeptanz durch Leitungsorgan |
| F 2 | ⚠️ WARNING | Gate passierbar — NFR als Pflicht-Task vor Go-Live erzeugen |
| F 1 | ℹ️ INFO | Gate passierbar — NFR als Empfehlung dokumentieren |
| F 0 | ✅ PASS | Kein Handlungsbedarf |
| F 5 | ⏭️ SKIP | Prüfpunkt nicht anwendbar — Begründung im Audit Trail |
