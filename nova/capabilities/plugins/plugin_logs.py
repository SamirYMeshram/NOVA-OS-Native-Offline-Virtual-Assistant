from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class PluginLogsCapability(Capability):
    spec = CapabilitySpec(
        name='plugin_logs',
        domain='plugins',
        description='Plugin logs capability for the plugins domain.',
        commands=['analyze plugin logs', 'plan plugin logs', 'execute safe plugin logs workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return PluginLogsCapability()
