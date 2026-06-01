from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class DownloadTriageCapability(Capability):
    spec = CapabilitySpec(
        name='download_triage',
        domain='files',
        description='Download triage capability for the files domain.',
        commands=['analyze download triage', 'plan download triage', 'execute safe download triage workflow'],
        permissions=['local.read'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return DownloadTriageCapability()
