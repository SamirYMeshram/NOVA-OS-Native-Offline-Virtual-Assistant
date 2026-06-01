from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class SemanticFileSearchCapability(Capability):
    spec = CapabilitySpec(
        name='semantic_file_search',
        domain='files',
        description='Semantic file search capability for the files domain.',
        commands=['analyze semantic file search', 'plan semantic file search', 'execute safe semantic file search workflow'],
        permissions=['local.read'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return SemanticFileSearchCapability()
