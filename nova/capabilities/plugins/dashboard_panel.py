from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class DashboardPanelCapability(Capability):
    spec = CapabilitySpec(
        name='dashboard_panel',
        domain='plugins',
        description='Dashboard panel capability for the plugins domain.',
        commands=['analyze dashboard panel', 'plan dashboard panel', 'execute safe dashboard panel workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return DashboardPanelCapability()
