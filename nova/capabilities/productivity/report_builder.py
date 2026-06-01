from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class ReportBuilderCapability(Capability):
    spec = CapabilitySpec(
        name='report_builder',
        domain='productivity',
        description='Report builder capability for the productivity domain.',
        commands=['analyze report builder', 'plan report builder', 'execute safe report builder workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return ReportBuilderCapability()
