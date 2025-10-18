"""
Example: Advanced usage with custom configuration
"""

from deep_decoder import (
    deep_decode_data,
    get_decoding_statistics,
    format_result_as_json,
    EncodingType
)

def main():
    print("=" * 70)
    print("ADVANCED USAGE EXAMPLES")
    print("=" * 70)
    
    # Example 1: Custom encoding priority
    print("\n1. Custom Encoding Priority")
    encoded = "SGVsbG8gV29ybGQh"
    result = deep_decode_data(
        encoded,
        encoding_priority=[
            EncodingType.BASE64,
            EncodingType.HEX,
            EncodingType.URI_ENCODED
        ],
        enable_detection=False
    )
    print(f"   Result: {result.final_data}")
    print(f"   Steps: {result.iterations}")
    
    # Example 2: Detailed step analysis
    print("\n2. Step-by-Step Analysis")
    encoded = "%3Cscript%3Ealert%281%29%3C%2Fscript%3E"
    result = deep_decode_data(encoded)
    
    print(f"   Input: {encoded}")
    print(f"   Output: {result.final_data}")
    print("\n   Decoding Steps:")
    for step in result.steps:
        if step.success:
            print(f"   - Step {step.iteration}: {step.encoding_type}")
            print(f"     Confidence: {step.confidence:.2%}")
            print(f"     Size: {step.input_length} → {step.output_length} bytes")
    
    # Example 3: Statistics
    print("\n3. Decoding Statistics")
    encoded = "JTNDc2NyaXB0JTNFYWxlcnQoMSklM0MlMkZzY3JpcHQlM0U="
    result = deep_decode_data(encoded)
    stats = get_decoding_statistics(result)
    
    print(f"   Successful iterations: {stats['successful_iterations']}")
    print(f"   Size reduction: {stats['size_reduction_percent']}%")
    print(f"   Most effective: {stats['most_effective_encoding']}")
    print(f"   Average confidence: {stats['average_confidence']}")
    
    # Example 4: JSON export
    print("\n4. JSON Export")
    encoded = "48656C6C6F"
    result = deep_decode_data(encoded)
    json_output = format_result_as_json(result)
    print(f"   JSON output (truncated):")
    print(f"   {json_output[:200]}...")
    
    # Example 5: Handling cycles
    print("\n5. Cycle Detection")
    # Create a scenario that might cycle
    encoded = "test%20data"
    result = deep_decode_data(encoded, auto_stop_on_cycle=True)
    print(f"   Cycle detected: {result.cycle_detected}")
    print(f"   Max iterations reached: {result.reached_max_iterations}")
    
    # Example 6: Max iterations control
    print("\n6. Custom Max Iterations")
    encoded = "SGVsbG8gV29ybGQh"
    result = deep_decode_data(encoded, max_iterations=5)
    print(f"   Result: {result.final_data}")
    print(f"   Max iterations: 5")
    print(f"   Actual iterations: {result.iterations}")

if __name__ == "__main__":
    main()
