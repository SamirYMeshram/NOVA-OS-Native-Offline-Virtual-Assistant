from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class ToolRegistryCapability(Capability):
    spec = CapabilitySpec(
        name='tool_registry',
        domain='plugins',
        description='Tool registry capability for the plugins domain.',
        commands=['analyze tool registry', 'plan tool registry', 'execute safe tool registry workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return ToolRegistryCapability()
