from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class WeeklyReviewCapability(Capability):
    spec = CapabilitySpec(
        name='weekly_review',
        domain='productivity',
        description='Weekly review capability for the productivity domain.',
        commands=['analyze weekly review', 'plan weekly review', 'execute safe weekly review workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return WeeklyReviewCapability()
