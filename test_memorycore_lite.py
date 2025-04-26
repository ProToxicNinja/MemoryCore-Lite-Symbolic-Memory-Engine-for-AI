# test_memorycore_lite.py

from memorycore.symbolic_core import MemoryCore

def test_memorycore_lite():
    print("🧠 Starting MemoryCore Lite Test...")

    core = MemoryCore()

    input_text = "Beyond the stars, new worlds awaken."
    print(f"\n🌌 Input text:\n{input_text}")

    token_ids = core.encode(input_text)
    print(f"\n🔢 Token IDs:\n{token_ids}")

    byte_data = core.to_bytes(token_ids)
    print(f"\n📦 Encoded Bytes:\n{byte_data}")

    recovered_ids = core.from_bytes(byte_data)
    print(f"\n🔄 Recovered IDs:\n{recovered_ids}")

    output = core.decode(recovered_ids)
    print(f"\n🧾 Decoded Output:\n{output}")

    assert token_ids == recovered_ids, "❌ Token IDs mismatch after byte roundtrip!"
    print("\n✅ MemoryCore Lite basic test PASSED!")

if __name__ == "__main__":
    test_memorycore_lite()
