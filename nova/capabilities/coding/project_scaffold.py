from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class ProjectScaffoldCapability(Capability):
    spec = CapabilitySpec(
        name='project_scaffold',
        domain='coding',
        description='Project scaffold capability for the coding domain.',
        commands=['analyze project scaffold', 'plan project scaffold', 'execute safe project scaffold workflow'],
        permissions=['local.use'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return ProjectScaffoldCapability()
