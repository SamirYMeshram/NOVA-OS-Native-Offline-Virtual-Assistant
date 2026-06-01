from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class PluginLoaderCapability(Capability):
    spec = CapabilitySpec(
        name='plugin_loader',
        domain='plugins',
        description='Plugin loader capability for the plugins domain.',
        commands=['analyze plugin loader', 'plan plugin loader', 'execute safe plugin loader workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return PluginLoaderCapability()
