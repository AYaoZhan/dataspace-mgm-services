# Changelog

All notable changes to this project will be documented in this file.
See also the overarching [Eclipse Tractus-X changelog](https://eclipse-tractusx.github.io/changelog) for the Tractus-X releases.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Repository set-up according to the [Tractus-X Release Guidelines](https://eclipse-tractusx.github.io/docs/release): legal documentation, `.tractusx` metadata file, contribution templates, Dependabot and security scans (CodeQL, KICS, Trivy, TruffleHog), container build and documentation structure ([dataspace-mgm-ui#1](https://github.com/eclipse-tractusx/dataspace-mgm-ui/issues/1))
- Eclipse Dash IP check aligned with tractusx-testlab: `dependencies.yml` only checks, the new `dependencies-update.yml` regenerates `DEPENDENCIES` daily, requests IP reviews (secret `DASH_GITLAB_API_TOKEN`) and opens a pull request.
- Hackathon scaffold: all modules of the spec mounted as stand-ins, Process Orchestration (C12-M1), test Portal IAM (Keycloak), EBW stack for tests with a real wallet, `demo.py` and the setup check `check.py`.
- Event inbox `POST /api/v1/events/inbox` (FRAMEWORK 6, OP-54): receives the CloudEvents of split-out modules in structured or binary content mode, with the token of the service account of the publishing module, and delivers each `source` and `id` once. First controller of the new `controllers/` package: one folder per API category and version, as in the Industry Core Hub backend.
- Feature-first layout and runtimes made of features ([ADR-0003](docs/architecture/decisions/ADR-0003-feature-first-layout-and-runtimes.md)): the onboarding modules C1-M2 and C3-M1 and the technical users C2-M3 move from `modules/` to `features/registration/`, `features/company_profile/` and `features/technical_user/` (`controllers/` with one folder per API path segment, `services/`, `managers/`, `models/`, `router.py`, `main.py`, index), without changing their API; `runtimes/` builds hybrid (`onboarding`) or single-feature runtimes, selected in the image with `RUNTIME`; `MODULE_URLS` accepts readable feature names.
- C4-M1 Credentials moves from `modules/c4_m1/` to `features/credentials/` (ADR-0003): controllers per API path segment, the rules and the issuer route choice with the built-in stand-in issuer in `services/`, the credential store and the issuer clients in `managers/`; pydantic models of the API in `models/credentials.py` and the tables of README 5 as SQLModel tables in the feature's own database (`CREDENTIALS_DATABASE_URL`, `C4_M1_DATABASE_URL`, `DATABASE_URL`, else in-memory SQLite).
- C3-M2 CSP Connection moves from `modules/c3_m2/` to `features/csp_connection/` in the same layout (ADR-0003), with its own pydantic models on `portal_common.models`, a README, and its tables as SQLModel classes in its own database (`portal_common.database`) instead of in-memory dicts.
- C11-M1 Notifications moves from `modules/c11_m1/` to `features/notifications/` (ADR-0003): the inbox operations in `controllers/notifications/`, rules, event engine, closing, recipients and inbox logic in `services/`, the store, the background worker with its retry policy, the neighbour client and the stand-in data of C2-M2 in `managers/`, the rule type, the pydantic models of the API and the SQLModel tables of README 5 in `models/`; the inbox is stored in the feature's own database (`NOTIFICATIONS_DATABASE_URL`, in-memory SQLite without one).
- The connectors C6-M1 move from `modules/c6_m1/` to `features/connector/` in the feature-first layout of ADR-0003 (`controllers/` per API path segment, `services/`, `managers/` with the repository, the neighbour client and the stand-in data in `managers/data/`, `models/` with pydantic models and SQLModel tables in its own database).
- Folder rules of a feature in `features/AGENTS.md` (F1 to F14) and the skill `feature-architecture` (`feature-check.py`), which checks them statically; `tests/test_feature_architecture.py` runs it on every feature. The company profile's `config.py` and stand-in data move to `managers/`, the Problem factories of the technical users to `models/errors.py`.
- Shared pydantic bases for the models of every feature in `portal_common.models` (`ApiModel`, `RequestBody`, `StepRequest`, `StepResult`, `Page`, `Uuid`, `Bpnl`, `CountryCode`); `portal_common.database`, one SQLAlchemy/SQLModel database per feature (`<FEATURE>_DATABASE_URL`, then `<SPEC_ID>_DATABASE_URL`, then `DATABASE_URL`, else in-memory SQLite; new dependency `sqlmodel`); the feature rules F15 (a `README.md` that names the migrated module and explains the feature), F16 (own pydantic models in `models/`) and F17 (SQLModel tables in `models/tables.py`) in `features/AGENTS.md` and `feature-check.py`.
- One runtime per module ([ADR-0002](docs/architecture/decisions/ADR-0002-runtime-per-module.md)): `ENABLED_FEATURES` starts the same image with only some modules, `EVENT_SINKS` forwards published events to the other runtimes' event inbox (retries, off the request path), the Helm chart renders one Deployment and Service per runtime (`runtimes`), and `docker-compose.poc.yml` runs the registration and the company profile as two pods (`deploy/poc/poc_check.py`).

### Changed

- **Breaking:** the migrated features are served under readable paths instead of their spec ids: `/api/registration`
  (was `/api/c1-m2`), `/api/company-profile` (was `/api/c3-m1`) and `/api/technical-user` (was `/api/c2-m3`); the old
  paths answer 404. Problem types, event
  sources, permissions and service accounts keep the spec id. Concept for one database per feature in a shared
  PostgreSQL instance ([ADR-0003](docs/architecture/decisions/ADR-0003-feature-first-layout-and-runtimes.md)).
- **Breaking:** C4-M1 Credentials is served under `/api/credentials` (was `/api/c4-m1`); the old path answers 404, and the callback address given to the issuers is `/api/credentials/issuer-callbacks/{credentialKind}`. Problem types, event sources, permissions and `svc-c4-m1` keep the spec id.
- **Breaking:** C8-M1 Offers moves from `modules/c8_m1/` to `features/offers/` (ADR-0003) and is served under `/api/offers` (was `/api/c8-m1`); the old path answers 404. Problem types, event sources, permissions and `svc-c8-m1` keep the spec id.
- **Breaking:** C3-M2 CSP Connection is served under `/api/csp-connection` (was `/api/c3-m2`); the old path answers
  404, and the CSP stand-in calls back `/api/csp-connection/csp-notifications`. Problem types, events, permissions
  and `svc-c3-m2` keep the spec id.
- **Breaking:** C11-M1 Notifications is served under `/api/notifications` (was `/api/c11-m1`); the old path answers
  404. Problem types, events, permissions and `svc-c11-m1` keep the spec id.
- **Breaking:** the connectors C6-M1 are served under `/api/connector` (was `/api/c6-m1`); the old path answers 404.
  Problem types, events, permissions and `svc-c6-m1` keep the spec id.
- Outgoing HTTP calls of `portal_common.http` use one pooled client (keep-alive).
- The company profile keeps its state in SQLModel tables on `portal_common.database` instead of the memory and the hand-written PostgreSQL transport: it also reads `COMPANY_PROFILE_DATABASE_URL` (before `C3_M1_DATABASE_URL` and `DATABASE_URL`), uses the `pg8000` driver instead of `psycopg`, and no longer answers `501 not-implemented` for a missing driver. Its responses are pydantic models; list endpoints refuse `page < 0` and `size` outside 1 to 100 with 400.

- Events are CloudEvents 1.0 (`specversion`, `id`, `source` `urn:<module>`, `type`, `time`, `datacontenttype`, `data`) as proposed in the spec (FRAMEWORK 6, OP-54): `events.publish(module, type, data)`; the flat form `events.publish({"eventType": ...})` is deprecated; consumers read the content from `event["data"]`.

### Fixed

- Align the Docker build and runtime images with the project's required Python 3.12 version.
- Every module of an installation reads its own database variable (`C2_M2_DATABASE_URL`, `C3_M1_DATABASE_URL`); `DATABASE_URL` stays the fallback for a module that runs alone. Before, one `DATABASE_URL` switched C2-M2 and C3-M1 to the same database ([#54](https://github.com/eclipse-tractusx/dataspace-mgm-services/issues/54)).

[Unreleased]: https://github.com/eclipse-tractusx/dataspace-mgm-service/commits/main
