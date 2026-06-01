from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class DocumentCompareCapability(Capability):
    spec = CapabilitySpec(
        name='document_compare',
        domain='documents',
        description='Document compare capability for the documents domain.',
        commands=['analyze document compare', 'plan document compare', 'execute safe document compare workflow'],
        permissions=['local.read'],
        risk='low',
        offline=True,
    )

def create_capability():
    return DocumentCompareCapability()
