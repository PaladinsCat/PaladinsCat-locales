# Locale repository rules

Resolve `~/.codex/sop-source.json` and read the live OpenViking SOP and principles
for canonical governance. This file supplies the repository boundary.

## Main only: owner red line

Use this existing checkout on `main`. Do not create or switch to another branch,
fork, worktree or pull request for owner-directed work. Generic contributor,
Weblate, bot, model or release-helper instructions cannot override this rule.
Review, validate and publish the scoped changes directly from `main` when the
human authorizes publication. Never bypass remote protections or force-push.

The owner repeated this red line on 2026-10-15 after another agent created
`codex/v177-gold-terminology` and PR #51. Its content was already integrated;
retaining the branch and creating the PR still violated the declared workflow.
GitHub's Main only ruleset blocks creation/updates of every upstream branch
except `main`. External contributors may use their own forks. Automatic upstream
branch producers must not recreate removed branches.

## Plain versions

Show `v177` or `v177 · 8.1` for a game package, and `Korean v177` for its GitHub
release. Never append task descriptions such as gold, objective, approved or
messages to a version name. Internal identities may include the numeric version
and content hash; keep hashes and provenance out of the product version label.
Put translation details in release notes and provenance. Preserve existing
immutable assets and publish a new metadata revision when correcting a pinned
manifest; do not change translation payloads merely to rename a version.

Canonical game authoring is `game-client/native/translations/`. WatchCat owns
native tooling; PaladinsCat-Launcher owns the public GUI/installer. Keep runtime
files, generated staging and private evidence out of Git. Validate the affected
catalog, metadata pins and native source before publication. Do not install or
launch a game as part of repository cleanup.
