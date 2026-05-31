from nova.router.classifier import IntentClassifier
from nova.router.intents import Intent

def test_classifier():
    c = IntentClassifier()
    assert c.classify('remember that I like local AI') == Intent.MEMORY_SAVE
    assert c.classify('scan files ./Downloads') == Intent.FILE_SCAN
    assert c.classify('clean my downloads folder') == Intent.FILE_ORGANIZE
