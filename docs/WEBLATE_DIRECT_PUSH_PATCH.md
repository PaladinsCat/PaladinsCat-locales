# Weblate Direct-Push Patch (github-app → main, no PR)

Weblate 6.0.8 has **no built-in "push directly, no PR" mode** for the
`github-app` integration. `GithubRepository.push()` always calls
`create_pull_request()` at the end, even in the non-fork (App) path.

This patch makes the GitHub App push **directly to `main`** — no PR, no fork.

## Why this exists

Project rules (2026-09-17):
1. The locales repo must contain **only the `main` branch**.
2. **Weblate auto-merge** must work.

The default Weblate github-app flow creates a `weblate-*` branch + PR, which
violates rule 1 (extra branch) and requires manual PR review (violates rule 2).
This patch eliminates both.

## How it works

A `sitecustomize.py` is placed at `/app/data/python/` inside the Weblate
container. That directory is on `sys.path` (via `weblate-docker.pth`) and is
**writable + persistent** (named volume), unlike the read-only site-packages.

`sitecustomize` runs at interpreter startup for every Weblate process
(granian web + celery workers). It installs an import hook that patches
`GithubAppRepository.push()` the moment `weblate.vcs.github` is first imported
(after Django is configured), replacing the PR-opening `super().push()` with a
direct `GitRepository.push(branch)` — a plain `git push origin main:main`.

## Governance change (deliberate)

Direct-to-main pushes **bypass the PR review + `analyze`/`validate` (CodeQL)
status checks** for Weblate commits. This was a deliberate decision to enable
auto-merge. Human pushes still go through PR review (the App's direct push is
the only path that skips it).

## One-step re-apply (after any Weblate update)

The patch lives in the container and is **lost on every Weblate image update**.
After updating Weblate, re-apply with:

```bash
# On the Weblate VPS (40.160.82.10:2222, user paladinscat):
# 1. Copy this file into the container's /app/data/python/
docker cp /home/paladinscat/weblate/sitecustomize.py \
  paladinscat-weblate-weblate-1:/app/data/python/sitecustomize.py

# 2. Restart the services so the running workers pick it up
sudo supervisorctl -c /etc/supervisor/supervisord.conf restart \
  granian celery celery-beat

# 3. Verify (should print "patched: True")
docker exec paladinscat-weblate-weblate-1 \
  /app/venv/bin/python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','weblate.settings')
django.setup()
from weblate.trans.models import Component
c = Component.objects.get(slug='pageslocalization')
print('patched:', getattr(c.repository,'_paladinscat_patched','n/a'))
"
```

## Verified (2026-09-17)

- No-op push (same SHA): **200** — App can write `main`.
- Real commit push via `repo.push()`: commit landed on `main`, **no PR created**,
  **no fork**. Confirmed `open PRs: []` and `main HEAD == local commit`.
- Test commit + revert both pushed cleanly through the patched path.

## Branch-protection state (2026-09-17)

- `required_status_checks`: **disabled** (was `analyze` + `validate`, strict).
  Required because a direct push has no PR to trigger CodeQL.
- `required_pull_request_reviews`: still **1** (code-owner) — applies to human
  PRs only; the App's direct push is exempt.
- `allow_force_pushes`: true.
- `required_linear_history`: true.
- `enforce_admins`: false.
