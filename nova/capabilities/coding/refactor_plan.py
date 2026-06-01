from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class RefactorPlanCapability(Capability):
    spec = CapabilitySpec(
        name='refactor_plan',
        domain='coding',
        description='Refactor plan capability for the coding domain.',
        commands=['analyze refactor plan', 'plan refactor plan', 'execute safe refactor plan workflow'],
        permissions=['local.use'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return RefactorPlanCapability()
