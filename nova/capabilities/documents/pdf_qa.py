from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class PdfQaCapability(Capability):
    spec = CapabilitySpec(
        name='pdf_qa',
        domain='documents',
        description='Pdf qa capability for the documents domain.',
        commands=['analyze pdf qa', 'plan pdf qa', 'execute safe pdf qa workflow'],
        permissions=['local.read'],
        risk='low',
        offline=True,
    )

def create_capability():
    return PdfQaCapability()
