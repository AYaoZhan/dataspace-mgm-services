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
#  This program is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
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
"""Process Orchestration steps."""

from collections.abc import Callable

from fastapi import APIRouter, Body
from portal_common.problems import route_class

from features.technical_users import interface
from features.technical_users.controllers.dependencies import perm
from features.technical_users.managers.config import MODULE

router = APIRouter(route_class=route_class(MODULE))


def _register_step(name: str, function: Callable[[dict], dict]) -> None:
    path = f"/{name}"
    permission_path = f"/steps/{name}"

    def endpoint(body: dict = Body(...), _: dict = perm("POST", permission_path)):
        return function(body)

    endpoint.__name__ = "step_" + name.replace("-", "_")
    router.add_api_route(path, endpoint, methods=["POST"], summary=f"Step: {name}")


for _name, _function in {
    "create-for-subscription": interface.create_for_subscription,
    "apply-wallet-access": interface.apply_wallet_access,
    "delete": interface.delete,
    "disable-company-technical-users": interface.disable_company_technical_users,
    "enable-company-technical-users": interface.enable_company_technical_users,
    "disable-subscription-technical-users": interface.disable_subscription_technical_users,
}.items():
    _register_step(_name, _function)