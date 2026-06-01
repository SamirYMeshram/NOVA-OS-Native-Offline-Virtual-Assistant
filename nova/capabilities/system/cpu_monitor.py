from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class CpuMonitorCapability(Capability):
    spec = CapabilitySpec(
        name='cpu_monitor',
        domain='system',
        description='Cpu monitor capability for the system domain.',
        commands=['analyze cpu monitor', 'plan cpu monitor', 'execute safe cpu monitor workflow'],
        permissions=['local.read'],
        risk='low',
        offline=True,
    )

def create_capability():
    return CpuMonitorCapability()
