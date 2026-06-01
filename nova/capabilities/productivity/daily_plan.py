from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class DailyPlanCapability(Capability):
    spec = CapabilitySpec(
        name='daily_plan',
        domain='productivity',
        description='Daily plan capability for the productivity domain.',
        commands=['analyze daily plan', 'plan daily plan', 'execute safe daily plan workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return DailyPlanCapability()
