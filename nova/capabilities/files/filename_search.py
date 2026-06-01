from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class FilenameSearchCapability(Capability):
    spec = CapabilitySpec(
        name='filename_search',
        domain='files',
        description='Filename search capability for the files domain.',
        commands=['analyze filename search', 'plan filename search', 'execute safe filename search workflow'],
        permissions=['local.read'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return FilenameSearchCapability()
