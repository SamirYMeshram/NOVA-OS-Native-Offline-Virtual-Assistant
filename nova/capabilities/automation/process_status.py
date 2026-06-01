from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class ProcessStatusCapability(Capability):
    spec = CapabilitySpec(
        name='process_status',
        domain='automation',
        description='Process status capability for the automation domain.',
        commands=['analyze process status', 'plan process status', 'execute safe process status workflow'],
        permissions=['local.use'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return ProcessStatusCapability()
