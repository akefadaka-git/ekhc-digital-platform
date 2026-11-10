# Ethiopian Kale Heywot Church Operating System (EKHC OS)

A national, Amharic-first, multilingual digital platform intended to support church governance, administration, membership, ministries, communication, education, and organizational operations across Ethiopia.

## Project status

**Stage:** A1 — Assessment, specification, and architecture (draft; not approved or frozen)

This repository is the independent home of EKHC OS. It is not part of ARNA, MASES, MaaleNex, or IROKA.

## Governance and delivery gates

Work is Owner-governed and stage-gated:

1. **A1 — Assessment and specification:** establish authoritative requirements, validate organizational terminology and hierarchy, assess risks, and prepare the architecture for review.
2. **A2 — Read-only reconciliation:** compare the approved baseline with authoritative source material and existing work without implementation changes.
3. **A3 — Implementation:** begin only after A1 approval and A2 reconciliation authorization.
4. **A4 — Verification:** validate implementation, security, quality, and acceptance criteria.
5. **A5 — Deployment readiness:** assess separately; deployment requires separate authorization.

No production features, production data migrations, deployment, signing, or publication are authorized by this initial repository foundation.

## Foundational constraints

- Amharic-first and multilingual experience.
- Ethiopian calendar as the default calendar, with Gregorian preference support where required.
- Web, Android, iOS, and offline-capable PWA are target delivery channels, subject to A1 validation.
- Offline-first behavior with controlled synchronization is a design requirement to validate.
- Organization-scoped authorization, role/permission controls, and auditable actions are mandatory design concerns.
- The authoritative organizational baseline for current A1 work is the EKHC Constitution / Bylaw, Sixth Revision, 2012 E.C. (2020 G.C.), in Amharic.
- Constitutional names must be preserved in Amharic as canonical labels; translations are secondary and must not introduce a new organizational meaning.
- The terms **ወረዳ** and **District** are prohibited in the application, documentation, code, database schemas, APIs, UI, reports, and analytics. Do not translate ኅብረት as “District”; use the constitutional Amharic name and a separately verified English equivalent only.
- Existing EKHC UI and related work must be discovered and assessed before any replacement or integration; do not overwrite it blindly.

## Constitutional source baseline — initial A1 extraction

The working source is titled **የኢትዮጵያ ቃለ ሕይወት ቤተ ክርስቲያን — መተዳደሪያ ደንብ (ለስድስተኛ ጊዜ የተሻሻለ), 2012 ዓ.ም.** The publicly accessible copy identifies EKHC as copyright holder and EKHC Communication and Literature Department as publisher. Its hosting on a third-party platform does not independently prove authenticity; seek confirmation against EKHC's own publication where possible.

Public copy (reference only; do not reproduce the full copyrighted text):
https://www.scribd.com/document/943135783/የቃለ-ህይወት-መተዳደሪያ-ደንብ

Official corroborating sources:
- https://ekhc.et/
- https://ekhc.et/amh/

The constitution governs organizational authority and offices. Current website content and official social channels may corroborate current departments, ministries, office names, and public-facing practice, but must not silently amend or override constitutional provisions.

### Article 7 — principal authority and offices

Article 7.1 identifies the principal authority-bearing assemblies at the four constitutional levels:

1. አጥቢያ ቤተ ክርስቲያን ጠቅላላ ጉባኤ
2. የአጥቢያ ቤተ ክርስቲያናት ኅብረት ጠቅላላ ጉባኤ
3. የቀጣና ጠቅላላ ጉባኤ
4. የኢትዮጵያ ቃለ ሕይወት ቤተ ክርስቲያን ጠቅላላ ጉባኤ

Article 7.2 names the following office types:
- የአጥቢያ ቤተ ክርስቲያን ጽ/ቤት
- የአጥቢያ ቤተ ክርስቲያናት ኅብረት ጽ/ቤት
- ልዩ የአጥቢያ ቤተ ክርስቲያናት ኅብረት ጽ/ቤት
- ታዳጊ የአጥቢያ ቤተ ክርስቲያናት ኅብረት ጽ/ቤት
- የቀጣና ጽ/ቤት
- ዋና ጽ/ቤት

Article 7.3 provides for each level office to have its own organization and internal procedures. Governing assemblies and administrative offices must therefore be separate entity types in the system.

### Article 11 — Local Church service and leadership bodies

Article 11.1 enumerates:
- የአባላት ጠቅላላ ጉባኤ
- የሽማግሌዎች ጉባኤ
- መጋብያን እና ወንጌላውያን
- የሴቶች አገልግሎት
- የወጣቶች አገልግሎት
- የልጆች አገልግሎት
- የዲያቆናት አገልግሎት
- የቤተ ክርስቲያን እና የማኅበረሰብ ሁለንተናዊ አገልግሎት
- ሌሎች አገልጋይ ሠራተኞች እና ልዩ ልዩ አገልግሎቶች

These categories must not be automatically reclassified as departments, committees, or executive offices without the relevant constitutional provision.

### Constitutional article ranges

The constitution's contents organize the document as follows:
- Articles 9–24: አጥቢያ ቤተ ክርስቲያን
- Articles 25–41: የአጥቢያ ቤተ ክርስቲያናት ኅብረት
- Articles 42–56: ቀጣና
- Articles 57–77: የኢትዮጵያ ቃለ ሕይወት ቤተ ክርስቲያን
- Articles 78–105: ልዩ ልዩ ድንጋጌዎች

These ranges are navigation references, not a substitute for extracting each provision and its exact sub-clauses.

## Terminology and data rules

- Preserve constitutional Amharic names as canonical labels.
- Use ቀጣና for the constitutional Zone level.
- Preserve ኅብረት as the constitutional term; do not replace it with a prohibited or unverified English label.
- Do not invent organizational tiers, offices, departments, committees, titles, roles, or reporting lines.
- Distinguish governing assemblies, boards/committees, offices, service bodies, departments, and individual officeholders.
- Store the source article and sub-article reference for each organizational rule.
- Record conflicting, incomplete, or unverified information as UNVERIFIED, CONFLICT, or NOT FOUND. Never silently infer.
- Current officeholders and current operational arrangements require separate, dated evidence.

## A1 completion requirements

Before A1 can be submitted for Owner approval:

1. Extract Articles 7–8 and 9–105, including relevant sub-clauses, powers, responsibilities, elections, terms, appointment, reporting, authority, discipline, audit, and handover provisions.
2. Build a source-to-system reconciliation matrix with exact Amharic names, article references, carefully verified English working translations, entity type, parent relationship, authority, and verification status.
3. Reconcile the constitutional baseline against EKHC's official website and verified official social channels without treating web copy as constitutional amendment.
4. Identify any later approved amendments or official policies, if evidenced.
5. Deliver a formal requirements specification, organization model, permissions/authority model, audit model, and architecture proposal.
6. Keep implementation frozen until explicit A1 approval.

## Scope discipline

This repository starts with governance, assessment, and specification. Do not introduce production application code or broaden scope without an approved stage gate.

## Current status

**A1 — IN PROGRESS.** This documentation update is an initial source-backed baseline only. No production feature, live member data, real officeholder record, migration, deployment, or external integration has been implemented.
