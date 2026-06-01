from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class QuoteCitationsCapability(Capability):
    spec = CapabilitySpec(
        name='quote_citations',
        domain='documents',
        description='Quote citations capability for the documents domain.',
        commands=['analyze quote citations', 'plan quote citations', 'execute safe quote citations workflow'],
        permissions=['local.read'],
        risk='low',
        offline=True,
    )

def create_capability():
    return QuoteCitationsCapability()
