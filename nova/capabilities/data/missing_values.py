from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class MissingValuesCapability(Capability):
    spec = CapabilitySpec(
        name='missing_values',
        domain='data',
        description='Missing values capability for the data domain.',
        commands=['analyze missing values', 'plan missing values', 'execute safe missing values workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return MissingValuesCapability()
