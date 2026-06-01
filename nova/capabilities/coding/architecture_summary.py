from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class ArchitectureSummaryCapability(Capability):
    spec = CapabilitySpec(
        name='architecture_summary',
        domain='coding',
        description='Architecture summary capability for the coding domain.',
        commands=['analyze architecture summary', 'plan architecture summary', 'execute safe architecture summary workflow'],
        permissions=['local.use'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return ArchitectureSummaryCapability()
