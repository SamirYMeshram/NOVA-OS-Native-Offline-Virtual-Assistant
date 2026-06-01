from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class CapabilityCatalogCapability(Capability):
    spec = CapabilitySpec(
        name='capability_catalog',
        domain='plugins',
        description='Capability catalog capability for the plugins domain.',
        commands=['analyze capability catalog', 'plan capability catalog', 'execute safe capability catalog workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return CapabilityCatalogCapability()
