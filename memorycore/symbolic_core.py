# symbolic_core.py

from memorycore.tokenizer_lite import LiteTokenizer

class MemoryCore:
    def __init__(self, model_path="memorycore/assets/sp64k.model"):
        self.tokenizer = LiteTokenizer()

    def encode(self, text):
        return self.tokenizer.encode(text)

    def decode(self, ids):
        return self.tokenizer.decode(ids)

    def to_bytes(self, ids):
        return self.tokenizer.to_bytes(ids)

    def from_bytes(self, byte_data):
        return self.tokenizer.from_bytes(byte_data)
