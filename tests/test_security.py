from nova.core.security import evaluate_shell_command, is_protected_path

def test_blocks_dangerous_shell():
    d = evaluate_shell_command('rm -rf /')
    assert not d.allowed
    assert d.risk in {'high','critical'}

def test_allows_echo():
    d = evaluate_shell_command('echo hello')
    assert d.allowed
