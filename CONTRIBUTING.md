# Contributing translations

## Owner-directed agent work

The owner's red line is the existing `main` checkout only. Do not create agent
branches, worktrees, forks or PRs. Review and run the relevant validators before
authorized direct publication from `main`; respect remote protections. The
upstream Main only ruleset blocks creation and updates of every other branch.
Dependabot branch-producing updates are disabled; reviewed dependency changes
use the same main-only owner workflow. Security scanning and alerts remain on.
External contributors may use their own forks, without upstream feature branches.
See AGENTS.md. Release/version labels are plain, for example `Korean v177`;
do not add a task description or content hash to the visible version name.

## Rules

- External contributors create branches only in their own forks. Owner agents
  keep this checkout on `main`.
- Edit target-language values only. Do not rename or add application keys.
- Keep JSON valid and use UTF-8 characters directly.
- Preserve placeholders such as `{name}`, `@@TOKEN@@`, `%s`, and `%1$s`.
- Use BCP 47 locale directories such as `fr`, `pt-BR`, or `zh-CN`.
- Partial modules are allowed; missing strings fall back to English.
- Do not include Weblate credentials, exports, application code, or unrelated
  files.

Before committing, run:

```powershell
npm install
npm run validate
```

GitHub Actions repeats these checks for every pull request. It rejects invalid
module paths, unknown keys, empty or oversized strings, malformed Unicode,
changed placeholders, invalid CSV rows, and duplicate game message IDs.

## Weblate workflow

Weblate is the normal translation workspace at
[translate.paladinscat.com](https://translate.paladinscat.com). It synchronizes with this
repository. Upstream branch publication is blocked by the main-only rule.
Reviewed exports can be applied by the owner on `main`; a fork-based integration
requires its own separately configured destination.

1. sign in at [translate.paladinscat.com](https://translate.paladinscat.com)
   and choose your language;
2. submit translations; language reviewers approve wording in Weblate;
3. export only approved strings for owner review;
4. validate the diff and publish the reviewed source on `main`;
5. the frontend validates and compiles that locale revision before
   opening its separate locale-pin pull request.

GitHub `main` remains the source of truth and release approval boundary.
Weblate must not push directly to `main` or create an upstream branch.

## Local Git fallback

When Weblate is unavailable, external contributors use a personal fork, edit only
target-language values, run `npm run validate`, and open a normal pull request.
This route has the same validation and review requirements.
