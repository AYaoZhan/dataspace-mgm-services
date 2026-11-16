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
"""Configuration of the credentials (README 4), read from the environment at call time and never at import
(AGENTS.md rule 6). The defaults are listed in OPEN-QUESTIONS.md (decision 3)."""
from __future__ import annotations

import datetime as dt
import os


def onboarding_types() -> list[str]:
    raw = os.environ.get("ONBOARDING_CREDENTIAL_TYPES") or "BPN,MEMBERSHIP"
    return [t.strip().upper() for t in raw.split(",") if t.strip()]


def resend_after() -> dt.timedelta:
    try:
        return dt.timedelta(hours=float(os.environ.get("RESEND_AFTER_HOURS") or 24))
    except ValueError:
        return dt.timedelta(hours=24)


def issuer_mode() -> str:
    """`ISSUER_MODE`: `OWN` (default) or `CSP`."""
    return os.environ.get("ISSUER_MODE", "OWN")


def csp_issuer_configured() -> bool:
    return bool(os.environ.get("CSP_ISSUER_URL"))


def issuer_routes_configured() -> bool:
    return bool(os.environ.get("ISSUER_ROUTES", "").strip())


def issuer_routes() -> dict[str, str]:
    """`ISSUER_ROUTES`: `SAP_DIV:CREDENTIAL_ISSUER,IDENTITY_HUB:ISSUER_SERVICE,...` as a dict."""
    out = {}
    for part in os.environ.get("ISSUER_ROUTES", "").split(","):
        if ":" in part:
            provider, route = part.split(":", 1)
            out[provider.strip()] = route.strip()
    return out


def stub_issuer_delay() -> float:
    """`STUB_ISSUER_DELAY_SECONDS` (default 1, never negative)."""
    try:
        return max(0.0, float(os.environ.get("STUB_ISSUER_DELAY_SECONDS", "1")))
    except ValueError:
        return 1.0


def stub_issuer_fail_types() -> set[str]:
    """`STUB_ISSUER_FAIL_TYPES`: credential types the stand-in declines."""
    return {t.strip().upper() for t in os.environ.get("STUB_ISSUER_FAIL_TYPES", "").split(",") if t.strip()}
