from nova.capabilities.registry import load_capabilities, capability_index

def test_capability_catalog():
    caps = load_capabilities()
    assert len(caps) >= 80
    idx = capability_index()
    assert 'pdf_qa' in idx
