from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class ReadmeWriterCapability(Capability):
    spec = CapabilitySpec(
        name='readme_writer',
        domain='coding',
        description='Readme writer capability for the coding domain.',
        commands=['analyze readme writer', 'plan readme writer', 'execute safe readme writer workflow'],
        permissions=['local.use'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return ReadmeWriterCapability()
