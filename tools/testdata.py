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
"""Shared test data package (`testdata/`): one catalogue of terms, the OSP company, test persons."""
from __future__ import annotations

import functools
import json

from portal_common import settings
from portal_common.spec import ROOT

DIR = ROOT / "testdata"


@functools.lru_cache(maxsize=None)
def agreements() -> list[dict]:
    """Terms with `agreementId` (C3-M1) and `agreementKey` + `version` (C1-M2), one entry per version."""
    return json.loads((DIR / "agreements.json").read_text(encoding="utf-8"))["agreements"]


def agreements_for_roles(roles: list[str]) -> list[dict]:
    """Terms assigned to one of the company roles (scope `COMPANY_ROLE`)."""
    return [a for a in agreements() if set(a["companyRoles"]) & set(roles)]


def required_agreements(roles: list[str]) -> list[dict]:
    """Required terms of an application (C1-M2 6.8): scope `ALL` plus the terms of the roles."""
    return [a for a in agreements() if a["scope"] == "ALL" or set(a["companyRoles"]) & set(roles)]


def agreement_id(key: str, version: str) -> str | None:
    return next((a["agreementId"] for a in agreements() if a["agreementKey"] == key and a["version"] == version), None)


def osp_company() -> dict | None:
    """Seed data of the OSP company of this installation (`ospCompanyFile` in the settings)."""
    path = settings.resolve_path(settings.get("ospCompanyFile"))
    return json.loads(path.read_text(encoding="utf-8")) if path and path.exists() else None


@functools.lru_cache(maxsize=None)
def applicant_companies() -> dict[str, dict]:
    """Companies that apply, with the test IDs of FRAMEWORK 7a where it defines them."""
    return json.loads((DIR / "applicant-companies.json").read_text(encoding="utf-8"))["companies"]


def test_company_id(ebwoid: str | None) -> str | None:
    """`companyId` of FRAMEWORK 7a for a company with this EBWOID, if 7a defines one."""
    return next((c.get("companyId") for c in applicant_companies().values() if ebwoid and c.get("ebwoid") == ebwoid),
                None)
