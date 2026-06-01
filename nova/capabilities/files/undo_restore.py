from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class UndoRestoreCapability(Capability):
    spec = CapabilitySpec(
        name='undo_restore',
        domain='files',
        description='Undo restore capability for the files domain.',
        commands=['analyze undo restore', 'plan undo restore', 'execute safe undo restore workflow'],
        permissions=['local.read'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return UndoRestoreCapability()
