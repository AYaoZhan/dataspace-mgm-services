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
"""In-process contract of the connectors (call convention, AGENTS.md): the steps of README 8 and the query of
README 9 under their convention names, and the operations of people (README 7), which only the controllers call.
Other modules and Process Orchestration import only from here; the logic lives in `services/`."""
from __future__ import annotations

from features.connector import services
from features.connector.models import MODULE
from features.connector.services import (
    change_endpoint,
    delete_connector,
    get_connector,
    list_connectors,
    register_connector,
    register_connector_as_a_service,
    reset,
)

__all__ = [
    "MODULE", "change_endpoint", "deactivate_subscription_connectors", "delete_connector", "get_connector",
    "list_connectors", "list_connectors_internal", "register_connector", "register_connector_as_a_service", "reset",
    "unlink_technical_user",
]


# -- steps for Process Orchestration (README 8): input = JSON body incl. processId and stepRunId ---
def deactivate_subscription_connectors(input: dict) -> dict:
    return services.deactivate_subscription_connectors(input)


def unlink_technical_user(input: dict) -> dict:
    return services.unlink_technical_user(input)


# -- queries for other modules (README 9): parameters by their openapi names ------------------------
def list_connectors_internal(*, technicalUserId: str | None = None, **_other) -> list:
    """9.1: the ACTIVE connectors that use this technical user, as `ConnectorRef`."""
    return services.list_connectors_internal(technical_user_id=technicalUserId)
