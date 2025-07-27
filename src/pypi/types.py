from dataclasses import dataclass
from datetime import datetime
from typing import Any

from packaging.version import InvalidVersion, Version
from typing_extensions import Self


@dataclass
class Downloads:
    last_day: int
    last_month: int
    last_week: int

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            last_day=data["last_day"],
            last_month=data["last_month"],
            last_week=data["last_week"],
        )


@dataclass
class ProjectInfo:
    author: str
    author_email: str
    bugtrack_url: str | None
    classifiers: list[str]
    description: str
    description_content_type: str
    docs_url: str | None
    download_url: str
    downloads: Downloads
    dynamic: list[str]
    home_page: str
    keywords: str
    license: str
    maintainer: str
    maintainer_email: str
    name: str
    package_url: str
    platform: str | None
    project_url: str
    project_urls: dict[str, str]
    provides_extra: list[str]
    release_url: str
    requires_dist: list[str]
    requires_python: str
    summary: str
    version: Version
    yanked: bool
    yanked_reason: str | None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            author=data["author"],
            author_email=data["author_email"],
            bugtrack_url=data["bugtrack_url"],
            classifiers=data["classifiers"],
            description=data["description"],
            description_content_type=data["description_content_type"],
            docs_url=data["docs_url"],
            download_url=data["download_url"],
            downloads=Downloads.from_json(data["downloads"]),
            dynamic=data.get("dynamic", []),
            home_page=data["home_page"],
            keywords=data["keywords"],
            license=data["license"],
            maintainer=data["maintainer"],
            maintainer_email=data["maintainer_email"],
            name=data["name"],
            package_url=data["package_url"],
            platform=data["platform"],
            project_url=data["project_url"],
            project_urls=data["project_urls"],
            provides_extra=data.get("provides_extra", []),
            release_url=data["release_url"],
            requires_dist=data.get("requires_dist", []),
            requires_python=data["requires_python"],
            summary=data["summary"],
            version=Version(data["version"]),
            yanked=data["yanked"],
            yanked_reason=data["yanked_reason"],
        )


@dataclass
class Digests:
    blake2b_256: str
    md5: str
    sha256: str

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            blake2b_256=data["blake2b_256"],
            md5=data["md5"],
            sha256=data["sha256"],
        )


@dataclass
class ReleaseFile:
    comment_text: str
    digests: Digests
    downloads: int
    filename: str
    has_sig: bool
    md5_digest: str
    packagetype: str
    python_version: str
    requires_python: str | None
    size: int
    upload_time: datetime
    upload_time_iso_8601: datetime
    url: str
    yanked: bool
    yanked_reason: str | None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            comment_text=data["comment_text"],
            digests=Digests.from_json(data["digests"]),
            downloads=data["downloads"],
            filename=data["filename"],
            has_sig=data["has_sig"],
            md5_digest=data["md5_digest"],
            packagetype=data["packagetype"],
            python_version=data["python_version"],
            requires_python=data["requires_python"],
            size=data["size"],
            upload_time=datetime.fromisoformat(data["upload_time"].replace("Z", "+00:00")),
            upload_time_iso_8601=datetime.fromisoformat(
                data["upload_time_iso_8601"].replace("Z", "+00:00")
            ),
            url=data["url"],
            yanked=data["yanked"],
            yanked_reason=data["yanked_reason"],
        )


@dataclass
class Vulnerability:
    aliases: list[str]
    details: str
    summary: str | None
    fixed_in: list[str]
    id: str
    link: str
    source: str
    withdrawn: str | None

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        return cls(
            aliases=data["aliases"],
            details=data["details"],
            summary=data.get("summary"),
            fixed_in=data["fixed_in"],
            id=data["id"],
            link=data["link"],
            source=data["source"],
            withdrawn=data["withdrawn"],
        )


@dataclass
class ProjectResponse:
    info: ProjectInfo
    last_serial: int
    releases: dict[Version, list[ReleaseFile]]
    urls: list[ReleaseFile]
    vulnerabilities: list[Vulnerability]

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        releases: dict[Version, list[ReleaseFile]] = {}

        # Handle case where releases key might not exist (specific version endpoints)
        if releases_data := data.get("releases"):
            for version_str, files in releases_data.items():
                try:
                    version_key = Version(version_str)
                except InvalidVersion:
                    # Skip invalid version strings
                    continue
                else:
                    release_files: list[ReleaseFile] = []
                    for file_data in files:
                        release_files.append(ReleaseFile.from_json(file_data))
                    releases[version_key] = release_files

        return cls(
            info=ProjectInfo.from_json(data["info"]),
            last_serial=data["last_serial"],
            releases=releases,
            urls=[ReleaseFile.from_json(f) for f in data["urls"]],
            vulnerabilities=[
                Vulnerability.from_json(vuln) for vuln in data.get("vulnerabilities", [])
            ],
        )
