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
"""The steps of the subscriptions in the flows of Process Orchestration: `notify-provider` and
`send-activation-callback` (client ID of the instance and a rotated secret of the technical user to the provider's
`callbackUrl`, C10-M1 11.2)."""
from __future__ import annotations

from features.subscriptions.managers import neighbour_client, provider_client, store
from features.subscriptions.models.subscription import MODULE
from portal_common import standin
from portal_common.problems import Problem


def notify_provider(input: dict) -> dict:
    s = store.subscriptions.get(input.get("offerSubscriptionId"))
    if not s:
        raise Problem(MODULE, 404, "not-found", retryable=False)
    customer = neighbour_client.query_company(s["customerCompanyId"])
    provider_client.call(s["providerCompanyId"], "setup", {
        "offerSubscriptionId": s["offerSubscriptionId"], "offerId": s["offerId"], "customerCompanyId": s["customerCompanyId"],
        "customerName": customer.get("name"), "customerCountry": (customer.get("address") or {}).get("countryCode"),
        "setupExpected": s["offerType"] == "APP"})
    return standin.step_reply(input)


def send_activation_callback(input: dict) -> dict:
    s = store.subscriptions.get(input.get("offerSubscriptionId"))
    if not s:
        raise Problem(MODULE, 404, "not-found", retryable=False)
    client_id = input.get("clientId")   # iamClientId of the instance client (C10-M1 8.2)
    config = store.provider_config.get(s["providerCompanyId"])
    if not config or not config.get("callbackUrl"):
        return standin.step_reply(input)    # without a callbackUrl: nothing to do
    technical_user = None
    for acc in input.get("technicalUsers") or []:
        r = neighbour_client.rotate_subscription_credentials(acc["technicalUserId"], s["offerSubscriptionId"])
        technical_user = {"clientId": r["iamClientId"], "clientSecret": r["secret"]}
    provider_client.call(s["providerCompanyId"], "callback", {"offerSubscriptionId": s["offerSubscriptionId"],
                                                              "instanceUrl": s["instanceUrl"], "clientId": client_id,
                                                              "technicalUser": technical_user})
    return standin.step_reply(input)
