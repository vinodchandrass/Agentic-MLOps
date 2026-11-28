from pathlib import Path
import json, subprocess, sys, tempfile, shutil
root = Path(__file__).resolve().parent
scripts = ('AMEAF_Phase_C/validate_properties.py', 'AMEAF_Phase_D/robustness.py', 'AMEAF_Phase_E/analyse.py')
for name in scripts:
    script = root / 'reproducibility' / name
    reference = script.parent / 'results.json'
    original = reference.read_bytes()
    expected = json.loads(original)
    with tempfile.TemporaryDirectory() as tmp:
        isolated = Path(tmp) / script.name
        shutil.copyfile(script, isolated)
        actual = json.loads(subprocess.check_output([sys.executable, '-B', str(isolated)], cwd=tmp))
    if actual != expected or reference.read_bytes() != original:
        raise SystemExit(f'Mismatch: {name}')
    print(f'PASS: {name}')
