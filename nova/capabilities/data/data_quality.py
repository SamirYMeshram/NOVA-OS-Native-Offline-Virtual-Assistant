from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class DataQualityCapability(Capability):
    spec = CapabilitySpec(
        name='data_quality',
        domain='data',
        description='Data quality capability for the data domain.',
        commands=['analyze data quality', 'plan data quality', 'execute safe data quality workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return DataQualityCapability()
