from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class StatisticsReportCapability(Capability):
    spec = CapabilitySpec(
        name='statistics_report',
        domain='data',
        description='Statistics report capability for the data domain.',
        commands=['analyze statistics report', 'plan statistics report', 'execute safe statistics report workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return StatisticsReportCapability()
