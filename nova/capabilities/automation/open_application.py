from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class OpenApplicationCapability(Capability):
    spec = CapabilitySpec(
        name='open_application',
        domain='automation',
        description='Open application capability for the automation domain.',
        commands=['analyze open application', 'plan open application', 'execute safe open application workflow'],
        permissions=['local.use'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return OpenApplicationCapability()
