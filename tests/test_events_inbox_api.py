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
"""Event inbox of the installation, `POST /api/v1/events/inbox` (FRAMEWORK 6, proposal OP-54)."""
import json
import uuid

import pytest
from fastapi.testclient import TestClient

from conftest import BASE, bearer, person_token
from portal_common import events, tokens
from portal_common import http as phttp
from scaffold import app as scaffold_app

INBOX = "/api/v1/events/inbox"
STRUCTURED = {"Content-Type": "application/cloudevents+json"}
APPLICATION = "0f8e2d4c-6b1a-4c3e-8f7d-2a9b1c0d3e4f"   # FRAMEWORK 7a / C12-M1 README 14
COMPANY = "c0000001-0000-4000-8000-000000000001"
ERIKA = "5a1c0001-0000-4000-8000-000000000001"


@pytest.fixture
def app():
    app = scaffold_app.create_app()
    phttp.register_local(BASE, app)   # token endpoint and JWKS of the test IAM
    yield app
    scaffold_app.reset_all(app.state.entries)


@pytest.fixture
def client(app):
    return TestClient(app, base_url=BASE)


def submitted(**overrides) -> dict:
    """ApplicationSubmitted of C1-M2 as in FRAMEWORK 6 (example) with a fresh id."""
    return {"specversion": "1.0", "id": str(uuid.uuid4()), "source": "urn:c1-m2", "type": "ApplicationSubmitted",
            "time": "2026-11-06T09:30:00Z", "datacontenttype": "application/json",
            "data": {"applicationId": APPLICATION, "companyId": COMPANY, "kind": "ONBOARDING",
                     "existingCompany": False, "applicantSub": ERIKA}} | overrides


def svc(module: str) -> dict:
    return bearer(tokens.service_token(module))


def logged(event_id: str) -> list[dict]:
    return [e for e in events.RELAY.log if e["id"] == event_id]


# ---------------------------------------------------------------- accepted
def test_structured_mode_puts_the_event_on_the_bus_unchanged(client):
    ev = submitted()
    r = client.post(INBOX, headers=svc("c1-m2") | STRUCTURED, content=json.dumps(ev))
    assert r.status_code == 202 and r.content == b""
    assert logged(ev["id"]) == [ev]   # same id, time and data; nothing added


def test_binary_mode_takes_the_attributes_from_the_ce_headers(client):
    ev = submitted()
    headers = {f"ce-{a}": ev[a] for a in ("specversion", "id", "source", "type")}
    headers |= {"ce-time": "2026-11-06T09%3A30%3A00Z",   # header values are percent-encoded (HTTP binding)
                "Content-Type": "application/json; charset=utf-8"}
    r = client.post(INBOX, headers=svc("c1-m2") | headers, content=json.dumps(ev["data"]))
    assert r.status_code == 202
    assert logged(ev["id"]) == [ev]


def test_same_source_and_id_again_is_accepted_and_delivered_once(client):
    ev = submitted()
    for _ in range(2):
        assert client.post(INBOX, headers=svc("c1-m2") | STRUCTURED, content=json.dumps(ev)).status_code == 202
    assert len(logged(ev["id"])) == 1


def test_a_received_event_starts_the_process_like_a_local_one(app):
    with TestClient(app, base_url=BASE) as client:   # relay and worker of C12-M1 run
        ev = submitted()
        assert client.post(INBOX, headers=svc("c1-m2") | STRUCTURED, content=json.dumps(ev)).status_code == 202
        assert events.RELAY.wait_idle(10)
        started = [e for e in events.RELAY.log if e["type"] == "ProcessStarted"]
    assert [(e["source"], e["data"]["flowKey"], e["data"]["subjectId"]) for e in started] == [
        ("urn:c12-m1", "onboarding", APPLICATION)]   # C12-M1 README 13 case 2, started through the inbox


# ---------------------------------------------------------------- refused
def _problem(r, status: int, name: str) -> dict:
    assert r.status_code == status, r.text
    assert r.headers["content-type"].startswith("application/problem+json")
    body = r.json()
    assert body["type"] == f"urn:events:problem:{name}"
    return body


def test_token_of_the_service_account_of_the_source_is_required(client):
    body = json.dumps(submitted())
    _problem(client.post(INBOX, headers=STRUCTURED, content=body), 401, "unauthorized")
    _problem(client.post(INBOX, headers=bearer("not-a-token") | STRUCTURED, content=body), 401, "unauthorized")
    _problem(client.post(INBOX, headers=bearer(person_token("otto")) | STRUCTURED, content=body), 403, "forbidden")
    p = _problem(client.post(INBOX, headers=svc("c3-m1") | STRUCTURED, content=body), 403, "forbidden")
    assert "urn:c3-m1" in p["detail"]   # a module only delivers its own events
    assert events.RELAY.log == []


@pytest.mark.parametrize("content_type", ["text/plain", "application/cloudevents-batch+json", None])
def test_other_content_types_are_refused(client, content_type):
    headers = svc("c1-m2") | ({"Content-Type": content_type} if content_type else {})
    _problem(client.post(INBOX, headers=headers, content=json.dumps(submitted())), 415, "unsupported-media-type")


@pytest.mark.parametrize("overrides,drop,hint", [
    ({}, "time", "missing"),
    ({"subject": APPLICATION}, None, "not allowed"),                       # no other attributes (FRAMEWORK 6)
    ({"specversion": "0.3"}, None, "specversion"),
    ({"id": "1"}, None, "UUID"),
    ({"source": "urn:portal"}, None, "source"),
    ({"type": "org.example.application.submitted"}, None, "PascalCase"),
    ({"time": "2026-11-06T09:30:00"}, None, "time zone"),
    ({"datacontenttype": "text/plain"}, None, "datacontenttype"),
    ({"data": [1, 2]}, None, "JSON object"),
    ({"data": {"applicationId": APPLICATION, "clientSecret": "s"}}, None, "secrets"),   # FRAMEWORK 4.6
])
def test_events_that_do_not_meet_framework_6_are_refused(client, overrides, drop, hint):
    ev = submitted(**overrides)
    if drop:
        ev.pop(drop)
    p = _problem(client.post(INBOX, headers=svc("c1-m2") | STRUCTURED, content=json.dumps(ev)), 400, "validation")
    assert hint in p["detail"]
    assert events.RELAY.log == []


def test_body_that_is_not_json_or_a_ce_datacontenttype_header_is_refused(client):
    _problem(client.post(INBOX, headers=svc("c1-m2") | STRUCTURED, content=b"{not json"), 400, "validation")
    ev = submitted()
    headers = {f"ce-{a}": ev[a] for a in ("specversion", "id", "source", "type", "time")}
    headers |= {"ce-datacontenttype": "application/json", "Content-Type": "application/json"}
    _problem(client.post(INBOX, headers=svc("c1-m2") | headers, content=json.dumps(ev["data"])), 400, "validation")


def test_the_inbox_is_in_the_openapi_document_with_both_content_modes(client):
    doc = client.get("/openapi.json").json()
    op = doc["paths"][INBOX]["post"]
    assert set(op["requestBody"]["content"]) == {"application/cloudevents+json", "application/json"}
    assert op["tags"] == ["Event Inbox"] and "Event Inbox" in {t["name"] for t in doc["tags"]}


# ---------------------------------------------------------------- security review (6 Nov 2026)
def _client_token(client_id: str, **client) -> str:
    from tools import test_iam
    iam = test_iam.iam()
    iam.clients.setdefault(client_id, {"secret": "test-only", "permissions": set(), **client})
    return iam.client_token(client_id)


def test_a_module_cannot_publish_the_events_of_another_module(client):
    """Consumers match on `type` alone: svc-c1-m2 must not approve its own application (C1-M3's event)."""
    approved = submitted(type="ApplicationApproved", data={"applicationId": APPLICATION, "companyId": COMPANY,
                                                          "kind": "ONBOARDING", "existingCompany": False})
    p = _problem(client.post(INBOX, headers=svc("c1-m2") | STRUCTURED, content=json.dumps(approved)), 403, "forbidden")
    assert "ApplicationApproved is not an event of c1-m2" in p["detail"]
    unknown = submitted(type="SomethingInvented")
    _problem(client.post(INBOX, headers=svc("c1-m2") | STRUCTURED, content=json.dumps(unknown)), 403, "forbidden")
    assert events.RELAY.log == []


@pytest.mark.parametrize("client_id", ["svc-test-internal", "svc-c99-m1", "svc-c1-m2-evil", "portal-ui"])
def test_other_service_accounts_are_forbidden_not_an_error(client, client_id):
    r = client.post(INBOX, headers=bearer(_client_token(client_id)) | STRUCTURED, content=json.dumps(submitted()))
    _problem(r, 403, "forbidden")   # no 500 for an account without a module of the spec


def test_technical_user_tokens_are_refused(client):
    tok = _client_token("svc-c1-m2-tu", technicalRoles={"x"}, companyId=COMPANY, bpn=None)   # aud is not portal-core
    _problem(client.post(INBOX, headers=bearer(tok) | STRUCTURED, content=json.dumps(submitted())), 401, "unauthorized")


def test_secrets_are_refused_also_in_nested_data(client):
    ev = submitted(data={"applicationId": APPLICATION, "access": [{"clientSecret": "s"}]})
    p = _problem(client.post(INBOX, headers=svc("c1-m2") | STRUCTURED, content=json.dumps(ev)), 400, "validation")
    assert "access[0].clientSecret" in p["detail"]


def test_bodies_larger_than_the_limit_are_refused(client, monkeypatch):
    monkeypatch.setenv("EVENT_INBOX_MAX_BYTES", "2048")
    big = submitted(data={"applicationId": APPLICATION, "note": "x" * 4096})
    _problem(client.post(INBOX, headers=svc("c1-m2") | STRUCTURED, content=json.dumps(big)), 413, "payload-too-large")

    def chunks():   # without Content-Length (chunked)
        yield json.dumps(big).encode()
    _problem(client.post(INBOX, headers=svc("c1-m2") | STRUCTURED, content=chunks()), 413, "payload-too-large")
    assert events.RELAY.log == []


def test_non_ascii_digits_in_source_are_refused(client):
    ev = submitted(source="urn:c١-m٢")   # Arabic-Indic digits match \d, not [0-9]
    _problem(client.post(INBOX, headers=svc("c1-m2") | STRUCTURED, content=json.dumps(ev)), 400, "validation")
