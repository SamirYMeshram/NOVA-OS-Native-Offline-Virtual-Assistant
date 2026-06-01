from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class ProjectHistoryCapability(Capability):
    spec = CapabilitySpec(
        name='project_history',
        domain='memory',
        description='Project history capability for the memory domain.',
        commands=['analyze project history', 'plan project history', 'execute safe project history workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return ProjectHistoryCapability()
