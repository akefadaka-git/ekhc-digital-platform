# EKHC OS — A3 corrective implementation record for A4-F01–F04

**Base:** `a8042051824ddb50592492ee75d5aad24d1bb03a`  
**Corrective branch:** `a3/monitoring-operational-readiness-a4-corrections`  
**Scope:** Owner-authorized A3 corrective work only; no merge, deployment, schedule activation, or A5.

## Corrections

- **A4-F01:** Removed the misleading hard-wall-clock interpretation. The implementation now names the 63-second figure a nominal configured socket-timeout plus backoff budget. Documentation explicitly states that urllib's timeout is an inactivity timeout and a continuously streaming response can exceed the nominal budget. No hard end-to-end deadline is claimed.
- **A4-F02:** Replaced the literal escaped newline sequence between the retry explanation and read-only controls with actual Markdown paragraph breaks.
- **A4-F03:** Corrected report evidence references to be reconciled against the exact corrective implementation commit and its workflow run metadata after CI completes.
- **A4-F04:** Added tests proving HTTP 429/5xx exhaustion stops after exactly three attempts and exactly two backoff sleeps, and that `main()` returns exit code 2 with an INCOMPLETE summary on OSV transport failure.

## Boundaries

The response-size cap, retry classification, three-attempt maximum, 1s/2s backoff, read-only permissions, empty exception register, inactive schedule, and operational-notification limitations remain unchanged. The accepted A4 branch and `main` are not modified.
