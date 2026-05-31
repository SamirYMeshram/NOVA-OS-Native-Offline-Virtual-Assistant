from nova.security.command_policy import CommandPolicy
from nova.security.redaction import redact_secrets

def test_command_policy_blocks_dangerous():
    a = CommandPolicy().assess('rm -rf /')
    assert not a.allowed

def test_redaction():
    assert '<REDACTED>' in redact_secrets('api_key=abc123456789')
