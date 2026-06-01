import os
from pathlib import Path
import pytest

@pytest.fixture(autouse=True)
def nova_home(tmp_path, monkeypatch):
    monkeypatch.setenv('NOVA_HOME', str(tmp_path/'.nova'))
