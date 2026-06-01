from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class CalendarExportCapability(Capability):
    spec = CapabilitySpec(
        name='calendar_export',
        domain='productivity',
        description='Calendar export capability for the productivity domain.',
        commands=['analyze calendar export', 'plan calendar export', 'execute safe calendar export workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return CalendarExportCapability()
