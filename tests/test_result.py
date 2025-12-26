import csv
from pathlib import Path

import package.result as r


def _write_csv(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Symbol'])
        for s in rows:
            writer.writerow([s])


def test_comparison_creates_result(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    _write_csv(tmp_path / 'Data' / 'gdata.csv', ['A', 'B'])
    _write_csv(tmp_path / 'Data' / 'gdata_prev.csv', ['B', 'C'])
    _write_csv(tmp_path / 'Data' / 'ldata.csv', ['X', 'Y'])
    _write_csv(tmp_path / 'Data' / 'ldata_prev.csv', ['Y', 'Z'])

    calls = []
    monkeypatch.setattr(r, 'upload_to_cloud', lambda name, file_id: calls.append(name))

    r.comparison()

    assert (tmp_path / 'Data' / 'comparison_result.csv').exists()
    assert 'result' in calls
