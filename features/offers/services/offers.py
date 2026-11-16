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
"""Stand-in of C8-M1 Offers, hackathon core path: a provider creates an offer (company role checked
at C3-M1), sets roles and the technical user profile, submits; OSP staff approve (`OfferApproved`);
`get_offer_internal` serves the lookup `offer` of Process Orchestration and Subscriptions.
"""
from __future__ import annotations

import uuid

from features.offers.managers import neighbour_client, offer_repository
from features.offers.models import MODULE, ROLE_FOR, problem
from portal_common import events


def reset() -> None:
    offer_repository.reset()


def provider_of(offer_id: str) -> str | None:
    """The provider company of an offer, for the scope `company` of the controllers; None if unknown."""
    offer = offer_repository.get(offer_id)
    return offer and offer["providerCompanyId"]


def _offer(offer_id: str) -> dict:
    offer = offer_repository.get(offer_id)
    if not offer:
        raise problem(404, "not-found")
    return offer


def create_offer(*, company_id: str | None, body: dict) -> dict:
    kind = body.get("offerType")
    if kind not in ROLE_FOR or not body.get("name"):
        raise problem(400, "validation", detail="offerType APP or SERVICE and name")
    company = neighbour_client.query_company(company_id) if company_id else None
    if not company or ROLE_FOR[kind] not in company.get("companyRoles", []):
        raise problem(403, "company-role-missing", detail=f"company role {ROLE_FOR[kind]} missing")
    return offer_repository.add({
        "offerId": str(uuid.uuid4()), "status": "DRAFT", "offerType": kind, "name": body["name"],
        "providerCompanyId": company_id, "instanceKind": body.get("instanceKind", "MULTI") if kind == "APP" else None,
        "instanceUrl": body.get("instanceUrl"), "roles": [], "technicalUserProfile": None, "agreements": []})


def get_offer(offer_id: str) -> dict:
    return _offer(offer_id)


def replace_planned_roles(offer_id: str, roles: list) -> list:
    offer = _offer(offer_id)
    offer["roles"] = [{"name": r["name"], "descriptions": r.get("descriptions", [])} for r in roles]
    return offer["roles"]


def put_technical_user_profile(offer_id: str, body: dict) -> dict:
    offer = _offer(offer_id)
    if not body.get("name") or not body.get("roles"):
        raise problem(400, "validation")
    offer["technicalUserProfile"] = {"name": body["name"], "roles": [{"name": r["name"]} for r in body["roles"]]}
    return offer["technicalUserProfile"]


def submit_offer(offer_id: str) -> dict:
    offer = _offer(offer_id)
    if offer["status"] != "DRAFT":
        raise problem(409, "invalid-state")
    if offer["offerType"] == "APP" and not offer["roles"]:
        raise problem(409, "incomplete", detail="an app needs roles")
    offer["status"] = "IN_REVIEW"
    return offer


def approve_offer(offer_id: str) -> dict:
    offer = _offer(offer_id)
    if offer["status"] != "IN_REVIEW":
        raise problem(409, "invalid-state")
    offer["status"] = "ACTIVE"
    events.publish(MODULE, "OfferApproved", {"offerId": offer_id, "offerType": offer["offerType"],
                                             "providerCompanyId": offer["providerCompanyId"]})
    return offer


def get_offer_internal(offer_id: str) -> dict:
    """README 9: the offer with `hasTechnicalUserProfile`."""
    offer = _offer(offer_id)
    return offer | {"hasTechnicalUserProfile": offer["technicalUserProfile"] is not None}
