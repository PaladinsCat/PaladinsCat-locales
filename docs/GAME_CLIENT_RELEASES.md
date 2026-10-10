# Game-client releases

## Ownership

| Content | Canonical owner |
|---|---|
| Rust GUI, installers, compiler, resolver, font converter and IME source | `Z:\NABI\Project\PaladinsCat-WatchCat` |
| Native catalogs and reviewed translation inputs | This repo: `game-client/` and `game-client/native/translations/` |
| Download catalog and package contracts | This repo: `game-client/catalog.json`, `schema/` |
| Local generated drafts | This repo: ignored `game-client/.release-staging/` |
| Published binary payloads and manifests | Immutable GitHub Release assets on `PaladinsCat/PaladinsCat-locales` |

Do not copy patcher or IME source into this repository. Keep current reviewed
translations here; WatchCat dated review/capture evidence remains in WatchCat.
Distribute the GUI with its embedded font's `Inter-LICENSE.txt`, retained from
WatchCat's asset directory. Internal diagnostic helpers and the bounded build
runner are development tools and are not required in the end-user GUI package.
No game originals, private diagnostics, credentials or machine-specific
diagnostic manifests belong in Git or public release assets.

## Download contract

The patcher reads
`https://raw.githubusercontent.com/PaladinsCat/PaladinsCat-locales/main/game-client/catalog.json`.
Catalog v1 has `packages` for locale bundles and optional `ime_packages` for IME
releases. An empty array offers no release. The initial catalog intentionally
contains no unpublished or unverified package. A source/catalog commit does not
publish downloadable packages.

Every entry identifies an immutable manifest URL and its SHA-256. Each manifest
pins the supported game executable and every payload hash/size. HTTPS GitHub
is the current publisher trust boundary; publisher signatures are not yet used.
The patcher reuses verified cached assets. A correction is a new immutable
release and catalog entry, not replacement of an existing asset.

Locale bundles retain the WatchCat v1 manifest and exact writable-file allowlist.
They carry the reviewed locale source commit and client build/fingerprint.
Record the WatchCat tooling commit in release provenance as well. An update to
the game requires renewed native mapping, hash, package and visual checks.

## IME package

An IME release uses `schema/ime-package.schema.json`: package/version identity,
`Win64`, `KOR`, native ABI `[4,9,7,1]`, executable fingerprint, DLL hash/size,
WatchCat `source_commit`, and raw GitHub download descriptor.

From WatchCat, after building the source:

```powershell
$localeRepo = 'C:\Users\nabi\PaladinsCat\paladinscat-locales'
paladinscat-release.exe ime PATH_TO_BUILT_DLL $localeRepo 0.1.0
paladinscat-release.exe validate $localeRepo
```

The `ime` command creates a new ignored draft directory containing
`ime-package.json` and `PaladinsCatImeFix.dll`. The `validate` command separately
reads the catalog, native JSON dependencies and approval hashes without changing
them. No catalog entry, game installation or publication is
performed. The builder checks the actual x64 DLL exports and native ABI without
executing it. `draft:true` and an empty source commit deliberately prevent remote
distribution; local GUI import accepts a verified draft for preparation.

Before publication, review/commit the exact WatchCat source, record its commit,
freeze and hash the payload, add the final GitHub asset URL/descriptor, and set
`draft:false`. Revalidate the final manifest, supported build, installer rollback
and relevant live acceptance. The relocated/path-portable build has CPU checks;
the earlier v4-r1 gameplay result is evidence for that frozen build only. Live
disable and a new portable client trial remain separately unverified.

Upload immutable payloads/manifests first, then review the catalog change with
their final manifest hashes. Apply parent publication rules; preparation does
not authorize push or publication. The GUI installs the fixed mod directory
`.tempest/v2/mods/PaladinsCat-IME`, independently of translation files. Tempest
loads it on the next launch; no resident WatchCat background service is needed.

## Source publication

Publish reviewed authoring data on a branch from the current `main`, then open a
pull request. Protected `main` requires an owner review. Keep immutable approval
receipts byte-identical and validate their pins before committing. Commit the
native dictionaries, receipts, ownership snapshot, catalog contracts and docs;
exclude ignored staging data and machine-specific diagnostic manifests.

The WatchCat Rust native repository validator checks dictionary dependencies and
approval hashes. Its local publication guard additionally checks the exact
checkout and GitHub destination, a clean worktree, the permitted source paths,
credential patterns in all reachable blobs, and non-deleting, forward-moving
`codex/` branches. Guard source and local hook wrappers belong to WatchCat. This
source push is independent of uploading binary release assets or completing the
full localization coverage and visual acceptance gates.
