"""Tests for utility helpers in utils module."""
import builtins
from pathlib import Path
import importlib.util
import pytest

# Load utils module from repository root
utils_path = Path(__file__).resolve().parents[1] / "utils.py"
spec = importlib.util.spec_from_file_location("utils", utils_path)
utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utils)

get_file_path = utils.get_file_path
normalize_path = utils.normalize_path


def test_get_file_path(monkeypatch):
    user_input = "~/sample/file.txt"
    monkeypatch.setattr(builtins, "input", lambda _: user_input)
    result = get_file_path()
    assert result == Path(user_input).expanduser()


def test_normalize_path_absolute(tmp_path):
    file = tmp_path / "data.txt"
    file.write_text("content")
    assert normalize_path(file) == file.resolve()


def test_normalize_path_relative(tmp_path, monkeypatch):
    file = tmp_path / "data.txt"
    file.write_text("content")
    monkeypatch.chdir(tmp_path)
    assert normalize_path(Path("data.txt")) == file.resolve()


def test_normalize_path_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(FileNotFoundError):
        normalize_path(Path("absent.txt"))
