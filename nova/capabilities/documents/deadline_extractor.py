from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class DeadlineExtractorCapability(Capability):
    spec = CapabilitySpec(
        name='deadline_extractor',
        domain='documents',
        description='Deadline extractor capability for the documents domain.',
        commands=['analyze deadline extractor', 'plan deadline extractor', 'execute safe deadline extractor workflow'],
        permissions=['local.read'],
        risk='low',
        offline=True,
    )

def create_capability():
    return DeadlineExtractorCapability()
