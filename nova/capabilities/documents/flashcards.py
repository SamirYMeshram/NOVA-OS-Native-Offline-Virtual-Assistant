from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class FlashcardsCapability(Capability):
    spec = CapabilitySpec(
        name='flashcards',
        domain='documents',
        description='Flashcards capability for the documents domain.',
        commands=['analyze flashcards', 'plan flashcards', 'execute safe flashcards workflow'],
        permissions=['local.read'],
        risk='low',
        offline=True,
    )

def create_capability():
    return FlashcardsCapability()
