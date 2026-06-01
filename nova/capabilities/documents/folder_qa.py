from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class FolderQaCapability(Capability):
    spec = CapabilitySpec(
        name='folder_qa',
        domain='documents',
        description='Folder qa capability for the documents domain.',
        commands=['analyze folder qa', 'plan folder qa', 'execute safe folder qa workflow'],
        permissions=['local.read'],
        risk='low',
        offline=True,
    )

def create_capability():
    return FolderQaCapability()
