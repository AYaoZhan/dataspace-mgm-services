# Copyright (c) 2026 Contributors to the Eclipse Foundation
# SPDX-License-Identifier: Apache-2.0
"""Keep the container interpreters aligned with the project's Python version."""
from pathlib import Path


def test_docker_stages_use_project_python():
    root = Path(__file__).resolve().parents[1]
    python_version = (root / ".python-version").read_text().strip()
    images = [
        line.split()[1]
        for line in (root / "Dockerfile").read_text().splitlines()
        if line.startswith("FROM ")
    ]
    assert images == [f"python:{python_version}-alpine"] * 2
