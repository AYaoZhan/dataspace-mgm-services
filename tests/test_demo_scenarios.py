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
"""Acceptance scenarios 1-3 of demo.py in one process: installation OSP A with the modules of the
repository (stand-ins or team modules) plus the shared CSP stand-in, without any workaround.
demo.py runs the same code against real processes."""
import contextlib
import json

from fastapi.testclient import TestClient

import demo
from conftest import BASE, needs_admin_api
from portal_common import csp as csp_client
from portal_common import http as phttp
from scaffold import app as scaffold_app
from tools.csp_standin.app import create_app as create_csp
from tools.keys import ec_jwk

CSP = "http://csp.test"


@contextlib.contextmanager
def installation(tmp_path, monkeypatch):
    """OSP A with the shared CSP stand-in in one process; yields after scenarios 1-3 ran."""
    priv, pub = ec_jwk("osp-a")
    (tmp_path / "key.json").write_text(json.dumps(priv))
    (tmp_path / "trust.json").write_text(json.dumps({demo.OSP_A_ID: {
        "name": "OSP A", "installationUrl": BASE, "jwk": pub,
        "iamTokenUrl": f"{BASE}/auth/realms/CX-Central/protocol/openid-connect/token"}}))
    for k, v in {"CSP_TRUST_FILE": tmp_path / "trust.json", "CSP_PUBLIC_URL": CSP, "CSP_URL": f"{CSP}/v1",
                 "CSP_TOKEN_URL": f"{CSP}/oauth/token", "CSP_JWKS_URL": f"{CSP}/.well-known/jwks.json",
                 "OSP_SIGNING_KEY_FILE": tmp_path / "key.json", "CSP_CALLBACK_DELAY_SECONDS": "0",
                 "RETRY_BASE_SECONDS": "0.2", "WORKER_POLL_SECONDS": "0.1"}.items():
        monkeypatch.setenv(k, str(v))
    csp_client.reset()
    phttp.register_local(CSP, create_csp())
    app = scaffold_app.create_app()
    with TestClient(app, base_url=BASE):
        t = demo.Target(osp_a=BASE, csp=CSP, quiet=True)
        t.ok = demo.run(t, ["1", "2", "3"])
        try:
            yield t
        finally:
            scaffold_app.reset_all(app.state.entries)   # no state (e.g. provider calls) for later tests


@needs_admin_api
def test_scenarios_1_to_3_with_stand_ins(tmp_path, monkeypatch):
    with installation(tmp_path, monkeypatch) as t:
        pass
    failed = [(s, label, d) for s, steps in t.results.items() for label, o, d in steps if not o]
    for f in failed:
        print("FAILED", f)
    assert t.ok and not failed, failed
    assert sum(len(v) for v in t.results.values()) >= 30
