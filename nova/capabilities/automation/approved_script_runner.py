from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class ApprovedScriptRunnerCapability(Capability):
    spec = CapabilitySpec(
        name='approved_script_runner',
        domain='automation',
        description='Approved script runner capability for the automation domain.',
        commands=['analyze approved script runner', 'plan approved script runner', 'execute safe approved script runner workflow'],
        permissions=['local.use'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return ApprovedScriptRunnerCapability()
