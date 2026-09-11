# Game-client translation artifacts

Approved game translations are stored as one UTF-8 CSV per game language:

```text
game-client/de.csv
game-client/fr.csv
```

Each file has exactly two columns:

```csv
message_id,value
42189,Translated text
```

`message_id` is the stable identity from the decoded game catalog. Files are
committed on a translation branch and reviewed as a normal GitHub pull request.
Do not replace IDs with the repeated game `key` field.

## Native game sources

The checked-in packs are generated from native game language data, not from
machine translation or string-key matching. `source-manifest.json` records the
game language code, source package checksum, and exact string count for every
pack. This preserves the terminology players see in the game, including
champion, ability, item, card, and mode names.

The old `import-game-client-locales.py` default depends on the removed
Tempest/GameDecoder workflow. Do not run that default or restore its Python
decoder in WatchCat. WatchCat's maintained localization tooling is Rust-only.
Treat the installed client as read-only; verify source package hashes against
`source-manifest.json` before reusing these decoded catalogs. DAT files contain
typed binary records after XOR decoding, not plain UTF-16 INI text.

The importer exports current client languages only: `en`, `de`, `es-419`, `fr`,
`ja`, `ko`, `pl`, `pt-BR`, `ru`, `tr`, `zh-CN`, and `zh-TW`. Korean uses the
maintained decoded catalog and must be checked separately against the reviewed
custom-pack build evidence; its CSV hash is not the installed DAT hash. The
importer deliberately excludes `ESN` (the stale English fallback) and `DEB`
(debug English).

## Game-term glossary for UI translation

Build the curated native-term glossary after refreshing the client packs:

```powershell
python tools/refresh/build-game-term-glossary.py
```

`term-glossary.json` supplies game-specific UI term candidates. Verify their
meaning in context: the broadest-language-coverage heuristic can select the
wrong homonym (for example, end credits instead of match currency). Preserve
the reviewed overrides in `fixed-ui-terms.json`. Apply verified terms when
translating frontend UI and surrounding prose; translate ordinary copy normally.

`reviewed-ability-names.json` contains the batch's entity-disambiguated proper
names, with native names first in every language and English fallback otherwise.
Verify its source checksums and values without changing any files:

```powershell
python -X utf8 tools/refresh/build-reviewed-ability-names.py --check
```

See [native language style and source checks](../docs/NATIVE_LANGUAGE_STYLE.md).

`tools/refresh/translate-frontend-general-copy.py` applies this rule mechanically: it direct-
translates non-game frontend modules only, masks native glossary terms and
placeholders during translation, and restores them afterward. It never touches
Korean or `game/*` descriptions.

## Frontend game terms

To add native terms and descriptions to the frontend, run the second importer
after refreshing the client packs:

```powershell
python tools/refresh/import-frontend-game-locales.py
npm run validate
```

The legacy importer also has semantic and title-adjacent matching paths; it is
not an exact-match-only approval mechanism. Review the candidates and pending
contributor work before running it. The September native batch used only exact
English matches after formatting normalization, followed by target wording
review. Existing translations must be preserved. Do not use `--force` for gap
filling. The
companion `frontend-game-match-manifest.json` reports the coverage and makes
gaps explicit; unmatched strings remain available for human translation instead
of being guessed.

These CSVs are translation artifacts, not game binaries. Game installation or
DAT rebuilding is a separate WatchCat workflow, not part of website translation.
The game-client source manifest must be available in the contributor's local
toolchain before adding a target CSV; the PaladinsCat VPS no longer publishes a
game catalog or stores game translation submissions.
