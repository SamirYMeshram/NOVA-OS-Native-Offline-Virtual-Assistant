from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class SettingsManagerCapability(Capability):
    spec = CapabilitySpec(
        name='settings_manager',
        domain='system',
        description='Settings manager capability for the system domain.',
        commands=['analyze settings manager', 'plan settings manager', 'execute safe settings manager workflow'],
        permissions=['local.read'],
        risk='low',
        offline=True,
    )

def create_capability():
    return SettingsManagerCapability()
