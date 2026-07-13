import os
import urllib.parse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

GITHUB_HOSTS = {"github.com", "raw.githubusercontent.com", "api.github.com"}

_session = requests.Session()
_session.mount(
    "https://",
    HTTPAdapter(
        max_retries=Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"],
        )
    ),
)


def _github_token():
    return (
        os.environ.get("GH_TOKEN")
        or os.environ.get("GITHUB_TOKEN")
        or os.environ.get("API_TOKEN_GITHUB")
    )


def _auth_headers(url):
    host = urllib.parse.urlparse(url).hostname or ""
    if host in GITHUB_HOSTS:
        token = _github_token()
        if token:
            return {"Authorization": f"Bearer {token}"}
    return {}


def fetch(url, *, headers=None, timeout=30.0):
    merged_headers = _auth_headers(url)
    if headers:
        merged_headers.update(headers)
    resp = _session.get(url, headers=merged_headers, timeout=timeout)
    host = urllib.parse.urlparse(url).hostname or ""
    if resp.status_code in (401, 403) or (
        resp.status_code == 404 and host in GITHUB_HOSTS and not _github_token()
    ):
        hint = ""
        if host in GITHUB_HOSTS and not _github_token():
            hint = (
                " (set GH_TOKEN, GITHUB_TOKEN, or API_TOKEN_GITHUB"
                " to access private repos)"
            )
        raise RuntimeError(
            f"Auth failed for {url}: HTTP {resp.status_code}{hint}"
        )
    resp.raise_for_status()
    return resp
