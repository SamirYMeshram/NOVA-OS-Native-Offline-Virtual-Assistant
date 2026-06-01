from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class DuplicateDetectionCapability(Capability):
    spec = CapabilitySpec(
        name='duplicate_detection',
        domain='files',
        description='Duplicate detection capability for the files domain.',
        commands=['analyze duplicate detection', 'plan duplicate detection', 'execute safe duplicate detection workflow'],
        permissions=['local.read'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return DuplicateDetectionCapability()
