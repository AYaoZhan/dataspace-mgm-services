# Copyright (c) 2026 Contributors to the Eclipse Foundation
# SPDX-License-Identifier: Apache-2.0
"""Test tools: test issuer (PID provider and register), trust list of the core services, demo OSP."""

import json
import os
import time
from html import escape

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

from common.issuer import Issuer
from common.jose import sign_jws, signing_jwk, x5c
from common.statuslist import StatusList
from common.web import page, qr, read_form
from test_tools import config, osp
from test_tools.data import DEFINITIONS, TYPES, claims_with

# Status lists are read by the EBW-Connector only, so a local address survives a new tunnel address.
STATUS_BASE_URL = (os.environ.get("STATUS_BASE_URL") or config.PUBLIC_URL).rstrip("/")
REGISTRY = config.DATA_DIR / "issued.json"

status_list = StatusList(config.DATA_DIR / "status-list.json", f"{STATUS_BASE_URL}/status-lists/1")


def load_registry() -> list[dict]:
    return json.loads(REGISTRY.read_text()) if REGISTRY.exists() else []


def record(cid: str, claims: dict, status: dict | None, label: str) -> None:
    registry = load_registry()
    registry.append(
        {
            "index": status["status_list"]["idx"] if status else None,
            "type": TYPES[cid],
            "label": label,
            "issued_at": time.strftime("%Y-%m-%d %H:%M"),
        }
    )
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(registry, indent=1, ensure_ascii=False))


issuer = Issuer(
    config.PUBLIC_URL,
    config.ISSUER_KEY,
    {"kid": signing_jwk(config.ISSUER_KEY)["kid"], "x5c": x5c(config.ISSUER_CERT)},
    DEFINITIONS,
    "EBW test issuer",
    status_list,
    on_issued=record,
    validity=config.CREDENTIAL_VALIDITY_SECONDS,
)

app = FastAPI(title="EBW test tools")
app.include_router(issuer.router)
app.include_router(osp.router)

COPY = """<script>
function copyText(id) { navigator.clipboard.writeText(document.getElementById(id).textContent); }
</script>"""


@app.get("/", response_class=HTMLResponse)
def index():
    _, person_link = issuer.create_offer({"pid": claims_with("pid", None), "mandate": claims_with("mandate", None)}, "Erika Mustermann")
    _, company_link = issuer.create_offer({"lpid": claims_with("lpid", None)}, "Beispiel Maschinenbau GmbH")
    rows = "".join(
        f"<tr><td>{entry['index']}</td><td>{escape(entry['type'])}</td><td>{escape(entry['label'])}</td>"
        f"<td>{escape(entry['issued_at'])}</td><td>"
        + (
            ""
            if entry["index"] is None
            else f'<form method="post" action="/revoke/{entry["index"]}">'
            + (
                '<span class="fail">revoked</span> <button class="secondary">restore</button>'
                if status_list.is_revoked(entry["index"])
                else '<button class="danger">revoke</button>'
            )
            + "</form>"
        )
        + "</td></tr>"
        for entry in reversed(load_registry()[-30:])
    )
    body = (
        '<div class="box"><h2>EUDI Wallet of the person</h2>'
        "<p>Test PID and mandate from the register: Erika Mustermann, legal representative "
        "of Beispiel Maschinenbau GmbH. Scan with the wallet.</p>"
        + qr(person_link)
        + f'<p><a class="button" href="{escape(person_link)}">Open in wallet</a></p></div>'
        '<div class="box"><h2>Test PID for another person</h2>'
        "<p>For example for an employee who gets a power of attorney from the Business Wallet. "
        "Name and date of birth must match the power of attorney.</p>"
        '<form method="post" action="/pid">'
        '<label for="given_name">Given name</label><input id="given_name" name="given_name" required>'
        '<label for="family_name">Family name</label><input id="family_name" name="family_name" required>'
        '<label for="birthdate">Date of birth</label><input id="birthdate" name="birthdate" type="date" required>'
        "<button>Offer test PID</button></form></div>"
        '<div class="box"><h2>Business Wallet</h2>'
        "<p>LPID of Beispiel Maschinenbau GmbH. Paste the link in the Business Wallet under "
        "“Fetch the company credential (LPID)”.</p>"
        f'<pre id="lpid-link">{escape(company_link)}</pre>'
        "<p><button class=\"secondary\" onclick=\"copyText('lpid-link')\">Copy link</button></p></div>"
        '<div class="box"><h2>Core services</h2><p>Signed trust list: '
        '<a href="/trust-list.json">view</a> · <a href="/trust-list">as JWS</a></p></div>'
        '<div class="box"><h2>OSP 2.0 demo portal</h2><p>Sign-in and onboarding through the EBW-Connector: '
        '<a href="/osp">Open the portal</a></p></div>'
        '<div class="box"><h2>Issued credentials</h2>'
        f"<table><tr><th>No.</th><th>Type</th><th>For</th><th>Time</th><th>Status</th></tr>{rows}</table></div>"
        f'<p class="muted">The offers are valid for 10 minutes; reloading creates new ones.</p>{COPY}'
    )
    return HTMLResponse(page("Test tools", body, brand="EBW test tools"))


@app.post("/pid", response_class=HTMLResponse)
async def pid_offer(request: Request):
    form = await read_form(request)
    person = {k: form.get(k, "").strip() for k in ("given_name", "family_name", "birthdate")}
    if not all(person.values()):
        return RedirectResponse("/", status_code=303)
    _, link = issuer.create_offer({"pid": claims_with("pid", person)}, f"{person['given_name']} {person['family_name']}")
    body = (
        f"<p>Test PID for <b>{escape(person['given_name'])} {escape(person['family_name'])}</b>, "
        f"born {escape(person['birthdate'])}. Scan with the EUDI Wallet of this person.</p>"
        + qr(link)
        + f'<p><a class="button" href="{escape(link)}">Open in wallet</a> <a class="button secondary" href="/">Back</a></p>'
    )
    return HTMLResponse(page("Test PID", body, brand="EBW test tools"))


@app.post("/revoke/{index}")
def revoke(index: int):
    status_list.set_revoked(index, not status_list.is_revoked(index))
    return RedirectResponse("/", status_code=303)


@app.post("/api/offers")
async def api_offer(request: Request):
    """For automated tests: offer with test variants, e.g. {"credentials": {"pid": {}, "mandate": {"role": "x"}}}."""
    body = await request.json()
    wanted = body.get("credentials") or {"pid": {}, "mandate": {}}
    claims = {cid: claims_with(cid, overrides) for cid, overrides in wanted.items() if cid in DEFINITIONS}
    offer_id, link = issuer.create_offer(claims, body.get("label", "API"))
    return {"offer_id": offer_id, "link": link}


@app.post("/api/revoke/{index}")
def api_revoke(index: int):
    status_list.set_revoked(index, True)
    return {"revoked": index}


def trust_list_payload() -> dict:
    now = int(time.time())
    return {
        "iss": config.PUBLIC_URL,
        "iat": now,
        "exp": now + 24 * 3600,
        "entries": [
            {
                "name": "ebw-test-issuer",
                "credential_types": ["PID", "LPID", "MANDATE"],
                "jwks": {"keys": [signing_jwk(config.ISSUER_KEY)]},
            }
        ],
    }


@app.get("/trust-list")
def trust_list():
    header = {"typ": "trust-list+jwt", "kid": signing_jwk(config.TRUST_LIST_KEY)["kid"]}
    return Response(sign_jws(header, trust_list_payload(), config.TRUST_LIST_KEY), media_type="application/jwt")


@app.get("/trust-list.json")
def trust_list_json():
    return JSONResponse(trust_list_payload())


@app.get("/trust-list/signer-jwks")
def trust_list_signer():
    return {"keys": [signing_jwk(config.TRUST_LIST_KEY)]}
