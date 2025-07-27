from typing import Any
from urllib.parse import quote

import httpx
from typing_extensions import Self

from .types import ProjectResponse


class PyPIClient:
    def __init__(self, base_url: str = "https://pypi.org") -> None:
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient()

    async def get_project(self, project_name: str) -> ProjectResponse:
        """Fetch project JSON metadata from PyPI API."""
        url = f"{self.base_url}/pypi/{quote(project_name)}/json"

        try:
            response = await self.client.get(url, headers={"Accept": "application/json"})
            response.raise_for_status()
            data = response.json()
            return ProjectResponse.from_json(data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Project '{project_name}' not found on PyPI")
            raise

    async def get_project_version(self, project_name: str, version: str) -> ProjectResponse:
        """Fetch specific version JSON metadata from PyPI API."""
        url = f"{self.base_url}/pypi/{quote(project_name)}/{quote(version)}/json"

        try:
            response = await self.client.get(url, headers={"Accept": "application/json"})
            response.raise_for_status()
            data = response.json()
            return ProjectResponse.from_json(data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise ValueError(f"Project '{project_name}' version '{version}' not found on PyPI")
            raise

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.client.aclose()

    async def close(self) -> None:
        await self.client.aclose()
