# memorycore/tokenizer_lite.py

import re

class LiteTokenizer:
    def __init__(self):
        pass  # No model loading needed

    def encode(self, text):
        # Very basic split on spaces + some punctuation handling
        words = re.findall(r'\b\w+\b', text.lower())
        ids = [hash(word) % 10000 for word in words]  # simple hash to IDs
        return ids

    def decode(self, ids):
        # In real symbolic core, you can't fully decode hashes.
        return "[Decoded {} tokens]".format(len(ids))

    def to_bytes(self, token_ids):
        return b"".join(tid.to_bytes(4, 'little') for tid in token_ids)

    def from_bytes(self, byte_data):
        return [int.from_bytes(byte_data[i:i+4], 'little') for i in range(0, len(byte_data), 4)]
