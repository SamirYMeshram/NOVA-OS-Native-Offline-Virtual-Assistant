from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class WorkspaceCreatorCapability(Capability):
    spec = CapabilitySpec(
        name='workspace_creator',
        domain='files',
        description='Workspace creator capability for the files domain.',
        commands=['analyze workspace creator', 'plan workspace creator', 'execute safe workspace creator workflow'],
        permissions=['local.read'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return WorkspaceCreatorCapability()
