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
"""Public interface of C12-M1 Process Orchestration for other modules (README 9). C12-M1 has no steps."""
from __future__ import annotations

from portal_common import standin
from portal_common.problems import Problem

from . import engine as eng

MODULE = eng.MODULE
SUBJECT_TYPES = {"APPLICATION", "COMPANY", "TECHNICAL_USER", "OFFER", "SUBSCRIPTION", "CONNECTOR"}


def find_processes_of_subject(*, subjectType: str, subjectId: str) -> list:
    """`GET /internal/processes`: the processes of one subject, newest first."""
    if subjectType not in SUBJECT_TYPES:
        raise Problem(MODULE, 400, "validation", detail="subjectType")
    items = [eng.summary(p) for p in list(eng.get_engine().processes.values())
             if p["subjectType"] == subjectType and p["subjectId"] == subjectId]
    return sorted(items, key=lambda x: x["createdAt"], reverse=True)


__getattr__ = standin.missing_interface(MODULE)
