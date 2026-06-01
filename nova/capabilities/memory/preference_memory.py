from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class PreferenceMemoryCapability(Capability):
    spec = CapabilitySpec(
        name='preference_memory',
        domain='memory',
        description='Preference memory capability for the memory domain.',
        commands=['analyze preference memory', 'plan preference memory', 'execute safe preference memory workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return PreferenceMemoryCapability()
