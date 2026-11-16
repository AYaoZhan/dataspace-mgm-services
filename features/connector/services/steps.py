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
"""The steps of the connectors for Process Orchestration (README 8)."""
from __future__ import annotations

from portal_common import standin

from ..managers.store import LOCK, connectors, deleted_technical_users, ended_subscriptions, now, write_audit
from ..models import ACTIVE, INACTIVE
from .common import publish_deactivated, step_input


def deactivate_subscription_connectors(input: dict) -> dict:
    """8.1: the connector of an ended or declined subscription becomes INACTIVE, without technical user.
    Also clears a link that an INACTIVE connector still holds (deleted while the subscription was
    PENDING, README 7.6). `ConnectorDeactivated` only for a real change of status, so a repetition
    publishes nothing and answers DONE with an empty list."""
    sub_id = step_input(input, "offerSubscriptionId")
    changed = []
    with LOCK:
        ended_subscriptions.add(sub_id)   # also without connectors, so a later registration is refused
        for c in connectors.values():
            if c["offer_subscription_id"] != sub_id or (c["status"] == INACTIVE and c["technical_user_id"] is None):
                continue
            was_active = c["status"] == ACTIVE
            c.update(status=INACTIVE, technical_user_id=None, changed_at=now())
            write_audit("deactivate-subscription-connectors", c["id"])
            if was_active:
                publish_deactivated(c)
            changed.append(c["id"])
    return standin.step_reply(input, {"connectorIds": changed})


def unlink_technical_user(input: dict) -> dict:
    """8.2: removes the deleted technical user from the connector that uses it; the connector keeps its status."""
    tu_id = step_input(input, "technicalUserId")
    changed = []
    with LOCK:
        deleted_technical_users.add(tu_id)   # also without connectors, so a later registration is refused
        for c in connectors.values():
            if c["technical_user_id"] == tu_id:
                c.update(technical_user_id=None, changed_at=now())
                write_audit("unlink-technical-user", c["id"])
                changed.append(c["id"])
    return standin.step_reply(input, {"connectorIds": changed})
