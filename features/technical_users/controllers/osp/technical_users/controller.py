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
"""OSP-wide technical-user operations."""

from typing import Annotated

from fastapi import APIRouter, Query
from fastapi import Path as PathParam

from portal_common.problems import route_class

from features.technical_users import interface
from features.technical_users.controllers.dependencies import perm
from features.technical_users.managers.config import MODULE
from features.technical_users.models import Origin, Status, WalletAccess

router = APIRouter(route_class=route_class(MODULE))


@router.get("", summary="List the technical users of all companies")
def list_all_technical_users(page: Annotated[int, Query(ge=0)] = 0,
                             size: Annotated[int, Query(ge=1, le=100)] = 20,
                             company_id: Annotated[str | None, Query(alias="companyId")] = None,
                             status: Annotated[list[Status] | None, Query()] = None, origin: Origin | None = None,
                             wallet_access: Annotated[WalletAccess | None, Query(alias="walletAccess")] = None,
                             disabled: bool | None = None,
                             _: dict = perm("GET", "/osp/technical-users")):
    return interface.list_all_technical_users(page=page, size=size, company_id=company_id, status=status,
                                              origin=origin, wallet_access=wallet_access, disabled=disabled)


@router.get("/{id}", summary="Details of any technical user")
def get_any_technical_user(technical_user_id: Annotated[str, PathParam(alias="id")],
                           _: dict = perm("GET", "/osp/technical-users/{id}")):
    return interface.get_any_technical_user(id=technical_user_id)