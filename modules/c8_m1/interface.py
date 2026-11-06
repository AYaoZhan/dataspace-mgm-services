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
"""Public interface of the C8-M1 stand-in: `getOfferInternal` serves the lookup `offer` of Process
Orchestration and Subscriptions."""
from __future__ import annotations

from portal_common import standin
from portal_common.problems import Problem

MODULE = "c8-m1"
offers: dict[str, dict] = {}


def reset() -> None:
    offers.clear()


def get_offer_internal(*, offerId: str) -> dict:
    o = offers.get(offerId)
    if not o:
        raise Problem(MODULE, 404, "not-found")
    return o | {"hasTechnicalUserProfile": o["technicalUserProfile"] is not None}


__getattr__ = standin.missing_interface(MODULE)   # steps and queries not implemented yet: stand-in
