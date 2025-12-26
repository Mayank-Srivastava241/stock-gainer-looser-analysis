import csv
import pathlib

import package.transform_csv_create as t


def test_create_csv_creates_files_and_uploads(tmp_path, monkeypatch):
    # Run inside a temporary working directory so we don't modify repo files
    monkeypatch.chdir(tmp_path)

    # Prepare the Data directory
    (tmp_path / 'Data').mkdir()

    # Monkeypatch network-heavy or brittle functions
    monkeypatch.setattr(t, 'fetch_nse_gainer_data', lambda: 'dummy')
    monkeypatch.setattr(t, 'fetch_nse_looser_data', lambda: 'dummy')
    # Make process_data return deterministic small data
    monkeypatch.setattr(t, 'process_data', lambda data: [['SYM1', '10'], ['SYM2', '20']])

    calls = []
    monkeypatch.setattr(t, 'upload_to_cloud', lambda name, file_id: calls.append(name))

    t.create_csv()

    assert (tmp_path / 'Data' / 'gdata.csv').exists()
    assert (tmp_path / 'Data' / 'ldata.csv').exists()
    assert 'gainer' in calls and 'looser' in calls
