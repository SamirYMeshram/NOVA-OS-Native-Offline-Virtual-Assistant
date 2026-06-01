from __future__ import annotations
from nova.capabilities.base import Capability, CapabilitySpec

class ScreenshotCaptureCapability(Capability):
    spec = CapabilitySpec(
        name='screenshot_capture',
        domain='automation',
        description='Screenshot capture capability for the automation domain.',
        commands=['analyze screenshot capture', 'plan screenshot capture', 'execute safe screenshot capture workflow'],
        permissions=['local.use'],
        risk='medium',
        offline=True,
    )

def create_capability():
    return ScreenshotCaptureCapability()
