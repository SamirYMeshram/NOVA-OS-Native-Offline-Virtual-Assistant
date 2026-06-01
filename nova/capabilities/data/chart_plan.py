from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class ChartPlanCapability(Capability):
    spec = CapabilitySpec(
        name='chart_plan',
        domain='data',
        description='Chart plan capability for the data domain.',
        commands=['analyze chart plan', 'plan chart plan', 'execute safe chart plan workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return ChartPlanCapability()
