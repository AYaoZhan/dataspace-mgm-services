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
"""Company-scoped technical-user operations."""

from typing import Annotated

from fastapi import APIRouter, Body, Query
from fastapi import Path as PathParam
from fastapi.responses import JSONResponse, Response

from portal_common.problems import route_class

from features.technical_users import interface
from features.technical_users.controllers.dependencies import company_scoped, perm
from features.technical_users.managers.config import MODULE
from features.technical_users.models import Origin, Status, WalletAccess

router = APIRouter(route_class=route_class(MODULE))
LANG = Query("de", pattern="^[a-z]{2}$")
COMPANY_PATH = "/companies/{companyId}/technical-users"
ACCOUNT_PATH = COMPANY_PATH + "/{id}"


@router.get("", summary="List the technical users visible to the company")
def list_technical_users(company_id: Annotated[str, PathParam(alias="companyId")],
                         page: Annotated[int, Query(ge=0)] = 0,
                         size: Annotated[int, Query(ge=1, le=100)] = 20,
                         status: Annotated[list[Status] | None, Query()] = None, origin: Origin | None = None,
                         wallet_access: Annotated[WalletAccess | None, Query(alias="walletAccess")] = None,
                         claims: dict = perm("GET", COMPANY_PATH)):
    company_scoped(claims, company_id)
    return interface.list_technical_users(company_id=company_id, page=page, size=size, status=status,
                                          origin=origin, wallet_access=wallet_access)


@router.post("", status_code=201, summary="Create a technical user")
def create_technical_user(company_id: Annotated[str, PathParam(alias="companyId")],
                          body: Annotated[dict, Body()], claims: dict = perm("POST", COMPANY_PATH)):
    sub = company_scoped(claims, company_id)
    return interface.create_technical_user(company_id=company_id, body=body, actor_sub=sub)


@router.get("/assignable-roles", summary="Roles that the company can assign")
def list_assignable_roles(company_id: Annotated[str, PathParam(alias="companyId")], lang: str = LANG,
                          claims: dict = perm("GET", COMPANY_PATH + "/assignable-roles")):
    company_scoped(claims, company_id)
    return interface.list_assignable_roles(company_id=company_id, lang=lang)


@router.get("/{id}", summary="Details of a technical user")
def get_technical_user(company_id: Annotated[str, PathParam(alias="companyId")],
                       technical_user_id: Annotated[str, PathParam(alias="id")],
                       claims: dict = perm("GET", ACCOUNT_PATH)):
    company_scoped(claims, company_id)
    return interface.get_technical_user(id=technical_user_id, company_id=company_id)


@router.patch("/{id}", summary="Change name, description or roles")
def update_technical_user(company_id: Annotated[str, PathParam(alias="companyId")],
                          technical_user_id: Annotated[str, PathParam(alias="id")],
                          body: Annotated[dict, Body()], claims: dict = perm("PATCH", ACCOUNT_PATH)):
    sub = company_scoped(claims, company_id)
    return interface.update_technical_user(id=technical_user_id, company_id=company_id, body=body, actor_sub=sub)


@router.delete("/{id}", status_code=204, summary="Delete a technical user")
def delete_technical_user(company_id: Annotated[str, PathParam(alias="companyId")],
                          technical_user_id: Annotated[str, PathParam(alias="id")],
                          claims: dict = perm("DELETE", ACCOUNT_PATH)):
    sub = company_scoped(claims, company_id)
    status_code, account = interface.delete_technical_user(id=technical_user_id, company_id=company_id,
                                                           actor_sub=sub)
    if status_code == 202:
        return JSONResponse(account, status_code=202)
    return Response(status_code=204)


@router.post("/{id}/credentials/rotate", summary="Create a new secret")
def rotate_credentials(company_id: Annotated[str, PathParam(alias="companyId")],
                       technical_user_id: Annotated[str, PathParam(alias="id")],
                       claims: dict = perm("POST", ACCOUNT_PATH + "/credentials/rotate")):
    sub = company_scoped(claims, company_id)
    return interface.rotate_credentials(id=technical_user_id, company_id=company_id, actor_sub=sub)