from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class SafeShellReviewCapability(Capability):
    spec = CapabilitySpec(
        name='safe_shell_review',
        domain='automation',
        description='Safe shell review capability for the automation domain.',
        commands=['analyze safe shell review', 'plan safe shell review', 'execute safe safe shell review workflow'],
        permissions=['local.use'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return SafeShellReviewCapability()
