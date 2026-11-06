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
"""Stand-in of C11-M1 Notifications: a small subset of the rules, enough to see the inbox work.

- `ApplicationSubmitted` -> `APPLICATION_SUBMITTED` for the applicant;
- `ApplicationCompleted` -> `APPLICATION_COMPLETED` for the applicant;
- `ProcessStepFailed` -> `PROCESS_STEP_FAILED` for every person with the portal role `OSP Admin`;
  `ProcessStepRetriggered` (same step), `ProcessCompleted`, `ProcessEnded` close it (`done`).
Recipients by portal role are read from the test IAM (the real module asks C2-M2).
Events are CloudEvents (FRAMEWORK 6): the rules match `type` and read the fields of `data`;
`sourceEventId` of a notification is the event `id`.

`GET /notifications/events` (README 7.6): Server-Sent Events `notification-created`,
`notification-done` and `resync` for the own inbox, through `portal_common.sse`.
"""
from __future__ import annotations

import datetime as dt
import uuid
from typing import Annotated

from fastapi import Header, Request

from portal_common import sse, standin
from tools import iam_backend

STANDIN = True
MODULE = "c11-m1"
router = standin.router(MODULE)
notifications: list[dict] = []
applicants: dict[str, str] = {}   # applicationId -> sub
BROKER = sse.Broker()
TOPICS = {"APPLICATION_SUBMITTED": "INFO", "APPLICATION_COMPLETED": "INFO", "PROCESS_STEP_FAILED": "ACTION"}
STAFF = {"PROCESS_STEP_FAILED"}   # R17 is a staff notification; the stand-in stores it per OSP Admin


def reset() -> None:
    notifications.clear()
    applicants.clear()
    BROKER.reset()


def _add(user: str, ntype: str, event: dict, **content) -> None:
    n = {"id": str(uuid.uuid4()), "userId": user, "type": ntype, "topic": TOPICS[ntype], "read": False,
         "done": False, "createdAt": dt.datetime.now(dt.UTC).isoformat(), "sourceEventId": event["id"],
         "content": content}
    notifications.append(n)
    BROKER.publish("notification-created", {   # README 7.6: no content, only IDs, types and states
        "notificationId": n["id"], "type": ntype, "topic": n["topic"], "forStaff": ntype in STAFF,
        "done": False if n["topic"] == "ACTION" else None, "createdAt": n["createdAt"]}, {"sub": user})


def _close(match) -> None:
    for n in notifications:
        if n["topic"] == "ACTION" and not n["done"] and match(n):
            n["done"], n["doneAt"] = True, dt.datetime.now(dt.UTC).isoformat()
            BROKER.publish("notification-done", {"notificationId": n["id"], "doneAt": n["doneAt"]}, {"sub": n["userId"]})


def on_event(event: dict) -> None:
    """A CloudEvent of the relay (FRAMEWORK 6): the name is `type`, the fields are in `data`."""
    t, d = event["type"], event.get("data") or {}
    if t == "ApplicationSubmitted":
        applicants[d["applicationId"]] = d["applicantSub"]
        _add(d["applicantSub"], "APPLICATION_SUBMITTED", event, applicationId=d["applicationId"])
    elif t == "ApplicationCompleted" and d.get("applicationId") in applicants:
        _add(applicants[d["applicationId"]], "APPLICATION_COMPLETED", event, applicationId=d["applicationId"])
    elif t == "ProcessStepFailed":
        for uid in iam_backend.backend(MODULE).users_with_portal_role("OSP Admin"):
            _add(uid, "PROCESS_STEP_FAILED", event, processId=d["processId"], stepKey=d.get("stepKey"))
    elif t == "ProcessStepRetriggered":
        _close(lambda n: n["type"] == "PROCESS_STEP_FAILED" and n["content"] == {
            "processId": d["processId"], "stepKey": d.get("stepKey")})
    elif t in ("ProcessCompleted", "ProcessEnded"):
        _close(lambda n: n["type"] == "PROCESS_STEP_FAILED" and n["content"]["processId"] == d["processId"])


@router.get("/notifications/events")
def inbox_events(request: Request, claims: dict = standin.perm(MODULE, "GET", "/notifications/events"),
                 last_event_id: Annotated[str | None, Header(alias="Last-Event-ID")] = None):
    """README 7.6: without Last-Event-ID only new events; an id no longer kept gives `resync`."""
    sub = claims["sub"]
    return sse.response(BROKER, request, claims, last_event_id, visible=lambda meta: meta.get("sub") == sub,
                        on_gap=lambda: [("resync", {})])


@router.get("/notifications")
def inbox(claims: dict = standin.perm(MODULE, "GET", "/notifications")):
    items = [n for n in notifications if n["userId"] == claims["sub"]]
    return {"items": items, "page": 0, "size": len(items), "total": len(items)}
