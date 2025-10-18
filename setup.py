from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="deep-decoder",
    version="1.0.1",
    author="khoilv2005",
    author_email="khoilv2005@example.com",
    description="Deep Decoder for IDS/IPS, WAF - A comprehensive multi-layer encoding/decoding library for security analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/khoilv2005/deep-decoder",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security",
        "Topic :: Text Processing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        # Không có dependencies ngoài standard library
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=22.0",
            "flake8>=5.0",
            "mypy>=0.990",
        ],
    },
    keywords="decoder encoder base64 url hex html encoding decoding security ids ips waf",
    project_urls={
        "Bug Reports": "https://github.com/khoilv2005/deep-decoder/issues",
        "Source": "https://github.com/khoilv2005/deep-decoder",
    },
)
