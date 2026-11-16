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
"""The connectors of the own company (README 7, scope `company` from the token): the calling company and person
go to the operations of `interface.py`."""
from __future__ import annotations

from fastapi import Body, Response

from features.connector import interface
from features.connector.models import Role, Status, Type
from portal_common.routing import Controller, Page, Permission, Size

controller = Controller("Connector: Connectors")


@controller.get("", summary="Connectors of the own company")
def list_connectors(role: Role | None = None, type: Type | None = None, status: Status | None = None,
                    page: int = Page, size: int = Size, claims: dict = Permission):
    return interface.list_connectors(claims.get("company_id"), role=role, type=type, status=status, page=page,
                                     size=size)


@controller.post("", status_code=201, summary="Register a company connector")
def register_connector(body: dict = Body(...), claims: dict = Permission):
    return interface.register_connector(claims.get("company_id"), claims.get("sub"), body)


@controller.post("/as-a-service", status_code=201, summary="Register a connector as a service for a customer")
def register_connector_as_a_service(body: dict = Body(...), claims: dict = Permission):
    return interface.register_connector_as_a_service(claims.get("company_id"), claims.get("sub"), body)


@controller.get("/{connectorId}", summary="One connector")
def get_connector(connectorId: str, claims: dict = Permission):
    return interface.get_connector(claims.get("company_id"), connectorId)


@controller.patch("/{connectorId}", summary="Change the endpoint")
def change_endpoint(connectorId: str, body: dict = Body(...), claims: dict = Permission):
    return interface.change_endpoint(claims.get("company_id"), claims.get("sub"), connectorId, body)


@controller.delete("/{connectorId}", status_code=204, summary="Delete a connector")
def delete_connector(connectorId: str, claims: dict = Permission):
    interface.delete_connector(claims.get("company_id"), claims.get("sub"), connectorId)
    return Response(status_code=204)
