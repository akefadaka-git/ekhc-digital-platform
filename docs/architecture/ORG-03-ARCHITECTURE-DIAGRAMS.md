# ORG-03 A1 Architecture Diagrams

**Document ID:** EKHC-ORG03-A1-ARCH-003  
**Status:** Conceptual draft — subject to institutional evidence and Owner approval  
**Baseline:** Synthetic A3 commit `fca11fd4d975aa55e2bd2f7e975c832802eb7bf1`

These diagrams express logical boundaries, not deployed infrastructure. They do not imply that any provider, institutional directory, records service, KMS/HSM or hosting environment has been selected or connected.

## 1. System context

```mermaid
flowchart LR
  H[Institutional human actors] -->|authenticate| IDP[Institution-approved identity authority]
  H --> C[Web / mobile client]
  C --> API[ORG-03 API boundary]
  IDP -->|identity assertion| API
  API --> POL[Server-side policy decision]
  POL --> WF[ORG-03 workflow service]
  WF --> DB[(Transactional persistence)]
  WF --> OUT[Transactional outbox]
  OUT --> NA[Notification adapter]
  NA --> NP[Approved provider - future decision]
  NP -->|delivery evidence| NA
  NA --> WF
  WF --> RR[Restricted-record adapter]
  RR --> RS[Institutional records system - future decision]
  WF --> AUD[Security and audit pipeline]
  KMS[Independent key custody] --> WF
  TIME[Authoritative time service] --> WF
  DB --> BK[Independent backup / recovery domain]
  AUD --> SIEM[Institutional monitoring - future decision]
```

## 2. Trust boundaries and data flows

```mermaid
flowchart TB
  subgraph Z1[Untrusted client zone]
    UI[Browser / mobile client]
  end
  subgraph Z2[Institution identity zone]
    IDP[Identity provider / federation]
    AUTH[Institutional appointment and delegation source]
  end
  subgraph Z3[Application security zone]
    GW[API gateway]
    PE[Authentication and policy enforcement]
    WF[Workflow state machine]
  end
  subgraph Z4[Data zone]
    DB[(Workflow DB and append-only events)]
    OB[(Outbox / inbox)]
    AUD[(Audit records)]
  end
  subgraph Z5[Independent trust services]
    KMS[KMS / HSM custody]
    TS[Trusted time source]
    CP[Independent checkpoint service]
    BK[Independent backup domain]
  end
  subgraph Z6[Institution controlled external services]
    REC[Restricted records service]
    MSG[Approved notification provider]
  end
  UI -->|untrusted command and claimed metadata| GW
  IDP -->|authenticated subject assertion| PE
  AUTH -->|versioned authority evidence| PE
  GW --> PE --> WF
  WF --> DB
  WF --> OB --> MSG
  MSG -->|provider receipt only| OB
  WF --> REC
  WF --> KMS
  TS --> WF
  DB --> CP
  DB --> BK
  WF --> AUD
```

## 3. Conceptual deployment zones

```mermaid
flowchart TB
  subgraph EDGE[Institution-approved ingress]
    WAF[WAF / rate limiting]
    LB[Load balancer]
  end
  subgraph APP[Private application zone]
    API1[API instance A]
    API2[API instance B]
    WORK[Background workers]
  end
  subgraph DATA[Restricted data zone]
    DB[(HA relational database)]
    QUEUE[(Transactional outbox tables)]
  end
  subgraph TRUST[Separate trust and operations zone]
    KEY[KMS / HSM]
    TIME[Time synchronization]
    LOG[Central audit / SIEM]
    BACKUP[Immutable independent backups]
  end
  subgraph EXT[Institution-approved external boundaries]
    IDP[Identity provider]
    RECORDS[Records system]
    PROVIDER[Notification provider]
  end
  WAF --> LB
  LB --> API1
  LB --> API2
  API1 --> DB
  API2 --> DB
  API1 --> KEY
  API2 --> KEY
  WORK --> DB
  WORK --> QUEUE
  WORK --> PROVIDER
  API1 --> IDP
  API2 --> IDP
  API1 --> RECORDS
  API2 --> RECORDS
  API1 --> TIME
  API2 --> TIME
  WORK --> LOG
  DB --> BACKUP
```

This is a logical target only. Network segmentation, trust routes, data residency, tenancy, redundancy and administrator access remain decisions for the institution.

## 4. Acknowledgement and escalation sequence

```mermaid
sequenceDiagram
  participant Actor as Authorized actor
  participant API as ORG-03 API
  participant Policy as Authority and policy service
  participant DB as Transactional store
  participant Worker as Outbox worker
  participant Provider as Notification provider
  participant Responder as Assigned responder
  Actor->>API: Submit workflow command
  API->>Policy: Authenticate and authorize
  Policy-->>API: Decision plus evidence reference
  API->>DB: Atomic event + aggregate + idempotency + outbox
  DB-->>API: Commit confirmed
  API-->>Actor: Stable command result
  Worker->>DB: Claim outbox item
  Worker->>Provider: Send minimal notification
  Provider-->>Worker: Provider receipt
  Worker->>DB: Record provider receipt separately
  Responder->>API: Authenticated acknowledgement
  API->>Policy: Revalidate current authority and scope
  Policy-->>API: Authorization decision
  API->>DB: Append human acknowledgement event
  Note over DB: Delivery receipt is not human acknowledgement; acknowledgement is not closure
```

## 5. Diagram controls and unresolved items

- Client data is untrusted until validated and authorized server-side.
- Identity assertions and appointment/delegation evidence are separate inputs.
- KMS/HSM, time, checkpoint, backup and audit services must have explicit trust and administrator boundaries.
- Provider receipt is not human acknowledgement.
- Restricted-record access has its own authorization and audit boundary.
- The database/outbox atomicity and independent checkpoint protocol require a detailed design.
- No component shown here is proof of institutional availability or approval.

**Status:** conceptual diagrams prepared; deployment-specific topology and institutional trust paths remain UNRESOLVED.
