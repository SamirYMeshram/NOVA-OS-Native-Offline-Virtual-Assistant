from nova.cli import main

def test_cli_status(capsys):
    main(['status'])
    out = capsys.readouterr().out
    assert 'python' in out

def test_cli_route(capsys):
    main(['route','analyze project folder'])
    assert 'code.analyze' in capsys.readouterr().out
