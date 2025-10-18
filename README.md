# Deep Decoder for IDS/IPS, WAF

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-khoilv2005-181717?logo=github)](https://github.com/khoilv2005/deep-decoder)

A comprehensive multi-layer encoding/decoding library designed for security professionals working with **IDS (Intrusion Detection Systems)**, **IPS (Intrusion Prevention Systems)**, and **WAF (Web Application Firewalls)**. Automatically detects and decodes various encoding schemes including Base64, URL encoding, HTML entities, Hex, and more.

## 🎯 Use Cases

### Security Analysis & Threat Detection
- **IDS/IPS Signature Analysis**: Decode obfuscated attack payloads
- **WAF Bypass Detection**: Identify encoding-based evasion techniques  
- **Malware Analysis**: Decode encoded command & control communications
- **Log Analysis**: Decode encoded data in security logs
- **Forensics**: Uncover hidden data through multiple encoding layers

### Real-World Examples

```python
# Decode double-encoded directory traversal attack
suspicious = "%252F%252E%252E%252F%252E%252E%252Fetc%252Fpasswd"
decoded = quick_decode(suspicious)  # ../../etc/passwd

# Decode obfuscated XSS payload
xss = "JTNDc2NyaXB0JTNFYWxlcnQoMSklM0MlMkZzY3JpcHQlM0U="
decoded = quick_decode(xss)  # <script>alert(1)</script>

# Decode hex-encoded SQL injection
sql = "27204f52202731273d2731"
decoded = quick_decode(sql)  # ' OR '1'='1
```

## 🚀 Features

- **🔍 Smart Detection**: Automatically detects encoding types based on patterns
- **🔄 Multi-layer Decoding**: Recursively decodes through multiple encoding layers
- **🛡️ Security-Focused**: Designed for IDS/IPS, WAF, and security analysis
- **📊 Confidence Scoring**: Provides confidence levels for each decoding step
- **⚡ Fast & Efficient**: Cycle detection prevents infinite loops
- **🔧 12+ Encoding Types**:
  - Base64 (strict and lenient modes)
  - URL/URI Encoding (single and double encoded)
  - HTML Entities
  - XML Entities  
  - JavaScript Escape Sequences
  - JSON Escape Sequences
  - Unicode Escape Sequences
  - Hexadecimal
  - ROT13

## 📦 Installation

```bash
pip install deep-decoder
```

Or install from source:

```bash
git clone https://github.com/khoilv2005/deep-decoder.git
cd deep-decoder
pip install -e .
```

## 🔧 Quick Start

### Basic Usage

```python
from deep_decoder import quick_decode

# Simple decoding
encoded = "SGVsbG8gV29ybGQh"
decoded = quick_decode(encoded)
print(decoded)  # Output: Hello World!
```

### Security Analysis - IDS/IPS/WAF

```python
from deep_decoder import deep_decode_data, get_decoding_statistics

# Analyze suspicious payload (Path Traversal Attack: Base64 + Double URL-encoded)
suspicious_payload = "JTI1MkYuLiUyNTJGZXRjJTI1MkZwYXNzd2Q="
result = deep_decode_data(suspicious_payload, max_iterations=20)

print(f"🔍 Original: {suspicious_payload}")
print(f"✅ Decoded: {result.final_data}")  # Output: /../etc/passwd
print(f"📊 Encoding layers: {result.iterations}")
print(f"⏱️ Time: {result.total_time_ms:.2f}ms")
print(f"🔄 Cycle detected: {result.cycle_detected}")

# Get detailed statistics
stats = get_decoding_statistics(result)
print(f"\n📈 Analysis:")
print(f"  - Successful steps: {stats['successful_iterations']}")
print(f"  - Size reduction: {stats['size_reduction_percent']}%")
print(f"  - Most effective: {stats['most_effective_encoding']}")
print(f"  - Avg confidence: {stats['average_confidence']}")

# Show decoding steps
print(f"\n🔬 Decoding Steps:")
for step in result.steps:
    if step.success:
        print(f"  [{step.iteration}] {step.encoding_type} (confidence: {step.confidence:.2%})")
```

### Advanced Usage - Custom Configuration

```python
from deep_decoder import deep_decode_data, EncodingType

# Specify custom encoding priority for specific attack patterns
result = deep_decode_data(
    input_data="your_encoded_data",
    max_iterations=15,
    encoding_priority=[
        EncodingType.URI_ENCODED,      # Check URL encoding first
        EncodingType.DOUBLE_ENCODED,   # Then double encoding
        EncodingType.BASE64,           # Then Base64
        EncodingType.HEX               # Finally Hex
    ],
    enable_detection=True  # Still use auto-detection
)
```

## 📖 Common Security Scenarios

### 1. WAF Bypass Detection

```python
# Detect double URL-encoded path traversal
waf_bypass = "%252E%252E%252F%252E%252E%252Fadmin"
result = quick_decode(waf_bypass)
print(result)  # ../../admin
```

### 2. XSS Payload Analysis  

```python
# Multi-layer encoded XSS
xss_payload = "JTNDc2NyaXB0JTNFYWxlcnQlMjhkb2N1bWVudC5jb29raWUlMjklM0MlMkZzY3JpcHQlM0U="
result = deep_decode_data(xss_payload)
print(f"Attack vector: {result.final_data}")
# <script>alert(document.cookie)</script>
```

### 3. SQL Injection Detection

```python
# Hex-encoded SQL injection
sql_hex = "27204f52202731273d2731"
result = quick_decode(sql_hex)
print(result)  # ' OR '1'='1
```

### 4. Command Injection Analysis

```python
# Unicode-escaped command injection
cmd_injection = "\\u0063\\u0061\\u0074\\u0020\\u002f\\u0065\\u0074\\u0063\\u002f\\u0070\\u0061\\u0073\\u0073\\u0077\\u0064"
result = quick_decode(cmd_injection)
print(result)  # cat /etc/passwd
```

### 5. Log Analysis

```python
# Decode encoded data from security logs
from deep_decoder import deep_decode_data

log_entry = "GET %2f%2e%2e%2f%2e%2e%2fadmin HTTP/1.1"
result = deep_decode_data(log_entry)
print(f"Attack detected: {result.final_data}")
```

## 📊 API Reference

### Main Functions

#### `deep_decode_data(input_data, max_iterations=15, auto_stop_on_cycle=True, encoding_priority=None, enable_detection=True)`

Performs multi-layer decoding with detailed results.

**Parameters:**
- `input_data` (str): Data to decode
- `max_iterations` (int): Maximum decoding iterations (default: 15)
- `auto_stop_on_cycle` (bool): Stop if cycle detected (default: True)
- `encoding_priority` (List[EncodingType]): Custom encoding priority
- `enable_detection` (bool): Enable auto-detection (default: True)

**Returns:** `DecodeResult` object with:
- `final_data`: Decoded data
- `iterations`: Number of iterations
- `steps`: List of decoding steps
- `cycle_detected`: Whether a cycle was detected
- `total_time_ms`: Processing time in ms

#### `quick_decode(data, max_iterations=10)`

Quick decoding without detailed information.

#### `get_decoding_statistics(result)`

Returns decoding statistics dictionary.

#### `format_result_as_json(result)`

Converts DecodeResult to JSON string.

### Individual Decoders

All return `Tuple[str, float]` (decoded_data, confidence):

- `try_decode_base64(data)` - Base64 decoding
- `try_decode_hex(data)` - Hexadecimal decoding
- `try_decode_uri_encoded(data)` - URL decoding
- `decode_html_entities(data)` - HTML entities decoding
- `try_decode_unicode_escape(data)` - Unicode escape decoding
- And 7 more encoding types...

### Utility Functions

- `detect_encoding_type(data)` - Detect possible encoding types
- `calculate_hash(data)` - Calculate MD5 hash
- `is_printable_utf8(data)` - Check UTF-8 validity

## 🛡️ Security Best Practices

1. **Always validate decoded output** before using in security decisions
2. **Set reasonable max_iterations** to prevent resource exhaustion
3. **Use confidence scores** to filter false positives
4. **Log decoding attempts** for audit trails
5. **Combine with other security tools** for comprehensive analysis

## 🔬 Technical Details

### Supported Encoding Types

| Encoding Type | Example | Use Case |
|--------------|---------|----------|
| Base64 | `SGVsbG8=` | Data obfuscation |
| URL Encoding | `%3Cscript%3E` | WAF bypass |
| Double URL | `%252F` | Deep WAF bypass |
| HTML Entities | `&lt;script&gt;` | XSS obfuscation |
| Hex | `48656c6c6f` | Binary data |
| Unicode Escape | `\u0041` | Character obfuscation |
| ROT13 | `Uryyb` | Simple cipher |

### Detection Algorithm

1. **Pattern Analysis**: Examines data patterns for encoding signatures
2. **Confidence Scoring**: Assigns confidence based on pattern matching
3. **Iterative Decoding**: Applies decoders in priority order
4. **Cycle Detection**: Prevents infinite loops with hash tracking
5. **Validation**: Checks UTF-8 validity and printability

## 📈 Performance

- **Fast**: Processes most payloads in < 1ms
- **Efficient**: Minimal memory footprint
- **Scalable**: Handles large datasets
- **Safe**: Cycle detection prevents hangs

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Additional encoding types (Base32, Base85, etc.)
- [ ] Binary data support
- [ ] Custom decoder plugins
- [ ] Performance optimizations
- [ ] CLI tool
- [ ] More test cases

1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewEncoder`)
3. Commit changes (`git commit -m 'Add NewEncoder'`)
4. Push to branch (`git push origin feature/NewEncoder`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python standard library - no external dependencies
- Designed for security professionals
- Tested against real-world attack payloads

## 📞 Support & Contact

- **GitHub Issues**: [Report bugs or request features](https://github.com/khoilv2005/deep-decoder/issues)
- **GitHub**: [@khoilv2005](https://github.com/khoilv2005)

## 🔖 Version History

See [CHANGELOG.md](CHANGELOG.md) for version history.

---

**Built for security professionals by security professionals** 🛡️

Made with ❤️ by [khoilv2005](https://github.com/khoilv2005)
