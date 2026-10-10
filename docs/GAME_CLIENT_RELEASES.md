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
releases. An empty array offers no release. A source/catalog commit does not
publish downloadable packages. The GUI also accepts an explicit public GitHub
catalog asset URL in Repository settings, while retaining the repository link.
This permits inspection of a published preview before its catalog PR is merged.

Every entry identifies an immutable manifest URL and its SHA-256. Each manifest
pins the supported game executable and every payload hash/size. HTTPS GitHub
is the current publisher trust boundary; publisher signatures are not yet used.
The patcher reuses verified cached assets. A correction is a new immutable
release and catalog entry, not replacement of an existing asset.

Locale bundles retain the WatchCat v1 manifest and exact writable-file allowlist.
They carry the reviewed locale source commit and client build/fingerprint.
Record the exact committed IME source and packaging executable hash in release
provenance. Do not label an IME-only commit as the packaging implementation
commit. An update to the game requires renewed native mapping, hash, package and
visual checks.

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

A user-authorized preview may be published with those pending checks explicitly
listed in both catalog and manifest notes. `draft:false` permits downloading; it
does not mean stable, fully translated, or accepted on a live client. Mark the
GitHub release as a prerelease, exclude it from latest stable, and retain the
pending gates in provenance. Stable promotion still requires those checks.

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

## Published preview: 2026-10-10

[game-client-preview-20261010-r1](https://github.com/PaladinsCat/PaladinsCat-locales/releases/tag/game-client-preview-20261010-r1)
contains Korean v172 and IME 0.1.0 for the exact Win64 8.1 executable fingerprint.
Both catalog entries and manifests explicitly say PREVIEW. Translation review,
unresolved native ownership, targeted visual checks, portable IME gameplay and
live disable remain pending.

| Manifest | SHA-256 |
|---|---|
| `locale-package.json` | `a67cdc912b2420e4885f2eb0fcfb628c5c08b6ba20e0f2eb5bfc3e6a6474ea5c` |
| `ime-package.json` | `b64c71f21d472afd62ccc114f9faa68c23f76e53c52e83bcdf26815085581f7e` |

Locale source: `9192457a4907d3508c5de0ffe6ef6dff54fa6d16`.
WatchCat IME source: `3b361669eedd02190f7a242483e3bfa84cd63775`.
The release has 15 immutable assets, including nine compressed locale payloads,
the DLL, both manifests, the catalog, provenance and font notice. The production
Rust download engine verified both packages from a fresh cache, including
compressed and decoded hashes/sizes, actual DLL exports and ABI `[4,9,7,1]`.
These checks did not install into a game or execute the DLL.

Reproduce in WatchCat with the built `paladinscat-release` Rust CLI:

```text
assemble-preview BUNDLE_JSON IME_PACKAGE_JSON LOCALE_REPO NEW_TAG LOCALE_COMMIT IME_COMMIT
verify-downloads PUBLIC_CATALOG_URL NEW_EMPTY_CACHE_DIRECTORY
use-catalog PUBLIC_CATALOG_URL
```

`assemble-preview` refuses an existing tag directory, prepares gzip payloads,
final manifests, catalog and provenance under ignored `.release-staging`, and
publishes nothing. Upload all assets to a draft GitHub prerelease, verify their
identities and sizes, then publish under the user's release authorization.
Run `verify-downloads` against the public asset catalog in a fresh cache before
offering it. `use-catalog` downloads/verifies both families into the GUI cache
and persists that catalog URL and prepared selections; it changes no game files.
Submit the matching `game-client/catalog.json` through an owner-reviewed PR.
