from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class MemoryPruningCapability(Capability):
    spec = CapabilitySpec(
        name='memory_pruning',
        domain='memory',
        description='Memory pruning capability for the memory domain.',
        commands=['analyze memory pruning', 'plan memory pruning', 'execute safe memory pruning workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return MemoryPruningCapability()
