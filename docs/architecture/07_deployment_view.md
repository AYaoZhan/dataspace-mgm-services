# 7. Deployment view

```mermaid
flowchart TB
    subgraph k8s["Kubernetes namespace of the OSP"]
        ing["Ingress"]
        subgraph chart["Helm release of charts/dataspace-mgm"]
            fe["Deployment frontend<br/>tractusx/dataspace-mgm-ui<br/>nginx-unprivileged, port 8080"]
            be["Deployment backend<br/>tractusx/dataspace-mgm-service<br/>uvicorn, port 8000"]
            cm["ConfigMaps<br/>config.json, installation.json"]
            sec["Secrets<br/>service client secret, signing key"]
        end
    end
    kc["Portal IAM (Keycloak)"]
    cspc["Core services of the CSP"]
    ing --> fe
    ing --> be
    cm --> fe
    cm --> be
    sec --> be
    be --> kc
    be --> cspc
```

| Element | Description |
|---|---|
| Product Helm chart | [`charts/dataspace-mgm`](../../charts/dataspace-mgm) installs backend and UI of one installation (TRG 5.08). |
| Backend container | `tractusx/dataspace-mgm-service`, built from the [Dockerfile](../../Dockerfile) on `python:3.12-alpine`, runs as user 10001 with a read-only root file system. |
| UI container | `tractusx/dataspace-mgm-ui`, static files on `nginxinc/nginx-unprivileged`, runtime configuration in `/config.json`. |
| Portal IAM | Keycloak with the realm of C2-M5; not part of the chart yet. |
| Databases | Not needed yet (data in memory); one PostgreSQL database per module will be added. |

Installation and configuration are described in [INSTALL.md](../../INSTALL.md) and the [admin guide](../admin/README.md).

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: https://github.com/eclipse-tractusx/dataspace-mgm-service/blob/main/docs/architecture/07_deployment_view.md
