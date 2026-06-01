from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class OpenFolderCapability(Capability):
    spec = CapabilitySpec(
        name='open_folder',
        domain='automation',
        description='Open folder capability for the automation domain.',
        commands=['analyze open folder', 'plan open folder', 'execute safe open folder workflow'],
        permissions=['local.use'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return OpenFolderCapability()
