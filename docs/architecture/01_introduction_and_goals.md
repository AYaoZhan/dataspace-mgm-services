# 1. Introduction and goals

## 1.1 Requirements overview

The Dataspace Management is the modernised portal of Eclipse Tractus-X. It lets an **onboarding service provider (OSP)**
admit companies to a dataspace such as Catena-X and manage them afterwards:

- registration and review of companies (C1), with the identity of persons and companies proven by wallets (EUDI Wallet, Business Wallet),
- people, roles and technical users of the companies (C2),
- the company profile and the connection to the core services of the core service provider (CSP) (C3),
- credentials and dataspace wallets of the companies (C4),
- connectors, offers (apps and services), subscriptions and notifications (C6 to C11),
- the flows across these modules, run by Process Orchestration (C12).

Today's portal is a monolith whose user interface owns orchestration and business rules, and a third party cannot use a
capability without the portal UI. The Dataspace Management splits the portal into modules with clear interfaces and
makes these interfaces the only way in. **No single party runs the portal for all participants of a dataspace:** every OSP
runs its own installation, the CSP provides trust (OSP 2.0, decided on 28 Oct 2026).

## 1.2 Quality goals

| Priority | Quality goal | Motivation |
|---|---|---|
| 1 | Interoperability | Every capability is reachable through its documented interface (OpenAPI), by the UI of the OSP and by third parties. |
| 2 | Security and data protection | Sign-in without passwords through wallets; permissions per operation; no secrets in events; data minimisation per module. |
| 3 | Modifiability | One module per folder with its own interface and data, replaceable without touching the others; flows are data, not code. |
| 4 | Operability | One Helm chart per installation; every OSP decides which services it runs itself and which it uses from the CSP. |

## 1.3 Stakeholders

| Role | Expectation |
|---|---|
| Onboarding service provider (OSP) | Runs and configures its own portal installation; reviews and onboards companies. |
| Core service provider (CSP) | Provides the trust list, company identifiers (BPN), the directory BPN → DID and discovery. |
| Company administrators and members | Register their company and manage people, technical users, connectors and subscriptions. |
| App and service providers | Publish offers and manage subscriptions. |
| Operators | Install, configure, monitor and upgrade the installation (see the [admin guide](../admin/README.md)). |
| Developers | Implement modules against the module specifications. |

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: https://github.com/eclipse-tractusx/dataspace-mgm-service/blob/main/docs/architecture/01_introduction_and_goals.md
