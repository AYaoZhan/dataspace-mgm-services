# 2. Architecture constraints

| Constraint | Background |
|---|---|
| Open source under the Eclipse Foundation | Apache-2.0 for code, CC-BY-4.0 for documentation; Eclipse Development Process and IP policy; third-party dependencies are checked with the Eclipse Dash License Tool. |
| Tractus-X Release Guidelines (TRGs) | Repository structure, documentation, container images on DockerHub, Helm charts, security scans; see the [release guidelines](https://eclipse-tractusx.github.io/docs/release). |
| Python 3.12 and FastAPI | Decided for the modular monolith (FRAMEWORK 1). Dependencies are managed with `uv` (`pyproject.toml`, `uv.lock`). |
| OpenAPI 3.1 per module | `openapi.yaml` of a module is the contract for the UI, for third parties and for calls in the same process. |
| Keycloak as Portal IAM | Configured only, no extensions (C2-M5). Only modules of C2 write to Keycloak. |
| PostgreSQL, one database per module | No module reads or writes the database of another module (FRAMEWORK 1). The current code base keeps its data in memory. |
| Kubernetes and Helm | The installation of an OSP is deployed with the product Helm chart in [`charts/dataspace-mgm`](../../charts/dataspace-mgm). |
| Wallet standards | OpenID4VP and OpenID Connect at the EBW-Connector (C5-M1); EUDI Wallet (PID, mandate) and Business Wallet (LPID). |

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: https://github.com/eclipse-tractusx/dataspace-mgm-service/blob/main/docs/architecture/02_architecture_constraints.md
