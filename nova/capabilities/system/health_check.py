from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class HealthCheckCapability(Capability):
    spec = CapabilitySpec(
        name='health_check',
        domain='system',
        description='Health check capability for the system domain.',
        commands=['analyze health check', 'plan health check', 'execute safe health check workflow'],
        permissions=['local.read'],
        risk='low',
        offline=True,
    )

def create_capability():
    return HealthCheckCapability()
