"""
Deep Decoder for IDS/IPS, WAF - A comprehensive multi-layer encoding/decoding library
"""

from .decoder import (
    # Main functions
    deep_decode_data,
    quick_decode,
    
    # Enums
    EncodingType,
    
    # Data classes
    DecodeStep,
    DecodeResult,
    
    # Individual decoders
    try_decode_base64,
    try_decode_base64_lenient,
    try_decode_hex,
    try_decode_uri_encoded,
    try_decode_double_encoded,
    decode_html_entities,
    decode_xml_entities,
    try_decode_js_escape,
    try_decode_json_escape,
    try_decode_rot13,
    try_decode_unicode_escape,
    
    # Utility functions
    detect_encoding_type,
    format_result_as_json,
    get_decoding_statistics,
)

__version__ = "1.0.2"
__author__ = "khoilv2005"
__all__ = [
    "deep_decode_data",
    "quick_decode",
    "EncodingType",
    "DecodeStep",
    "DecodeResult",
    "try_decode_base64",
    "try_decode_base64_lenient",
    "try_decode_hex",
    "try_decode_uri_encoded",
    "try_decode_double_encoded",
    "decode_html_entities",
    "decode_xml_entities",
    "try_decode_js_escape",
    "try_decode_json_escape",
    "try_decode_rot13",
    "try_decode_unicode_escape",
    "detect_encoding_type",
    "format_result_as_json",
    "get_decoding_statistics",
]
