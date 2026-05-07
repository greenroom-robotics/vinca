# Greenroom pixi.toml schema (ROS)

`greenroom_pixi_manifest.schema.json` extends pixi's official manifest
schema with the `[package.metadata.ros]` table that the vinca pixi shim
reads. Use it for editor completion and validation in any pixi.toml
that backs a ROS conda package.

It's a standard JSON Schema (draft 2020-12), so any TOML LSP that
supports JSON Schema will work — tombi, taplo (Even Better TOML), etc.

## Wiring it up

### Per-file `#:schema` directive

Add this as the first line of the source repo's `pixi.toml`:

```toml
#:schema https://raw.githubusercontent.com/Greenroom-Robotics/vinca/master/vinca/schemas/greenroom_pixi_manifest.schema.json
```

Most TOML LSPs pick this up automatically. Pin to a tag or commit SHA
instead of `master` when you want stable behavior.

### Repo-wide config

For multi-package repos, configure your LSP to apply the schema to all
manifests at once. The exact config file and syntax depends on the LSP
you're using — see your LSP's docs for schema mapping.

## What it covers

The schema validates and provides completion for:

- All standard pixi.toml fields (via `allOf` of the upstream pixi
  schema at `https://pixi.sh/latest/schema/manifest/schema.json`).
- `[package.metadata.ros]` with:
  - `build_type` (required, one of `ament_cmake` / `ament_python` /
    `ament_cargo`)
  - `is_message_package` (boolean)
  - `test_dependencies` (`{name = version-spec}` table)

`additionalProperties: false` is enforced inside `[package.metadata.ros]`
so typos surface as diagnostics. Anything outside that subtree is
constrained only by the upstream pixi schema — including the rest of
`[package.metadata]`, which stays open for other tooling.
