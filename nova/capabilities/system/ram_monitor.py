from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class RamMonitorCapability(Capability):
    spec = CapabilitySpec(
        name='ram_monitor',
        domain='system',
        description='Ram monitor capability for the system domain.',
        commands=['analyze ram monitor', 'plan ram monitor', 'execute safe ram monitor workflow'],
        permissions=['local.read'],
        risk='low',
        offline=True,
    )

def create_capability():
    return RamMonitorCapability()
