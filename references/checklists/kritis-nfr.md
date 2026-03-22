# KRITIS-NFR-Checkliste

Automatische Prüfliste für nicht-funktionale Anforderungen in KRITIS-regulierten Umgebungen. SpecForge prüft jede Story gegen diese Kategorien und ergänzt fehlende NFRs.

## 1. Verfügbarkeit (AVA)

| # | Prüfpunkt | Mindestanforderung KRITIS | Frage an Spec |
|---|-----------|--------------------------|---------------|
| AVA-01 | Uptime-SLA | ≥99,9% (8,76h Downtime/Jahr) | Ist ein Uptime-Zielwert definiert? |
| AVA-02 | RTO | ≤4h für kritische Systeme | Ist die maximale Wiederherstellungszeit definiert? |
| AVA-03 | RPO | ≤1h für kritische Daten | Ist der maximale Datenverlust-Zeitraum definiert? |
| AVA-04 | Redundanz | Kein Single Point of Failure | Sind Redundanz-Anforderungen dokumentiert? |
| AVA-05 | Failover | Automatisches Failover ≤60s | Ist Failover-Verhalten spezifiziert? |
| AVA-06 | Backup-Strategie | 3-2-1-Regel | Ist eine Backup-Strategie definiert? |
| AVA-07 | Disaster Recovery | DR-Plan mit dokumentiertem Testrhythmus | Ist ein DR-Szenario beschrieben? |
| AVA-08 | Degraded Mode | Definiertes Verhalten bei Teilausfall | Ist Degraded-Mode-Verhalten spezifiziert? |

## 2. Sicherheit (SEC)

| # | Prüfpunkt | Mindestanforderung KRITIS | Frage an Spec |
|---|-----------|--------------------------|---------------|
| SEC-01 | Authentifizierung | MFA für administrative Zugänge | Ist das Auth-Verfahren spezifiziert? |
| SEC-02 | Autorisierung | RBAC/ABAC mit Least Privilege | Ist das Berechtigungsmodell definiert? |
| SEC-03 | Verschlüsselung at Rest | AES-256 oder gleichwertig | Sind Verschlüsselungsanforderungen dokumentiert? |
| SEC-04 | Verschlüsselung in Transit | TLS 1.3 | Ist Transport-Verschlüsselung spezifiziert? |
| SEC-05 | Secrets Management | Kein Klartext, Vault/KMS Pflicht | Ist Secrets-Handling beschrieben? |
| SEC-06 | Input Validation | Whitelist-basiert, serverseitig | Sind Validierungsregeln definiert? |
| SEC-07 | Session Management | Timeout, Rotation, Secure Flags | Sind Session-Anforderungen dokumentiert? |
| SEC-08 | API Security | Rate Limiting, API Keys/OAuth, CORS | Sind API-Sicherheitsanforderungen definiert? |
| SEC-09 | Vulnerability Management | CVE-Scan wöchentlich, kritisch in 48h | Ist der Patch-Prozess beschrieben? |
| SEC-10 | Penetration Testing | Jährlich durch externen Dienstleister | Ist Pen-Testing vorgesehen? |

## 3. Audit & Logging (AUD)

| # | Prüfpunkt | Mindestanforderung KRITIS | Frage an Spec |
|---|-----------|--------------------------|---------------|
| AUD-01 | Audit-Logging | Alle schreibenden Operationen + Auth-Events | Welche Events werden geloggt? |
| AUD-02 | Log-Retention | ≥90 Tage, ≥1 Jahr für Security-Events | Ist die Aufbewahrungsdauer definiert? |
| AUD-03 | Log-Integrität | Tamper-Proof (Append-Only, Signierung) | Ist Log-Integrität sichergestellt? |
| AUD-04 | Log-Zentralisierung | SIEM-Integration | Werden Logs zentral aggregiert? |
| AUD-05 | Nachvollziehbarkeit | Wer hat wann was geändert | Ist die Audit-Granularität definiert? |
| AUD-06 | NIS2-Meldepflicht | 24h Frühwarnung, 72h Vollmeldung | Ist der Meldeprozess berücksichtigt? |

## 4. Performance (PER)

| # | Prüfpunkt | Mindestanforderung | Frage an Spec |
|---|-----------|-------------------|---------------|
| PER-01 | Response Time | p95 ≤[Xms] für kritische Operationen | Sind Latenz-Zielwerte definiert? |
| PER-02 | Throughput | [X] Requests/Sekunde unter Last | Ist der Durchsatz spezifiziert? |
| PER-03 | Concurrent Users | [X] gleichzeitige Benutzer | Ist die Concurrent-User-Anzahl definiert? |
| PER-04 | Skalierung | Horizontal/Vertikal, Auto-Scaling-Trigger | Ist Skalierungsverhalten beschrieben? |
| PER-05 | Ressourcenlimits | CPU, RAM, Storage Budgets pro Service | Sind Ressourcenlimits definiert? |

## 5. Datenschutz (DAT)

| # | Prüfpunkt | Mindestanforderung DSGVO | Frage an Spec |
|---|-----------|-------------------------|---------------|
| DAT-01 | Datenkategorien | Klassifizierung aller verarbeiteten Daten | Welche Datenkategorien werden verarbeitet? |
| DAT-02 | Rechtsgrundlage | Art. 6 DSGVO pro Verarbeitungszweck | Ist die Rechtsgrundlage dokumentiert? |
| DAT-03 | Löschkonzept | Automatische Löschung nach Zweckerfüllung | Sind Löschfristen definiert? |
| DAT-04 | Datenminimierung | Nur erforderliche Daten erheben | Wird Datenminimierung eingehalten? |
| DAT-05 | Betroffenenrechte | Auskunft, Löschung, Portabilität | Sind Betroffenenrechte technisch berücksichtigt? |
| DAT-06 | DSFA | Datenschutz-Folgenabschätzung bei hohem Risiko | Ist eine DSFA erforderlich? |
| DAT-07 | Auftragsverarbeitung | AVV bei externen Dienstleistern | Sind AVV-Anforderungen dokumentiert? |

## 6. Betrieb (OPS)

| # | Prüfpunkt | Mindestanforderung | Frage an Spec |
|---|-----------|-------------------|---------------|
| OPS-01 | Monitoring | Health Checks, Alerting, Dashboards | Ist Monitoring spezifiziert? |
| OPS-02 | Deployment | Zero-Downtime, Rollback-Fähigkeit | Ist die Deployment-Strategie beschrieben? |
| OPS-03 | Configuration Management | Externalisiert, versioniert, nicht im Code | Ist Config-Management definiert? |
| OPS-04 | Incident Response | Eskalationspfade, Runbooks | Ist ein Incident-Response-Prozess definiert? |
| OPS-05 | Kapazitätsplanung | Prognostiziertes Wachstum berücksichtigt | Sind Kapazitätsannahmen dokumentiert? |

---

## Anwendung

1. SpecForge iteriert bei jeder Story-Erzeugung über alle 6 Kategorien
2. Fehlende NFRs werden als `[NFR-Lücke: ...]` markiert
3. Bei KRITIS-Projekten sind AVA, SEC, AUD Pflicht — keine Ausnahme
4. Bei Nicht-KRITIS empfiehlt SpecForge relevante Kategorien basierend auf Domäne
5. NFRs ohne quantifizierten Zielwert werden als "nicht testbar" markiert

## Schweregrad bei fehlenden NFRs

| Kategorie | KRITIS-Projekt | Nicht-KRITIS |
|-----------|---------------|-------------|
| AVA | BLOCKER | MAJOR |
| SEC | BLOCKER | MAJOR |
| AUD | BLOCKER | MINOR |
| PER | MAJOR | MINOR |
| DAT | BLOCKER (bei PII) | MAJOR (bei PII) |
| OPS | MAJOR | MINOR |
