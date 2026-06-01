from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class TableExtractionCapability(Capability):
    spec = CapabilitySpec(
        name='table_extraction',
        domain='documents',
        description='Table extraction capability for the documents domain.',
        commands=['analyze table extraction', 'plan table extraction', 'execute safe table extraction workflow'],
        permissions=['local.read'],
        risk='low',
        offline=True,
    )

def create_capability():
    return TableExtractionCapability()
