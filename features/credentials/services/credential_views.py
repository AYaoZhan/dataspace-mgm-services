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
"""Read views of the credentials (README 7.1, 7.2, 9.1): rows of the store as the API shows them."""
from __future__ import annotations

import datetime as dt

from features.credentials.managers import config
from features.credentials.managers.credential_store import store
from features.credentials.models.values import TYPES


def _iso(value: dt.datetime | None) -> str | None:
    return value.isoformat() if value else None


def _status_view(row: dict) -> dict:
    return {"credentialType": row["credential_type"], "status": row["status"], "requestedAt": _iso(row.get("requested_at")),
            "issuedAt": _iso(row.get("issued_at")), "revokedAt": _iso(row.get("revoked_at"))}


def _rows_of(cid: str) -> list[dict]:
    rows = store().list_credentials(company_id=cid, size=1000)
    return sorted(rows, key=lambda r: TYPES.index(r["credential_type"]) if r["credential_type"] in TYPES else len(TYPES))


def query_company_credentials(*, companyId: str) -> dict:
    """README 9.1: status per credential type and the last round; an unknown company gives an empty list."""
    run = store().get_run(companyId)
    return {"companyId": companyId, "credentials": [_status_view(r) for r in _rows_of(companyId)],
            "run": None if run is None else {
                "status": run["status"], "credentialTypes": list(run["credential_types"]),
                "startedAt": _iso(run["started_at"]), "finishedAt": _iso(run.get("finished_at"))}}


def list_company_credentials(company_id: str) -> list[dict]:
    """README 7.1: no messages of the issuer, no routes; onboarding types without a row show `NONE`."""
    views = {r["credential_type"]: _status_view(r) for r in _rows_of(company_id)}
    for t in config.onboarding_types():
        views.setdefault(t, {"credentialType": t, "status": "NONE", "requestedAt": None, "issuedAt": None,
                             "revokedAt": None})
    return [views[t] for t in sorted(views, key=lambda t: TYPES.index(t) if t in TYPES else len(TYPES))]


def detail_view(row: dict) -> dict:
    """OSP view (README 7.2): every field except secrets (`CredentialDetail`)."""
    return {"id": row["id"], "companyId": row["company_id"], "credentialType": row["credential_type"],
            "status": row["status"], "route": row["route"], "issuerDid": row.get("issuer_did") or None,
            "walletProvider": row.get("wallet_provider"), "bpn": row.get("bpn"), "holderDid": row.get("holder_did"),
            "requestRef": row.get("request_ref") or None, "attempt": row["attempt"],
            "requestedAt": _iso(row.get("requested_at")), "issuedAt": _iso(row.get("issued_at")),
            "failedAt": _iso(row.get("failed_at")), "revokedAt": _iso(row.get("revoked_at")),
            "failureReason": row.get("failure_reason"), "revocationReason": row.get("revocation_reason"),
            "createdAt": _iso(row["created_at"]), "changedAt": _iso(row["changed_at"])}


def list_credentials(statuses=None, credential_type=None, company_id=None, route=None, requested_before=None,
                     page: int = 0, size: int = 20) -> dict:
    """README 7.2: filters, sorted by `changedAt` descending, paged."""
    if requested_before is not None and requested_before.tzinfo is None:
        requested_before = requested_before.replace(tzinfo=dt.UTC)
    filters = dict(company_id=company_id, statuses=statuses, credential_type=credential_type, route=route,
                   requested_before=requested_before)
    rows = store().list_credentials(page=page, size=size, **filters)
    return {"items": [detail_view(r) for r in rows], "page": page, "size": size,
            "total": store().count_credentials(**filters)}
