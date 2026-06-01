from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class DesktopShortcutsCapability(Capability):
    spec = CapabilitySpec(
        name='desktop_shortcuts',
        domain='automation',
        description='Desktop shortcuts capability for the automation domain.',
        commands=['analyze desktop shortcuts', 'plan desktop shortcuts', 'execute safe desktop shortcuts workflow'],
        permissions=['local.use'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return DesktopShortcutsCapability()
