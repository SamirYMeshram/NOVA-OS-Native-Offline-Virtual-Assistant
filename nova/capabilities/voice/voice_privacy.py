from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class VoicePrivacyCapability(Capability):
    spec = CapabilitySpec(
        name='voice_privacy',
        domain='voice',
        description='Voice privacy capability for the voice domain.',
        commands=['analyze voice privacy', 'plan voice privacy', 'execute safe voice privacy workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return VoicePrivacyCapability()
