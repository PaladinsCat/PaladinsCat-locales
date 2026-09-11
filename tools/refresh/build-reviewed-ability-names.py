"""Export reviewed ability names by stable game message ID, never fuzzy matching.

Print JSON for review, or use --check to verify the checked-in export. This tool
does not write catalogs, decode/install game files, or change contributor text.
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
# Scope: ability references in the September 2026 authored gap-filling batch.
# Repeated English labels require entity context, not broadest language coverage.
SOURCES = {
    'Aphotic Reaver': ('omen', ['248199']),
    'Blast Back': ('saati', ['220063']),
    'Charge': ('fernando', ['127066', '209913']),
    'Combat Trance': ('tiberius', ['206443']),
    'Conviction': ('azaan', ['221049']),  # Not Furia's card, 199974.
    'Crouching Tigron': ('tiberius', ['206426']),
    'Dash': ('vatu', ['216161']),
    'Deadly Domain': ('omen', ['248203']),
    'Envelop': ('rei', ['217230']),
    'Explosive Dodge': ('vii', ['222411']),
    'Hail of Bombs': ('bettylabomba', ['223905']),
    'Heavy Blade': ('tiberius', ['206429']),
    'Ignition': ('raum', ['207710']),  # Not Furia's card, 199971.
    'Juggernaut': ('raum', ['207706']),
    'Obliteration': ('vora', ['212105']),
    'Projection': ('corvus', ['210342']),
    'Reckoning': ('azaan', ['220929']),  # Not a title, spray, or item.
    'Sanctuary': ('azaan', ['221063']),  # Not the map, 145312.
    'Savage Tear': ('kasumi', ['239360']),
    'Shadow Bombs': ('vatu', ['217385']),
    'Soul Harvest': ('raum', ['207702']),
    'Tendril': ('vora', ['212457']),
}


def select_name(english, values):
    """Only a single, usable native value wins. Unknown/internal stays English."""
    usable = {v.strip() for v in values if v and v.strip()}
    if any('_' in v or '<' in v or '{' in v for v in usable):
        return {'value': english, 'status': 'fallback-internal-label'}
    if len(usable) > 1:
        return {'value': english, 'status': 'fallback-conflicting-values'}
    if not usable:
        return {'value': english, 'status': 'fallback-missing'}
    value = usable.pop()
    return {'value': value, 'status': 'same-as-English' if value == english else 'native'}


def build():
    catalogs, checksums = {}, {}
    for path in sorted((REPOSITORY/'game-client').glob('*.csv')):
        with path.open(encoding='utf-8', newline='') as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames != ['message_id', 'value']:
                raise ValueError(f'Invalid CSV header: {path.name}')
            rows = list(reader)
        catalogs[path.stem] = {r['message_id']: r['value'] for r in rows}
        if len(catalogs[path.stem]) != len(rows):
            raise ValueError(f'Duplicate message IDs: {path.name}')
        checksums[path.name] = hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
    terms = {}
    for english, (champion, ids) in SOURCES.items():
        if any(catalogs['en'].get(mid) != english for mid in ids):
            raise ValueError(f'Reviewed source changed: {english}')
        terms[english] = {
            'champion': champion,
            'messageIds': ids,
            'locales': {locale: select_name(english, [cat.get(mid) for mid in ids])
                        for locale, cat in catalogs.items() if locale != 'en'},
        }
    return {'schemaVersion': 1, 'scope': 'Reviewed ability references in the September 2026 gap batch',
            'sourceCsvLfSha256': checksums, 'terms': terms}


if __name__ == '__main__':
    result = build()
    if '--check' in sys.argv:
        current = json.loads((REPOSITORY/'game-client/reviewed-ability-names.json').read_text(encoding='utf-8'))
        if current != result:
            raise SystemExit('Ability-name export is stale; review source differences before updating.')
        print(f'Checked {len(result["terms"])} ability names across 11 languages.')
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
