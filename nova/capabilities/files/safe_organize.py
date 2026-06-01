from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class SafeOrganizeCapability(Capability):
    spec = CapabilitySpec(
        name='safe_organize',
        domain='files',
        description='Safe organize capability for the files domain.',
        commands=['analyze safe organize', 'plan safe organize', 'execute safe safe organize workflow'],
        permissions=['local.read'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return SafeOrganizeCapability()
