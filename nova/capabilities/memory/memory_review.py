from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class MemoryReviewCapability(Capability):
    spec = CapabilitySpec(
        name='memory_review',
        domain='memory',
        description='Memory review capability for the memory domain.',
        commands=['analyze memory review', 'plan memory review', 'execute safe memory review workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return MemoryReviewCapability()
