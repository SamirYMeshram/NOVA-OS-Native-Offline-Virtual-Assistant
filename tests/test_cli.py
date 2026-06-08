from nova.cli import main
from nova.config import NovaConfig
import os

def test_cli_status(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("NOVA_HOME", str(tmp_path))
    main(["status"])
    out = capsys.readouterr().out
    assert "nova_home" in out

def test_cli_think(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("NOVA_HOME", str(tmp_path))
    main(["think", "scan", "this", "folder"])
    assert "file.scan" in capsys.readouterr().out
