# Native terminology and language style

## Source checks on September 11, 2026

Installed DAT SHA-256 values matched `source-manifest.json` for English, German,
Latin American Spanish, French, Japanese, Polish, Brazilian Portuguese, Russian,
Turkish, Simplified Chinese and Traditional Chinese. The existing decoded CSVs
were reused; no game files were edited and no new DAT decoder was necessary.

Korean is a custom expanded pack, not the old small stock pack. Its installed
14,648,628-byte DAT has SHA-256
`334c5ccea9bb7d7443e0bfb324cb2d27e58db8a23a39f3e0e2945a3dc1e9a5bc`,
matching WatchCat's `kor-skills-v5` build report (112,865 records). That report
does not make the older maintained Korean CSV a fresh export of the custom DAT.
The reviewed Korean ability-name entries remain English in that CSV. No new
Korean proper names were invented, and no Korean catalog values were overwritten.
The custom pack's Korean skill descriptions were consulted for style only.

The name and description review manifests record the CSV checksums used, with
CRLF normalized to LF so Git checkouts on different operating systems agree.
Raw game packages, private paths and contributor-review exports are not published.

## Entity identity comes before string similarity

Native `message_id` identifies a string; an English label alone may not identify
the correct ability. Azaan's Conviction is `221049`, not Furia's card `199974`.
Azaan's Reckoning is `220929`, not the similarly named cosmetic or item.
His Sanctuary is `221063`, not the map `145312`. Raum's Ignition is `207710`,
not Furia's card `199971`. Missing Azaan/Raum entries in the Chinese packs must
not borrow translations from those unrelated older entities.

Native Chinese values such as `Tigron_Barrier`, `Tigron_Leap` and
`Tigron_heavyBlade` are internal labels, not localized proper names. Those names
stay Combat Trance, Crouching Tigron and Heavy Blade until a dedicated usable
native title is verified. English fallback for a name does not prevent translating
the surrounding description.

## Language-specific guidance

These are working conventions observed in native strings and existing
contributions, not claims of independent native-speaker approval. Match the
surrounding module's voice. Do not mechanically replace words in contributor text.

| Locale | Terms and phrasing to preserve |
|---|---|
| de | Abklingzeit; native health cards use Gesundheit and LP. Card effects can use Erhöht/Verringert; action descriptions commonly use imperatives. |
| es-419 | Salud/PS and tiempo de recarga; use direct second-person skill descriptions. Preserve hasta for an upper bound, not an exact target count. |
| fr | PV, compétence, temps de recharge. Skill descriptions commonly use vous. Introduce quoted ability names with la compétence to avoid awkward name inflection. |
| ja | Native health-card wording uses HP; クールダウン and ～する/～される suit compact descriptions. Preserve verified katakana/kanji names, such as テンドリル. |
| ko | Respect fixed-ui-terms.json: 경쟁전, 실드, 실딩 and the existing community vocabulary. Reviewed custom-pack descriptions use ～합니다/～줍니다. Keep unverified proper names in English. |
| pl | Zdrowie/PZ, czas odnowienia; Zwiększa/Skraca for effects. Use zdolności plus a quoted title when a name would otherwise require an uncertain case ending. |
| pt-BR | Vida, dano and intervalo in native skill copy. Use Brazilian forms and third-person effect descriptions. Correct malformed grammar without renaming native abilities. |
| ru | Урон, ед., время восстановления for ability cooldowns; do not confuse this with weapon reloading. Use quoted invariant ability titles where appropriate. |
| tr | Can, Bekleme Süresi; maintain Turkish casing and case endings. Use yeteneğinin/ yeteneğini around fixed ability names where required by the sentence. |
| zh-CN | 生命值、冷却时间、积分; compact effect-first copy and Simplified characters. Never import debug identifiers or an older card's name for a newer ability. |
| zh-TW | 生命值、冷卻時間、積分; Traditional characters throughout. Verify the locale's own value rather than converting Simplified text mechanically. |

Native message `150103` supplies the health-card comparison, `54706`/`162695`
supply cooldown labels, and `212457` supplies Tendril. The reviewed description
import supplies short skill examples for eight European/Japanese locales and
the two Chinese variants. Existing Korean contributions and the custom-pack
review supply Korean style evidence.

## Mechanics and review boundary

Strip only recognized presentation tags, not game commands such as `<CMD=...>`.
Preserve scaled placeholders, quantities, percentages, target restrictions,
effect types and timing. A native translation can be shorter than current
English while omitting a mechanic: reject it or explicitly adapt it.

This pass reviewed 125 additions, adapting 15. Examples include restoring
Atlas's brief banishment and return position in French, Caspian's projectile
piercing in Turkish, and VII's upper target limit in Spanish. Other incomplete
native candidates were left pending. Existing translations and pending Weblate
contributor work were preserved. Nothing was approved in Weblate or deployed.
