# Regulierungs-Checklisten für SpecForge beitragen

Anleitung zur Erstellung branchenspezifischer NFR-Checklisten als SpecForge-Extension. Die DORA-Extension (`references/custom/@dora/`) dient als Referenzimplementierung.

---

## Extension-Paket-Struktur

Jede Regulierungs-Checkliste wird als Extension-Paket unter `references/custom/` abgelegt:

```
references/custom/@{regulierung}/
├── manifest.md              ← Scope, Trigger, Modi, Perspektiven
└── checklisten/
    └── {regulierung}-nfr.md ← Checkliste im Standard-Schema
```

---

## 1. manifest.md — Pflichtfelder

Die `manifest.md` beschreibt die Extension und steuert das automatische Laden über Trigger-Begriffe.

### Pflicht-Abschnitte

| Abschnitt | Beschreibung | Beispiel (DORA) |
|-----------|-------------|-----------------|
| **Scope** | Regulierungsname, Rechtsquelle, Zielgruppe | "Digital Operational Resilience Act (EU 2022/2554). Zielgruppe: Finanzunternehmen..." |
| **Trigger-Begriffe** | Komma-separierte Liste von Begriffen, die die Extension automatisch laden | "DORA, EU 2022/2554, BaFin, TLPT..." |
| **Trigger-Modi** | Welche SpecForge-Modi die Extension unterstützt | "Modus 1 (Specify): NFR-Scan..." |
| **Perspektiven-Mapping** | Tabelle: `perspective`-Wert → Rollenbezeichnung | "regulated_entity → Finanzunternehmen" |
| **F-Stufen-Zuordnung** | Tabelle: Kategorie × Perspektive → F-Stufe bei fehlendem NFR | "IRM × regulated_entity → F4" |
| **Enthaltene Checklisten** | Auflistung der Checklisten-Dateien mit Prüfpunkt-Anzahl | "dora-nfr.md — 58 Prüfpunkte in 6 Kategorien" |

### Optionale Abschnitte

| Abschnitt | Beschreibung |
|-----------|-------------|
| **Pflicht-Abfrage bei Aktivierung** | Fragen, die vor der ersten Prüfung gestellt werden müssen (z.B. Perspektive) |
| **Überschneidungen** | Hinweise auf Interaktion mit anderen Regulierungen |

---

## 2. Checklisten-Schema

Jede NFR-Checkliste folgt einem einheitlichen Tabellenformat.

### Kopfzeile (Pflicht)

```markdown
# {Regulierung}-NFR-Checkliste

Automatische Prüfliste für nicht-funktionale Anforderungen nach {Regulierung}
({Rechtsquelle}). SpecForge prüft jede Story gegen diese Kategorien und
ergänzt fehlende NFRs.
```

### Kategorien mit Prüfpunkt-Tabellen (Pflicht)

Jede Kategorie enthält eine Tabelle mit folgenden Pflicht-Spalten:

| Spalte | Pflicht | Beschreibung | Format |
|--------|---------|--------------|--------|
| `#` | Ja | Eindeutige ID | `{KAT}-{NN}` (z.B. `IRM-01`, `SEC-03`) |
| Prüfpunkt | Ja | Kurze Beschreibung des Prüfgegenstands | Frei, max. 80 Zeichen |
| Mindestanforderung | Ja | Konkrete Anforderung aus der Regulierung | Quantifiziert wenn möglich |
| Rechtsquelle | Ja | Artikel/Paragraph-Referenz | z.B. "Art. 6(1), 6(5)" |
| Frage an Spec | Ja | Prüffrage gegen die Spezifikation | Geschlossene Frage (Ja/Nein-beantwortbar) |

**Beispiel:**

```markdown
| # | Prüfpunkt | Mindestanforderung | Rechtsquelle | Frage an Spec |
|---|-----------|-------------------|--------------|---------------|
| IRM-01 | IKT-Risikomanagement-Framework | Dokumentiert, jährlich reviewed | Art. 6(1) | Ist ein IKT-Risikomanagement-Framework definiert? |
```

### Perspektive-Hinweise (Pflicht wenn Perspektiven definiert)

Nach jeder Kategorie-Tabelle: Fließtext mit Erläuterungen zur Anwendung pro Perspektive.

```markdown
**Perspektive B (IKT-Drittdienstleister):** IRM-01 bis IRM-06 gelten analog...
**Perspektive C (Beratung):** IRM-01 bis IRM-14 als Prüfrahmen für den Kunden...
```

### Anwendungshinweise (Pflicht)

Am Ende der Checkliste:

```markdown
## Anwendung

1. Perspektive klären: Vor der ersten Prüfung die Perspektive abfragen
2. SpecForge iteriert bei jeder Story-Erzeugung über alle Kategorien
3. Fehlende NFRs werden als `[NFR-Lücke F{n}: {ID} — {Beschreibung}]` markiert
4. Pflicht-Kategorien für diese Regulierung: [Liste]
5. Querschnitts-Kategorien: [Liste — werden immer mitgeprüft]
6. NFRs ohne quantifizierten Zielwert werden als "nicht testbar" markiert
```

### F-Stufen-Zuordnung (Pflicht)

Tabelle mit F-Stufen pro Kategorie und Perspektive:

```markdown
## F-Stufen bei fehlenden NFRs

| Kategorie | {Perspektive A} | {Perspektive B} | {Perspektive C} | _default |
|-----------|----------------|----------------|----------------|----------|
| KAT-1 | F4 | F3 | F2 | F3 |
| KAT-2 | F4 | F4 | F1 | F4 |
```

Die Spalte `_default` ist Pflicht und wird verwendet, wenn keine Perspektive gesetzt ist oder die Perspektive nicht in der Tabelle vorkommt.

---

## 3. Validierung

Bevor eine Extension als fertig gilt, muss sie diese 4-Schritte-Prüfung bestehen:

### Schritt 1: Schema-Prüfung

- [ ] Alle Pflicht-Spalten in jeder Prüfpunkt-Tabelle vorhanden?
- [ ] IDs im Format `{KAT}-{NN}` (Kategorie-Kürzel + zweistellige Nummer)?
- [ ] Rechtsquellen referenziert (Artikel/Paragraph)?
- [ ] Fragen an Spec als geschlossene Fragen formuliert?
- [ ] Keine doppelten IDs?

### Schritt 2: F-Stufen-Prüfung

- [ ] F-Stufen-Zuordnungstabelle vorhanden?
- [ ] Für jede Kategorie und jede definierte Perspektive eine F-Stufe zugewiesen?
- [ ] `_default`-Spalte vorhanden?
- [ ] Nur gültige F-Stufen verwendet (F0–F5)?

### Schritt 3: Manifest-Prüfung

- [ ] manifest.md enthält alle Pflicht-Abschnitte (Scope, Trigger-Begriffe, Trigger-Modi, Perspektiven-Mapping, F-Stufen-Zuordnung, Enthaltene Checklisten)?
- [ ] Trigger-Begriffe sind spezifisch genug (keine generischen Begriffe wie "Sicherheit")?
- [ ] Perspektiven-Mapping stimmt mit Checkliste überein?

### Schritt 4: Smoke-Test

- [ ] Modus 5 (Checklist) mit der neuen Extension gegen eine Minimal-Spec ausführen
- [ ] Mindestens 1 NFR-Lücke korrekt erkannt und mit F-Stufe markiert?
- [ ] Perspektive-Abfrage funktioniert (wenn Pflicht-Abfrage definiert)?
- [ ] Extension wird bei Trigger-Begriff automatisch geladen?

---

## 4. Referenzimplementierung

Die DORA-Extension unter `references/custom/@dora/` dient als vollständiges Beispiel:

- `@dora/manifest.md` — Scope, Trigger, 3 Perspektiven, 6 Kategorien
- `@dora/checklisten/dora-nfr.md` — 58 Prüfpunkte, F-Stufen nach PrüfbV § 27

---

## 5. Kandidatenliste

| Regulierung | Branche | Priorität | Status |
|-------------|---------|-----------|--------|
| DORA (EU 2022/2554) | Finanzsektor | Hoch | ✅ Fertig |
| BAIT | Banken (DE) | Hoch | 🔧 Stub |
| MaRisk | Finanzsektor (DE) | Hoch | Offen |
| PCI-DSS 4.0 | Zahlungsverkehr | Mittel | Offen |
| EnWG / IT-Sicherheitskatalog | Energiesektor | Mittel | Offen |
| VAIT | Versicherungen (DE) | Mittel | Offen |
| MDR (EU 2017/745) | Medizinprodukte | Niedrig | Offen |
| UNECE R155/R156 | Automotive | Niedrig | Offen |
