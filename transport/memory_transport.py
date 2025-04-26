from transport.sync_protocol import SyncProtocol
import binascii

class MemoryTransport:
    def __init__(self):
        pass

    def prepare_memory(self, memory_entry):
        """
        Takes a memory dictionary and prepares it for sending.
        """
        memory_id = memory_entry["id"]
        bytecode = bytes.fromhex(memory_entry["bytecode"])
        tags = memory_entry.get("tags", [])
        origin = "local"  # or dynamic node name

        packet = SyncProtocol.create_packet(memory_id, bytecode, tags, origin)
        return SyncProtocol.encode_packet(packet)

    def load_memory_from_bin(self, data_bytes):
        """
        Takes received bytes and decodes into a memory dictionary.
        """
        packet = SyncProtocol.decode_packet(data_bytes)
        memory = {
            "id": packet["id"],
            "bytecode": packet["bytecode"],
            "tags": packet.get("tags", []),
            "origin": packet.get("origin", "unknown")
        }
        return memory

    def hash_memory(self, memory_entry):
        """
        Compute a quick hash of a memory for deduplication.
        """
        packet = {
            "id": memory_entry["id"],
            "bytecode": memory_entry["bytecode"],
            "tags": memory_entry.get("tags", []),
            "origin": memory_entry.get("origin", "unknown")
        }
        return SyncProtocol.hash_packet(packet)

    def save_memory_as_bin(self, memory_entry):
        """
        New method: Converts a memory dictionary into raw bytes for sending.
        """
        packet = SyncProtocol.create_packet(
            memory_entry["id"],
            bytes.fromhex(memory_entry["bytecode"]),
            memory_entry.get("tags", []),
            memory_entry.get("origin", "local")
        )
        return SyncProtocol.encode_packet(packet)
