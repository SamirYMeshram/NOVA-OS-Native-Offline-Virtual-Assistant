from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class OfflineSttCapability(Capability):
    spec = CapabilitySpec(
        name='offline_stt',
        domain='voice',
        description='Offline stt capability for the voice domain.',
        commands=['analyze offline stt', 'plan offline stt', 'execute safe offline stt workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return OfflineSttCapability()
