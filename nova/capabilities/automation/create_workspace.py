from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class CreateWorkspaceCapability(Capability):
    spec = CapabilitySpec(
        name='create_workspace',
        domain='automation',
        description='Create workspace capability for the automation domain.',
        commands=['analyze create workspace', 'plan create workspace', 'execute safe create workspace workflow'],
        permissions=['local.use'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return CreateWorkspaceCapability()
