#!/usr/bin/env bash
set -euo pipefail

project="${1:-$PWD}"
archive="${2:?usage: package-site.sh PROJECT_DIR ARCHIVE_PATH}"
hosting="$project/.openai/hosting.json"
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

test -f "$hosting" || { echo "Missing .openai/hosting.json" >&2; exit 2; }

stage="$(mktemp -d)"
trap 'rm -rf "$stage"' EXIT
build_kind="$(node "$script_dir/prepare-site-build.cjs" "$project" "$stage/dist")"
mkdir -p "$stage/dist/.openai"
# Keep current source settings, but retain attribution emitted only by the build.
# Static preparation has already normalized the staged static.directory.
node - "$hosting" "$project/dist/.openai/hosting.json" "$stage/dist/.openai/hosting.json" "$build_kind" <<'NODE'
const fs = require("node:fs");
const { isDeepStrictEqual } = require("node:util");
const [sourcePath, builtPath, stagedPath, kind] = process.argv.slice(2);
const read = (filename) => JSON.parse(fs.readFileSync(filename, "utf8"));
const source = read(sourcePath);
const built = fs.existsSync(builtPath) ? read(builtPath) : {};
if (
  source.artifact_metadata != null &&
  built.artifact_metadata != null &&
  !isDeepStrictEqual(source.artifact_metadata, built.artifact_metadata)
) {
  throw new Error("Conflicting artifact_metadata in source and built hosting manifests; rebuild with consistent attribution before packaging.");
}
const staged = kind === "worker" ? source : read(stagedPath);
const attribution = built.artifact_metadata ?? source.artifact_metadata;
if (attribution != null) staged.artifact_metadata = attribution;
fs.writeFileSync(stagedPath, JSON.stringify(staged, null, 2) + "\n");
NODE
if test -d "$project/drizzle"; then
  mkdir -p "$stage/dist/.openai/drizzle"
  cp -R "$project/drizzle"/. "$stage/dist/.openai/drizzle"/
fi

mkdir -p "$(dirname "$archive")"
tar -C "$stage" -czf "$archive" dist
archive_entries="$(tar -tzf "$archive")"
grep -qx 'dist/.openai/hosting.json' <<<"$archive_entries"
printf '%s\n' "$archive"
