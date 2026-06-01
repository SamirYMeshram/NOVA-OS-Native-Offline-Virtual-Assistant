from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class WorkflowPackCapability(Capability):
    spec = CapabilitySpec(
        name='workflow_pack',
        domain='plugins',
        description='Workflow pack capability for the plugins domain.',
        commands=['analyze workflow pack', 'plan workflow pack', 'execute safe workflow pack workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return WorkflowPackCapability()
