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
#  The program is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#  CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.
#
#  AI Disclosure: This file was entirely AI-generated.
#  The AI-generated portions are made available under CC0-1.0 and not subject
#  to the project's license. The human contributor has reviewed and verified
#  that the code is correct.
#
#  SPDX-License-Identifier: Apache-2.0 AND CC0-1.0
#  Assisted-By: GitHub Copilot (Claude Sonnet 5.5)
#################################################################################
"""Internal technical-user queries and subscription credential rotation."""

from typing import Annotated

from fastapi import APIRouter, Body
from fastapi import Path as PathParam
from fastapi import Query

from portal_common.problems import route_class

from features.technical_users import interface
from features.technical_users.controllers.dependencies import perm
from features.technical_users.managers.config import MODULE
from features.technical_users.models.schemas import SubscriptionCredentialsRequest
from features.technical_users.services import validation

router = APIRouter(route_class=route_class(MODULE))


@router.get("/{id}", summary="Can the account be used for a connector?")
def check_technical_user(technical_user_id: Annotated[str, PathParam(alias="id")],
                         company_id: Annotated[str, Query(alias="companyId")],
                         offer_subscription_id: Annotated[str | None, Query(alias="offerSubscriptionId")] = None,
                         _: dict = perm("GET", "/internal/technical-users/{id}")):
    return interface.check_technical_user(id=technical_user_id, companyId=company_id,
                                          offerSubscriptionId=offer_subscription_id)


@router.post("/{id}/credentials/rotate", summary="Rotate a subscription account's secret")
def rotate_subscription_credentials(technical_user_id: Annotated[str, PathParam(alias="id")],
                                    body: Annotated[dict, Body()],
                                    _: dict = perm("POST", "/internal/technical-users/{id}/credentials/rotate")):
    request = validation.parse(SubscriptionCredentialsRequest, body)
    return interface.rotate_subscription_credentials(id=technical_user_id,
                                                     offerSubscriptionId=request.offerSubscriptionId)