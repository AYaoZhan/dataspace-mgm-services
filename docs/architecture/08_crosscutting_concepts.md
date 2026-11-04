# 8. Crosscutting concepts

## 8.1 Tokens, permissions and portal roles

- People call through the UI with their token from the Portal IAM of the OSP. Every module validates signature (JWKS),
  issuer of its own installation, expiry and audience `portal-core`.
- Permissions are client roles on the client `portal-core`, named `<verb>_<object>` (e.g. `register_company`), with a scope
  `company`, `osp` or `own`. Portal roles (`Company Admin`, `IT Admin`, `Member`, `OSP Reviewer`, `OSP Admin`, `Applicant`)
  bundle permissions.
- Process Orchestration and modules in the same process call without a token; over HTTP, the service accounts
  `svc-<module>` with the permissions `execute_steps_<module>` and `query_<module>` are used.

## 8.2 Steps, events and the outbox

- Paths under `/steps/...` are steps for Process Orchestration, paths under `/internal/...` are queries for other modules.
- Every module publishes its events through its own outbox; events never contain secrets.

## 8.3 Errors

Errors are returned as Problem Details (RFC 9457) with a `type` per error as listed in section 12 of each module spec.

## 8.4 Secrets and data protection

- No passwords: people sign in with the EUDI Wallet.
- Secrets (client secrets, signing keys) are provided as Kubernetes secrets, never in values files that are committed.
- Each module stores only the data it needs and documents what it deliberately does not store (section 5 of each module spec).

## 8.5 Installation settings

Every installation has one settings file (`ospId`, `ospName`, `ospCompanyId`, dataspace, master data) that every module
reads at start-up (FRAMEWORK 4.8). In Kubernetes it is provided by the Helm chart (`backend.installation`).

## 8.6 Internationalisation

Roles carry descriptions per language as role attributes (`description.de`, `description.en`); error and validation
messages of the API are keys that the UI translates.

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: https://github.com/eclipse-tractusx/dataspace-mgm-service/blob/main/docs/architecture/08_crosscutting_concepts.md
