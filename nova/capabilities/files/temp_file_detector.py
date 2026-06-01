from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class TempFileDetectorCapability(Capability):
    spec = CapabilitySpec(
        name='temp_file_detector',
        domain='files',
        description='Temp file detector capability for the files domain.',
        commands=['analyze temp file detector', 'plan temp file detector', 'execute safe temp file detector workflow'],
        permissions=['local.read'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return TempFileDetectorCapability()
