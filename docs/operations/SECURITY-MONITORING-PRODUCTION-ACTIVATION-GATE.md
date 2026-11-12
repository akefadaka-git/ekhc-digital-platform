# EKHC OS — Security Monitoring Production Activation Gate

**Status:** DOCUMENTED — NOT AUTHORIZED  
**Applies to:** read-only OSV advisory and exception-expiry monitor  
**Scheduled time configured:** 06:15 UTC daily

## 1. Current state

The workflow has a daily schedule, manual dispatch, A3 push validation, and pull-request validation. GitHub scheduled workflows execute only from the repository default branch. This A3 branch is not the default branch, so the daily schedule is inactive. Manual dispatch and applicable branch/PR checks do not activate the schedule.

This document does not enable, move, or activate the schedule. Default-branch integration, merge, deployment, production operation, and A5 remain separately gated and are not authorized by the A3 implementation approval.

## 2. Mandatory activation prerequisites

Every item below must be evidenced and separately reviewed before any proposal to activate production scheduling:

- [ ] Exact-head A4 verification of the final implementation commit, including quality and monitoring workflow results.
- [ ] Independent review of retry classification, bounded response handling, report rendering, and failure/exit behavior.
- [ ] Confirmation that only least-privilege read permissions are required and remain configured.
- [ ] Explicit Owner approval for default-branch integration and schedule activation; these are distinct decisions.
- [ ] Verified notification channel, recipient identities, and delivery behavior; no channel or recipient is assumed by this repository.
- [ ] Verified acknowledgement expectations, responder availability, backup/holiday coverage, and escalation path.
- [ ] Verified custody and access controls for restricted exception records; the public metadata register remains non-sensitive and empty unless separately authorized.
- [ ] Controlled rehearsal using synthetic, non-sensitive fixtures, including a positive advisory report, retry exhaustion, an overdue reminder, and an INCOMPLETE result.
- [ ] Evidence that the rehearsal is received and understood by the authorized responders; a green GitHub job alone is insufficient.
- [ ] Documented rollback/disable procedure and named Owner authorization record.

## 3. Prohibited shortcuts

- Do not merge or retarget the workflow to the default branch as an implementation convenience.
- Do not treat a successful manual run as activation or proof of human notification.
- Do not invent recipients, roles, escalation routes, or response coverage.
- Do not create real exception records for testing or modify approval/status metadata automatically.
- Do not broaden permissions, add secrets, install/update dependencies, or access protected/production data for this work package.
- Do not activate scheduled production monitoring without separate explicit Owner authorization.

## 4. Decision record

**Current disposition:** NOT READY FOR PRODUCTION ACTIVATION.  
**Schedule:** INACTIVE OFF DEFAULT BRANCH.  
**Notification and human response:** UNVERIFIED.  
**Default-branch integration / merge:** NOT AUTHORIZED.  
**Deployment / production operation / A5:** NOT AUTHORIZED.

The activation gate is documentation only. Reassessment requires evidence for each prerequisite and a separate Owner decision.
