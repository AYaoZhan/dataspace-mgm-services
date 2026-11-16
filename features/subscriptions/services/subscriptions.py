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
"""Subscriptions of the app path of FRAMEWORK 5.8: subscribe, start setup, activate (only when the setup process at
C12-M1 is not `RUNNING` or `FAILED`, 6.3). A subscription is visible to its customer and to the provider of the
offer; another company gets 404."""
from __future__ import annotations

import uuid

from features.subscriptions.managers import neighbour_client, store
from features.subscriptions.models.subscription import EVENT_FIELDS, MODULE
from portal_common import events
from portal_common.problems import Problem


def _visible(claims: dict, sid: str, provider_only: bool = False) -> dict:
    s = store.subscriptions.get(sid)
    cid = claims.get("company_id")
    if not s or cid not in (s["providerCompanyId"], s["customerCompanyId"]):
        raise Problem(MODULE, 404, "not-found")
    if provider_only and cid != s["providerCompanyId"]:
        raise Problem(MODULE, 403, "forbidden")
    return s


def _event_fields(s: dict) -> dict:
    """Content of the subscription events (C10-M1 section 10)."""
    return {k: s[k] for k in EVENT_FIELDS}


def _setup_status(sid: str) -> str | None:
    procs = neighbour_client.find_processes_of_subscription(sid)
    setup = next((p for p in procs if p["flowKey"] == "subscription-setup"), None)
    return setup["status"] if setup else None


def subscribe(claims: dict, body: dict) -> dict:
    cid = claims.get("company_id")
    offer = neighbour_client.get_offer_internal(body.get("offerId"))
    if not offer or offer["status"] != "ACTIVE":
        raise Problem(MODULE, 409, "offer-not-active")
    if offer["providerCompanyId"] == cid:
        raise Problem(MODULE, 409, "own-offer")
    s = {"offerSubscriptionId": str(uuid.uuid4()), "offerId": offer["offerId"], "offerType": offer["offerType"],
         "instanceKind": offer.get("instanceKind"), "customerCompanyId": cid,
         "providerCompanyId": offer["providerCompanyId"], "status": "REQUESTED", "instanceUrl": None}
    store.subscriptions[s["offerSubscriptionId"]] = s
    events.publish(MODULE, "SubscriptionRequested", _event_fields(s))
    return s


def get_subscription(claims: dict, sid: str) -> dict:
    s = _visible(claims, sid)
    return s | {"setupStatus": _setup_status(s["offerSubscriptionId"])}


def start_setup(claims: dict, sid: str, body: dict) -> dict:
    s = _visible(claims, sid, provider_only=True)
    if s["status"] != "REQUESTED":
        raise Problem(MODULE, 409, "invalid-state")
    s["status"], s["instanceUrl"] = "PENDING", body.get("instanceUrl")
    events.publish(MODULE, "SubscriptionSetupStarted", {**_event_fields(s), "instanceUrl": s["instanceUrl"]})
    return s


def activate(claims: dict, sid: str) -> dict:
    s = _visible(claims, sid, provider_only=True)
    if s["status"] != "PENDING":
        raise Problem(MODULE, 409, "invalid-state")
    status = _setup_status(sid)
    if status == "RUNNING":
        raise Problem(MODULE, 409, "setup-not-finished")
    if status == "FAILED":
        raise Problem(MODULE, 409, "setup-failed")
    s["status"] = "ACTIVE"
    events.publish(MODULE, "SubscriptionActivated", {**_event_fields(s), "instanceKind": s["instanceKind"]})
    return s
