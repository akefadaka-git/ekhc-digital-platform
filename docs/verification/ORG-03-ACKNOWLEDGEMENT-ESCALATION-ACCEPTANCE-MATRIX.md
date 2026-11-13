# ORG-03 Verification and Acceptance Matrix

**Test mode:** Synthetic fixtures only. No real recipients, contacts, alerts, or institutional channels.  
**Execution status:** NOT RUN — rehearsal requires separate Owner authorization.

| ID | Scenario | Expected behavior | Evidence required |
|---|---|---|---|
| O3-01 | Primary and backup refer to same responder | Roster activation rejected | Validation result |
| O3-02 | Primary assignment missing/expired/unaccepted | Coverage INCOMPLETE; no activation | Roster validation record |
| O3-03 | Backup assignment missing/expired/unaccepted | Coverage INCOMPLETE; no activation | Roster validation record |
| O3-04 | Owner/delegate route missing or delegation expired | AUTHORITY_ROUTE_UNAVAILABLE; operational status NOT VERIFIED | Escalation validation record |
| O3-05 | Primary accepts alert | PRIMARY_ACKNOWLEDGED; append-only human event recorded | Redacted acknowledgement event |
| O3-06 | Primary explicitly unable to accept | Immediate BACKUP_ROUTED | Transition and event references |
| O3-07 | Primary does not acknowledge by due time | SLA_BREACH_PRIMARY; route to backup | Clock calculation and transition |
| O3-08 | Backup cannot accept or misses target | SLA_BREACH_BACKUP; escalate to Owner/delegate | Escalation event |
| O3-09 | Primary delivery fails | DELIVERY_UNCONFIRMED; approved alternate route only | Provider failure and fallback evidence |
| O3-10 | All delivery routes fail | Preserve unconfirmed state; raise control failure; never claim human receipt | Failure audit trail |
| O3-11 | Shift handover without incoming acceptance | Outgoing assignment remains responsible; coverage gap raised | Handover event |
| O3-12 | Alert outside coverage / holiday | Apply approved calendar and route to current backup/authority; no inferred coverage | Calendar and routing evidence |
| O3-13 | Acknowledgement from unauthorized role | Reject as valid acknowledgement; retain attempted event as audit evidence | Authorization decision |
| O3-14 | Human acknowledgement arrives after deadline | Record actual time and SLA breach; do not rewrite due time | Immutable timestamps |
| O3-15 | Acknowledgement mistaken for closure | Alert remains open pending separate disposition and closure authority | State transition evidence |
| O3-16 | Public artifact contains names, phone/email, credentials or restricted content | Publication rejected; remove sensitive data before public commit | Privacy review |

## Acceptance criteria

- All roster assignments are distinct, accepted, authorized and time-bounded.
- Coverage calendar and business-day clock are approved, explicit and testable.
- Each route has a verified institutional destination and redacted delivery evidence.
- Human acknowledgement is distinct from provider delivery and workflow completion.
- Primary-to-backup-to-Owner/delegate transitions are append-only and auditable.
- Missing assignments, delivery failures, expired delegation and missed targets fail closed.
- No synthetic test creates a real institutional notification or changes production state.
- A4 closure requires exact-head CI, independent evidence review, and separately authorized synthetic rehearsal where required.

**Current disposition:** Process design and test matrix prepared; all execution evidence remains NOT RUN / NOT PROVIDED. Operational readiness remains NOT VERIFIED.
