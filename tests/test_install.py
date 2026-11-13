import argparse
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("apply", ROOT / "apply_wt_theme.py")
apply = importlib.util.module_from_spec(spec)
spec.loader.exec_module(apply)

class InstallTests(unittest.TestCase):
    def test_jsonc_preservation_repeat_and_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory)
            settings = p / "settings.json"
            initial = '{// keep values, comments can be normalized\n"profiles":{"list":[{"name":"Custom","commandline":"https://example.test/a,b"}],"defaults":{"font":{"weight":"bold"}}},"keybindings":[{"keys":"alt+x"}],}'
            settings.write_text(initial)
            profiles = [p / "PowerShell" / "profile.ps1", p / "WindowsPowerShell" / "profile.ps1"]
            profiles[0].parent.mkdir()
            profiles[0].write_text("# unrelated user configuration\n$ExistingValue = 1\n", encoding="utf-16")
            args=argparse.Namespace(settings=str(settings), background=None, icon=None, starship=None, profile=[str(x) for x in profiles])
            apply.install(args)
            backups_before = set(p.rglob("*.bak-bigfish-*"))
            first = settings.read_bytes()
            apply.install(args)
            self.assertEqual(settings.read_bytes(), first)
            self.assertEqual(set(p.rglob("*.bak-bigfish-*")), backups_before)
            data=json.loads(settings.read_text())
            self.assertEqual(data['profiles']['list'][0]['commandline'], 'https://example.test/a,b')
            self.assertEqual(data['keybindings'], [{'keys':'alt+x'}])
            self.assertEqual(data['profiles']['defaults']['font']['weight'], 'bold')
            self.assertEqual(data['profiles']['defaults']['backgroundImageStretchMode'], 'uniformToFill')
            self.assertEqual(len(data['schemes']), 1)
            for profile in profiles:
                self.assertEqual(profile.read_text(encoding='utf-8-sig').count(apply.START), 1)
            self.assertIn('$ExistingValue = 1', profiles[0].read_text(encoding='utf-8-sig'))
            self.assertTrue(any(x.read_text()==initial for x in p.glob('settings.json.bak-*')))

    def test_reject_conflicting_targets(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'settings.json'
            p.write_text('{}')
            args=argparse.Namespace(settings=str(p),background=None,icon=None,starship=None,profile=[str(p)])
            with self.assertRaises(ValueError):
                apply.install(args)
            self.assertEqual(p.read_text(), '{}')

    def test_invalid_asset_does_not_change_settings(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'settings.json'
            p.write_text('{}')
            args=argparse.Namespace(settings=str(p),background=str(p.parent/'missing.png'),icon=None,starship=None,profile=[])
            with self.assertRaises(FileNotFoundError):
                apply.install(args)
            self.assertEqual(p.read_text(), '{}')

if __name__ == '__main__':
    unittest.main()
