import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('whmcs_package', ROOT / 'scripts/package.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class PackageTests(unittest.TestCase):
    def test_all_and_independent_adapters(self):
        for component in ['all', 'cpanel', 'plesk']:
            with self.subTest(component=component), tempfile.TemporaryDirectory() as temporary:
                archive, digest = builder.build(temporary, component)
                first = archive.read_bytes()
                self.assertEqual(builder.build(temporary, component)[1], digest)
                self.assertEqual(archive.read_bytes(), first)
                self.assertEqual(hashlib.sha256(first).hexdigest(), digest)
                self.assertEqual(archive.with_suffix('.zip.sha256').read_text().split()[0], digest)
                with zipfile.ZipFile(archive) as package:
                    expected = set(builder.DOCUMENTS) | {'SHA256SUMS'}
                    for backend, (module, names) in builder.MODULES.items():
                        if component in ['all', backend]:
                            expected.update('modules/addons/' + module + '/' + name for name in names)
                    self.assertEqual(set(package.namelist()), expected)
                    self.assertEqual(len(package.namelist()), len(expected))
                    self.assertIsNone(package.testzip())
                    self.assertFalse(any(name.startswith(('extension/', 'src/', 'tests/', 'integrations/'))
                                         or 'evidence' in name or name.endswith('configuration.php') for name in package.namelist()))
                    for line in package.read('SHA256SUMS').decode().splitlines():
                        checksum, name = line.split('  ', 1)
                        self.assertEqual(hashlib.sha256(package.read(name)).hexdigest(), checksum)
                    for item in package.infolist():
                        self.assertEqual(item.external_attr >> 16, 0o100644)
                        self.assertEqual(item.date_time, (2026, 10, 17, 0, 0, 0))

    def test_distribution_versions_are_not_panel_versions(self):
        metadata = json.loads((ROOT / 'components.json').read_text())
        self.assertEqual(metadata['distribution_version'], (ROOT / 'VERSION').read_text().strip())
        self.assertEqual(metadata['components']['cpanel']['module'], 'help4_disk_usage')
        self.assertEqual(metadata['components']['plesk']['module'], 'help4_disk_usage_plesk')
        self.assertEqual(len(set(metadata['components']['cpanel']['tables']) & set(metadata['components']['plesk']['tables'])), 0)
        self.assertFalse(metadata['native_validation_complete'])

    def test_runtime_provenance_and_unchanged_native_fixtures(self):
        provenance = json.loads((ROOT / 'UPSTREAM.json').read_text())
        changes = {row['destination']: row for row in provenance['post_import_changes']}
        changed_path = 'modules/addons/help4_disk_usage_plesk/lib/Transport.php'
        self.assertTrue(provenance['runtime_rewritten'])
        self.assertEqual(set(changes), {changed_path})
        rows = [row for row in provenance['imports']
                if row['category'] in ['runtime', 'native-contract-fixture']]
        self.assertEqual(sum(row['category'] == 'runtime' for row in rows), 12)
        self.assertEqual(sum(row['category'] == 'native-contract-fixture' for row in rows), 7)
        for row in rows:
            with self.subTest(path=row['destination']):
                self.assertEqual(row['import_sha256'], row['source_sha256'])
                expected = changes[row['destination']]['reviewed_sha256'] if row['destination'] in changes else row['source_sha256']
                self.assertEqual(hashlib.sha256((ROOT / row['destination']).read_bytes()).hexdigest(), expected)

    def test_git_checkout_keeps_reviewed_lf_bytes(self):
        paths = ['modules/addons/help4_disk_usage/hooks.php',
                 'tests/fixtures/plesk/extension/plib/library/Access.php']
        attributes = subprocess.check_output(['git', 'check-attr', '-z', 'eol', '--', *paths], cwd=ROOT)
        self.assertEqual(attributes.split(b'\0')[:-1],
                         [value.encode() for path in paths for value in [path, 'eol', 'lf']])

    def private_source(self, directory):
        target = Path(directory) / 'source'
        shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns('.git', 'dist', '__pycache__'))
        return target

    def test_failed_inventory_or_version_validation_preserves_outputs(self):
        for failure in ['unexpected', 'missing', 'version', 'config']:
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as temporary:
                original = builder.ROOT
                try:
                    builder.ROOT = self.private_source(temporary)
                    destination = Path(temporary) / 'packages'
                    archive, _ = builder.build(destination)
                    before = archive.read_bytes(), archive.with_suffix('.zip.sha256').read_bytes()
                    if failure == 'unexpected':
                        (builder.ROOT / 'modules/addons/help4_disk_usage/private.php').write_text('synthetic-private')
                    elif failure == 'missing':
                        (builder.ROOT / 'modules/addons/help4_disk_usage/hooks.php').unlink()
                    elif failure == 'version':
                        (builder.ROOT / 'VERSION').write_text('../../unsafe')
                    else:
                        path = builder.ROOT / 'components.json'
                        data = json.loads(path.read_text())
                        data['components']['plesk']['version'] = '99.0.0'
                        path.write_text(json.dumps(data))
                    with self.assertRaises((RuntimeError, FileNotFoundError)):
                        builder.build(destination)
                    self.assertEqual((archive.read_bytes(), archive.with_suffix('.zip.sha256').read_bytes()), before)
                finally:
                    builder.ROOT = original

    @unittest.skipIf(os.name == 'nt', 'POSIX symlink control; Windows junction has a separate control')
    def test_symlink_refuses_before_output_creation(self):
        with tempfile.TemporaryDirectory() as temporary:
            original = builder.ROOT
            try:
                builder.ROOT = self.private_source(temporary)
                file = builder.ROOT / 'modules/addons/help4_disk_usage/hooks.php'
                file.unlink()
                file.symlink_to(ROOT / 'modules/addons/help4_disk_usage/hooks.php')
                destination = Path(temporary) / 'packages'
                with self.assertRaises(RuntimeError):
                    builder.build(destination)
                self.assertFalse(destination.exists())
            finally:
                builder.ROOT = original

    @unittest.skipUnless(os.name == 'nt', 'Actual Windows junction metadata control')
    def test_windows_junction_refuses_before_traversal(self):
        with tempfile.TemporaryDirectory() as temporary:
            original = builder.ROOT
            try:
                builder.ROOT = self.private_source(temporary)
                junction = builder.ROOT / 'modules/addons/help4_disk_usage/templates'
                shutil.rmtree(junction)
                target = Path(temporary) / 'target'
                target.mkdir()
                (target / 'clientarea.tpl').write_text('must not be traversed')
                subprocess.run(['cmd', '/c', 'mklink', '/J', str(junction), str(target)], check=True, capture_output=True)
                destination = Path(temporary) / 'packages'
                with self.assertRaises(RuntimeError):
                    builder.build(destination)
                self.assertFalse(destination.exists())
                junction.rmdir()
            finally:
                builder.ROOT = original


if __name__ == '__main__':
    unittest.main()
