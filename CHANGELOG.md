# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2025-10-18

### Fixed
- Fixed path traversal example in README (corrected from `/.p.p//etc/passwd` to `/../etc/passwd`)
- Updated example encoded payload to properly demonstrate Base64 + Double URL-encoding attack

### Documentation
- Corrected security analysis example with proper path traversal attack string

## [1.0.1] - 2025-10-18

### Changed
- Added comprehensive English comments/documentation throughout the codebase
- All functions, classes, and code blocks now have bilingual comments (English/Vietnamese)
- Improved code readability for international developers

### Documentation
- Enhanced inline documentation with English translations
- Better code comments for maintainability

## [1.0.0] - 2025-10-18

### Added
- Initial release of Deep Decoder
- Support for 12+ encoding types:
  - Base64 (strict and lenient modes)
  - URL/URI encoding (single and double)
  - HTML entities
  - XML entities
  - JavaScript escape sequences
  - JSON escape sequences
  - Unicode escape sequences
  - Hexadecimal
  - ROT13
- Automatic encoding detection
- Multi-layer recursive decoding
- Cycle detection to prevent infinite loops
- Confidence scoring for each decoding step
- Detailed statistics and reporting
- JSON export functionality
- Quick decode function for simple use cases
- Comprehensive documentation and examples
- Zero external dependencies (Python standard library only)

### Features
- `deep_decode_data()`: Main decoding function with full details
- `quick_decode()`: Simple decoding without details
- `format_result_as_json()`: Export results as JSON
- `get_decoding_statistics()`: Get decoding statistics
- Individual decoder functions for each encoding type
- Custom encoding priority configuration
- Configurable maximum iterations
- Automatic and manual encoding detection modes

### Documentation
- Complete README with usage examples
- API reference documentation
- Security analysis examples
- Installation instructions
- Contributing guidelines

[1.0.0]: https://github.com/yourusername/deep-decoder/releases/tag/v1.0.0
