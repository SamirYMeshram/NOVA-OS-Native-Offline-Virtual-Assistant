from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class StudyNotesCapability(Capability):
    spec = CapabilitySpec(
        name='study_notes',
        domain='documents',
        description='Study notes capability for the documents domain.',
        commands=['analyze study notes', 'plan study notes', 'execute safe study notes workflow'],
        permissions=['local.read'],
        risk='low',
        offline=True,
    )

def create_capability():
    return StudyNotesCapability()
