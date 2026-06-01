from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class SecurityReviewCapability(Capability):
    spec = CapabilitySpec(
        name='security_review',
        domain='coding',
        description='Security review capability for the coding domain.',
        commands=['analyze security review', 'plan security review', 'execute safe security review workflow'],
        permissions=['local.use'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return SecurityReviewCapability()
