"""Exercise current-edition and authoring-provenance guards on isolated copies."""
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
PAGE = 'Science_Teesside/Build/SCI_B_W3_Backbones.html'
TARGETS = 'tools/easter/SCIENCE_ORIGINAL_TARGETS.json'
MANIFEST = 'Science_Teesside/Teaching_Packs/BUILD/SOURCE_MANIFEST.json'


def overlay(source, destination, copies):
    """Copy only mutation targets; link untouched inputs without writing them."""
    destination.mkdir(exist_ok=True)
    for item in source.iterdir():
        if item.name == '.git':
            continue
        relative_copies = [p for p in copies if p.parts[0] == item.name]
        target = destination / item.name
        if relative_copies and item.is_dir():
            overlay(item, target, [Path(*p.parts[1:]) for p in relative_copies])
        elif relative_copies:
            shutil.copyfile(item, target)
        else:
            target.symlink_to(item.resolve(), target_is_directory=item.is_dir())


def run(root):
    return subprocess.run([sys.executable, str(ROOT / 'tools/science_teaching_packs/check_packs.py'),
                           '--root', str(root)], text=True, capture_output=True)


def main():
    baseline = run(ROOT)
    assert baseline.returncode == 0, baseline.stderr
    print('PASS current reviewed classroom editions and archived source provenance')
    controls = [
        ('classroom byte defect', PAGE, 'Classroom source drift'),
        ('wrong reviewed source hash', TARGETS, 'Classroom source drift'),
        ('rewritten historical source', MANIFEST, 'Pack source provenance drift'),
    ]
    for name, relative, message in controls:
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            overlay(ROOT, root, [Path(relative)])
            target = root / relative
            original = target.read_bytes()
            if relative == PAGE:
                target.write_bytes(original + b'\n<p>Planted wrong classroom content</p>\n')
            else:
                document = json.loads(original)
                if relative == TARGETS:
                    next(row for row in document['targets'] if row['path'] == PAGE)['expectedPatchedSha256'] = '0' * 64
                else:
                    document['lessons'][0]['source']['sha256'] = '0' * 64
                target.write_text(json.dumps(document))
            result = run(root)
            assert result.returncode != 0 and message in result.stderr, (name, result.returncode, result.stdout, result.stderr)
            print(f'PASS control: {name}; exit {result.returncode}; {message}')
            target.write_bytes(original)
            restored = run(root)
            assert restored.returncode == 0, restored.stderr
            print(f'PASS restored: {name}; exit {restored.returncode}')


if __name__ == '__main__':
    main()
