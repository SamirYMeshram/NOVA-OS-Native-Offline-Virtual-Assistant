from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class PermissionModelCapability(Capability):
    spec = CapabilitySpec(
        name='permission_model',
        domain='plugins',
        description='Permission model capability for the plugins domain.',
        commands=['analyze permission model', 'plan permission model', 'execute safe permission model workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return PermissionModelCapability()
