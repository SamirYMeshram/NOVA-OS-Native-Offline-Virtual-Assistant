from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class OfflineTtsCapability(Capability):
    spec = CapabilitySpec(
        name='offline_tts',
        domain='voice',
        description='Offline tts capability for the voice domain.',
        commands=['analyze offline tts', 'plan offline tts', 'execute safe offline tts workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return OfflineTtsCapability()
