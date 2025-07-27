from dataclasses import dataclass
from typing import Any

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
    version: str
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
            version=data["version"],
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
    upload_time: str
    upload_time_iso_8601: str
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
            upload_time=data["upload_time"],
            upload_time_iso_8601=data["upload_time_iso_8601"],
            url=data["url"],
            yanked=data["yanked"],
            yanked_reason=data["yanked_reason"],
        )


@dataclass
class ProjectResponse:
    info: ProjectInfo
    last_serial: int
    releases: dict[str, list[ReleaseFile]]
    urls: list[ReleaseFile]
    vulnerabilities: list[Any]

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Self:
        releases = {}

        # Handle case where releases key might not exist (specific version endpoints)
        if "releases" in data:
            for version, files in data["releases"].items():
                release_files = []
                for file_data in files:
                    if isinstance(file_data, str) and file_data == "...":
                        continue
                    release_files.append(ReleaseFile.from_json(file_data))
                releases[version] = release_files

        return cls(
            info=ProjectInfo.from_json(data["info"]),
            last_serial=data["last_serial"],
            releases=releases,
            urls=[ReleaseFile.from_json(f) for f in data["urls"]],
            vulnerabilities=data.get("vulnerabilities", []),
        )
