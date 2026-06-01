from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class TasksCapability(Capability):
    spec = CapabilitySpec(
        name='tasks',
        domain='productivity',
        description='Tasks capability for the productivity domain.',
        commands=['analyze tasks', 'plan tasks', 'execute safe tasks workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return TasksCapability()
