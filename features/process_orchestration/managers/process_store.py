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
"""Process store: the processes, the delivered events and the audit of Process Orchestration.

In memory (no database yet): a restart loses the processes (upgrade: tables of README 5). The engine
holds the lock; the store itself is not thread-safe.
"""
from __future__ import annotations

from collections.abc import Iterable


class ProcessStore:
    def __init__(self) -> None:
        self.processes: dict[str, dict] = {}
        self.processed_events: set[str] = set()
        self.audit: list[dict] = []                    # retriggers (README 7.4)
        self.call_log: list[tuple[str, dict]] = []     # (step, input) of every call, in order
        self.streamed: dict[str, tuple] = {}           # processId -> last state sent to the UI (README 7.6)

    def first_delivery(self, event_id: str | None) -> bool:
        """README 6.7: an event `id` is processed once; an event without `id` always counts."""
        if event_id in self.processed_events:
            return False
        if event_id:
            self.processed_events.add(event_id)
        return True

    def add(self, proc: dict) -> dict:
        self.processes[proc["id"]] = proc
        return proc

    def get(self, process_id: str) -> dict | None:
        return self.processes.get(process_id)

    def all(self) -> list[dict]:
        return list(self.processes.values())

    def open_process(self, flow_key: str, value, open_states: Iterable[str]) -> dict | None:
        """The open process of a flow with this correlation value (README 6.5)."""
        return next((p for p in self.processes.values() if p["flowKey"] == flow_key
                     and p["correlationValue"] == value and p["status"] in open_states), None)

    def record_call(self, call: str, data: dict) -> None:
        self.call_log.append((call, data))

    def record_retrigger(self, entry: dict) -> None:
        self.audit.append(entry)

    def stream_changed(self, process_id: str, state: tuple) -> bool:
        """Remembers the state sent to the UI; False when it is the one sent last."""
        if self.streamed.get(process_id) == state:
            return False
        self.streamed[process_id] = state
        return True
