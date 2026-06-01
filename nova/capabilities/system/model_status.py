from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class ModelStatusCapability(Capability):
    spec = CapabilitySpec(
        name='model_status',
        domain='system',
        description='Model status capability for the system domain.',
        commands=['analyze model status', 'plan model status', 'execute safe model status workflow'],
        permissions=['local.read'],
        risk='low',
        offline=True,
    )

def create_capability():
    return ModelStatusCapability()
