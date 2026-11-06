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
"""Trust list of the core services (C5-M1 11.3)."""

import json
import time
from pathlib import Path

import httpx

from common.jose import keys_from_jwks, verify_jws
from connector import config
from connector.errors import VerificationError

_cache: dict = {"until": 0.0, "entries": []}


def _load() -> list[dict]:
    if config.TRUST_LIST_FILE:
        return json.loads(Path(config.TRUST_LIST_FILE).read_text()).get("entries", [])
    token = httpx.get(config.TRUST_LIST_URL, timeout=5).raise_for_status().text
    signers = keys_from_jwks(json.loads(config.TRUST_LIST_SIGNER_FILE.read_text()))
    for _, key in signers:
        try:
            header, payload = verify_jws(token, key)
        except ValueError:
            continue
        if header.get("typ") != "trust-list+jwt":
            raise ValueError("typ of the trust list is not trust-list+jwt")
        if payload.get("exp", time.time() + 1) < time.time():
            raise ValueError("trust list expired")
        return payload.get("entries", [])
    raise ValueError("signature of the trust list does not verify")


def entries() -> list[dict]:
    if _cache["until"] < time.time():
        try:
            _cache["entries"] = _load()
            _cache["until"] = time.time() + config.TRUST_LIST_CACHE_SECONDS
        except (httpx.HTTPError, ValueError, OSError) as exc:
            print(f"Trust list not available: {exc}", flush=True)
    return _cache["entries"]


def find_key(credential_type: str, issuer_jwt: str, iss: str | None) -> tuple[dict, object]:
    """Trust list entry and key that verify the credential; raises VerificationError."""
    issuer_listed = False
    for entry in entries():
        if credential_type not in entry.get("credential_types", []):
            continue
        if entry.get("iss"):
            if entry["iss"] != iss:
                continue
            issuer_listed = True
        for _, key in keys_from_jwks(entry.get("jwks", {})):
            try:
                verify_jws(issuer_jwt, key)
                return entry, key
            except ValueError:
                continue
    if issuer_listed:
        raise VerificationError("INVALID_SIGNATURE", f"signature of {iss} does not verify")
    raise VerificationError("UNTRUSTED_ISSUER", f"{credential_type} issuer {iss} is not in the trust list")
