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
"""In-process contract of the dataspace wallets (call convention, AGENTS.md): the steps of README 8 and the queries
of README 9 under their convention names. Other modules and Process Orchestration import only from here; the logic
lives in `services/`.

Provider: SAP DIV, IdentityHub or the dataspace wallet of the CSP (`managers/providers/`, README 6.1, 6.11). The
holder access (API key or client secret) is stored encrypted and only returned by the query for C4-M1.
"""
from __future__ import annotations

from portal_common import standin

from .managers import crypto, providers
from .managers.wallet_store import WalletStore
from .models import MODULE
from .services import account_service, wallet_service

__all__ = [
    "MODULE", "create_wallet", "create_wallet_account", "delete_wallet_account", "get_holder_access",
    "get_wallet_account_internal", "get_wallet_info", "reset", "store", "wallet_view",
]


def store() -> WalletStore:
    """The active store."""
    return wallet_service.get_store()


def reset() -> None:
    """Clear the store, the key cache and the state of the provider adapters."""
    wallet_service.reset()
    crypto.reset()
    providers.reset()


# -- steps for Process Orchestration (README 8): input = JSON body incl. processId and stepRunId ---
def create_wallet(input: dict) -> dict:
    """Step `create-wallet` (README 8.1)."""
    return wallet_service.create_wallet(input)


def create_wallet_account(input: dict) -> dict:
    """Step `create-wallet-account` (README 8.2)."""
    return account_service.create_wallet_account(input)


def delete_wallet_account(input: dict) -> dict:
    """Step `delete-wallet-account` (README 8.3)."""
    return account_service.delete_wallet_account(input)


# -- queries for other modules (README 9): parameters by their openapi names ------------------------
def get_wallet_info(*, companyId: str) -> dict:
    """Query `getWalletInfo` (README 9.1): the wallet without secrets."""
    return wallet_service.wallet_info(companyId)


def wallet_view(*, companyId: str) -> dict:
    """Body of `GET /companies/{companyId}/wallet` (README 7.1, openapi `Wallet`)."""
    return wallet_service.wallet_view(companyId)


def get_holder_access(*, companyId: str, claims: dict | None = None) -> dict:
    """Query `getHolderAccess` (README 9.3), only for C4-M1. `claims` is set by the HTTP route; in the same
    process the audit entry holds the name of the calling module."""
    return wallet_service.holder_access(companyId, claims)


def get_wallet_account_internal(*, technicalUserId: str) -> dict:
    """Query `getWalletAccountInternal` (README 9.2)."""
    return account_service.get_wallet_account_internal(technicalUserId=technicalUserId)


__getattr__ = standin.missing_interface(MODULE)   # steps and queries not implemented yet: stand-in
