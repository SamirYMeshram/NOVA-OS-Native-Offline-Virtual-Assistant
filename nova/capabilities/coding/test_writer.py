from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class TestWriterCapability(Capability):
    spec = CapabilitySpec(
        name='test_writer',
        domain='coding',
        description='Test writer capability for the coding domain.',
        commands=['analyze test writer', 'plan test writer', 'execute safe test writer workflow'],
        permissions=['local.use'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return TestWriterCapability()
