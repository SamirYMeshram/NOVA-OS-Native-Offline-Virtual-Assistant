from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class NoiseHandlingCapability(Capability):
    spec = CapabilitySpec(
        name='noise_handling',
        domain='voice',
        description='Noise handling capability for the voice domain.',
        commands=['analyze noise handling', 'plan noise handling', 'execute safe noise handling workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return NoiseHandlingCapability()
