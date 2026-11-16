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
"""Credentials for OSP staff (README 7.2, 7.3), permission `manage_credentials`."""
from __future__ import annotations

import datetime as dt
import uuid
from typing import Literal

from fastapi import Body, Query

from features.credentials import interface
from portal_common.routing import Controller, Permission

controller = Controller("Credentials: OSP Credentials")


@controller.get("", summary="List the credentials")
def list_credentials(page: int = Query(0, ge=0), size: int = Query(20, ge=1, le=100),
                     status: list[Literal["REQUESTED", "ISSUED", "FAILED", "CANCELLED", "REVOCATION_PENDING",
                                          "REVOKED"]] | None = Query(None),
                     credentialType: Literal["BPN", "MEMBERSHIP"] | None = None,
                     companyId: uuid.UUID | None = None,
                     route: Literal["CREDENTIAL_ISSUER", "ISSUER_SERVICE", "CSP_ISSUER", "STUB"] | None = None,
                     requestedBefore: dt.datetime | None = None,
                     _: dict = Permission):
    """README 7.2 (OSP staff, `manage_credentials`)."""
    return interface.list_credentials(statuses=status, credential_type=credentialType,
                                      company_id=str(companyId) if companyId else None, route=route,
                                      requested_before=requestedBefore, page=page, size=size)


@controller.post("/{credentialId}/confirm-revocation", summary="Confirm a revocation done by hand")
def confirm_revocation(credentialId: str, body: dict = Body(...), claims: dict = Permission):
    """README 7.3 (OSP staff, `manage_credentials`)."""
    return interface.confirm_revocation(credentialId, body, claims)
