from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class OldFileAuditCapability(Capability):
    spec = CapabilitySpec(
        name='old_file_audit',
        domain='files',
        description='Old file audit capability for the files domain.',
        commands=['analyze old file audit', 'plan old file audit', 'execute safe old file audit workflow'],
        permissions=['local.read'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return OldFileAuditCapability()
