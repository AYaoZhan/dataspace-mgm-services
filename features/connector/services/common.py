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
"""Helpers of the connector services: UUIDs in one spelling, the step input and the deactivation event."""
from __future__ import annotations

import uuid

from portal_common import events
from portal_common.problems import Problem

from ..models import MODULE


def publish_deactivated(c: dict) -> None:
    events.publish(MODULE, "ConnectorDeactivated", {"connectorId": c["id"], "companyId": c["host_company_id"]})


def is_uuid(value) -> bool:
    if not isinstance(value, str):
        return False
    try:
        uuid.UUID(value)
    except ValueError:
        return False
    return True


def canonical(value: str) -> str:
    """One spelling per UUID (lower case, with hyphens), so that comparisons and links do not depend
    on the casing a caller used."""
    return str(uuid.UUID(value))


def step_input(input: dict, key: str) -> str:
    """StepInput of openapi.yaml: `processId`, `stepRunId` and the business key, all UUIDs.
    Checked before anything changes (README 8, FRAMEWORK 4.4)."""
    if not isinstance(input, dict):
        raise Problem(MODULE, 400, "validation", detail="JSON object required", retryable=False)
    errors = [{"field": f, "message": "UUID required"} for f in ("processId", "stepRunId", key)
              if not is_uuid(input.get(f))]
    if errors:
        raise Problem(MODULE, 400, "validation", errors=errors, retryable=False)
    return canonical(input[key])
