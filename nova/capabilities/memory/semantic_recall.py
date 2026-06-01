from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class SemanticRecallCapability(Capability):
    spec = CapabilitySpec(
        name='semantic_recall',
        domain='memory',
        description='Semantic recall capability for the memory domain.',
        commands=['analyze semantic recall', 'plan semantic recall', 'execute safe semantic recall workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return SemanticRecallCapability()
