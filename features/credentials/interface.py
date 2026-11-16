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
`issue-credentials` and `revoke-credentials` and the query `query_company_credentials`, plus `report_status` for
issuers in the same process. Input and answer are the JSON of `openapi.yaml` (dicts), as over HTTP; an invalid
input is 400 `validation`. Other modules and Process Orchestration import only from here; the rules are in
`services/`, the storage and the issuer clients in `managers/`.
"""
from __future__ import annotations

from features.credentials.managers.credential_store import store as _store
from features.credentials.models.credentials import IssueCredentials, RevokeCredentials, as_json
from features.credentials.models.problems import MODULE, parse
from features.credentials.services import credential_service, credential_views

__all__ = ["MODULE", "issue_credentials", "query_company_credentials", "report_status", "reset", "revoke_credentials",
           "store"]


def store():
    """The active `CredentialStore`."""
    return _store()


def issue_credentials(input: dict) -> dict:
    """Step `issue-credentials` (README 8.1)."""
    return credential_service.issue_credentials(parse(IssueCredentials, input)).to_json()


def revoke_credentials(input: dict) -> dict:
    """Step `revoke-credentials` (README 8.2)."""
    return credential_service.revoke_credentials(parse(RevokeCredentials, input)).to_json()


def query_company_credentials(*, companyId: str) -> dict:
    """Query `query_company_credentials` (README 9.1)."""
    return as_json(credential_views.query_company_credentials(companyId=companyId))


def report_status(kind: str, bpn: str, status: str, message: str | None = None) -> None:
    """README 7.4 steps 3 and 4: processes the status report of an issuer."""
    credential_service.report_status(kind, bpn, status, message)


def reset() -> None:
    """Empties the tables, cancels pending STUB timers, clears the routes state."""
    credential_service.reset()
