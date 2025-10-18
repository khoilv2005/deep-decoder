"""
Example: Basic usage of Deep Decoder
"""

from deep_decoder import quick_decode, deep_decode_data

def main():
    print("=" * 70)
    print("BASIC USAGE EXAMPLES")
    print("=" * 70)
    
    # Example 1: Quick decode
    print("\n1. Quick Decode - Base64")
    encoded = "SGVsbG8gV29ybGQh"
    decoded = quick_decode(encoded)
    print(f"   Input:  {encoded}")
    print(f"   Output: {decoded}")
    
    # Example 2: URL encoding
    print("\n2. Quick Decode - URL Encoding")
    encoded = "q=%3Cscript%3Ealert%281%29%3C%2Fscript%3E"
    decoded = quick_decode(encoded)
    print(f"   Input:  {encoded}")
    print(f"   Output: {decoded}")
    
    # Example 3: HTML entities
    print("\n3. Quick Decode - HTML Entities")
    encoded = "&lt;script&gt;alert&#40;1&#41;&lt;&#x2F;script&gt;"
    decoded = quick_decode(encoded)
    print(f"   Input:  {encoded}")
    print(f"   Output: {decoded}")
    
    # Example 4: Detailed decoding
    print("\n4. Detailed Decode - Multiple Layers")
    encoded = "JTNDc2NyaXB0JTNFYWxlcnQoMSklM0MlMkZzY3JpcHQlM0U="
    result = deep_decode_data(encoded)
    print(f"   Input:  {encoded}")
    print(f"   Output: {result.final_data}")
    print(f"   Iterations: {result.iterations}")
    print(f"   Time: {result.total_time_ms:.2f}ms")
    
    # Example 5: Hex encoding
    print("\n5. Quick Decode - Hex")
    encoded = "48656C6C6F20576F726C6421"
    decoded = quick_decode(encoded)
    print(f"   Input:  {encoded}")
    print(f"   Output: {decoded}")

if __name__ == "__main__":
    main()
