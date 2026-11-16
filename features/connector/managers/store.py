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
"""The register of the connectors (README 5) and the audit log (FRAMEWORK 4.3), in memory (OPEN-QUESTIONS.md 1),
with the data of the built-in stand-ins of C3-M1 and C10-M1 (README 11, `data/`)."""
from __future__ import annotations

import datetime as dt
import json
import threading
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"

# One lock for every change of the register: the uniqueness checks of README 5 and the change that
# follows them run as one unit, so that of two concurrent requests the second sees the first (409).
LOCK = threading.RLock()

connectors: dict[str, dict] = {}     # connectorId -> row of table `connector` (README 5)
audit: list[dict] = []               # table `audit_entry` (FRAMEWORK 4.3)
stub_companies: dict[str, str] = {}          # built-in stand-in of C3-M1: companyId -> status (README 11)
stub_subscriptions: dict[str, dict] = {}     # built-in stand-in of C10-M1: offerSubscriptionId -> subscription
ended_subscriptions: set[str] = set()        # subscriptions that step 8.1 has run for; no new connector after it
deleted_technical_users: set[str] = set()    # accounts that step 8.2 has run for (deleted in C2-M3); never linked again


def _load(name: str) -> dict:
    path = DATA / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def reset() -> None:
    with LOCK:
        connectors.clear()
        audit.clear()
        ended_subscriptions.clear()
        deleted_technical_users.clear()
        stub_companies.clear()
        stub_companies.update(_load("stub-companies.json").get("companies", {}))
        stub_subscriptions.clear()
        stub_subscriptions.update({s["offerSubscriptionId"]: s
                                   for s in _load("stub-subscriptions.json").get("subscriptions", [])})


def now() -> str:
    return dt.datetime.now(dt.UTC).isoformat().replace("+00:00", "Z")


def write_audit(operation: str, object_id: str, sub: str | None = None, company_id: str | None = None) -> None:
    """FRAMEWORK 4.3: time, acting person, company, operation, object. No secrets, no names."""
    audit.append({"at": now(), "sub": sub, "companyId": company_id, "operation": operation, "objectId": object_id})


reset()
