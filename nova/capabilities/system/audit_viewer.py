from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class AuditViewerCapability(Capability):
    spec = CapabilitySpec(
        name='audit_viewer',
        domain='system',
        description='Audit viewer capability for the system domain.',
        commands=['analyze audit viewer', 'plan audit viewer', 'execute safe audit viewer workflow'],
        permissions=['local.read'],
        risk='low',
        offline=True,
    )

def create_capability():
    return AuditViewerCapability()
