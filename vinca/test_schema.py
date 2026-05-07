"""Tests for the Greenroom pixi.toml JSON schema.

Validates the local `[tool.ros]` extension. The upstream pixi schema is
not fetched here — those checks are the job of the editor / LSP.
"""

from __future__ import annotations

import json
import tomllib
from pathlib import Path

import jsonschema

SCHEMA_PATH = (
    Path(__file__).parent / "schemas" / "greenroom_pixi_manifest.schema.json"
)
FIXTURES = Path(__file__).parent / "test_fixtures" / "pixi_manifests"


def _validator() -> jsonschema.Draft202012Validator:
    schema = json.loads(SCHEMA_PATH.read_text())
    return jsonschema.Draft202012Validator(schema)


def test_valid_fixture_has_no_errors() -> None:
    v = _validator()
    with (FIXTURES / "with_deps" / "pixi.toml").open("rb") as f:
        data = tomllib.load(f)
    assert list(v.iter_errors(data)) == []


def test_missing_build_type_fails_validation() -> None:
    v = _validator()
    errors = list(v.iter_errors({"tool": {"ros": {}}}))
    assert any("build_type" in e.message for e in errors)


def test_unknown_build_type_fails_validation() -> None:
    v = _validator()
    errors = list(v.iter_errors({"tool": {"ros": {"build_type": "cmake"}}}))
    assert any("ament_cmake" in e.message for e in errors)


def test_unknown_ros_metadata_key_fails_validation() -> None:
    v = _validator()
    errors = list(
        v.iter_errors(
            {"tool": {"ros": {"build_type": "ament_python", "typo": True}}}
        )
    )
    assert any("typo" in e.message for e in errors)


def test_missing_tool_ros_fails_validation() -> None:
    v = _validator()
    errors = list(v.iter_errors({"package": {"name": "x", "version": "0.0.1"}}))
    assert any("tool" in e.message or "ros" in e.message for e in errors)
