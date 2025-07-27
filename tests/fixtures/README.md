# Test Fixtures

This directory contains example JSON responses from PyPI API for testing purposes.

## Files

- `requests_latest.json` - Latest version of the requests package
- `requests_2_31_0.json` - Specific version (2.31.0) of the requests package
- `numpy_latest.json` - Latest version of the numpy package
- `fetch_examples.py` - Script to fetch/refresh example data

## Updating Test Data

To refresh the test data with the latest information from PyPI:

```bash
uv run fetch_examples.py
```

To fetch specific packages:

```bash
# Fetch latest versions
uv run fetch_examples.py --packages requests numpy pandas

# Fetch specific versions
uv run fetch_examples.py --packages requests:2.31.0 numpy:1.26.0

# Mix of latest and specific versions
uv run fetch_examples.py --packages requests requests:2.31.0 numpy
```

## Why These Packages?

- **requests** - Popular HTTP library with simple structure
- **numpy** - Scientific computing library with complex metadata
- Both packages have stable APIs and are unlikely to disappear

These examples cover common PyPI response patterns including:

- Multiple release files (wheels, source distributions)
- Various classifiers and metadata fields
- Different package types and uv run version requirements
- Optional fields that may or may not be present
