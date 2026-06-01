from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class DisablePluginCapability(Capability):
    spec = CapabilitySpec(
        name='disable_plugin',
        domain='plugins',
        description='Disable plugin capability for the plugins domain.',
        commands=['analyze disable plugin', 'plan disable plugin', 'execute safe disable plugin workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return DisablePluginCapability()
