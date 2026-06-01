from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class PushToTalkCapability(Capability):
    spec = CapabilitySpec(
        name='push_to_talk',
        domain='voice',
        description='Push to talk capability for the voice domain.',
        commands=['analyze push to talk', 'plan push to talk', 'execute safe push to talk workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return PushToTalkCapability()
