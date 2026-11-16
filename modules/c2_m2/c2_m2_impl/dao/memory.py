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
#  SPDX-License-Identifier: Apache-2.0
#################################################################################
"""In-memory implementations of the C2-M2 DAO interfaces for use when `DATABASE_URL` is empty."""
from __future__ import annotations

import contextlib
import copy
from collections.abc import Iterable, Iterator, Sequence
from pathlib import Path

from modules.c2_m2.c2_m2_api.model.constants import (BindingStatus, InstanceClientStatus,
                                                     InstanceKind, InvitationKind)
from modules.c2_m2.c2_m2_impl.dao.app_client_template_dao import AppClientTemplateDao
from modules.c2_m2.c2_m2_impl.dao.app_instance_client_dao import AppInstanceClientDao
from modules.c2_m2.c2_m2_impl.dao.audit_log_dao import AuditLogDao
from modules.c2_m2.c2_m2_impl.dao.company_dao import CompanyDao
from modules.c2_m2.c2_m2_impl.dao.company_user_dao import CompanyUserDao
from modules.c2_m2.c2_m2_impl.dao.dao_service import DaoService
from modules.c2_m2.c2_m2_impl.dao.invitation_dao import InvitationDao
from modules.c2_m2.c2_m2_impl.dao.role_assignment_log_dao import RoleAssignmentLogDao
from modules.c2_m2.c2_m2_impl.internal.model import (AppClientTemplate, AppInstanceClient,
                                                     AuditLogEntry, Company, CompanyUser,
                                                     Invitation, RoleAssignmentLogEntry)
from modules.c2_m2.c2_m2_impl.internal.services import Database


class MemoryDatabase(Database):
    """In-memory stub Database: transactions and locks are no-ops."""

    @contextlib.contextmanager
    def transaction(self) -> Iterator[None]:
        yield

    @contextlib.contextmanager
    def lock(self, name: str) -> Iterator[None]:
        yield

    def query(self, sql: str, params: Sequence = ()) -> list[dict]:
        return []

    def execute(self, sql: str, params: Sequence = ()) -> None:
        pass

    def upsert(self, table: str, key: str, columns: Sequence[str], params: Sequence,
               casts: dict[str, str] | None = None) -> None:
        pass

    def migrate(self, location: Path) -> None:
        pass


class MemoryCompanyDao(CompanyDao):
    def __init__(self) -> None:
        self._companies: dict[str, Company] = {}

    @contextlib.contextmanager
    def lock(self, company_id: str) -> Iterator[None]:
        yield

    def get(self, company_id: str) -> Company | None:
        c = self._companies.get(company_id)
        return copy.deepcopy(c) if c else None

    def save(self, company: Company) -> None:
        self._companies[company.company_id] = copy.deepcopy(company)


class MemoryCompanyUserDao(CompanyUserDao):
    def __init__(self) -> None:
        self._bindings: dict[str, CompanyUser] = {}

    @contextlib.contextmanager
    def lock_account(self, user_id: str) -> Iterator[None]:
        yield

    def save(self, binding: CompanyUser) -> None:
        self._bindings[binding.id] = copy.deepcopy(binding)

    def current_of(self, user_id: str) -> CompanyUser | None:
        for b in self._bindings.values():
            if b.user_id == user_id and b.status in (BindingStatus.ACTIVE, BindingStatus.DISABLED):
                return copy.deepcopy(b)
        return None

    def list_of(self, user_id: str, company_id: str) -> list[CompanyUser]:
        matching = [
            copy.deepcopy(b) for b in self._bindings.values()
            if b.user_id == user_id and b.company_id == company_id
        ]
        matching.sort(key=lambda b: b.created_at)
        return matching

    def list_of_company(self, company_id: str | None, statuses: Iterable[BindingStatus]) -> list[CompanyUser]:
        status_set = set(statuses)
        matching = [
            copy.deepcopy(b) for b in self._bindings.values()
            if (company_id is None or b.company_id == company_id) and b.status in status_set
        ]
        matching.sort(key=lambda b: b.created_at)
        return matching


class MemoryAppClientTemplateDao(AppClientTemplateDao):
    def __init__(self) -> None:
        self._templates: dict[str, AppClientTemplate] = {}

    @contextlib.contextmanager
    def lock(self, app_id: str) -> Iterator[None]:
        yield

    def get(self, app_id: str) -> AppClientTemplate | None:
        t = self._templates.get(app_id)
        return copy.deepcopy(t) if t else None

    def save(self, template: AppClientTemplate) -> None:
        self._templates[template.app_id] = copy.deepcopy(template)


class MemoryAppInstanceClientDao(AppInstanceClientDao):
    def __init__(self) -> None:
        self._clients: dict[str, AppInstanceClient] = {}
        self._next_number = 1

    def get(self, instance_client_id: str) -> AppInstanceClient | None:
        c = self._clients.get(instance_client_id)
        return copy.deepcopy(c) if c else None

    def save(self, instance_client: AppInstanceClient) -> None:
        self._clients[instance_client.id] = copy.deepcopy(instance_client)

    def find_by_subscription(self, offer_subscription_id: str) -> AppInstanceClient | None:
        for c in self._clients.values():
            if c.offer_subscription_id == offer_subscription_id:
                return copy.deepcopy(c)
        return None

    def find_single(self, app_id: str) -> AppInstanceClient | None:
        for c in self._clients.values():
            if (c.app_id == app_id and c.instance_kind == InstanceKind.SINGLE
                    and c.status != InstanceClientStatus.DISABLED):
                return copy.deepcopy(c)
        return None

    def find_by_iam_client_id(self, iam_client_id: str) -> AppInstanceClient | None:
        for c in self._clients.values():
            if c.iam_client_id == iam_client_id:
                return copy.deepcopy(c)
        return None

    def list_of_app(self, app_id: str) -> list[AppInstanceClient]:
        matching = [copy.deepcopy(c) for c in self._clients.values() if c.app_id == app_id]
        matching.sort(key=lambda c: c.created_at)
        return matching

    def list_all(self) -> list[AppInstanceClient]:
        matching = [copy.deepcopy(c) for c in self._clients.values()]
        matching.sort(key=lambda c: c.created_at)
        return matching

    def next_client_number(self) -> int:
        num = self._next_number
        self._next_number += 1
        return num


class MemoryInvitationDao(InvitationDao):
    def __init__(self) -> None:
        self._invitations: dict[str, Invitation] = {}

    @contextlib.contextmanager
    def lock(self, invitation_id: str) -> Iterator[None]:
        yield

    @contextlib.contextmanager
    def lock_staff(self) -> Iterator[None]:
        yield

    def get(self, invitation_id: str) -> Invitation | None:
        i = self._invitations.get(invitation_id)
        return copy.deepcopy(i) if i else None

    def save(self, invitation: Invitation) -> None:
        self._invitations[invitation.id] = copy.deepcopy(invitation)

    def find_by_code_hash(self, code_hash: str) -> Invitation | None:
        for i in self._invitations.values():
            if i.code_hash == code_hash:
                return copy.deepcopy(i)
        return None

    def list_of(self, kind: InvitationKind, company_id: str | None) -> list[Invitation]:
        matching = [
            copy.deepcopy(i) for i in self._invitations.values()
            if i.kind == kind and (company_id is None or i.company_id == company_id)
        ]
        matching.sort(key=lambda i: i.created_at)
        return matching

    def list_all(self) -> list[Invitation]:
        matching = [copy.deepcopy(i) for i in self._invitations.values()]
        matching.sort(key=lambda i: i.created_at)
        return matching


class MemoryAuditLogDao(AuditLogDao):
    def __init__(self) -> None:
        self._entries: list[AuditLogEntry] = []

    def add(self, entry: AuditLogEntry) -> None:
        self._entries.append(copy.deepcopy(entry))

    def list_all(self) -> list[AuditLogEntry]:
        return [copy.deepcopy(e) for e in self._entries]


class MemoryRoleAssignmentLogDao(RoleAssignmentLogDao):
    def __init__(self) -> None:
        self._entries: list[RoleAssignmentLogEntry] = []

    def add(self, entry: RoleAssignmentLogEntry) -> None:
        self._entries.append(copy.deepcopy(entry))

    def list_all(self) -> list[RoleAssignmentLogEntry]:
        return [copy.deepcopy(e) for e in self._entries]


def memory_dao_service(db: Database | None = None) -> DaoService:
    """Returns a DaoService backed entirely by in-memory stores."""
    db = db or MemoryDatabase()
    return DaoService(
        db,
        MemoryAppClientTemplateDao(),
        MemoryAppInstanceClientDao(),
        MemoryCompanyDao(),
        MemoryCompanyUserDao(),
        MemoryInvitationDao(),
        MemoryAuditLogDao(),
        MemoryRoleAssignmentLogDao(),
    )


__all__ = [
    "MemoryAppClientTemplateDao",
    "MemoryAppInstanceClientDao",
    "MemoryAuditLogDao",
    "MemoryCompanyDao",
    "MemoryCompanyUserDao",
    "MemoryDatabase",
    "MemoryInvitationDao",
    "MemoryRoleAssignmentLogDao",
    "memory_dao_service",
]
