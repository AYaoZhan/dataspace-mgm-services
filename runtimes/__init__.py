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
#  The program is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#  CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.
#
#  AI Disclosure: This file was entirely AI-generated.
#  The AI-generated portions are made available under CC0-1.0 and not subject
#  to the project's license. The human contributor has reviewed and verified
#  that the code is correct.
#
#  SPDX-License-Identifier: Apache-2.0 AND CC0-1.0
#  Assisted-By: GitHub Copilot (Claude Sonnet 5.5)
#################################################################################
"""Composable FastAPI runtimes for feature packages and legacy modules."""

from collections.abc import Callable
from types import ModuleType

from fastapi import FastAPI


def create_runtime(*features: ModuleType | str) -> FastAPI:
    """Create a full installation or a pod with the selected features/modules."""
    from scaffold.app import create_app

    return create_app(features or None)


def serve(factory: Callable[[], FastAPI]) -> None:
    """Serve an application factory using the configured host and port."""
    import os

    import uvicorn

    uvicorn.run(factory, factory=True, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", "8000")))


__all__ = ["create_runtime", "serve"]