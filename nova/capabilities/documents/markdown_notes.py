from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class MarkdownNotesCapability(Capability):
    spec = CapabilitySpec(
        name='markdown_notes',
        domain='documents',
        description='Markdown notes capability for the documents domain.',
        commands=['analyze markdown notes', 'plan markdown notes', 'execute safe markdown notes workflow'],
        permissions=['local.read'],
        risk='low',
        offline=True,
    )

def create_capability():
    return MarkdownNotesCapability()
