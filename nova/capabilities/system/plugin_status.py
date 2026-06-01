from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class PluginStatusCapability(Capability):
    spec = CapabilitySpec(
        name='plugin_status',
        domain='system',
        description='Plugin status capability for the system domain.',
        commands=['analyze plugin status', 'plan plugin status', 'execute safe plugin status workflow'],
        permissions=['local.read'],
        risk='low',
        offline=True,
    )

def create_capability():
    return PluginStatusCapability()
