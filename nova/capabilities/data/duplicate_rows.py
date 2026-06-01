from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class DuplicateRowsCapability(Capability):
    spec = CapabilitySpec(
        name='duplicate_rows',
        domain='data',
        description='Duplicate rows capability for the data domain.',
        commands=['analyze duplicate rows', 'plan duplicate rows', 'execute safe duplicate rows workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return DuplicateRowsCapability()
