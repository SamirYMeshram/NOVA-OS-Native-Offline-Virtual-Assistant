from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class BugHunterCapability(Capability):
    spec = CapabilitySpec(
        name='bug_hunter',
        domain='coding',
        description='Bug hunter capability for the coding domain.',
        commands=['analyze bug hunter', 'plan bug hunter', 'execute safe bug hunter workflow'],
        permissions=['local.use'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return BugHunterCapability()
