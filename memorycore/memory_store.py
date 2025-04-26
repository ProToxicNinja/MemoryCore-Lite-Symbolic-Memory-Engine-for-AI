import json
import uuid
import os
from datetime import datetime, timezone

from memorycore.symbolic_core import MemoryCore  # ✅ This is fine

MEMORY_PATH = os.path.join("memorycore", "symbolic_memory.jsonl")

class MemoryStore:
    def __init__(self, path=MEMORY_PATH):
        self.path = path
        self.core = MemoryCore("memorycore/assets/sp64k.model")
        if not os.path.exists(self.path):
            with open(self.path, 'w') as f:
                pass
    
    def save_thought(self, input_text, token_ids, bytecode, tags=None):
        tags = tags or []
        memory = {
            "id": str(uuid.uuid4()),
            "input_text": input_text,
            "token_ids": token_ids,
            "bytecode": bytecode.hex(),
            "tags": tags,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        with open(self.path, "a") as f:
            f.write(json.dumps(memory) + "\n")
    
    def load_memory(self):
        with open(self.path, "r") as f:
            return [json.loads(line) for line in f if line.strip()]
    
    def get_by_tag(self, tag):
        return [entry for entry in self.load_memory() if tag in entry.get("tags", [])]
    
    def search_by_token(self, token_id):
        return [entry for entry in self.load_memory() if token_id in entry.get("token_ids", [])]
    
    def export_bin(self, memory_id):
        for entry in self.load_memory():
            if entry["id"] == memory_id:
                return bytes.fromhex(entry["bytecode"])
        return None
    
    def import_bin(self, input_text, token_ids, bin_data, tags=None):
        self.save_thought(input_text, token_ids, bin_data, tags)
    
    def encode_and_store(self, input_text, tags=None):
        token_ids = self.core.encode(input_text)
        bytecode = self.core.to_bytes(token_ids)
        
        if tags is None:
            tags = []
            lowered = input_text.lower()
            if any(word in lowered for word in ["star", "galaxy", "moon", "space"]):
                tags.append("cosmic")
            if any(word in lowered for word in ["remember", "recall", "forgot"]):
                tags.append("memory")
            if any(word in lowered for word in ["battle", "war", "fight", "fell"]):
                tags.append("conflict")
            if any(word in lowered for word in ["name", "legend", "legacy"]):
                tags.append("legacy")
        
        self.save_thought(input_text, token_ids, bytecode, tags)



