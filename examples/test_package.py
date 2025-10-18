"""
Example: Test the installed package
"""

def test_import():
    """Test if the package can be imported"""
    try:
        import deep_decoder
        print("✓ Package imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import package: {e}")
        return False

def test_basic_functions():
    """Test basic functionality"""
    from deep_decoder import quick_decode, deep_decode_data
    
    # Test Base64
    result = quick_decode("SGVsbG8gV29ybGQh")
    assert result == "Hello World!", f"Expected 'Hello World!', got '{result}'"
    print("✓ Base64 decoding works")
    
    # Test URL encoding
    result = quick_decode("%3Cscript%3E")
    assert result == "<script>", f"Expected '<script>', got '{result}'"
    print("✓ URL decoding works")
    
    # Test detailed decoding
    result = deep_decode_data("SGVsbG8gV29ybGQh")
    assert result.final_data == "Hello World!"
    assert result.iterations > 0
    print("✓ Detailed decoding works")

def test_all_decoders():
    """Test all individual decoders"""
    from deep_decoder import (
        try_decode_base64,
        try_decode_hex,
        decode_html_entities,
        try_decode_uri_encoded
    )
    
    # Test Base64
    decoded, confidence = try_decode_base64("SGVsbG8=")
    assert decoded == "Hello" and confidence > 0
    print("✓ Base64 decoder works")
    
    # Test Hex
    decoded, confidence = try_decode_hex("48656C6C6F")
    assert decoded == "Hello" and confidence > 0
    print("✓ Hex decoder works")
    
    # Test HTML entities
    decoded, confidence = decode_html_entities("&lt;script&gt;")
    assert decoded == "<script>" and confidence > 0
    print("✓ HTML entities decoder works")
    
    # Test URI encoding
    decoded, confidence = try_decode_uri_encoded("%3Cscript%3E")
    assert decoded == "<script>" and confidence > 0
    print("✓ URI decoder works")

def test_utilities():
    """Test utility functions"""
    from deep_decoder import (
        get_decoding_statistics,
        format_result_as_json,
        detect_encoding_type,
        EncodingType
    )
    
    from deep_decoder import deep_decode_data
    
    result = deep_decode_data("SGVsbG8gV29ybGQh")
    
    # Test statistics
    stats = get_decoding_statistics(result)
    assert isinstance(stats, dict)
    print("✓ Statistics function works")
    
    # Test JSON export
    json_str = format_result_as_json(result)
    assert "final_data" in json_str
    print("✓ JSON export works")
    
    # Test encoding detection
    encodings = detect_encoding_type("SGVsbG8gV29ybGQh")
    assert len(encodings) > 0
    assert encodings[0][0] == EncodingType.BASE64
    print("✓ Encoding detection works")

def main():
    print("=" * 70)
    print("TESTING DEEP DECODER PACKAGE")
    print("=" * 70)
    
    print("\n1. Testing Package Import")
    if not test_import():
        print("\n✗ Package import failed. Make sure to install the package first:")
        print("   pip install -e .")
        return
    
    print("\n2. Testing Basic Functions")
    try:
        test_basic_functions()
    except Exception as e:
        print(f"✗ Basic functions test failed: {e}")
        return
    
    print("\n3. Testing Individual Decoders")
    try:
        test_all_decoders()
    except Exception as e:
        print(f"✗ Individual decoders test failed: {e}")
        return
    
    print("\n4. Testing Utility Functions")
    try:
        test_utilities()
    except Exception as e:
        print(f"✗ Utility functions test failed: {e}")
        return
    
    print("\n" + "=" * 70)
    print("✓ ALL TESTS PASSED!")
    print("=" * 70)
    print("\nThe package is ready to use!")
    print("\nQuick start:")
    print("  from deep_decoder import quick_decode")
    print('  result = quick_decode("SGVsbG8gV29ybGQh")')
    print('  print(result)  # Hello World!')

if __name__ == "__main__":
    main()
