from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class CliGeneratorCapability(Capability):
    spec = CapabilitySpec(
        name='cli_generator',
        domain='coding',
        description='Cli generator capability for the coding domain.',
        commands=['analyze cli generator', 'plan cli generator', 'execute safe cli generator workflow'],
        permissions=['local.use'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return CliGeneratorCapability()
