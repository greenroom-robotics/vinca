# Greenroom pixi.toml schema (ROS)

`greenroom_pixi_manifest.schema.json` defines the `[tool.ros]` table that
the vinca pixi shim reads. Use it for editor completion and validation in
any pixi.toml that backs a ROS conda package.

ROS metadata lives under `[tool.ros]` because pixi only honors third-party
metadata under `[tool.*]` — see `SCHEMA_NOTES.md` for the rationale.

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

The schema validates and provides completion for `[tool.ros]`:

- `build_type` (required, one of `ament_cmake` / `ament_python` /
  `ament_cargo`)
- `is_message_package` (boolean)
- `test_dependencies` (`{name = version-spec}` table)

`additionalProperties: false` is enforced inside `[tool.ros]` so typos
surface as diagnostics. Anything outside that subtree is unconstrained by
this schema — layer pixi's own schema alongside it (e.g. via your LSP's
schema mapping) if you want validation of the rest of the manifest.
