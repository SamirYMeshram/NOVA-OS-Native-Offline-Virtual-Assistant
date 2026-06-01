from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class FastapiGeneratorCapability(Capability):
    spec = CapabilitySpec(
        name='fastapi_generator',
        domain='coding',
        description='Fastapi generator capability for the coding domain.',
        commands=['analyze fastapi generator', 'plan fastapi generator', 'execute safe fastapi generator workflow'],
        permissions=['local.use'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return FastapiGeneratorCapability()
