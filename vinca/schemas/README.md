# Greenroom pixi.toml schema (ROS)

`greenroom_pixi_manifest.schema.json` extends pixi's official manifest
schema with the `[package.metadata.ros]` table that the vinca pixi shim
reads. Use it for editor completion and validation in any pixi.toml
that backs a ROS conda package.

## Wiring it up

We use [tombi](https://github.com/tombi-toml/tombi) as the TOML LSP.

### Per-file `#:schema` directive

Add this as the first line of the source repo's `pixi.toml`:

```toml
#:schema https://raw.githubusercontent.com/Greenroom-Robotics/vinca/master/vinca/schemas/greenroom_pixi_manifest.schema.json
```

Tombi picks it up automatically. Pin to a tag or commit SHA instead of
`master` when you want stable behavior.

### Repo-wide via `tombi.toml`

For multi-package repos, put a `tombi.toml` at the repo root pointing
all relevant manifests at the schema. See the tombi docs for the
current config format — the per-file directive above works without any
extra config and is the simplest place to start.

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
