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
"""Installation settings (FRAMEWORK 4.8): one JSON file per installation, path in `SETTINGS_FILE`.

Every module reads the settings through `load()`; nothing else holds installation values, so a
second installation (OSP B) only needs another `SETTINGS_FILE`.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from .spec import ROOT

DEFAULT_FILE = ROOT / "config" / "osp-a" / "installation.json"
_cache: dict | None = None


def load() -> dict:
    global _cache
    if _cache is None:
        path = Path(os.environ.get("SETTINGS_FILE") or DEFAULT_FILE)
        data = json.loads(path.read_text(encoding="utf-8"))
        for key in ("ospId", "ospName", "ospCompanyId"):
            if not data.get(key):
                raise ValueError(f"{path}: setting {key!r} is missing (FRAMEWORK 4.8)")
        data["_file"] = str(path)
        _cache = data
    return _cache


def get(key: str, default=None):
    return load().get(key, default)


def resolve_path(value: str | None) -> Path | None:
    """Paths in the settings are relative to the settings file."""
    if not value:
        return None
    p = Path(value)
    return p if p.is_absolute() else Path(load()["_file"]).parent / p


def base_url() -> str:
    """Address under which this installation is reachable (callbacks, in-process calls)."""
    return os.environ.get("BASE_URL", "http://localhost:8000").rstrip("/")


def reset() -> None:
    global _cache
    _cache = None
