# 11. Risks and technical debt

| Risk or debt | Impact | Mitigation |
|---|---|---|
| Data is kept in memory. | Data is lost on restart; only one replica is possible. | Persistence with one PostgreSQL database per module; the chart will get the database dependencies (TRG 3.02). |
| Several modules are stand-ins that cover only the hackathon paths. | Other operations answer 501. | Replace the stand-ins with implementations following the module specs. |
| The OSP–CSP interface is a proposal of C3-M2. | Changes when the association defines it differently. | Only C3-M2 calls the CSP, so only C3-M2 changes. |
| Specification at version 0.2 with open points (OP-xx). | Interfaces can still change. | Provisional decisions are marked in `open-points.md`; the OpenAPI documents are versioned. |
| Python is not yet an aligned base image in TRG 4.02. | Release check finding. | Official `python` image from DockerHub, used as-is; alignment to be discussed in sig-infra. |

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: https://github.com/eclipse-tractusx/dataspace-mgm-service/blob/main/docs/architecture/11_risks_and_technical_debt.md
