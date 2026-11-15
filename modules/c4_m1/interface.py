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
#  Assisted-By: Claude Code (claude-sonnet-5-5)
#################################################################################
"""Public interface of C4-M1 Credentials (AGENTS.md call convention): the steps `issue-credentials` and
`revoke-credentials` and the query `query_company_credentials`. The rules are in `service.py`, the routes
to the issuers in `routes.py`, the storage in `store.py`.
"""
from __future__ import annotations

from portal_common import standin

from . import service

MODULE = "c4-m1"


def store():
    """The active `CredentialStore`."""
    return service.store()


def issue_credentials(input: dict) -> dict:
    """Step `issue-credentials` (README 8.1)."""
    return service.issue_credentials(input)


def revoke_credentials(input: dict) -> dict:
    """Step `revoke-credentials` (README 8.2)."""
    return service.revoke_credentials(input)


def query_company_credentials(*, companyId: str) -> dict:
    """Query `query_company_credentials` (README 9.1)."""
    return service.query_company_credentials(companyId=companyId)


def confirm_revocation(credential_id: str, body: object, claims: dict) -> dict:
    return service.confirm_revocation(credential_id, body, claims)


def list_credentials(*args, **kwargs):
    return service.list_credentials(*args, **kwargs)


def report_status(kind: str, bpn: str, status: str, message: str | None = None) -> None:
    return service.report_status(kind, bpn, status, message)


def reset() -> None:
    """Clears the store, cancels pending STUB timers, clears the routes state."""
    service.reset()


__getattr__ = standin.missing_interface(MODULE)   # steps and queries not implemented yet: stand-in
