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
"""In-process contract of the credentials (spec C4-M1, call convention of AGENTS.md): the steps
`issue-credentials` and `revoke-credentials` and the query `query_company_credentials`, plus the operations of
people and issuers, which only the controllers call. Other modules and Process Orchestration import only from
here; the rules are in `services/`, the storage and the issuer clients in `managers/`.
"""
from __future__ import annotations

from features.credentials.managers.credential_store import store as _store
from features.credentials.models.problems import MODULE
from features.credentials.services import credential_service, credential_views

__all__ = [
    "MODULE", "audit", "confirm_revocation", "issue_credentials", "list_company_credentials", "list_credentials",
    "query_company_credentials", "report_status", "reset", "revoke_credentials", "store", "validate_report",
]


def store():
    """The active `CredentialStore`."""
    return _store()


def issue_credentials(input: dict) -> dict:
    """Step `issue-credentials` (README 8.1)."""
    return credential_service.issue_credentials(input)


def revoke_credentials(input: dict) -> dict:
    """Step `revoke-credentials` (README 8.2)."""
    return credential_service.revoke_credentials(input)


def query_company_credentials(*, companyId: str) -> dict:
    """Query `query_company_credentials` (README 9.1)."""
    return credential_views.query_company_credentials(companyId=companyId)


def list_company_credentials(company_id: str) -> list[dict]:
    """README 7.1: the credentials of the own company."""
    return credential_views.list_company_credentials(company_id)


def list_credentials(*args, **kwargs):
    """README 7.2: every credential, for OSP staff."""
    return credential_views.list_credentials(*args, **kwargs)


def confirm_revocation(credential_id: str, body: object, claims: dict) -> dict:
    """README 7.3: OSP staff confirm a revocation done by hand."""
    return credential_service.confirm_revocation(credential_id, body, claims)


def validate_report(kind: str, body: object) -> tuple[str, str, str | None]:
    """README 7.4 step 2: checks the status report of an issuer."""
    return credential_service.validate_report(kind, body)


def report_status(kind: str, bpn: str, status: str, message: str | None = None) -> None:
    """README 7.4 steps 3 and 4: processes the status report of an issuer."""
    return credential_service.report_status(kind, bpn, status, message)


def audit(claims: dict, operation: str, company_id: str | None, object_ref: str, result: int) -> None:
    """Audit log entry of a changing operation over HTTP (README 5 `audit_entry`)."""
    credential_service.audit(claims, operation, company_id, object_ref, result)


def reset() -> None:
    """Clears the store, cancels pending STUB timers, clears the routes state."""
    credential_service.reset()
