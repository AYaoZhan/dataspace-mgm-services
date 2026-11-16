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
"""The connector of openapi.yaml: spec id, value sets and the view of a row of the register."""
from __future__ import annotations

from typing import Literal

MODULE = "c6-m1"

ACTIVE, INACTIVE = "ACTIVE", "INACTIVE"
COMPANY_CONNECTOR, CONNECTOR_AS_A_SERVICE = "COMPANY_CONNECTOR", "CONNECTOR_AS_A_SERVICE"

Role = Literal["provider", "host"]
Type = Literal["COMPANY_CONNECTOR", "CONNECTOR_AS_A_SERVICE"]
Status = Literal["ACTIVE", "INACTIVE"]


def view(c: dict) -> dict:
    """`Connector` of openapi.yaml."""
    return {"connectorId": c["id"], "name": c["name"], "endpoint": c["endpoint"], "location": c["location"],
            "type": c["type"], "status": c["status"], "providerCompanyId": c["provider_company_id"],
            "hostCompanyId": c["host_company_id"], "technicalUserId": c["technical_user_id"],
            "offerSubscriptionId": c["offer_subscription_id"], "createdAt": c["created_at"],
            "changedAt": c["changed_at"]}
