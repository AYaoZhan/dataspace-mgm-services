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
"""The spec id of the credentials and the Problem Details of README 12 (types `urn:c4-m1:problem:...`)."""
from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel, ValidationError

from portal_common.problems import Problem

MODULE = "c4-m1"


def upstream(detail: str) -> Problem:
    return Problem(MODULE, 502, "upstream-error", detail=detail, retryable=True)


def no_route(detail: str) -> Problem:
    return Problem(MODULE, 409, "no-issuer-route", detail=detail, retryable=False)


M = TypeVar("M", bound=BaseModel)


def parse(model: type[M], data: object) -> M:
    """`data` as `model`, or 400 `validation` with the fields at fault, as the HTTP layer answers (README 12)."""
    try:
        return model.model_validate(data)
    except ValidationError as e:
        errors = [{"field": ".".join(str(x) for x in err["loc"]), "message": err["msg"]} for err in e.errors()]
        raise Problem(MODULE, 400, "validation", retryable=False, errors=errors) from None
