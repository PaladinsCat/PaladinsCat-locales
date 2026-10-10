# Native client authoring

`translations/` is the canonical authoring directory for the WatchCat native
localization compiler. The initial 13 JSON inputs were moved here byte-for-byte
on 2026-10-10. `ownership.json` records that migration snapshot, including the
previous paths and initial SHA-256 values, including the four pinned name-approval
receipts in `reviews/` needed by the dictionaries. Receipt metadata can refer to
historical WatchCat review/audit paths; resolve that provenance in its original
repository. It is provenance, not a checksum lock
that forbids later reviewed translations.

`.gitattributes` disables line-ending conversion for native JSON. Approval pins
and this migration snapshot refer to exact bytes; Windows `core.autocrlf` must
not change them during staging or checkout.

Compiler, resolver, font converter, IME DLL and patch GUI source live exclusively
in `Z:\NABI\Project\PaladinsCat-WatchCat`. Set `PALADINSCAT_LOCALES` to this existing
checkout when invoking WatchCat tools. `champion-packet` uses that variable,
falling back to `%USERPROFILE%\PaladinsCat\paladinscat-locales`.

Keep exact English source hashes, native ownership references, approvals and
unresolved rows. Every new name requires manual review. Descriptions inherit
approved names within their verified entity scope. A shared message ID alone
does not establish ownership. Use the complete WatchCat pipeline and native
catalog gates before building a distributable locale.

The adjacent `../*.csv` catalogs remain native source exports. They are not the
custom native authoring dictionaries, patched DAT files or installed receipts.
Future target languages add reviewed dictionaries here and their own release
packages; they use the same resolver and installer contracts.

See [release ownership and publication](../../docs/GAME_CLIENT_RELEASES.md).
