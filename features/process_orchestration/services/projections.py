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
"""Views of a process for the API and the live stream (README 7.1, 7.6 to 7.8, 9)."""
from __future__ import annotations

import datetime as dt


def iso(t: dt.datetime | None) -> str | None:
    return t.isoformat() if t else None


def summary(p: dict) -> dict:
    """Process summary of README 7.1 and 9."""
    current = next((s["stepKey"] for s in p["steps"] if s["state"] not in ("DONE", "SKIPPED")), None)
    return {"id": p["id"], "flowKey": p["flowKey"], "flowVersion": p["flowVersion"], "subjectType": p["subjectType"],
            "subjectId": p["subjectId"], "status": p["status"], "currentStep": current, "endReason": p["endReason"],
            "createdAt": iso(p["createdAt"]), "updatedAt": iso(p["updatedAt"]), "finishedAt": iso(p["finishedAt"])}


def step_run(s: dict, detail: bool = False) -> dict:
    """A step run of README 7.2 and 7.3 (`detail`: with result and attempts)."""
    out = {k: s[k] for k in ("stepRunId", "stepKey", "call", "state", "attempts", "maxAttempts", "lastError")}
    out |= {"nextAttemptAt": iso(s["nextAttemptAt"]), "awaitUntil": iso(s["awaitUntil"]),
            "startedAt": iso(s["startedAt"]), "finishedAt": iso(s["finishedAt"])}
    if detail:
        out |= {"result": s["result"], "attempts_": s["attemptHistory"]}
    return out


def process_changed(p: dict) -> dict:
    """`data` of the stream event `process-changed` (README 7.6, `ProcessChanged`): IDs, keys and
    states only; no variables, results or errors."""
    s = summary(p)
    return {"processId": p["id"], "flowKey": p["flowKey"], "subjectType": p["subjectType"],
            "subjectId": p["subjectId"], "status": p["status"], "currentStep": s["currentStep"],
            "endReason": p["endReason"], "steps": [{"stepKey": r["stepKey"], "state": r["state"]} for r in p["steps"]],
            "updatedAt": s["updatedAt"]}


def stream_meta(p: dict) -> dict:
    """Who may see the stream events of a process (README 7.7, 7.8); never sent to the UI."""
    return {"processId": p["id"], "subjectType": p["subjectType"], "subjectId": p["subjectId"],
            "applicantSub": p["variables"].get("applicantSub")}
