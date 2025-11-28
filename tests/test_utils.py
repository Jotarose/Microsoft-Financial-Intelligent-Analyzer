# python
import json

from src import utils


def test_handle_file_path_creates_downloads_dir(tmp_path, monkeypatch):
    # Arrange: fake project structure: <tmp_path>/project/src/utils.py
    fake_utils_file = tmp_path / "project" / "src" / "utils.py"
    fake_utils_file.parent.mkdir(parents=True, exist_ok=True)
    fake_utils_file.write_text("# fake utils file for testing")

    # Point utils.__file__ to the fake path so handle_file_path computes project root under tmp_path
    monkeypatch.setattr(utils, "__file__", str(fake_utils_file))

    # Act
    file_name = "myfile.txt"
    result_path = utils.handle_file_path(file_name)

    # Assert: downloads folder is created under tmp_path/project/downloads
    expected_downloads = tmp_path / "project" / "downloads"
    assert expected_downloads.exists() and expected_downloads.is_dir()
    assert result_path == expected_downloads / file_name


def test_parse_data_mixed_reports():
    reports = [
        {"year": 2020, "data": {"revenue": 100}},
        {"year": 2021, "error": "Tabla no encontrada"},
    ]

    result = utils.parse_data(reports)

    assert result == {
        2020: {"revenue": 100},
        2021: "Tabla no encontrada",
    }


def test_save_data_writes_file(tmp_path):
    report = {"2020": {"a": 1, "b": 2}}
    target = tmp_path / "out.json"

    utils.save_data(str(target), report)

    # Read back and verify
    with open(target, encoding="utf-8") as f:
        loaded = json.load(f)

    assert loaded == report


def test_save_data_handles_permission_error_and_prints_message(monkeypatch, capsys):
    # Arrange: make json.dump raise PermissionError when called inside utils.save_data
    def fake_dump(*args, **kwargs):
        raise PermissionError("denied")

    monkeypatch.setattr(utils.json, "dump", fake_dump)

    # Act
    utils.save_data("irrelevant_path.json", {"x": 1})

    # Capture printed output and assert permission message is present
    captured = capsys.readouterr()
    assert "Permiso denegado" in captured.out or "Permiso" in captured.out
