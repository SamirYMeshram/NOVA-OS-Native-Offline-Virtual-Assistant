from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class DiskMonitorCapability(Capability):
    spec = CapabilitySpec(
        name='disk_monitor',
        domain='system',
        description='Disk monitor capability for the system domain.',
        commands=['analyze disk monitor', 'plan disk monitor', 'execute safe disk monitor workflow'],
        permissions=['local.read'],
        risk='low',
        offline=True,
    )

def create_capability():
    return DiskMonitorCapability()
