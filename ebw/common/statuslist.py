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
"""IETF Token Status List with one bit per credential (0 valid, 1 revoked)."""

import json
import time
import zlib
from pathlib import Path

from common.jose import b64url, b64url_decode, sign_jws

SIZE = 1024  # credentials per list


class StatusList:
    """A list kept in a JSON file: next free index and the revoked indexes."""

    def __init__(self, path: Path, uri: str):
        self.path = path
        self.uri = uri
        self.state = json.loads(path.read_text()) if path.exists() else {"next": 0, "revoked": []}

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.state))

    def allocate(self) -> dict:
        """Status claim for a new credential."""
        index = self.state["next"]
        if index >= SIZE:
            raise RuntimeError("status list is full")
        self.state["next"] = index + 1
        self._save()
        return {"status_list": {"idx": index, "uri": self.uri}}

    def set_revoked(self, index: int, revoked: bool = True) -> None:
        indexes = set(self.state["revoked"])
        indexes.add(index) if revoked else indexes.discard(index)
        self.state["revoked"] = sorted(indexes)
        self._save()

    def is_revoked(self, index: int) -> bool:
        return index in self.state["revoked"]

    def token(self, key, header: dict) -> str:
        bits = bytearray(SIZE // 8)
        for index in self.state["revoked"]:
            bits[index // 8] |= 1 << (index % 8)
        payload = {
            "sub": self.uri,
            "iat": int(time.time()),
            "ttl": 60,
            "status_list": {"bits": 1, "lst": b64url(zlib.compress(bytes(bits)))},
        }
        return sign_jws({"typ": "statuslist+jwt", **header}, payload, key)


def status_at(payload: dict, index: int) -> int:
    """Value at index of a status list token payload (already verified)."""
    status_list = payload["status_list"]
    bits = status_list.get("bits", 1)
    if bits not in (1, 2, 4, 8):
        raise ValueError("invalid bits")
    data = zlib.decompress(b64url_decode(status_list["lst"]))
    position = index * bits
    if position // 8 >= len(data):
        raise ValueError("index outside the status list")
    return (data[position // 8] >> (position % 8)) & ((1 << bits) - 1)
