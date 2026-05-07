"""Tests for the Greenroom pixi.toml JSON schema.

Validates only the local `[package.metadata.ros]` extension. The upstream
pixi schema referenced via `allOf` is not fetched here — those checks are
the job of the editor / LSP.
"""

from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import Any

import jsonschema

SCHEMA_PATH = (
    Path(__file__).parent / "schemas" / "greenroom_pixi_manifest.schema.json"
)
FIXTURES = Path(__file__).parent / "test_fixtures" / "pixi_manifests"


def _local_validator() -> jsonschema.Draft202012Validator:
    """Build a validator for the local extension only (no remote $refs)."""
    schema = json.loads(SCHEMA_PATH.read_text())
    local: dict[str, Any] = {
        "allOf": [{"$ref": "#/$defs/RosExtension"}],
        "$defs": schema["$defs"],
    }
    return jsonschema.Draft202012Validator(local)


def test_valid_fixture_has_no_errors() -> None:
    v = _local_validator()
    with (FIXTURES / "with_deps" / "pixi.toml").open("rb") as f:
        data = tomllib.load(f)
    assert list(v.iter_errors(data)) == []


def test_missing_build_type_fails_validation() -> None:
    v = _local_validator()
    errors = list(v.iter_errors({"package": {"metadata": {"ros": {}}}}))
    assert any("build_type" in e.message for e in errors)


def test_unknown_build_type_fails_validation() -> None:
    v = _local_validator()
    errors = list(
        v.iter_errors({"package": {"metadata": {"ros": {"build_type": "cmake"}}}})
    )
    assert any("ament_cmake" in e.message for e in errors)


def test_unknown_ros_metadata_key_fails_validation() -> None:
    v = _local_validator()
    errors = list(
        v.iter_errors(
            {
                "package": {
                    "metadata": {
                        "ros": {"build_type": "ament_python", "typo": True}
                    }
                }
            }
        )
    )
    assert any("typo" in e.message for e in errors)
