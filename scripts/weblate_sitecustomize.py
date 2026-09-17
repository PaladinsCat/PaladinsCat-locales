"""
PaladinsCat Weblate customization — direct push to main (no PR).

Weblate 6.0.8 has no built-in "push directly, no PR" mode for the
github-app integration: ``GithubRepository.push()`` always calls
``create_pull_request()`` at the end. This file patches
``weblate.vcs.github.GithubAppRepository.push()`` so the GitHub App pushes
translations straight to the source branch (``main``) instead of opening a
pull request.

Location: /app/data/python/sitecustomize.py
  - /app/data/python is on sys.path via weblate-docker.pth.
  - The ``site`` module imports ``sitecustomize`` at interpreter startup,
    so this runs for every Weblate process (granian web + celery workers).

Mechanism: an import hook. sitecustomize runs BEFORE Django is configured,
so we cannot import weblate.vcs.github directly here. Instead we wrap
builtins.__import__ and apply the patch the moment weblate.vcs.github is
first imported (which happens after django.setup()).

Idempotent + failure-safe: the patch is applied once and any error is
swallowed so it never breaks Weblate startup.

Re-apply after a Weblate image update:
  This file lives in the weblate-data volume and survives container
  recreation, so it persists across ``docker restart``. It only references
  stable names (GithubAppRepository / GitRepository.push), so a Weblate
  version bump keeps it working unless Weblate renames those. If a future
  Weblate changes the class layout, update this file and re-run the
  verification in docs/WEBLATE_DIRECT_PUSH_PATCH.md (locales repo).
"""
import builtins
import sys

_orig_import = builtins.__import__
_patched = False


def _apply(gh):
    global _patched
    if _patched:
        return
    try:
        from weblate.vcs import git as _git

        target = gh.GithubAppRepository

        def _push(self, branch):
            # Push straight to the source branch (self.branch, e.g. "main"),
            # bypassing GithubRepository.push() which always opens a PR.
            _git.GitRepository.push(self, self.branch)

        target.push = _push
        target._paladinscat_patched = True
        _patched = True
    except Exception:
        # Never break Weblate startup over the patch.
        pass


def _import(name, *args, **kwargs):
    mod = _orig_import(name, *args, **kwargs)
    if name == "weblate.vcs.github" and not _patched:
        gh = sys.modules.get("weblate.vcs.github")
        if gh is not None:
            _apply(gh)
    return mod


builtins.__import__ = _import
