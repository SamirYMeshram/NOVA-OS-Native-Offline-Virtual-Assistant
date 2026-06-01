from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class ExamQuizCapability(Capability):
    spec = CapabilitySpec(
        name='exam_quiz',
        domain='productivity',
        description='Exam quiz capability for the productivity domain.',
        commands=['analyze exam quiz', 'plan exam quiz', 'execute safe exam quiz workflow'],
        permissions=['local.use'],
        risk='low',
        offline=True,
    )

def create_capability():
    return ExamQuizCapability()
