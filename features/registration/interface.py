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
#  Assisted-By: GitHub Copilot (claude-opus-5.5)
"""In-process contract of the registration (call convention, AGENTS.md): the steps of README 8 and the queries
of README 9 under their convention names. Other services and Process Orchestration import only from here.

Every function answers with the same JSON the HTTP API sends (`services.shared.as_json`).
"""
from __future__ import annotations

from features.registration.models import MODULE
from features.registration.services import application_process_service as process
from features.registration.services.shared import as_json

__all__ = ["MODULE", "close_application", "complete_application", "get_application_internal",
           "list_agreements_internal", "list_applications_internal"]


def complete_application(input: dict) -> dict:
    return as_json(process.complete_application(input))


def close_application(input: dict) -> dict:
    return as_json(process.close_application(input))


def get_application_internal(*, applicationId: str, **other: object) -> dict:
    return as_json(process.get_application_internal(applicationId=applicationId, **other))


def list_applications_internal(*, applicationId: list[str] | str | None = None,
                               **other: object) -> list[dict]:
    return [as_json(x) for x in process.list_applications_internal(applicationId=applicationId, **other)]


def list_agreements_internal(*, status: str | None = None, **other: object) -> list[dict]:
    return [as_json(x) for x in process.list_agreements_internal(status=status, **other)]
