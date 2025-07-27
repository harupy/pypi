import json
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any, cast

import httpx
import pytest
from pytest_httpx import HTTPXMock

from pypi.clients import PyPIClient
from pypi.types import ProjectResponse


@pytest.fixture
def requests_data() -> dict[str, Any]:
    """Load requests package test data."""
    fixture_file = Path(__file__).parent.parent / "fixtures" / "requests_latest.json"
    with open(fixture_file) as f:
        return cast(dict[str, Any], json.load(f))


@pytest.fixture
def requests_version_data() -> dict[str, Any]:
    """Load requests package specific version test data."""
    fixture_file = Path(__file__).parent.parent / "fixtures" / "requests_2.31.0.json"
    with open(fixture_file) as f:
        return cast(dict[str, Any], json.load(f))


@pytest.fixture
def numpy_data() -> dict[str, Any]:
    """Load numpy package test data."""
    fixture_file = Path(__file__).parent.parent / "fixtures" / "numpy_latest.json"
    with open(fixture_file) as f:
        return cast(dict[str, Any], json.load(f))


@pytest.fixture
async def client() -> AsyncGenerator[PyPIClient, None]:
    """Create a PyPI client instance."""
    async with PyPIClient() as client:
        yield client


@pytest.mark.asyncio
async def test_get_project_requests(
    client: PyPIClient, requests_data: dict[str, Any], httpx_mock: HTTPXMock
) -> None:
    """Test successful retrieval of requests package."""
    httpx_mock.add_response(
        url="https://pypi.org/pypi/requests/json",
        json=requests_data,
        status_code=200,
    )

    result = await client.get_project("requests")

    assert isinstance(result, ProjectResponse)
    assert result.info.name == "requests"
    assert result.info.version == "2.32.4"
    assert result.info.author == "Kenneth Reitz"
    assert result.info.author_email == "me@kennethreitz.org"
    assert result.info.summary == "Python HTTP for Humans."
    assert result.info.license == "Apache-2.0"
    assert len(result.info.classifiers) > 0
    assert result.info.downloads.last_day >= -1
    assert result.info.downloads.last_month >= -1
    assert result.info.downloads.last_week >= -1
    assert len(result.releases) > 0
    assert len(result.urls) > 0


@pytest.mark.asyncio
async def test_get_project_numpy(
    client: PyPIClient, numpy_data: dict[str, Any], httpx_mock: HTTPXMock
) -> None:
    """Test successful retrieval of numpy package."""
    httpx_mock.add_response(
        url="https://pypi.org/pypi/numpy/json",
        json=numpy_data,
        status_code=200,
    )

    result = await client.get_project("numpy")

    assert isinstance(result, ProjectResponse)
    assert result.info.name == "numpy"
    assert result.info.author == "Travis E. Oliphant et al."
    assert "array computing" in result.info.summary.lower()
    assert len(result.info.classifiers) > 0
    assert len(result.releases) > 0
    assert len(result.urls) > 0


@pytest.mark.asyncio
async def test_get_project_version_requests(
    client: PyPIClient, requests_version_data: dict[str, Any], httpx_mock: HTTPXMock
) -> None:
    """Test successful specific version retrieval for requests."""
    httpx_mock.add_response(
        url="https://pypi.org/pypi/requests/2.31.0/json",
        json=requests_version_data,
        status_code=200,
    )

    result = await client.get_project_version("requests", "2.31.0")

    assert isinstance(result, ProjectResponse)
    assert result.info.name == "requests"
    assert result.info.version == "2.31.0"


@pytest.mark.asyncio
async def test_get_project_not_found(client: PyPIClient, httpx_mock: HTTPXMock) -> None:
    """Test handling of 404 for non-existent project."""
    httpx_mock.add_response(
        url="https://pypi.org/pypi/nonexistent/json",
        status_code=404,
    )

    with pytest.raises(ValueError, match="Project 'nonexistent' not found on PyPI"):
        await client.get_project("nonexistent")


@pytest.mark.asyncio
async def test_get_project_server_error(client: PyPIClient, httpx_mock: HTTPXMock) -> None:
    """Test handling of server errors."""
    httpx_mock.add_response(
        url="https://pypi.org/pypi/sampleproject/json",
        status_code=500,
    )

    with pytest.raises(httpx.HTTPStatusError):
        await client.get_project("sampleproject")


@pytest.mark.asyncio
async def test_project_name_encoding(
    client: PyPIClient, requests_data: dict[str, Any], httpx_mock: HTTPXMock
) -> None:
    """Test URL encoding of project names with special characters."""
    httpx_mock.add_response(
        url="https://pypi.org/pypi/my%20project/json",
        json=requests_data,
        status_code=200,
    )

    result = await client.get_project("my project")
    assert isinstance(result, ProjectResponse)


@pytest.mark.asyncio
async def test_custom_base_url(requests_data: dict[str, Any], httpx_mock: HTTPXMock) -> None:
    """Test using a custom base URL."""
    httpx_mock.add_response(
        url="https://custom.pypi.org/pypi/requests/json",
        json=requests_data,
        status_code=200,
    )

    async with PyPIClient(base_url="https://custom.pypi.org") as client:
        result = await client.get_project("requests")
        assert isinstance(result, ProjectResponse)


@pytest.mark.asyncio
async def test_context_manager(requests_data: dict[str, Any], httpx_mock: HTTPXMock) -> None:
    """Test async context manager functionality."""
    httpx_mock.add_response(
        url="https://pypi.org/pypi/requests/json",
        json=requests_data,
        status_code=200,
    )

    async with PyPIClient() as client:
        result = await client.get_project("requests")
        assert isinstance(result, ProjectResponse)

    # Client should be closed after exiting context
    # This is implicitly tested by the context manager


@pytest.mark.asyncio
async def test_close_method() -> None:
    """Test explicit close method."""
    client = PyPIClient()
    await client.close()
    # No exception should be raised


@pytest.mark.asyncio
async def test_real_data_structure(
    client: PyPIClient, requests_data: dict[str, Any], httpx_mock: HTTPXMock
) -> None:
    """Test that real PyPI data structure matches our types."""
    httpx_mock.add_response(
        url="https://pypi.org/pypi/requests/json",
        json=requests_data,
        status_code=200,
    )

    result = await client.get_project("requests")

    # Test nested objects
    assert hasattr(result.info.downloads, "last_day")
    assert hasattr(result.info.downloads, "last_month")
    assert hasattr(result.info.downloads, "last_week")

    # Test release files have digests
    for files in result.releases.values():
        for file in files:
            if file.digests:  # Some old releases might not have all digests
                assert hasattr(file.digests, "md5")
                assert hasattr(file.digests, "sha256")
                assert hasattr(file.digests, "blake2b_256")

    # Test URLs structure
    for url_file in result.urls:
        assert url_file.filename
        assert url_file.url
        assert url_file.packagetype in ["sdist", "bdist_wheel"]
