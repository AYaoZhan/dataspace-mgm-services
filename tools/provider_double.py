#################################################################################
#  Copyright (c) 2026 Contributors to the Eclipse Foundation
#
#  See the NOTICE file(s) distributed with this work for additional
#  information regarding copyright ownership.
#
#  This program and the accompanying materials are made available under the
#  terms of the Apache License, Version 2.0 which is available at
#  https://www.apache.org/licenses/LICENSE-2.0.
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#
#  AI Disclosure: This file was entirely AI-generated.
#  The AI-generated portions are made available under CC0-1.0 and not subject
#  to the project's license. The human contributor has reviewed and verified
#  that the code is correct.
#
#  SPDX-License-Identifier: Apache-2.0 AND CC0-1.0
#  Assisted-By: Claude Code (claude-opus-5-5)
#################################################################################
"""Test double of a provider system (C10-M1 11.2): `tokenUrl`, `setupUrl`, `callbackUrl`.

Mounted with prefix `/test-tools/provider`. Answers every call with 200 and records it;
`GET /test-tools/provider/calls` lists the calls (secrets masked).
"""
from __future__ import annotations

import secrets

from fastapi import APIRouter, Body, Form, Header, HTTPException

CLIENT_ID, CLIENT_SECRET = "portal", "test-only-provider-secret"
calls: list[dict] = []
_tokens: set[str] = set()

router = APIRouter(prefix="/test-tools/provider", tags=["Provider system test double (C10-M1 11.2)"])


def reset() -> None:
    calls.clear()
    _tokens.clear()


def _mask(o):
    if isinstance(o, dict):
        return {k: ("***" if "secret" in k.lower() else _mask(v)) for k, v in o.items()}
    return [_mask(x) for x in o] if isinstance(o, list) else o


def _check(authorization: str | None) -> None:
    if not authorization or authorization.removeprefix("Bearer ") not in _tokens:
        raise HTTPException(401, "unauthorized")


@router.post("/token")
def token(grant_type: str = Form(...), client_id: str = Form(...), client_secret: str = Form(...)):
    if grant_type != "client_credentials" or (client_id, client_secret) != (CLIENT_ID, CLIENT_SECRET):
        raise HTTPException(401, "invalid_client")
    t = secrets.token_urlsafe(16)
    _tokens.add(t)
    return {"access_token": t, "token_type": "Bearer", "expires_in": 300}


@router.post("/setup")
def setup(body: dict = Body(...), authorization: str | None = Header(None)):
    _check(authorization)
    calls.append({"kind": "setup", "body": body})
    return {"received": True}


@router.post("/callback")
def callback(body: dict = Body(...), authorization: str | None = Header(None)):
    _check(authorization)
    calls.append({"kind": "callback", "body": body,
                  "hasSecret": bool((body.get("technicalUser") or {}).get("clientSecret"))})
    return {"received": True}


@router.get("/calls")
def list_calls():
    return [_mask(c) for c in calls]
