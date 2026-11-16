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
#  The program is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#  CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.
#
#  AI Disclosure: This file was entirely AI-generated.
#  The AI-generated portions are made available under CC0-1.0 and not subject
#  to the project's license. The human contributor has reviewed and verified
#  that the code is correct.
#
#  SPDX-License-Identifier: Apache-2.0 AND CC0-1.0
#  Assisted-By: GitHub Copilot (Claude Sonnet 5.5)
#################################################################################
"""Run a named runtime with `python -m runtimes [name]`."""

import importlib
import os
import sys

from . import serve


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else os.getenv("RUNTIME", "installation")
    if len(sys.argv) > 2 or name not in {"installation", "onboarding"}:
        raise SystemExit("usage: python -m runtimes [installation|onboarding]")
    runtime = importlib.import_module(f"runtimes.{name}")
    serve(runtime.create_app)


if __name__ == "__main__":
    main()