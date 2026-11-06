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
"""Test keys as JWK (generated per run; test installation only, never for operation)."""
from __future__ import annotations

import base64
import json
from pathlib import Path

import jwt
from cryptography.hazmat.primitives.asymmetric import ec, rsa


def _b64(i: int, length: int | None = None) -> str:
    length = length or (i.bit_length() + 7) // 8
    return base64.urlsafe_b64encode(i.to_bytes(length, "big")).rstrip(b"=").decode()


def ec_jwk(kid: str) -> tuple[dict, dict]:
    """New EC P-256 key (ES256) as (private JWK, public JWK)."""
    k = ec.generate_private_key(ec.SECP256R1())
    n = k.private_numbers()
    pub = {"kty": "EC", "crv": "P-256", "kid": kid, "alg": "ES256", "use": "sig",
           "x": _b64(n.public_numbers.x, 32), "y": _b64(n.public_numbers.y, 32)}
    return {**pub, "d": _b64(n.private_value, 32)}, pub


def rsa_key(kid: str) -> tuple[object, dict]:
    """New RSA key (RS256) as (private key object, public JWK)."""
    k = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pub = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(k.public_key()))
    return k, {**pub, "kid": kid, "alg": "RS256", "use": "sig"}


def load_or_create_ec(path: Path, kid: str) -> tuple[dict, dict]:
    """Private EC JWK from `path`; created with its public part `<name>.pub.json` if missing."""
    pub_path = path.with_name(path.stem + ".pub.json")
    if path.exists() and pub_path.exists():
        return json.loads(path.read_text()), json.loads(pub_path.read_text())
    priv, pub = ec_jwk(kid)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(priv))
    pub_path.write_text(json.dumps(pub))
    return priv, pub


def private_key(jwk: dict):
    return jwt.PyJWK(jwk).key
