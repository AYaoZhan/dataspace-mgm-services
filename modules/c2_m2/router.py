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
"""Stand-in of C2-M2 Users and App Access: `assign-company-admin` (binds the applicant in the test
IAM), client template and instance clients of apps, and the queries on instance clients.
Writes to the in-memory test IAM through its Python API (the Keycloak Admin API is not simulated).
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



@router.post("/steps/assign-company-admin")
def assign_company_admin(body: dict = Body(...), _: dict = standin.perm(MODULE, "POST", "/steps/assign-company-admin")):
    return interface.assign_company_admin(body)


@router.post("/steps/create-client-template")
def create_client_template(body: dict = Body(...), _: dict = standin.perm(MODULE, "POST", "/steps/create-client-template")):
    return interface.create_client_template(body)


@router.post("/steps/create-instance-client")
def create_instance_client(body: dict = Body(...), _: dict = standin.perm(MODULE, "POST", "/steps/create-instance-client")):
    return interface.create_instance_client(body)


@router.post("/steps/enable-instance-client")
def enable_instance_client(body: dict = Body(...), _: dict = standin.perm(MODULE, "POST", "/steps/enable-instance-client")):
    return interface.enable_instance_client(body)


@router.post("/steps/disable-instance-client")
def disable_instance_client(body: dict = Body(...), _: dict = standin.perm(MODULE, "POST", "/steps/disable-instance-client")):
    return interface.disable_instance_client(body)


@router.get("/internal/app-instance-clients")
def list_instance_clients(_: dict = standin.perm(MODULE, "GET", "/internal/app-instance-clients"),
                          appId: str | None = None, offerSubscriptionId: str | None = None):
    return interface.list_app_instance_clients(appId=appId, offerSubscriptionId=offerSubscriptionId)


@router.get("/internal/app-instance-clients/{id}")
def get_instance_client(id: str, _: dict = standin.perm(MODULE, "GET", "/internal/app-instance-clients/{id}")):
    return interface.get_app_instance_client(id=id)
