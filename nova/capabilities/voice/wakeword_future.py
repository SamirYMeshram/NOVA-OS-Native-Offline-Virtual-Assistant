from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class WakewordFutureCapability(Capability):
    spec = CapabilitySpec(
        name='wakeword_future',
        domain='voice',
        description='Wakeword future capability for the voice domain.',
        commands=['analyze wakeword future', 'plan wakeword future', 'execute safe wakeword future workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return WakewordFutureCapability()
