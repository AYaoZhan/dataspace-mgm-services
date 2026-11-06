# Copyright (c) 2026 Contributors to the Eclipse Foundation
# SPDX-License-Identifier: Apache-2.0
"""HTTP controllers of the installation that belong to no module (base skeleton, FRAMEWORK 1).

Layout as in the Industry Core Hub backend: one folder per API category under `routers/`, one
folder per version, one file per controller with its own `router`:

    controllers/fastapi/routers/<category>/v1/<name>_api.py   router = APIRouter(prefix="/<category>")

`include(app)` mounts every controller under `/api/v1`, e.g. `POST /api/v1/events/inbox`. The APIs of
the modules stay in `modules/<id>/router.py` under `/api/<module>` (FRAMEWORK 4.1); a new category
gets its own folder here and one line in `v1_router()`.
"""
from __future__ import annotations

from fastapi import APIRouter, FastAPI

from .routers.events.v1 import inbox_api

API_V1 = "/api/v1"

TAGS = [
    {"name": inbox_api.TAG,
     "description": "Event inbox of the installation: receives the CloudEvents of split-out modules over HTTP "
                    "(FRAMEWORK 6, proposal OP-54)"},
]


def v1_router() -> APIRouter:
    router = APIRouter(prefix=API_V1)
    router.include_router(inbox_api.router)
    return router


def include(app: FastAPI) -> None:
    """Mounts the controllers and adds their tags to the OpenAPI document of the installation."""
    app.include_router(v1_router())
    known = {t["name"] for t in app.openapi_tags or []}
    app.openapi_tags = [*(app.openapi_tags or []), *(t for t in TAGS if t["name"] not in known)]
