# 6. Runtime view

## 6.1 Onboarding of a company with Business Wallet

The most important flow (FRAMEWORK 5.2). Every step after the submission runs through Process Orchestration and is
event-driven.

```mermaid
sequenceDiagram
    autonumber
    actor P as Person (EUDI Wallet)
    participant UI as Dataspace Management UI
    participant IAM as Portal IAM
    participant EBW as EBW-Connector (C5-M1)
    participant REG as Registration (C1-M2)
    participant PO as Process Orchestration (C12-M1)
    participant REV as Application Review (C1-M3)
    participant CSP as CSP Connection (C3-M2)
    actor R as OSP Reviewer

    P->>UI: sign in
    UI->>IAM: OpenID Connect
    IAM->>EBW: identity provider
    EBW-->>IAM: PID of the person
    P->>UI: register company
    UI->>EBW: verification attestation (PID, mandate, LPID)
    UI->>REG: create application with attestation
    REG-->>PO: ApplicationCreated
    P->>UI: submit with consents
    UI->>REG: submit
    REG-->>PO: ApplicationSubmitted
    PO->>REV: open-review (pre-check with duplicate check)
    REV->>CSP: find-companies
    R->>REV: approve
    REV-->>PO: ApplicationApproved
    PO->>CSP: register-company (BPN, home OSP)
    Note over PO: then assign-identifier, create-wallet, register-did,<br/>issue-credentials, register-membership,<br/>assign-company-admin, activate-company, complete-application
```

## 6.2 Further flows

The framework of the specification describes the other flows across modules: admission of an OSP, people of a company,
deactivation and reactivation of a company, transfer to another OSP, technical users with wallet access, app approval and
subscription, and connectors in the discovery. Process Orchestration runs all of them from `flows.yaml`.

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: https://github.com/eclipse-tractusx/dataspace-mgm-service/blob/main/docs/architecture/06_runtime_view.md
