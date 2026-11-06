# Copyright (c) 2026 Contributors to the Eclipse Foundation
# SPDX-License-Identifier: Apache-2.0
"""Event inbox of the installation: `POST /api/v1/events/inbox` (FRAMEWORK 6, proposal OP-54).

A split-out module (or a broker in front of it) delivers its events over HTTP with the CloudEvents
HTTP protocol binding:

- structured content mode: `Content-Type: application/cloudevents+json`, the whole CloudEvent as body;
- binary content mode: the attributes in `ce-` headers (`ce-specversion`, `ce-id`, `ce-source`,
  `ce-type`, `ce-time`), `data` as the body with `Content-Type: application/json`.

The token is that of the service account of the publishing module (`svc-<module>`, FRAMEWORK 4.2),
and `source` must be `urn:<module>` of that account: a module only publishes its own events. 202: the
event goes to the event bus unchanged (same `id` and `time`) and is delivered like an event published
in the process; the same `source` and `id` a second time is answered with 202 and delivered once.
Errors as Problem Details `urn:events:problem:<name>`: `validation` 400, `unauthorized` 401,
`forbidden` 403, `unsupported-media-type` 415 (any other content type, also batched content mode).
"""
from __future__ import annotations

import json
import logging
from urllib.parse import unquote

from fastapi import APIRouter, Header, Request, Response

from portal_common import events, problems, tokens
from portal_common.problems import Problem

AREA = "events"                       # Problem Details `urn:events:problem:<name>`
TAG = "Event Inbox"
STRUCTURED = "application/cloudevents+json"
BATCHED = "application/cloudevents-batch+json"
BINARY = events.DATACONTENTTYPE       # binary content mode: `data` as application/json
SERVICE_ACCOUNT_PREFIX = "svc-"
log = logging.getLogger("portal.events.inbox")

router = APIRouter(prefix="/events", tags=[TAG], route_class=problems.route_class(AREA))

_CLOUDEVENT_SCHEMA = {
    "type": "object",
    "required": list(events.ATTRIBUTES),
    "additionalProperties": False,
    "properties": {
        "specversion": {"const": events.SPECVERSION},
        "id": {"type": "string", "format": "uuid"},
        "source": {"type": "string", "pattern": r"^urn:c[0-9]+-m[0-9]+$", "examples": ["urn:c1-m2"]},
        "type": {"type": "string", "pattern": "^[A-Z][A-Za-z0-9]*$", "examples": ["ApplicationSubmitted"]},
        "time": {"type": "string", "format": "date-time"},
        "datacontenttype": {"const": events.DATACONTENTTYPE},
        "data": {"type": "object", "description": "content of the event (FRAMEWORK 6, README section 10)"},
    },
}
_PROBLEM = {"application/problem+json": {"schema": {"type": "object"}}}
_OPENAPI = {
    "requestBody": {
        "required": True,
        "content": {
            STRUCTURED: {"schema": _CLOUDEVENT_SCHEMA, "example": {
                "specversion": "1.0", "id": "b8e1f7a0-1c2d-4e3f-9a8b-7c6d5e4f3a2b", "source": "urn:c1-m2",
                "type": "ApplicationSubmitted", "time": "2026-11-06T09:30:00Z", "datacontenttype": "application/json",
                "data": {"applicationId": "0f8e2d4c-6b1a-4c3e-8f7d-2a9b1c0d3e4f",
                         "companyId": "c0000001-0000-4000-8000-000000000001", "kind": "ONBOARDING",
                         "existingCompany": False, "applicantSub": "5a1c0001-0000-4000-8000-000000000001"}}},
            BINARY: {"schema": {"type": "object", "description": "`data` of the event (binary content mode; the "
                                                                 "attributes are in the `ce-` headers)"}},
        },
    },
}
_RESPONSES = {
    202: {"description": "Accepted: the event is on the event bus (or was already received with this `source` and `id`)"},
    400: {"description": "validation: an attribute is missing or wrong (FRAMEWORK 6)", "content": _PROBLEM},
    401: {"description": "unauthorized: token missing or invalid", "content": _PROBLEM},
    403: {"description": "forbidden: not the service account of the module named in `source`", "content": _PROBLEM},
    415: {"description": "unsupported-media-type: neither structured nor binary content mode", "content": _PROBLEM},
}


def _media_type(request: Request) -> str:
    return request.headers.get("content-type", "").split(";", 1)[0].strip().lower()


def _publisher(authorization: str | None) -> str:
    """Module of the service account that calls (`svc-<module>`, `azp` of the token)."""
    claims = tokens.claims_from(authorization, AREA)
    client = claims.get("azp") or claims.get("client_id") or ""
    if not client.startswith(SERVICE_ACCOUNT_PREFIX):
        raise Problem(AREA, 403, "forbidden", detail="only the service account of a module (svc-<module>) delivers events")
    return client.removeprefix(SERVICE_ACCOUNT_PREFIX)


def _from_binary(request: Request, data: object) -> dict:
    """Binary content mode: every `ce-<attribute>` header is an attribute (percent-encoded value)."""
    event: dict = {name[3:]: unquote(value) for name, value in request.headers.items() if name.startswith("ce-")}
    if "datacontenttype" in event:
        raise ValueError("binary content mode: datacontenttype comes from Content-Type, not from a ce- header")
    return event | {"datacontenttype": BINARY, "data": data}


@router.post("/inbox", status_code=202, summary="Receive an event of a split-out module (CloudEvent)",
             openapi_extra=_OPENAPI, responses=_RESPONSES, response_class=Response)
async def receive_event(request: Request, authorization: str | None = Header(default=None)) -> Response:
    module = _publisher(authorization)
    media_type = _media_type(request)
    if media_type not in (STRUCTURED, BINARY):
        hint = " (batched content mode is not supported)" if media_type == BATCHED else ""
        raise Problem(AREA, 415, "unsupported-media-type",
                      detail=f"Content-Type {media_type or 'missing'}: use {STRUCTURED} or {BINARY}{hint}")
    try:
        body = json.loads(await request.body() or b"null")
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise Problem(AREA, 400, "validation", detail=f"body is not JSON: {e}") from None
    try:
        received = body if media_type == STRUCTURED else _from_binary(request, body)
        event = events.validate(received)
    except ValueError as e:
        raise Problem(AREA, 400, "validation", detail=str(e)) from None
    if event["source"] != events.source_of(module):
        raise Problem(AREA, 403, "forbidden",
                      detail=f"svc-{module} only delivers events with source {events.source_of(module)}")
    _, new = events.receive(event)
    log.info("event inbox: %s %s from %s%s", event["type"], event["id"], event["source"], "" if new else " (again)")
    return Response(status_code=202)
