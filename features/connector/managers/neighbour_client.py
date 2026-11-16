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
"""Neighbouring modules of C6-M1 (README 11) with their built-in stand-ins (empty address, `data/`)."""
from __future__ import annotations

from portal_common import neighbours

from ..models import ACTIVE, MODULE
from . import store


def company_status(company_id: str) -> str | None:
    """C3-M1 `query_company`: status of the company; None if C3-M1 does not know it."""
    if neighbours.is_standin("c3-m1"):
        return store.stub_companies.get(company_id, ACTIVE)
    company = neighbours.query(MODULE, "c3-m1", "query_company", companyId=company_id)
    return (company or {}).get("status")


def technical_user_usable(technical_user_id: str, host_company_id: str, offer_subscription_id: str | None) -> bool:
    """C2-M3 `check_technical_user` (C2-M3 9.1): `usableForConnector`."""
    if neighbours.is_standin("c2-m3"):
        return True
    params = {"id": technical_user_id, "companyId": host_company_id}
    if offer_subscription_id:
        params["offerSubscriptionId"] = offer_subscription_id
    answer = neighbours.query(MODULE, "c2-m3", "check_technical_user", **params)
    return bool(answer and answer.get("usableForConnector"))


def subscription(offer_subscription_id: str) -> dict | None:
    """C10-M1 `get_subscription_internal`: `status`, `providerCompanyId`, `customerCompanyId`."""
    if neighbours.is_standin("c10-m1"):
        return store.stub_subscriptions.get(offer_subscription_id)
    return neighbours.query(MODULE, "c10-m1", "get_subscription_internal", offerSubscriptionId=offer_subscription_id)
