# PyPI API Client

[![CI](https://github.com/harupy/pypi/actions/workflows/ci.yml/badge.svg)](https://github.com/harupy/pypi/actions/workflows/ci.yml)

A modern, type-safe Python client for the PyPI API.

## Features

- 🚀 **Async/await support** with httpx
- 📦 **Full PyPI API coverage** for package metadata
- 🔒 **Type-safe** with comprehensive type hints
- ✅ **Well tested** with real PyPI data
- 🎯 **Simple API** with context manager support

## Installation

```bash
pip install pypi
```

## Usage

```python
import asyncio
from pypi.clients import PyPIClient

async def main():
    async with PyPIClient() as client:
        # Get latest package info
        package = await client.get_project("requests")
        print(f"{package.info.name} {package.info.version}")
        print(f"Summary: {package.info.summary}")

        # Get specific version
        version = await client.get_project_version("requests", "2.31.0")
        print(f"Version {version.info.version} has {len(version.urls)} files")

asyncio.run(main())
```

## Development

Install development dependencies:

```bash
uv sync --dev
```

Run tests:

```bash
uv run pytest
```

Run linting and formatting:

```bash
uv run ruff check --fix
uv run ruff format
uv run mypy .
```

## License

MIT
