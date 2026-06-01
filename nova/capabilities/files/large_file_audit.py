from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class LargeFileAuditCapability(Capability):
    spec = CapabilitySpec(
        name='large_file_audit',
        domain='files',
        description='Large file audit capability for the files domain.',
        commands=['analyze large file audit', 'plan large file audit', 'execute safe large file audit workflow'],
        permissions=['local.read'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return LargeFileAuditCapability()
