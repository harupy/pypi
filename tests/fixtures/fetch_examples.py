"""
Fetch example JSON data from PyPI for testing purposes.

Usage:
    python fetch_examples.py
    python fetch_examples.py --packages requests numpy pandas
    python fetch_examples.py --package-version requests:2.31.0
"""

import argparse
import json
from pathlib import Path
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen

DEFAULT_PACKAGES = [
    ("requests", None),  # Latest version
    ("requests", "2.31.0"),  # Specific version
    ("numpy", None),  # Latest version
]


def fetch_package_json(package_name: str, version: str | None = None) -> dict[str, Any] | None:
    """Fetch JSON data for a package from PyPI."""
    if version:
        url = f"https://pypi.org/pypi/{quote(package_name)}/{quote(version)}/json"
        print(f"Fetching {package_name} version {version}...")
    else:
        url = f"https://pypi.org/pypi/{quote(package_name)}/json"
        print(f"Fetching {package_name} (latest)...")

    request = Request(url, headers={"Accept": "application/json"})

    try:
        with urlopen(request) as response:
            data = json.loads(response.read().decode("utf-8"))
            print(f"  ✓ Success: {data['info']['name']} {data['info']['version']}")
            return data
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None


def save_package_json(
    data: dict[str, Any],
    output_dir: Path,
    package_name: str,
    version: str | None = None,
    compact: bool = False,
) -> None:
    """Save package JSON data to a file."""
    if version:
        filename = f"{package_name}_{version}.json"
    else:
        filename = f"{package_name}_latest.json"

    output_path = output_dir / filename

    with open(output_path, "w") as f:
        if compact:
            json.dump(data, f, separators=(",", ":"))
        else:
            json.dump(data, f, indent=2)

    print(f"  → Saved to {output_path}")


def parse_package_spec(spec: str) -> tuple[str, str | None]:
    """Parse package specification in format 'package' or 'package:version'."""
    if ":" in spec:
        package, version = spec.split(":", 1)
        return package, version
    return spec, None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch example JSON data from PyPI for testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--packages",
        nargs="+",
        help="Package names to fetch (format: 'package' or 'package:version')",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).parent,
        help="Output directory for JSON files (default: current directory)",
    )

    parser.add_argument(
        "--compact",
        action="store_true",
        help="Save JSON in compact format (no indentation)",
    )

    args = parser.parse_args()

    # Determine which packages to fetch
    if args.packages:
        packages = [parse_package_spec(spec) for spec in args.packages]
    else:
        packages = DEFAULT_PACKAGES

    # Ensure output directory exists
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Fetch and save each package
    print(f"\nFetching {len(packages)} package(s) from PyPI...\n")

    for package_name, version in packages:
        data = fetch_package_json(package_name, version)
        if data:
            save_package_json(data, args.output_dir, package_name, version, args.compact)
        print()

    print("Done!")


if __name__ == "__main__":
    main()
