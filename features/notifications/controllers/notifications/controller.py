#################################################################################
#  Copyright (c) 2026 Technovative Solutions
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
"""HTTP operations on the own inbox (README 7): token, permission and parameters, then `inbox`
(what the caller sees), `listing` (the list query) and `marks` (the caller's read and hidden state).

`/count` and `/events` are declared before `/{notificationId}`, so they are matched first.
"""
from __future__ import annotations

import datetime as dt
from typing import Annotated, Literal

from fastapi import Header, Query, Request, Response

from features.notifications.services import inbox, listing, marks
from portal_common import sse
from portal_common.routing import Controller, Permission

controller = Controller("Notifications: Inbox")


@controller.get("")
def list_notifications(claims: dict = Permission,
                       topic: Literal["INFO", "ACTION"] | None = None,
                       ntype: Annotated[str | None, Query(alias="type")] = None,
                       read: bool | None = None,
                       done: bool | None = None,
                       createdSince: dt.datetime | None = None,
                       sort: Literal["createdAt.desc", "createdAt.asc"] = "createdAt.desc",
                       page: Annotated[int, Query(ge=0)] = 0,
                       size: Annotated[int, Query(ge=1, le=100)] = 20):
    """README 7.1: filters, sorting by `createdAt`, paging as in FRAMEWORK 4.1; invalid filters give 400."""
    filters = listing.Filters(topic, ntype, read, done, createdSince)
    return listing.list_page(inbox.own(claims), filters, newest_first=sort == "createdAt.desc", page=page, size=size)


@controller.get("/count")
def count_notifications(claims: dict = Permission):
    """README 7.2: counters of the own inbox (hidden ones left out)."""
    return inbox.count(claims)


@controller.get("/events")
def stream_notification_events(request: Request, claims: dict = Permission,
                               last_event_id: Annotated[str | None, Header(alias="Last-Event-ID")] = None):
    """README 7.6: without `Last-Event-ID` only new events; an id no longer kept gives `resync`."""
    return sse.response(inbox.events(), request, claims, last_event_id,
                        visible=inbox.stream_filter(claims), on_gap=lambda: [("resync", {})])


@controller.get("/{notificationId}")
def get_notification(notificationId: str, claims: dict = Permission):
    """README 7.3: one notification of the own inbox with `read` for the caller."""
    return inbox.get(notificationId, claims)


@controller.post("/{notificationId}/read", status_code=204)
def mark_read(notificationId: str, claims: dict = Permission):
    """README 7.4: set `read_at` for the caller; idempotent, the first time is kept."""
    marks.mark_read(inbox.find(notificationId, claims), claims.get("sub"))
    return Response(status_code=204)


@controller.post("/{notificationId}/unread", status_code=204)
def mark_unread(notificationId: str, claims: dict = Permission):
    """README 7.4: remove `read_at` for the caller; idempotent."""
    marks.mark_unread(inbox.find(notificationId, claims), claims.get("sub"))
    return Response(status_code=204)


@controller.post("/{notificationId}/hide", status_code=204)
def hide_notification(notificationId: str, claims: dict = Permission):
    """README 7.5: hide for the caller; an open task gives 409 `task-open`; idempotent."""
    marks.hide(inbox.find(notificationId, claims), claims.get("sub"))
    return Response(status_code=204)
