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
"""Value sets of C1-M3 (openapi.yaml, README 4, 6.2, 6.6) and the spec id."""
from __future__ import annotations

from typing import Literal

MODULE = "c1-m3"

Status = Literal["OPEN", "AWAITING_SECOND_APPROVAL", "APPROVED", "DECLINED", "CLOSED"]
Kind = Literal["ONBOARDING", "REACTIVATION", "TRANSFER"]
Verification = Literal["EBW", "DOCUMENTS"]
CheckKey = Literal["ATTESTATION_VALID", "REPRESENTATION_CONFIRMED", "COMPANY_DATA_MATCH", "NO_DUPLICATE",
                   "CSP_MATCH_EXPECTED", "CONSENTS_COMPLETE"]
CheckResult = Literal["PASSED", "FAILED", "NOT_APPLICABLE", "ERROR"]
FourEyesCase = Literal["CHECK_FAILED", "DOCUMENTS", "ALWAYS"]
CspOutcome = Literal["NO_MATCH", "EXPECTED_MATCH", "REGISTERED_HERE", "REGISTERED_AT_OTHER_OSP", "MULTIPLE_MATCHES",
                     "NAME_MATCH_ONLY", "BPN_MISMATCH"]
ClosureReason = Literal["WITHDRAWN"]

CHECK_ORDER: list[str] = list(CheckKey.__args__)
"""The checks in the order of README 6.2; responses list them in this order."""
FOUR_EYES = set(FourEyesCase.__args__)
AUTO_KINDS = {"ONBOARDING", "TRANSFER"}   # REACTIVATION is never approved automatically (6.6)
IN_REVIEW = ("OPEN", "AWAITING_SECOND_APPROVAL")
