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
"""Module registry: one folder per module of the spec, `modules/<module id with _>/`.

Contract of a module folder (a team replaces only its folder):
- `interface.py` with a function for every step and query of the spec (README, module structure);
- `router.py` with `router` (an `APIRouter` under the base path of the spec) and `reset()`;
- optional in `router.py`: `on_event(event)` (subscriber of the event relay), `on_startup()`;
- `STANDIN = True` marks the stand-in, `PROVIDED = True` a provided module (C12-M1); a team's
  module sets neither;
- an empty `__init__.py`, no top-level modules beside the folders.

The list of modules comes from the spec (every folder with an `/api/<module>` base). A module
without a folder is still mounted, as the spec-driven fallback (every path answers 501, steps DONE).
Every operation of the spec that a module does not implement is added from the fallback too.
"""
from __future__ import annotations

from collections.abc import Iterable
import importlib
import importlib.util
import pkgutil
from dataclasses import dataclass
from types import ModuleType
from collections.abc import Iterable

from portal_common import spec
import features

LAST = ("c11-m1", "c12-m1")   # subscribers that react to the events of all others


@dataclass
class Entry:
    id: str
    module: ModuleType | None   # router.py of the folder, None = spec fallback only
    kind: str                   # "stand-in", "provided", "team" or "fallback"


def _legacy_module(mid: str) -> ModuleType | None:
    name = f"modules.{mid.replace('-', '_')}.router"
    package = name.rsplit(".", 1)[0]
    if importlib.util.find_spec(package) and importlib.util.find_spec(name):
        return importlib.import_module(name)
    return None


def _discover_features() -> dict[str, ModuleType]:
    feature_modules = {}
    for package in pkgutil.iter_modules(features.__path__):
        module = importlib.import_module(f"features.{package.name}")
        mid = getattr(module, "MODULE", None)
        if mid:
            if mid in feature_modules:
                raise ValueError(f"multiple features declare module {mid}")
            feature_modules[mid] = module
    return feature_modules


def _resolve_selected(selected: ModuleType | str, known_modules: dict) -> tuple[str | None, ModuleType | None]:
    if isinstance(selected, ModuleType):
        module = selected
        mid = getattr(module, "MODULE", None)
    elif selected in known_modules:
        module = _legacy_module(selected)
        mid = selected
    else:
        module = importlib.import_module(f"features.{selected}")
        mid = getattr(module, "MODULE", None)
    return mid, module


def _select_features(selected_features: Iterable[ModuleType | str], known_modules: dict) -> dict[str, ModuleType]:
    selected_modules = {}
    for selected in selected_features:
        mid, module = _resolve_selected(selected, known_modules)
        if mid not in known_modules or module is None:
            raise ValueError(f"unknown feature or module: {selected}")
        if mid in selected_modules:
            raise ValueError(f"multiple selected features declare module {mid}")
        selected_modules[mid] = module
    return selected_modules


def _entry_module(mid: str, discovered: dict[str, ModuleType], selected: dict[str, ModuleType] | None):
    if selected is not None:
        return selected.get(mid)
    return discovered.get(mid) or _legacy_module(mid)


def _kind(module: ModuleType | None) -> str:
    if module is None:
        return "fallback"
    if getattr(module, "STANDIN", False):
        return "stand-in"
    if getattr(module, "PROVIDED", False):
        return "provided"
    return "team"


def load(selected_features: Iterable[ModuleType | str] | None = None) -> list[Entry]:
    known_modules = spec.modules()
    discovered = _discover_features()
    selected = _select_features(selected_features, known_modules) if selected_features is not None else None
    entries = []
    for mid in known_modules:
        mod = _entry_module(mid, discovered, selected)
        kind = _kind(mod)
        entries.append(Entry(mid, mod, kind))
    return sorted(entries, key=lambda e: (e.id in LAST, LAST.index(e.id) if e.id in LAST else 0, e.id))
