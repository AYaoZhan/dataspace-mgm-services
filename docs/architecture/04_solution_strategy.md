# 4. Solution strategy

| Goal | Approach |
|---|---|
| Interfaces are the only way in | Every module has an `openapi.yaml` (OpenAPI 3.1); the UI and third parties call the same interface. Permissions come from `x-permission` in the specification, not from code. |
| Replaceable modules | **Modular monolith** in Python with FastAPI: one folder per module with `interface.py` (public interface) and `router.py` (HTTP). Modules call each other in the same process through the public interface; a module can be split out and called over HTTP without changing its callers. |
| Flows without hidden coupling | **Process Orchestration** (C12-M1): flows are data (`flows.yaml`). Every step of a flow runs through Process Orchestration; modules call each other directly only for queries. Event-driven, long-running steps answer "running" and end with an event. |
| Own data per module | One PostgreSQL database and database user per module; references to other modules only by ID. Events go out through an outbox per module and never carry secrets. |
| Trust without a central portal | Every OSP runs its own installation; the CSP provides the trust list, the company identifier (BPN) with the home OSP, the directory BPN → DID and discovery. |
| Sign-in without passwords | The Portal IAM of an OSP has exactly one identity provider, the EBW-Connector, which checks the EUDI Wallet and the Business Wallet. |
| Testable in isolation | Every module has a built-in stand-in for its neighbours, so it can be developed and tested alone. |

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: https://github.com/eclipse-tractusx/dataspace-mgm-service/blob/main/docs/architecture/04_solution_strategy.md
