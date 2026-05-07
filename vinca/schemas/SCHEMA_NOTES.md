# Greenroom pixi manifest schema — design notes

`greenroom_pixi_manifest.schema.json` extends pixi's manifest schema with a
`[tool.ros]` table consumed by the vinca shim. This document explains why
the schema is shaped the way it is — read before editing.

## Why `[tool.ros]` and not `[package.metadata.ros]`

Pixi's upstream `Package` definition declares `additionalProperties: false`
and does not include a `metadata` field. A `metadata` key under `[package]`
is rejected by pixi at runtime. The only place pixi accepts arbitrary
third-party keys is the top-level `[tool.*]` namespace (same convention as
`pyproject.toml`).

So the vinca shim reads ROS-specific config from `[tool.ros]` rather than
`[package.metadata.ros]`. Pixi ignores `[tool.*]` entirely; it's free real
estate for tooling.

## Schema structure

Because our extension lives at the top level under `[tool.ros]`, we don't
need to vendor or `allOf` against pixi's `Package` def. The schema:

- Is permissive at the root (no `additionalProperties: false`) so pixi's
  own fields under `[package]`, `[dependencies]`, etc. don't trip the LSP.
- Requires `tool.ros` and validates its shape with
  `additionalProperties: false`, so typos surface as diagnostics.
- Defers all pixi-side validation to the upstream pixi schema (which the
  editor can layer in via a separate schema mapping if desired).

## When to update this schema

**Add a field to `[tool.ros]`:** edit `RosMetadata` in the JSON file.
Update existing manifests if the new field is required.

**Pixi-side validation:** not our job. Use pixi's published schema at
`https://pixi.sh/<version>/schema/manifest/schema.json` alongside this
one if you want full LSP coverage.
