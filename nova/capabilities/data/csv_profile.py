from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class CsvProfileCapability(Capability):
    spec = CapabilitySpec(
        name='csv_profile',
        domain='data',
        description='Csv profile capability for the data domain.',
        commands=['analyze csv profile', 'plan csv profile', 'execute safe csv profile workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return CsvProfileCapability()
