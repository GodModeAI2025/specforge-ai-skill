# STRIDE-Checkliste

Threat-Modeling-Framework für security-relevante Requirements. Bei jeder security-relevanten Story alle 6 Kategorien prüfen.

## S — Spoofing (Identitätsvortäuschung)

**Bedrohung:** Angreifer gibt sich als legitimer Benutzer, Service oder System aus.

| # | Prüfpunkt | Frage |
|---|-----------|-------|
| S-01 | Benutzer-Authentifizierung | Wie wird die Identität des Benutzers verifiziert? |
| S-02 | Service-zu-Service-Auth | Wie authentifizieren sich Services untereinander? (mTLS, API Keys, OAuth) |
| S-03 | Token-Validierung | Werden Tokens serverseitig validiert? Signaturprüfung? Ablaufzeit? |
| S-04 | Credential Storage | Wie werden Credentials gespeichert? (Hashing, Salting, Algorithmus) |
| S-05 | MFA | Ist MFA für privilegierte Operationen vorgesehen? |
| S-06 | Session Hijacking | Sind Sessions gegen Übernahme geschützt? (Secure, HttpOnly, SameSite) |

**Mitigations:** MFA, mTLS, JWT mit kurzer Laufzeit, Certificate Pinning, IP-Binding

## T — Tampering (Manipulation)

**Bedrohung:** Angreifer verändert Daten während Übertragung oder im Speicher.

| # | Prüfpunkt | Frage |
|---|-----------|-------|
| T-01 | Transport-Verschlüsselung | Ist TLS 1.3 für alle Kanäle erzwungen? |
| T-02 | Datenintegrität | Werden Checksummen/Signaturen für kritische Daten geprüft? |
| T-03 | Input Validation | Wird jeder Input serverseitig validiert? Whitelist-Ansatz? |
| T-04 | SQL Injection | Werden Prepared Statements / Parameterized Queries verwendet? |
| T-05 | XSS | Wird Output Encoding konsequent angewendet? CSP-Header? |
| T-06 | File Upload | Werden hochgeladene Dateien validiert? (Typ, Größe, Inhalt) |
| T-07 | Konfiguration | Sind Konfigurationsdateien gegen Manipulation geschützt? |

**Mitigations:** TLS 1.3, HMAC-Signaturen, Input Sanitization, CSP, Parameterized Queries

## R — Repudiation (Abstreitbarkeit)

**Bedrohung:** Benutzer oder System bestreitet eine durchgeführte Aktion.

| # | Prüfpunkt | Frage |
|---|-----------|-------|
| R-01 | Audit-Logging | Werden alle sicherheitsrelevanten Aktionen geloggt? |
| R-02 | Log-Inhalt | Enthält jeder Log-Eintrag: Actor, Timestamp, Action, Resource, Result? |
| R-03 | Log-Integrität | Sind Logs gegen nachträgliche Manipulation geschützt? |
| R-04 | Zeitstempel | Wird eine vertrauenswürdige Zeitquelle verwendet? (NTP) |
| R-05 | Nicht-Abstreitbarkeit | Gibt es digitale Signaturen für kritische Transaktionen? |
| R-06 | Log-Retention | Werden Logs gemäß regulatorischer Anforderungen aufbewahrt? |

**Mitigations:** Zentrales SIEM, Tamper-Proof Logging, Digitale Signaturen, NTP-Synchronisierung

## I — Information Disclosure (Informationsoffenlegung)

**Bedrohung:** Vertrauliche Informationen werden unbefugt offengelegt.

| # | Prüfpunkt | Frage |
|---|-----------|-------|
| I-01 | Fehlerbehandlung | Gibt das System interne Details in Fehlermeldungen preis? |
| I-02 | API-Responses | Werden nur minimal notwendige Daten zurückgegeben? |
| I-03 | Logging | Werden sensible Daten (Passwörter, Tokens, PII) in Logs maskiert? |
| I-04 | Encryption at Rest | Sind sensible Daten im Speicher verschlüsselt? |
| I-05 | Header-Leaks | Werden Server-/Framework-Versionen in HTTP-Headern unterdrückt? |
| I-06 | Directory Listing | Ist Directory Listing deaktiviert? |
| I-07 | Caching | Werden sensible Responses mit Cache-Control: no-store versehen? |
| I-08 | Seitenkanal | Sind Timing-Angriffe auf Auth-Endpunkte verhindert? |

**Mitigations:** Generische Fehlermeldungen, Field-Level Encryption, Log-Masking, Security Headers

## D — Denial of Service (Dienstverweigerung)

**Bedrohung:** Angreifer macht das System für legitime Benutzer unverfügbar.

| # | Prüfpunkt | Frage |
|---|-----------|-------|
| D-01 | Rate Limiting | Gibt es Request-Limits pro Client/IP/User? |
| D-02 | Resource Limits | Sind CPU, RAM, Connection-Pools begrenzt? |
| D-03 | Payload Limits | Gibt es Größenlimits für Requests, Uploads, Batch-Operationen? |
| D-04 | Timeout-Konfiguration | Sind Timeouts für alle externen Aufrufe konfiguriert? |
| D-05 | Circuit Breaker | Gibt es Circuit Breaker für abhängige Services? |
| D-06 | Queue-Schutz | Sind Message Queues gegen Überlauf geschützt? (DLQ, Backpressure) |
| D-07 | DDoS-Schutz | Ist DDoS-Mitigation vorgesehen? (WAF, CDN) |
| D-08 | Graceful Degradation | Ist definiert, wie das System bei Überlast reagiert? |

**Mitigations:** Rate Limiting, WAF, Auto-Scaling, Circuit Breaker, Bulkhead Pattern

## E — Elevation of Privilege (Rechteeskalation)

**Bedrohung:** Benutzer erlangt höhere Berechtigungen als vorgesehen.

| # | Prüfpunkt | Frage |
|---|-----------|-------|
| E-01 | Least Privilege | Haben Benutzer und Services nur minimal notwendige Rechte? |
| E-02 | Autorisierungsprüfung | Wird die Berechtigung bei jeder Operation serverseitig geprüft? |
| E-03 | IDOR | Sind Insecure Direct Object References verhindert? |
| E-04 | Admin-Funktionen | Sind administrative Funktionen zusätzlich abgesichert? |
| E-05 | Privilege Escalation via API | Kann ein Benutzer über API-Calls Rechte ändern, die er über UI nicht hat? |
| E-06 | Default Credentials | Werden Default-Passwörter bei Installation erzwungen geändert? |
| E-07 | Service Accounts | Sind Service-Accounts mit minimalen Rechten und rotierenden Credentials konfiguriert? |

**Mitigations:** RBAC/ABAC, Serverseitige Autorisierung, UUID-basierte Ressourcen-IDs, PAM

---

## Anwendung in SpecForge

1. Bei jeder Story mit SEC-NFR oder expliziter Anfrage
2. **Alle 6 Kategorien werden geprüft** — auch wenn nur einzelne offensichtlich relevant sind
3. Output: Tabelle im spec.md mit Bewertung pro Kategorie
4. Fehlende STRIDE-Analyse für security-relevante Stories = BLOCKER in Analyze
5. STRIDE wird bei Spec-Updates wiederholt, nicht nur einmalig

## Output-Format

```markdown
#### STRIDE-Bewertung: [SF-SEC-NNN]

| Kategorie | Relevant | Befund | Risiko | Mitigation | Status |
|-----------|----------|--------|--------|-----------|--------|
| Spoofing | Ja/Nein | ... | Hoch/Mittel/Niedrig | ... | Offen/Mitigiert |
| Tampering | ... | ... | ... | ... | ... |
| Repudiation | ... | ... | ... | ... | ... |
| Info Disclosure | ... | ... | ... | ... | ... |
| Denial of Service | ... | ... | ... | ... | ... |
| Elev. of Privilege | ... | ... | ... | ... | ... |

**Offene Risiken:** [Anzahl]
**Höchstes Risiko:** [Kategorie + Stufe]
```
