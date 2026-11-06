# Copyright (c) 2026 Contributors to the Eclipse Foundation
# SPDX-License-Identifier: Apache-2.0
"""Events of scenarios 1-3 against the spec: every event is a CloudEvent of FRAMEWORK 6 (OP-54),
its `source` is the module that owns its `type` (FRAMEWORK 6 catalogue, `Event*` schemas of the
module `openapi.yaml`) and its `data` carries the required fields of the event schema.

Works with both forms of the event schemas: new (`properties.type.const`, the content in `data`)
and old (`properties.eventType.const`, the content beside `eventId`, `eventType`, `occurredAt`)."""
import datetime as dt
import re
import uuid

from conftest import needs_admin_api
from portal_common import events, spec
from scaffold import registry
from test_demo_scenarios import installation

OLD_ENVELOPE = ("eventId", "eventType", "occurredAt")   # flat events before FRAMEWORK 6 / OP-54

# Required fields that the stand-ins do not publish yet (README section 10). Allowed only while
# the module is a stand-in; a team's module publishes every required field.
STANDIN_GAPS = {
    ("AppClientTemplateCreated", "iamClientId"), ("AppClientTemplateCreated", "roleNames"),
    ("AppInstanceClientCreated", "instanceKind"), ("AppInstanceClientCreated", "iamClientId"),
    ("AppInstanceClientCreated", "instanceUrl"), ("AppInstanceClientEnabled", "iamClientId"),
    ("AppInstanceClientDisabled", "iamClientId"),
    ("TechnicalUserCreated", "origin"), ("TechnicalUserCreated", "iamClientId"),
    ("DataspaceWalletCreated", "walletId"), ("DataspaceWalletCreated", "provider"),
    ("DataspaceWalletCreated", "didDocumentLocation"), ("DataspaceWalletCreated", "bpn"),
}


def catalogue() -> dict[str, set[str]]:
    """Event name -> modules that publish it: module column of the FRAMEWORK 6 table, module of
    the `openapi.yaml` that holds the event schema."""
    text = (spec.spec_dir() / "FRAMEWORK.md").read_text(encoding="utf-8")
    sec = re.search(r"^## 6\. Event catalogue\n(.*?)(?=^## )", text, re.S | re.M)
    assert sec, "FRAMEWORK.md has no section '6. Event catalogue'"
    out: dict[str, set[str]] = {}
    for mid, names in re.findall(r"^\| (C\d+-M\d+) \| ([^|]+)\|", sec.group(1), re.M):
        for name in re.findall(r"`([A-Z][A-Za-z0-9]+)`", names):
            out.setdefault(name, set()).add(mid.lower())
    for mid, ms in spec.modules().items():
        for name in event_schemas(ms):
            out.setdefault(name, set()).add(mid)
    return out


def event_schemas(ms: spec.ModuleSpec) -> dict[str, dict]:
    """Event name -> {"required": required fields of the content, "const": fixed CloudEvent
    attributes (new form only)} of the `Event*` schemas of one module."""
    out = {}
    for name, sch in (ms.document.get("components", {}).get("schemas") or {}).items():
        if not name.startswith("Event"):
            continue
        r = ms.resolve(sch)
        props = r.get("properties", {})
        new, old = (props.get("type") or {}).get("const"), (props.get("eventType") or {}).get("const")
        if new and "data" in props:
            out[new] = {"required": ms.resolve(props["data"]).get("required", []),
                        "const": {k: v["const"] for k, v in props.items()
                                  if k != "data" and isinstance(v, dict) and "const" in v}}
        elif old:
            out[old] = {"required": [f for f in r.get("required", []) if f not in OLD_ENVELOPE], "const": {}}
    return out


def scenario_events(tmp_path, monkeypatch) -> list[dict]:
    """Every event that scenarios 1-3 of demo.py published (`RELAY.log`), after the relay is idle."""
    with installation(tmp_path, monkeypatch):
        assert events.RELAY.wait_idle(10)
        log = list(events.RELAY.log)
    assert {"ApplicationSubmitted", "CompanyCreated", "ProcessStarted"} <= {ev.get("type") for ev in log}
    return log


def _utc(value) -> bool:
    try:
        return dt.datetime.fromisoformat(value).utcoffset() == dt.timedelta(0)
    except (TypeError, ValueError):
        return False


def _uuid(value) -> bool:
    try:
        return str(uuid.UUID(value)) == value
    except (TypeError, ValueError, AttributeError):
        return False


@needs_admin_api
def test_every_event_is_a_cloudevent_of_its_owner(tmp_path, monkeypatch):
    log = scenario_events(tmp_path, monkeypatch)
    owners = catalogue()
    wrong = []
    for ev in log:
        etype = ev.get("type")
        if set(ev) != set(events.ATTRIBUTES):
            wrong.append((etype, "attributes", sorted(set(ev) ^ set(events.ATTRIBUTES))))
            continue
        if ev["specversion"] != events.SPECVERSION or ev["datacontenttype"] != events.DATACONTENTTYPE:
            wrong.append((etype, "specversion/datacontenttype", ev["specversion"], ev["datacontenttype"]))
        if not _uuid(ev["id"]) or not _utc(ev["time"]) or not isinstance(ev["data"], dict):
            wrong.append((etype, "id/time/data", ev["id"], ev["time"], type(ev["data"]).__name__))
        if etype not in owners:
            wrong.append((etype, "not an event of the spec (FRAMEWORK 6, Event schemas)"))
        elif len(owners[etype]) != 1:
            wrong.append((etype, "the spec names more than one module", sorted(owners[etype])))
        elif ev["source"] != events.source_of(next(iter(owners[etype]))):
            wrong.append((etype, "source", ev["source"], sorted(owners[etype])))
    assert not wrong, wrong
    ids = [ev["id"] for ev in log]
    assert len(set(ids)) == len(ids), "event ids are not unique"


@needs_admin_api
def test_data_has_the_required_fields_of_the_event_schema(tmp_path, monkeypatch):
    log = scenario_events(tmp_path, monkeypatch)
    schemas = {name: s for ms in spec.modules().values() for name, s in event_schemas(ms).items()}
    standins = {events.source_of(e.id) for e in registry.load() if e.kind == "stand-in"}
    wrong, missing = [], set()
    for ev in log:
        sch = schemas.get(ev.get("type"))
        if not sch:
            continue   # no event schema in openapi.yaml (e.g. C12-M1): FRAMEWORK 6 only
        wrong += [(ev["type"], k, ev.get(k), v) for k, v in sch["const"].items() if ev.get(k) != v]
        allowed = STANDIN_GAPS if ev.get("source") in standins else set()
        missing |= {(ev["type"], ev.get("source"), f) for f in sch["required"]
                    if f not in ev.get("data", {}) and (ev["type"], f) not in allowed}
    assert not wrong, wrong
    assert not missing, sorted(missing)
