# Architecture documentation

Architecture documentation of the Eclipse Tractus-X **Dataspace Management** (new portal), following the
[arc42](https://arc42.org/) template (TRG 1.05). The binding source for the behaviour of every module is the
module specification (`README.md`, `openapi.yaml`, `open-points.md` per module) and its framework
(`FRAMEWORK.md`); this documentation summarises the architecture and links to the specification instead of repeating it.

| No. | Chapter | Content |
|---|---|---|
| 1 | [Introduction and goals](01_introduction_and_goals.md) | Purpose, quality goals, stakeholders |
| 2 | [Architecture constraints](02_architecture_constraints.md) | Technical, organisational and legal constraints |
| 3 | [Context and scope](03_context_and_scope.md) | OSP 2.0: the installation of an OSP and its neighbours |
| 4 | [Solution strategy](04_solution_strategy.md) | Modular monolith, flows as data, own data per module |
| 5 | [Building block view](05_building_block_view.md) | Capabilities and modules |
| 6 | [Runtime view](06_runtime_view.md) | Onboarding of a company |
| 7 | [Deployment view](07_deployment_view.md) | Helm chart, containers, configuration |
| 8 | [Crosscutting concepts](08_crosscutting_concepts.md) | Tokens and permissions, events, errors, secrets |
| 9 | [Architecture decisions](09_architecture_decisions.md) | Decision log |
| 10 | [Quality requirements](10_quality_requirements.md) | Quality scenarios |
| 11 | [Risks and technical debt](11_risks_and_technical_debt.md) | Known risks and open points |
| 12 | [Glossary](12_glossary.md) | Terms |

Diagrams are written in [Mermaid](https://mermaid.js.org/) directly in the Markdown files (TRG 1.04), so they can be
edited like text; GitHub renders them, and the [Mermaid Live Editor](https://mermaid.live/) can be used to preview changes.

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: https://github.com/eclipse-tractusx/dataspace-mgm-service/blob/main/docs/architecture/README.md
