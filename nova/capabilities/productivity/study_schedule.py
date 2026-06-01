from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class StudyScheduleCapability(Capability):
    spec = CapabilitySpec(
        name='study_schedule',
        domain='productivity',
        description='Study schedule capability for the productivity domain.',
        commands=['analyze study schedule', 'plan study schedule', 'execute safe study schedule workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return StudyScheduleCapability()
