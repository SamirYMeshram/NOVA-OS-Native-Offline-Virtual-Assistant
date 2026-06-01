from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class WorkflowMemoryCapability(Capability):
    spec = CapabilitySpec(
        name='workflow_memory',
        domain='memory',
        description='Workflow memory capability for the memory domain.',
        commands=['analyze workflow memory', 'plan workflow memory', 'execute safe workflow memory workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return WorkflowMemoryCapability()
