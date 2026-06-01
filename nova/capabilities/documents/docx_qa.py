from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class DocxQaCapability(Capability):
    spec = CapabilitySpec(
        name='docx_qa',
        domain='documents',
        description='Docx qa capability for the documents domain.',
        commands=['analyze docx qa', 'plan docx qa', 'execute safe docx qa workflow'],
        permissions=['local.read'],
        risk='low',
        offline=True,
    )

def create_capability():
    return DocxQaCapability()
