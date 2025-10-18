import base64
import urllib.parse
import html
import re
import json
import hashlib
from typing import Tuple, List, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime

# ============================================================================
# ENUM AND DATA CLASSES / ENUM VÀ DATA CLASSES
# ============================================================================

class EncodingType(Enum):
    """
    Supported encoding types / Các loại encoding được hỗ trợ
    """
    UNKNOWN = "unknown"
    BASE64 = "base64"
    HTML_ENTITY = "html_entity"
    URI_ENCODED = "uri_encoded"
    JS_ESCAPE = "js_escape"
    HEX = "hex"
    ROT13 = "rot13"
    JSON_ESCAPE = "json_escape"
    XML_ENTITY = "xml_entity"
    DOUBLE_ENCODED = "double_encoded"
    BASE64_LENIENT = "base64_lenient"
    UNICODE_ESCAPE = "unicode_escape"


@dataclass
class DecodeStep:
    """
    Record of a single decode step / Bản ghi một bước giải mã
    """
    iteration: int
    encoding_type: str
    success: bool
    input_length: int
    output_length: int
    input_hash: str
    output_hash: str
    message: str
    confidence: float = 0.0  # 0.0-1.0

@dataclass
class DecodeResult:
    """
    Final result of the decoding process / Kết quả cuối cùng của quá trình giải mã
    """
    final_data: str
    iterations: int
    total_steps: int
    steps: List[DecodeStep]
    cycle_detected: bool
    reached_max_iterations: bool
    total_time_ms: float
    original_data_hash: str
    final_data_hash: str

# ============================================================================
# UTILITY FUNCTIONS / HÀM UTILITY
# ============================================================================

def calculate_hash(data: str) -> str:
    """
    Calculate MD5 hash of data to detect cycles
    Tính MD5 hash của dữ liệu để phát hiện chu kỳ
    """
    return hashlib.md5(data.encode('utf-8', errors='replace')).hexdigest()

def is_printable_utf8(data: str) -> bool:
    """
    Check if data is valid UTF-8
    Kiểm tra xem dữ liệu có phải UTF-8 hợp lệ không
    """
    try:
        data.encode('utf-8').decode('utf-8')
        return True
    except (UnicodeDecodeError, UnicodeEncodeError):
        return False

def _looks_like_text(data: str) -> bool:
    """
    Check if data looks like regular text.
    Helps reduce false positives for encodings like ROT13.
    
    Kiểm tra xem dữ liệu có giống văn bản thông thường không.
    Giúp giảm false positive cho các encoding như ROT13.
    """
    if len(data) < 3:
        return False
    
    # Count alphabetic characters and whitespace / Đếm số ký tự chữ cái và khoảng trắng
    text_chars = sum(1 for c in data if c.isalpha() or c.isspace() or c in ',.!?;:')
    text_ratio = text_chars / len(data)
    
    # Check for at least one word longer than 2 characters / Kiểm tra có ít nhất 1 từ dài hơn 2 ký tự
    words = re.findall(r'\b[a-zA-Z]{3,}\b', data)
    
    return text_ratio > 0.6 and len(words) > 0

def estimate_confidence(original: str, decoded: str, encoding_type: EncodingType) -> float:
    """
    Estimate confidence of the decoding operation.
    Value from 0.0 (not confident) to 1.0 (very confident)
    
    Ước tính độ tin cậy của phép giải mã.
    Giá trị từ 0.0 (không tin cậy) đến 1.0 (rất tin cậy)
    """
    if original == decoded:
        return 0.0  # No decoding performed / Không giải mã được
    
    # Check valid UTF-8 / Kiểm tra UTF-8 hợp lệ
    try:
        decoded.encode('utf-8').decode('utf-8')
    except (UnicodeDecodeError, UnicodeEncodeError):
        return 0.2
    
    # Check reasonable length / Kiểm tra độ dài hợp lý
    if len(decoded) == 0 or len(decoded) > len(original) * 10:
        return 0.3
    
    # Confidence based on encoding type / Confidence dựa trên encoding type
    base_scores = {
        EncodingType.BASE64: 0.95,
        EncodingType.BASE64_LENIENT: 0.8,
        EncodingType.HEX: 0.9,
        EncodingType.URI_ENCODED: 0.85,
        EncodingType.DOUBLE_ENCODED: 0.8,
        EncodingType.HTML_ENTITY: 0.9,
        EncodingType.XML_ENTITY: 0.85,
        EncodingType.JS_ESCAPE: 0.8,
        EncodingType.JSON_ESCAPE: 0.85,
        EncodingType.ROT13: 0.6,
        EncodingType.UNICODE_ESCAPE: 0.8
    }
    
    confidence = base_scores.get(encoding_type, 0.7)
    
    # Reduce confidence if decoded string contains many non-printable characters
    # Giảm confidence nếu decoded string chứa nhiều ký tự không in được
    printable_ratio = sum(1 for c in decoded if c.isprintable() or c.isspace()) / len(decoded)
    if printable_ratio < 0.7:
        confidence *= 0.6
    
    # Increase confidence if decoded text looks like real text
    # Tăng confidence nếu decoded text trông giống văn bản thật
    if encoding_type == EncodingType.ROT13 and _looks_like_text(decoded):
        confidence = min(confidence * 1.3, 0.9)
    
    return min(confidence, 0.95)  # Limit max confidence / Giới hạn max confidence

# ============================================================================
# INDIVIDUAL DECODER FUNCTIONS / CÁC HÀM GIẢI MÃ ĐƠN LẺ
# ============================================================================

def decode_html_entities(data: str) -> Tuple[str, float]:
    """
    Decode HTML Entities (e.g., &lt;, &#x2F;, &#105;).
    Returns: (decoded_data, confidence)
    
    Giải mã HTML Entities (ví dụ: &lt;, &#x2F;, &#105;).
    Trả về: (dữ liệu_giải_mã, độ_tin_cậy)
    """
    try:
        decoded = html.unescape(data)
        confidence = estimate_confidence(data, decoded, EncodingType.HTML_ENTITY)
        return decoded, confidence
    except Exception:
        return data, 0.0

def decode_xml_entities(data: str) -> Tuple[str, float]:
    """
    Decode basic XML Entities (&quot;, &apos;, etc.).
    Returns: (decoded_data, confidence)
    
    Giải mã XML Entities cơ bản (&quot;, &apos;, v.v.).
    Trả về: (dữ liệu_giải_mã, độ_tin_cậy)
    """
    try:
        xml_entities = {
            '&quot;': '"',
            '&apos;': "'",
            '&lt;': '<',
            '&gt;': '>',
            '&amp;': '&'
        }
        decoded = data
        for entity, char in xml_entities.items():
            decoded = decoded.replace(entity, char)

        confidence = estimate_confidence(data, decoded, EncodingType.XML_ENTITY)
        return decoded, confidence
    except Exception:
        return data, 0.0

def try_decode_base64(data: str) -> Tuple[str, float]:
    """
    Attempt to decode Base64.
    Checks length and valid characters to minimize errors.
    Returns: (decoded_data, confidence)
    
    Cố gắng giải mã Base64.
    Kiểm tra độ dài, ký tự hợp lệ để giảm thiểu lỗi.
    Trả về: (dữ liệu_giải_mã, độ_tin_cậy)
    """
    try:
        # Remove whitespace / Loại bỏ khoảng trắng
        cleaned_data = data.strip()

        # Preliminary check: Base64 must have length as multiple of 4
        # Kiểm tra sơ bộ: Base64 phải có độ dài là bội số của 4
        if len(cleaned_data) % 4 != 0:
            return data, 0.0

        # Check characters (only A-Z, a-z, 0-9, +, /, =)
        # Kiểm tra ký tự (chỉ chứa A-Z, a-z, 0-9, +, /, =)
        if not re.fullmatch(r'^[A-Za-z0-9+/=\s]*$', cleaned_data):
            return data, 0.0

        # Base64 decode
        decoded_bytes = base64.b64decode(cleaned_data, validate=True)

        # Try decode to UTF-8 / Thử decode sang UTF-8
        decoded = decoded_bytes.decode('utf-8', errors='strict')
        confidence = estimate_confidence(data, decoded, EncodingType.BASE64)
        return decoded, confidence

    except Exception:
        return data, 0.0

def try_decode_base64_lenient(data: str) -> Tuple[str, float]:
    """
    Decode Base64 with lenient mode (ignores errors).
    Returns: (decoded_data, confidence)
    
    Giải mã Base64 với chế độ tolerant hơn (bỏ qua lỗi).
    Trả về: (dữ liệu_giải_mã, độ_tin_cậy)
    """
    try:
        cleaned_data = data.strip()

        # If length is not multiple of 4, add padding
        # Nếu độ dài không phải bội số của 4, thêm padding
        remainder = len(cleaned_data) % 4
        if remainder:
            cleaned_data += '=' * (4 - remainder)

        if not re.fullmatch(r'^[A-Za-z0-9+/=]*$', cleaned_data):
            return data, 0.0

        decoded_bytes = base64.b64decode(cleaned_data, validate=False)
        decoded = decoded_bytes.decode('utf-8', errors='replace')

        if decoded != data:
            confidence = estimate_confidence(data, decoded, EncodingType.BASE64_LENIENT)
            return decoded, confidence * 0.8  # Reduce confidence due to lenient mode / Giảm độ tin cậy vì tolerant

        return data, 0.0

    except Exception:
        return data, 0.0

def try_decode_hex(data: str) -> Tuple[str, float]:
    """
    Attempt to decode Hex encoding (e.g., 48656C6C6F20576F726C64).
    Returns: (decoded_data, confidence)
    
    Cố gắng giải mã Hex encoding (ví dụ: 48656C6C6F20576F726C64).
    Trả về: (dữ liệu_giải_mã, độ_tin_cậy)
    """
    try:
        cleaned_data = data.replace(' ', '').replace('\\x', '')

        # Check length must be even and at least 4 characters
        # Kiểm tra độ dài phải là số chẵn và có ít nhất 4 ký tự
        if len(cleaned_data) % 2 != 0 or len(cleaned_data) < 4:
            return data, 0.0

        # Check characters (only 0-9, a-f, A-F)
        # Kiểm tra ký tự (chỉ chứa 0-9, a-f, A-F)
        if not re.fullmatch(r'^[0-9a-fA-F]*$', cleaned_data):
            return data, 0.0

        decoded_bytes = bytes.fromhex(cleaned_data)
        decoded = decoded_bytes.decode('utf-8', errors='strict')

        confidence = estimate_confidence(data, decoded, EncodingType.HEX)
        return decoded, confidence

    except Exception:
        return data, 0.0

def try_decode_rot13(data: str) -> Tuple[str, float]:
    """
    Attempt to decode ROT13.
    Returns: (decoded_data, confidence)
    
    Cố gắng giải mã ROT13.
    Trả về: (dữ liệu_giải_mã, độ_tin_cậy)
    """
    try:
        decoded = ""
        for char in data:
            if 'a' <= char <= 'z':
                decoded += chr((ord(char) - ord('a') + 13) % 26 + ord('a'))
            elif 'A' <= char <= 'Z':
                decoded += chr((ord(char) - ord('A') + 13) % 26 + ord('A'))
            else:
                decoded += char

        # ROT13 has high false-positive rate, check carefully
        # ROT13 có tỉ lệ false-positive cao, kiểm tra kỹ
        if (decoded != data and 
            any(c.isalpha() for c in data) and 
            _looks_like_text(decoded)):
            confidence = estimate_confidence(data, decoded, EncodingType.ROT13)
            return decoded, confidence

        return data, 0.0

    except Exception:
        return data, 0.0

def try_decode_uri_encoded(data: str) -> Tuple[str, float]:
    """
    Decode URL-encoding (e.g., %20, %2F).
    Returns: (decoded_data, confidence)
    
    Giải mã URL-encoding (ví dụ: %20, %2F).
    Trả về: (dữ liệu_giải_mã, độ_tin_cậy)
    """
    try:
        if '%' not in data:
            return data, 0.0

        # Check reasonable % ratio (not too many)
        # Kiểm tra tỉ lệ % hợp lý (không quá nhiều)
        percent_count = data.count('%')
        if percent_count > len(data) / 2:  # Too many % may be false positive / Quá nhiều % có thể là false positive
            return data, 0.3

        decoded = urllib.parse.unquote(data, errors='replace')
        confidence = estimate_confidence(data, decoded, EncodingType.URI_ENCODED)
        return decoded, confidence

    except Exception:
        return data, 0.0

def try_decode_js_escape(data: str) -> Tuple[str, float]:
    r"""
    Decode JavaScript Escape Sequences (\uXXXX, \xXX, \n, \t, etc.).
    Returns: (decoded_data, confidence)
    
    Giải mã JavaScript Escape Sequences (\uXXXX, \xXX, \n, \t, v.v.).
    Trả về: (dữ liệu_giải_mã, độ_tin_cậy)
    """
    try:
        # Check if contains escape sequence / Kiểm tra xem có chứa escape sequence không
        if not re.search(r'\\(?:u[0-9a-fA-F]{4}|x[0-9a-fA-F]{2}|[ntrfvb\\"\'])', data):
            return data, 0.0

        # Use 'unicode_escape' to handle JS/JSON escape sequences
        # Sử dụng 'unicode_escape' để xử lý các chuỗi thoát của JS/JSON
        decoded = data.encode('utf-8').decode('unicode_escape')
        confidence = estimate_confidence(data, decoded, EncodingType.JS_ESCAPE)
        return decoded, confidence

    except Exception:
        return data, 0.0

def try_decode_json_escape(data: str) -> Tuple[str, float]:
    """
    Decode JSON escape sequences.
    Returns: (decoded_data, confidence)
    
    Giải mã JSON escape sequences.
    Trả về: (dữ liệu_giải_mã, độ_tin_cậy)
    """
    try:
        # Try parse as JSON string / Thử parse như JSON string
        if data.startswith('"') and data.endswith('"'):
            decoded = json.loads(data)
            confidence = estimate_confidence(data, decoded, EncodingType.JSON_ESCAPE)
            return decoded, confidence

        return data, 0.0

    except Exception:
        return data, 0.0

def try_decode_double_encoded(data: str) -> Tuple[str, float]:
    """
    Decode double-encoded URL (e.g., %252F → %2F → /).
    Returns: (decoded_data, confidence)
    
    Giải mã double-encoded URL (ví dụ: %252F → %2F → /).
    Trả về: (dữ liệu_giải_mã, độ_tin_cậy)
    """
    try:
        if '%25' not in data and '%252' not in data:
            return data, 0.0

        # Try decoding twice / Thử giải mã 2 lần
        first_decode = urllib.parse.unquote(data, errors='replace')
        second_decode = urllib.parse.unquote(first_decode, errors='replace')

        if second_decode != first_decode and second_decode != data:
            confidence = estimate_confidence(data, second_decode, EncodingType.DOUBLE_ENCODED)
            return second_decode, confidence * 0.9

        return data, 0.0

    except Exception:
        return data, 0.0

def try_decode_unicode_escape(data: str) -> Tuple[str, float]:
    r"""
    Decode Unicode escape sequences (\uXXXX).
    Returns: (decoded_data, confidence)
    
    Giải mã Unicode escape sequences (\uXXXX).
    Trả về: (dữ liệu_giải_mã, độ_tin_cậy)
    """
    try:
        if '\\u' not in data:
            return data, 0.0
            
        # Check pattern \uXXXX / Kiểm tra pattern \uXXXX
        unicode_pattern = r'\\u[0-9a-fA-F]{4}'
        if re.search(unicode_pattern, data):
            decoded = data.encode('utf-8').decode('unicode_escape')
            confidence = estimate_confidence(data, decoded, EncodingType.UNICODE_ESCAPE)
            return decoded, confidence
            
        return data, 0.0
    except Exception:
        return data, 0.0

# ============================================================================
# ENCODING TYPE DETECTION / HÀM PHÁT HIỆN LOẠI ENCODING
# ============================================================================

def detect_encoding_type(data: str) -> List[Tuple[EncodingType, float]]:
    """
    Detect encoding type based on data patterns.
    Returns list of possible encoding types sorted by likelihood (descending).
    
    Phát hiện loại encoding dựa trên pattern của dữ liệu.
    Trả về danh sách các loại encoding có thể theo độ khả năng giảm dần.
    """
    possibilities = []

    # Check Base64 / Kiểm tra Base64
    base64_pattern = r'^[A-Za-z0-9+/]*={0,2}$'
    cleaned_base64 = data.strip()
    if (len(cleaned_base64) % 4 == 0 and 
        re.fullmatch(base64_pattern, cleaned_base64) and
        len(cleaned_base64) >= 8):  # Base64 usually has minimum length / Base64 thường có độ dài tối thiểu
        possibilities.append((EncodingType.BASE64, 0.85))
        possibilities.append((EncodingType.BASE64_LENIENT, 0.7))

    # Check Hex / Kiểm tra Hex
    hex_clean = data.replace(' ', '').replace('\\x', '')
    if (len(hex_clean) % 2 == 0 and 
        len(hex_clean) >= 4 and  # Hex usually has minimum length / Hex thường có độ dài tối thiểu
        re.fullmatch(r'^[0-9a-fA-F]*$', hex_clean)):
        possibilities.append((EncodingType.HEX, 0.8))

    # Check URL-encoded / Kiểm tra URL-encoded
    percent_count = data.count('%')
    if (percent_count > 0 and 
        percent_count <= len(data) / 3 and  # Reasonable % ratio / Tỉ lệ % hợp lý
        re.search(r'%[0-9a-fA-F]{2}', data)):
        possibilities.append((EncodingType.URI_ENCODED, 0.9))

    # Check Double-encoded URL / Kiểm tra Double-encoded URL
    if '%25' in data or '%252' in data:
        possibilities.append((EncodingType.DOUBLE_ENCODED, 0.85))

    # Check HTML/XML Entities / Kiểm tra HTML/XML Entities
    if '&' in data:
        if re.search(r'&#(?:\d+|x[0-9a-fA-F]+);', data) or any(entity in data for entity in ['&lt;', '&gt;', '&amp;', '&quot;']):
            possibilities.append((EncodingType.HTML_ENTITY, 0.85))
            possibilities.append((EncodingType.XML_ENTITY, 0.7))

    # Check JS/JSON Escape / Kiểm tra JS/JSON Escape
    if '\\u' in data:
        possibilities.append((EncodingType.UNICODE_ESCAPE, 0.8))
        possibilities.append((EncodingType.JS_ESCAPE, 0.75))
    
    if '\\x' in data or any(seq in data for seq in ['\\n', '\\t', '\\r']):
        possibilities.append((EncodingType.JS_ESCAPE, 0.8))

    if data.startswith('"') and data.endswith('"') and '\\' in data:
        possibilities.append((EncodingType.JSON_ESCAPE, 0.8))

    # Check ROT13 - only when alphabetic characters exist / Kiểm tra ROT13 - chỉ khi có ký tự alphabet
    if any(c.isalpha() for c in data) and len(data) > 3:
        possibilities.append((EncodingType.ROT13, 0.4))  # Low confidence due to easy false positive / Confidence thấp vì dễ false positive

    # Sort by likelihood (descending) / Sắp xếp theo độ khả năng giảm dần
    possibilities.sort(key=lambda x: x[1], reverse=True)
    return possibilities

# ============================================================================
# MAIN DECODER FUNCTION / HÀM GIẢI MÃ CHÍNH
# ============================================================================

def deep_decode_data(
    input_data: str,
    max_iterations: int = 15,
    auto_stop_on_cycle: bool = True,
    encoding_priority: List[EncodingType] = None,
    enable_detection: bool = True
) -> DecodeResult:
    """
    Iteratively decode data through different encoding layers until data stabilizes
    or iteration limit is reached.
    
    Lặp lại việc giải mã dữ liệu qua các lớp khác nhau cho đến khi dữ liệu ổn định
    hoặc đạt giới hạn lặp.

    Args:
        input_data: Data to decode / Dữ liệu cần giải mã
        max_iterations: Maximum iterations (default: 15) / Số lần lặp tối đa (mặc định: 15)
        auto_stop_on_cycle: Auto stop if cycle detected (default: True) / Dừng tự động nếu phát hiện chu kỳ lặp (mặc định: True)
        encoding_priority: Priority list of encoding types to try / Danh sách ưu tiên các loại encoding để thử
        enable_detection: Enable automatic encoding detection (default: True) / Bật phát hiện encoding tự động (mặc định: True)

    Returns:
        DecodeResult: Detailed decode result / Kết quả giải mã chi tiết
    """
    start_time = datetime.now()

    # Input data validation / Validation dữ liệu đầu vào
    if not isinstance(input_data, str):
        return DecodeResult(
            final_data=str(input_data),
            iterations=0,
            total_steps=0,
            steps=[],
            cycle_detected=False,
            reached_max_iterations=False,
            total_time_ms=0,
            original_data_hash="",
            final_data_hash=""
        )

    if not input_data:
        return DecodeResult(
            final_data="",
            iterations=0,
            total_steps=0,
            steps=[],
            cycle_detected=False,
            reached_max_iterations=False,
            total_time_ms=0,
            original_data_hash=calculate_hash(""),
            final_data_hash=calculate_hash("")
        )

    # Limit input size (1MB) / Giới hạn kích thước đầu vào (1MB)
    if len(input_data) > 1024 * 1024:
        return DecodeResult(
            final_data=input_data,
            iterations=0,
            total_steps=0,
            steps=[],
            cycle_detected=False,
            reached_max_iterations=False,
            total_time_ms=0,
            original_data_hash=calculate_hash(input_data),
            final_data_hash=calculate_hash(input_data)
        )

    current_data = input_data.strip()
    original_data_hash = calculate_hash(input_data)
    seen_hashes = {original_data_hash: 0}  # Store hash history to detect cycles / Lưu lịch sử hashes để phát hiện chu kỳ
    steps: List[DecodeStep] = []

    # Setup encoding priority / Thiết lập ưu tiên encoding
    if encoding_priority is None:
        encoding_priority = [
            EncodingType.URI_ENCODED,
            EncodingType.DOUBLE_ENCODED,
            EncodingType.HTML_ENTITY,
            EncodingType.XML_ENTITY,
            EncodingType.JS_ESCAPE,
            EncodingType.UNICODE_ESCAPE,
            EncodingType.JSON_ESCAPE,
            EncodingType.BASE64,
            EncodingType.BASE64_LENIENT,
            EncodingType.HEX,
            EncodingType.ROT13,
        ]

    cycle_detected = False

    for iteration in range(1, max_iterations + 1):
        previous_data = current_data
        previous_hash = calculate_hash(previous_data)
        best_result = (previous_data, 0.0, EncodingType.UNKNOWN)

        # If detection enabled, use detection for priority / Nếu bật detection, sử dụng detection để ưu tiên
        if enable_detection and iteration == 1:
            detected_encodings = detect_encoding_type(current_data)
            # Combine with encoding priority / Kết hợp với encoding priority
            custom_priority = [enc for enc, _ in detected_encodings] + encoding_priority
        else:
            custom_priority = encoding_priority

        # Try decoding methods by priority / Thử các phương pháp giải mã theo ưu tiên
        for encoding_type in custom_priority:
            decoded_data, confidence = _try_decode_by_type(current_data, encoding_type)

            if decoded_data != current_data and confidence > best_result[1]:
                best_result = (decoded_data, confidence, encoding_type)

        current_data = best_result[0]
        confidence = best_result[1]
        encoding_type = best_result[2]

        # Record decode step / Ghi nhận bước giải mã
        current_hash = calculate_hash(current_data)
        step = DecodeStep(
            iteration=iteration,
            encoding_type=encoding_type.value,
            success=current_data != previous_data,
            input_length=len(previous_data),
            output_length=len(current_data),
            input_hash=previous_hash,
            output_hash=current_hash,
            message=f"Decoded {encoding_type.value} (confidence: {confidence:.2%})",
            confidence=confidence
        )
        steps.append(step)

        # Check if no change / Kiểm tra nếu không có thay đổi
        if current_data == previous_data:
            break

        # Check for cycle / Kiểm tra chu kỳ lặp
        if auto_stop_on_cycle:
            if current_hash in seen_hashes:
                cycle_detected = True
                break
            seen_hashes[current_hash] = iteration

    end_time = datetime.now()
    total_time_ms = (end_time - start_time).total_seconds() * 1000
    final_data_hash = calculate_hash(current_data)

    return DecodeResult(
        final_data=current_data,
        iterations=len(steps),
        total_steps=len(steps),
        steps=steps,
        cycle_detected=cycle_detected,
        reached_max_iterations=len(steps) >= max_iterations,
        total_time_ms=total_time_ms,
        original_data_hash=original_data_hash,
        final_data_hash=final_data_hash
    )

def _try_decode_by_type(data: str, encoding_type: EncodingType) -> Tuple[str, float]:
    """
    Helper function to decode by specific encoding type.
    Hàm helper để giải mã theo loại encoding cụ thể.
    """
    if encoding_type == EncodingType.BASE64:
        return try_decode_base64(data)
    elif encoding_type == EncodingType.BASE64_LENIENT:
        return try_decode_base64_lenient(data)
    elif encoding_type == EncodingType.HTML_ENTITY:
        return decode_html_entities(data)
    elif encoding_type == EncodingType.XML_ENTITY:
        return decode_xml_entities(data)
    elif encoding_type == EncodingType.URI_ENCODED:
        return try_decode_uri_encoded(data)
    elif encoding_type == EncodingType.DOUBLE_ENCODED:
        return try_decode_double_encoded(data)
    elif encoding_type == EncodingType.JS_ESCAPE:
        return try_decode_js_escape(data)
    elif encoding_type == EncodingType.JSON_ESCAPE:
        return try_decode_json_escape(data)
    elif encoding_type == EncodingType.HEX:
        return try_decode_hex(data)
    elif encoding_type == EncodingType.ROT13:
        return try_decode_rot13(data)
    elif encoding_type == EncodingType.UNICODE_ESCAPE:
        return try_decode_unicode_escape(data)
    else:
        return data, 0.0

# ============================================================================
# ADDITIONAL UTILITY FUNCTIONS / HÀM BỔ SUNG VÀ TIỆN ÍCH
# ============================================================================

def format_result_as_json(result: DecodeResult) -> str:
    """
    Convert decode result to JSON string for easy integration.
    Chuyển đổi kết quả giải mã sang JSON string để dễ tích hợp.
    """
    steps_data = [asdict(step) for step in result.steps]

    result_dict = {
        "final_data": result.final_data,
        "iterations": result.iterations,
        "total_steps": result.total_steps,
        "cycle_detected": result.cycle_detected,
        "reached_max_iterations": result.reached_max_iterations,
        "total_time_ms": result.total_time_ms,
        "original_data_hash": result.original_data_hash,
        "final_data_hash": result.final_data_hash,
        "steps": steps_data
    }

    return json.dumps(result_dict, ensure_ascii=False, indent=2)

def get_decoding_statistics(result: DecodeResult) -> Dict[str, Any]:
    """
    Detailed statistics about the decoding process.
    Thống kê chi tiết về quá trình giải mã.
    """
    if not result.steps:
        return {}
    
    successful_steps = [s for s in result.steps if s.success]
    if not successful_steps:
        return {
            "successful_iterations": 0,
            "total_size_reduction": 0,
            "size_reduction_percent": 0,
            "most_effective_encoding": None,
            "average_confidence": 0
        }
    
    total_size_reduction = result.steps[0].input_length - result.steps[-1].output_length
    size_reduction_percent = (total_size_reduction / result.steps[0].input_length) * 100 if result.steps[0].input_length > 0 else 0
    
    return {
        "successful_iterations": len(successful_steps),
        "total_size_reduction": total_size_reduction,
        "size_reduction_percent": round(size_reduction_percent, 2),
        "most_effective_encoding": max(successful_steps, key=lambda x: x.confidence).encoding_type,
        "average_confidence": round(sum(s.confidence for s in successful_steps) / len(successful_steps), 3)
    }

def quick_decode(data: str, max_iterations: int = 10) -> str:
    """
    Quick decode function, returns final result without details.
    Hàm giải mã nhanh, trả về kết quả cuối cùng mà không cần chi tiết.
    """
    result = deep_decode_data(data, max_iterations=max_iterations)
    return result.final_data
