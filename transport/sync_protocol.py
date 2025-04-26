import json
import hashlib
import uuid

class SyncProtocol:
    @staticmethod
    def create_packet(memory_id, bytecode, tags=None, origin=None):
        """
        Create a packet dictionary ready for network transmission.
        """
        packet = {
            "id": memory_id or str(uuid.uuid4()),
            "bytecode": bytecode.hex(),  # send as hex for safety
            "tags": tags or [],
            "origin": origin or "unknown"
        }
        return packet

    @staticmethod
    def encode_packet(packet):
        """
        Encode a packet dictionary into bytes.
        """
        json_str = json.dumps(packet)
        return json_str.encode('utf-8')

    @staticmethod
    def decode_packet(data_bytes):
        """
        Decode bytes into a packet dictionary.
        """
        json_str = data_bytes.decode('utf-8')
        packet = json.loads(json_str)
        return packet

    @staticmethod
    def hash_packet(packet):
        """
        Create a hash of the packet (for deduplication or validation).
        """
        relevant_data = packet["id"] + packet["bytecode"]
        return hashlib.sha256(relevant_data.encode('utf-8')).hexdigest()
