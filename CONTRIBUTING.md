# Contributing to Eclipse Tractus-X

Thanks for your interest in this project.

## Project description

The companies involved want to increase the automotive industry's
competitiveness, improve efficiency through industry-specific cooperation and
accelerate company processes through standardization and access to information
and data. A special focus is also on SMEs, whose active participation is of
central importance for the network's success. That is why Catena-X has been
conceived from the outset as an open network with solutions ready for SMEs,
where these companies will be able to participate quickly and with little IT
infrastructure investment. Tractus-X is meant to be the PoC project of the
Catena-X alliance focusing on parts traceability.

* https://projects.eclipse.org/projects/automotive.tractusx

## Project licenses

The Tractus-X project uses the following licenses:

* Apache-2.0 for code
* CC-BY-4.0 for non-code

## Terms of Use

This repository is subject to the Terms of Use of the Eclipse Foundation

* https://www.eclipse.org/legal/termsofuse.php

## Developer resources

Information regarding source code management, builds, coding standards, and
more.

* https://projects.eclipse.org/projects/automotive.tractusx/developer

Getting started:

* https://eclipse-tractusx.github.io/docs/developer

The project maintains the following source code repositories

* https://github.com/eclipse-tractusx/dataspace-mgm-service
* https://github.com/eclipse-tractusx/dataspace-mgm-ui

## How to contribute to the Dataspace Management

1. Sign the [Eclipse Contributor Agreement](#eclipse-contributor-agreement) with the email address you use for your commits.
2. Open an issue, or comment on an existing one, before you start bigger changes, so that the committers can give early feedback.
3. Fork the repository, create a branch from `main` and open a pull request against `main`.
4. Use [conventional commits](https://www.conventionalcommits.org) for the PR title (`feat:`, `fix:`, `docs:`, `chore:` ...): the titles are used for the release notes.
5. Add the copyright and license header ([License headers](#license-headers), TRG 7.02) to every new file, and keep the documentation and the `CHANGELOG.md` up to date.
6. New third-party dependencies must be approved by the [Eclipse Dash License Tool](https://github.com/eclipse-dash/dash-licenses); the `DEPENDENCIES` file is checked on every pull request.
7. Pull requests with more than 1000 lines of relevant code need an approved [IP review](https://eclipse-tractusx.github.io/docs/release/trg-7/trg-7-03) before they can be merged.

At least one committer has to approve a pull request before it is merged.

## License headers

Every new file starts with the copyright and license header of
[TRG 7.02](https://eclipse-tractusx.github.io/docs/release/trg-7/trg-7-02). Code with `#` comments (Python, shell, YAML, TOML, Dockerfile):

```text
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
```

- **Written with AI help:** keep the paragraph "AI Disclosure", the license `Apache-2.0 AND CC0-1.0` and the
  line `Assisted-By: <tool> (<model>)`, for example `Assisted-By: Claude Code (claude-opus-5-5)`.
- **Written without AI help:** leave out the paragraph "AI Disclosure" and the line `Assisted-By`, and write
  `SPDX-License-Identifier: Apache-2.0`.
- Other comment styles carry the same text: Helm templates inside `{{/* ... */}}`, Markdown inside
  `<!-- ... -->`.
- Documentation (`docs/`) keeps its NOTICE section at the end (`CC-BY-4.0`).

## Eclipse Development Process

This Eclipse Foundation open project is governed by the Eclipse Foundation
Development Process and operates under the terms of the Eclipse IP Policy.

* https://eclipse.org/projects/dev_process
* https://www.eclipse.org/org/documents/Eclipse_IP_Policy.pdf

## Eclipse Contributor Agreement

In order to be able to contribute to Eclipse Foundation projects you must
electronically sign the Eclipse Contributor Agreement (ECA).

* http://www.eclipse.org/legal/ECA.php

The ECA provides the Eclipse Foundation with a permanent record that you agree
that each of your contributions will comply with the commitments documented in
the Developer Certificate of Origin (DCO). Having an ECA on file associated with
the email address matching the "Author" field of your contribution's Git commits
fulfills the DCO's requirement that you sign-off on your contributions.

For more information, please see the Eclipse Committer Handbook:
https://www.eclipse.org/projects/handbook/#resources-commit

## Contact

Contact the project developers via the project's "dev" list.

* https://accounts.eclipse.org/mailing-list/tractusx-dev
