from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class ExportReportCapability(Capability):
    spec = CapabilitySpec(
        name='export_report',
        domain='data',
        description='Export report capability for the data domain.',
        commands=['analyze export report', 'plan export report', 'execute safe export report workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return ExportReportCapability()
