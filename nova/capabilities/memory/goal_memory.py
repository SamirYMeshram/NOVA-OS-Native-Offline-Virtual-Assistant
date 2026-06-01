from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class GoalMemoryCapability(Capability):
    spec = CapabilitySpec(
        name='goal_memory',
        domain='memory',
        description='Goal memory capability for the memory domain.',
        commands=['analyze goal memory', 'plan goal memory', 'execute safe goal memory workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return GoalMemoryCapability()
