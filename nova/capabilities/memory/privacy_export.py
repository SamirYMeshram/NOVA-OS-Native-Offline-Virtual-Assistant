from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class PrivacyExportCapability(Capability):
    spec = CapabilitySpec(
        name='privacy_export',
        domain='memory',
        description='Privacy export capability for the memory domain.',
        commands=['analyze privacy export', 'plan privacy export', 'execute safe privacy export workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return PrivacyExportCapability()
