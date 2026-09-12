"""Bounded regression checks; no game files or translation catalogs are written."""
import csv
import hashlib
import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, HERE/f'{name}.py')
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


importer = module('import-frontend-game-locales')
names = module('build-reviewed-ability-names')


class NativeTerminologyTests(unittest.TestCase):
    def test_real_repository_root(self):
        with patch.object(sys, 'argv', ['importer']):
            self.assertEqual(importer.parse_args().game_client_root, ROOT/'game-client')

    def test_format_only_normalization(self):
        self.assertEqual(importer.normalize_game_value(
            '[Armor] <font color="#1EBEF7">Health</font> {scale=50|50}.'), 'Health {50|50}.')
        self.assertEqual(importer.normalize_game_value('Hold <CMD=GBA_Jump>.'), 'Hold <CMD=GBA_Jump>.')
        self.assertIn('<script>', importer.normalize_game_value('<script>unknown</script>'))

    def test_scaled_and_named_placeholders(self):
        self.assertEqual(importer.placeholders('{50|50} {name} @@ITEM@@ %1$s'),
                         ['%1$s', '@@ITEM@@', '{50|50}', '{name}'])
        self.assertNotEqual(importer.placeholders('{50|50}'), importer.placeholders('{25|25}'))

    def test_fallback_is_not_guessed(self):
        for values in ([], ['Tigron_Barrier'], ['different', 'conflicting']):
            self.assertEqual(names.select_name('Combat Trance', values)['value'], 'Combat Trance')
        self.assertEqual(names.select_name('Tendril', ['テンドリル'])['value'], 'テンドリル')

    def test_reviewed_names_match_source(self):
        saved = json.loads((ROOT/'game-client/reviewed-ability-names.json').read_text(encoding='utf-8'))
        self.assertEqual(names.build(), saved)
        self.assertEqual(saved['terms']['Conviction']['messageIds'], ['221049'])
        self.assertEqual(saved['terms']['Sanctuary']['locales']['zh-CN']['status'], 'fallback-missing')

    def test_additional_reviewed_gap_imports(self):
        review = json.loads((ROOT/'game-client/reviewed-gap-description-import.json').read_text(encoding='utf-8'))
        catalogs = {}
        targets = {}
        for locale in {'en'} | {r['locale'] for r in review['entries']}:
            with (ROOT/f'game-client/{locale}.csv').open(encoding='utf-8', newline='') as stream:
                catalogs[locale] = {r['message_id']: r['value'] for r in csv.DictReader(stream)}
            targets[locale] = json.loads((ROOT/f'locales/{locale}/game/champions.json').read_text(encoding='utf-8'))
        seen = set()
        for record in review['entries']:
            locale, key, mid = record['locale'], record['key'], record['messageId']
            self.assertNotIn((locale, key), seen)
            seen.add((locale, key))
            source = targets['en'][key]
            self.assertEqual(importer.normalize_game_value(catalogs['en'][mid]), source)
            self.assertEqual(importer.normalize_game_value(catalogs[locale][mid]), targets[locale][key])
            self.assertEqual(importer.placeholders(source), importer.placeholders(targets[locale][key]))
        self.assertEqual(len(seen), 216)

    def test_reviewed_description_import(self):
        review = json.loads((ROOT/'game-client/reviewed-description-import.json').read_text(encoding='utf-8'))
        catalogs = {}
        for filename, expected in review['sourceCsvLfSha256'].items():
            path = ROOT/'game-client'/filename
            self.assertEqual(hashlib.sha256(path.read_bytes().replace(b'\r\n', b'\n')).hexdigest(), expected)
            with path.open(encoding='utf-8', newline='') as stream:
                catalogs[path.stem] = {r['message_id']: r['value'] for r in csv.DictReader(stream)}
        targets = {l: json.loads((ROOT/f'locales/{l}/game/champions.json').read_text(encoding='utf-8')) for l in catalogs}
        def quantities(s):
            return sorted(re.findall(r'\d+(?:[.,]\d+)?', re.sub(r'\{[^{}]+\}', '', s).replace(',', '.')))
        count = 0
        for key, record in review['descriptions'].items():
            source = targets['en'][key]
            self.assertEqual(importer.normalize_game_value(catalogs['en'][record['messageId']]), source)
            for locale in record['locales']:
                value = targets[locale][key]
                self.assertEqual(importer.placeholders(value), importer.placeholders(source))
                self.assertEqual(quantities(value), quantities(source), (locale, key))
                self.assertEqual(value.count('%'), source.count('%'))
                self.assertNotIn('<', value)
                count += 1
        self.assertEqual(count, 125)


if __name__ == '__main__':
    unittest.main()
