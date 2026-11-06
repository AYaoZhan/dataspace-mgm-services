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
"""Stand-in of C2-M3 Technical Users: `create-for-subscription` (technical user in the test IAM,
roles checked against C2-M5 6.4), the query of a technical user and the rotation of its secret
for Subscriptions. Secrets only in the answer of the rotation, never in step results or events.
"""
from __future__ import annotations

from fastapi import Body

from portal_common import standin

from . import interface
from .interface import MODULE

STANDIN = True
router = standin.router(MODULE)


def reset() -> None:
    interface.reset()


@router.post("/steps/create-for-subscription")
def create_for_subscription(body: dict = Body(...),
                            _: dict = standin.perm(MODULE, "POST", "/steps/create-for-subscription")):
    return interface.create_for_subscription(body)


@router.get("/internal/technical-users/{id}")
def get_technical_user(id: str, companyId: str | None = None, offerSubscriptionId: str | None = None,
                       _: dict = standin.perm(MODULE, "GET", "/internal/technical-users/{id}")):
    return interface.check_technical_user(id=id, companyId=companyId, offerSubscriptionId=offerSubscriptionId)


@router.post("/internal/technical-users/{id}/credentials/rotate")
def rotate(id: str, body: dict = Body(default={}),
           _: dict = standin.perm(MODULE, "POST", "/internal/technical-users/{id}/credentials/rotate")):
    return interface.rotate_subscription_credentials(id=id, offerSubscriptionId=body.get("offerSubscriptionId"))
