# ADR-0001: Events as CloudEvents 1.0, and an event inbox for split-out modules

**Status:** proposed (6 Nov 2026), pending the spec proposal OP-54
([portal-backend-spec#1](https://github.com/tx-arena-events/portal-backend-spec/pull/1)).
**Implemented in:** [#15](https://github.com/eclipse-tractusx/dataspace-mgm-services/pull/15).

## Context

Modules publish events through an outbox and an event bus; Process Orchestration (C12-M1) starts and continues flows
on them, Notifications (C11-M1) informs people. The spec (FRAMEWORK 6) described an event as a flat JSON object:
`eventId`, `eventType` and `occurredAt` next to the business fields. C12-M1 0.2 had dropped the earlier envelope of
`common.yaml`. Nothing defined how an event travels when a module is split out of the monolith (FRAMEWORK 4.7), and
the flat form mixes envelope and content, so a business field could collide with an envelope field.

## Decision

1. Every event is a [CloudEvent 1.0](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md) in the
   JSON event format: `specversion` `1.0`, `id` (UUID), `source` `urn:<module>` (e.g. `urn:c1-m2`), `type` (the name
   from the catalogue, e.g. `ApplicationSubmitted`), `time`, `datacontenttype` `application/json`, and the content
   of the catalogue in `data`. No extensions; `subject` and `dataschema` are not used.
2. Field names in flows (`trigger.when`, `subject.key`, `correlateBy`, process variables, `completesOn`) and in the
   rules of Notifications refer to fields of `data`. `flows.yaml` does not change.
3. Consumers detect a repeated delivery by `id`.
4. In the process the bus delivers the JSON object. Between processes the CloudEvents HTTP binding applies. An
   installation receives events of split-out modules at `POST /api/v1/events/inbox`, in structured
   (`application/cloudevents+json`) or binary (`ce-` headers) content mode.
5. The inbox accepts an event only from the service account of the module that owns it: the token (`svc-<module>`)
   must match `source`, and `type` must be an event of that module in the spec. Consumers match on `type` alone, so
   without the second check one module could, for example, publish the approval of an application in the name of
   C1-M3. Bodies are limited (`EVENT_INBOX_MAX_BYTES`, 64 KiB), secret-like keys are refused at any depth, the same
   `source` and `id` is delivered once.
6. Server-Sent Events stream messages for the UI (`process-changed`, `notification-*`) are not bus events and stay
   as they are.

## Alternatives

| Option | Why not |
|---|---|
| Keep the flat object | No standard for transport, tooling or brokers; envelope and content mixed. |
| Own envelope (`common.yaml` of 0.1) | Already dropped once; a home-made format with no tooling. |
| `type` with a reverse-DNS prefix (`org.eclipse.tractusx…`) | Events stay in the installation and the module is in `source`; open in OP-54 for when events leave it. |
| Path `/api/v1/event-bus/cloudevents` | Names the format instead of the resource; the inbox pairs with the outbox of FRAMEWORK 1. |

## Consequences

- `events.publish(MODULE, "<Type>", {data})`; subscribers read `event["type"]`, `event["id"]`, `event["data"]`.
  The flat form `events.publish({"eventType": ...})` still works for the hackathon team forks (deprecated, with a
  warning), consumers in those forks must change.
- C12-M1 reads the event names from both the new (`type`) and the old (`eventType`) schemas, so the service runs
  with the spec before and after OP-54.
- Brokers and tools that speak CloudEvents (e.g. Knative, Kafka bindings) can carry the events later without a
  change of format. Which broker is used stays open (C12-M1 open question 4).

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2026 Contributors to the Eclipse Foundation
- Source URL: https://github.com/eclipse-tractusx/dataspace-mgm-services/blob/main/docs/architecture/decisions/ADR-0001-events-as-cloudevents.md
