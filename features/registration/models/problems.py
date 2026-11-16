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
"""Problem factories of the registration that every layer uses: the validation Problem with its field errors
(FRAMEWORK 4.5) and the reading of a checked body into its model.
"""
from __future__ import annotations

from pydantic import BaseModel, ValidationError

from features.registration.models import MODULE
from portal_common.problems import Problem


def field_error(field: str, message: str) -> dict:
    return {"field": field, "message": message}


def validation_problem(errors: list[dict]) -> Problem:
    return Problem(MODULE, 400, "validation", errors=errors)


def parse[M: BaseModel](model: type[M], body: object) -> M:
    """The body as its model, after the checks of the service: what they let through but the types of the spec
    do not allow is a validation error like theirs, never a 500."""
    try:
        return model.model_validate(body)
    except ValidationError as e:
        raise validation_problem([field_error(".".join(map(str, err["loc"])) or "body", err["msg"])
                                  for err in e.errors()]) from e
