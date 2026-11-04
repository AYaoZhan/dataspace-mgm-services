# 12. Glossary

| Term | Meaning |
|---|---|
| BDRS | Directory from the company identifier (BPN) to the DID of the company, run by the CSP |
| BPN | Business Partner Number, the company identifier assigned by the CSP |
| Business Wallet | Wallet of the company (in the browser) that holds the LPID and issues mandates to employees |
| CSP | Core service provider: runs the core services (trust list, BPN, BDRS, discovery) and optionally an issuer or a dataspace wallet |
| Dataspace wallet | Wallet of a company in the dataspace that holds its credentials (e.g. IdentityHub) |
| EBW-Connector | Module C5-M1: checks the EUDI Wallet and the Business Wallet and is the identity provider of the Portal IAM |
| EUDI Wallet | European digital identity wallet of a person (on the phone) that holds the PID and the mandate |
| Installation | Everything one OSP runs: modules, Process Orchestration, databases, Portal IAM, EBW-Connector and UI |
| LPID | Legal person identification data of a company |
| Mandate | Authorisation of a person to act for a company, issued by the Business Wallet |
| OSP | Onboarding service provider: runs its own installation and onboards companies to the dataspace |
| PID | Person identification data from the EUDI Wallet |
| Portal IAM | Keycloak of an installation (C2-M5) with the client `portal-core`, permissions and portal roles |
| Process Orchestration | Module C12-M1 that runs the flows across modules |
| Stand-in | Built-in replacement of a neighbour so that a module can run and be tested alone |

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: https://github.com/eclipse-tractusx/dataspace-mgm-service/blob/main/docs/architecture/12_glossary.md
