from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class RemindersCapability(Capability):
    spec = CapabilitySpec(
        name='reminders',
        domain='productivity',
        description='Reminders capability for the productivity domain.',
        commands=['analyze reminders', 'plan reminders', 'execute safe reminders workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return RemindersCapability()
