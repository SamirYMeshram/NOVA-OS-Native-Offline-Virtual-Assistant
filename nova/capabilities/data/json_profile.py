from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class JsonProfileCapability(Capability):
    spec = CapabilitySpec(
        name='json_profile',
        domain='data',
        description='Json profile capability for the data domain.',
        commands=['analyze json profile', 'plan json profile', 'execute safe json profile workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return JsonProfileCapability()
