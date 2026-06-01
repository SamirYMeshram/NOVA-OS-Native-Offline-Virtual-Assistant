from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class CodeReviewerCapability(Capability):
    spec = CapabilitySpec(
        name='code_reviewer',
        domain='coding',
        description='Code reviewer capability for the coding domain.',
        commands=['analyze code reviewer', 'plan code reviewer', 'execute safe code reviewer workflow'],
        permissions=['local.use'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return CodeReviewerCapability()
