#!/usr/bin/python3
"""Bounded public GET collector. No shell, credentials, uploads or remote code."""
import concurrent.futures
import datetime
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/literature/fetch-manifest.json"
OUT = ROOT / "docs/literature/raw"
HOSTS = {
    "api.github.com", "raw.githubusercontent.com", "github.com",
    "api.crossref.org", "api.openalex.org", "api.semanticscholar.org",
    "arxiv.org", "export.arxiv.org", "www.arxiv.org",
    "proceedings.mlr.press", "jmlr.org", "www.jmlr.org",
    "proceedings.neurips.cc", "papers.nips.cc", "openreview.net",
    "www.nber.org", "nber.org", "www.aeaweb.org", "aeaweb.org",
    "www.bis.org", "bis.org", "www.federalreserve.gov", "federalreserve.gov",
    "www.bankofengland.co.uk", "www.ecb.europa.eu", "www.fca.org.uk",
    "pypi.org", "cran.r-project.org", "cran.rstudio.com",
    "www.pywhy.org", "docs.doubleml.org", "econml.azurewebsites.net",
    "tetrad.org", "www.phil.cmu.edu", "www.cs.cmu.edu", "web.mit.edu",
    "www.hsph.harvard.edu", "content.sph.harvard.edu", "miguelhernan.org",
    "matheusfacure.github.io", "scott.ph", "psantanna.com",
    "jonathandroth.com", "www.jonathandroth.com", "bcallaway11.github.io",
    "www.annualreviews.org", "academic.oup.com", "www.pnas.org",
    "www.nature.com", "nature.com", "www.science.org",
    "projecteuclid.org", "www.projecteuclid.org", "arxiv-vanity.com",
    "docs.ray.io", "duckdb.org", "docs.pola.rs", "arrow.apache.org",
    "spark.apache.org", "iceberg.apache.org", "openlineage.io",
    "docs.open-metadata.org", "docs.datahub.com", "docs.feast.dev",
    "developers.openai.com", "platform.openai.com", "learn.chatgpt.com",
}
MAX_BYTES = 64 * 1024 * 1024


def validate_url(url):
    parsed = urllib.parse.urlsplit(url)
    if (parsed.scheme != "https" or parsed.hostname not in HOSTS
            or parsed.username or parsed.password or parsed.port not in (None, 443)):
        raise ValueError("URL outside fixed public HTTPS allowlist")
    for item in socket.getaddrinfo(parsed.hostname, 443):
        if not ipaddress.ip_address(item[4][0]).is_global:
            raise ValueError("non-public address rejected")
    return url


class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch_one(item):
    key = item["id"]
    if not key or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-" for c in key):
        raise ValueError("invalid artifact id")
    extension = item.get("extension", "json")
    if extension not in {"json", "html", "txt", "xml", "pdf", "md"}:
        raise ValueError("invalid extension")
    destination = OUT / f"{key}.{extension}"
    receipt_path = OUT / f"{key}.receipt.json"
    if destination.is_symlink() or receipt_path.is_symlink():
        raise ValueError("symlink output rejected")
    if destination.exists() and receipt_path.exists():
        old = json.loads(receipt_path.read_text())
        if old.get("url") == item["url"] and old.get("sha256") == hashlib.sha256(destination.read_bytes()).hexdigest():
            return {"id": key, "status": "cached"}
    record = {"id": key, "url": item["url"], "accessed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        validate_url(item["url"])
        opener = urllib.request.build_opener(SafeRedirect())
        request = urllib.request.Request(item["url"], headers={"User-Agent": "CausalBankResearch/1.0 (public literature audit)", "Accept": "*/*"})
        with opener.open(request, timeout=40) as response:
            data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise ValueError("response exceeds 64 MiB cap")
            record.update(final_url=response.url, content_type=response.headers.get("Content-Type"), http_status=response.status)
        if extension == "pdf" and not data.startswith(b"%PDF-"):
            raise ValueError("response is not a PDF")
        if extension == "json":
            json.loads(data)
        temp = destination.with_suffix(destination.suffix + ".part")
        if temp.is_symlink():
            raise ValueError("symlink temporary file rejected")
        temp.write_bytes(data)
        os.replace(temp, destination)
        record.update(status="saved", path=str(destination.relative_to(ROOT)), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    except Exception as exc:
        record.update(status="failed", error=f"{type(exc).__name__}: {exc}")
    receipt_path.write_text(json.dumps(record, indent=2) + "\n")
    return {k: record[k] for k in ("id", "status", "error") if k in record}


def main():
    if sys.argv[1:] != ["fetch"]:
        raise SystemExit("Exact command: public_sources.py fetch")
    items = json.loads(MANIFEST.read_text())["requests"]
    if len(items) > 1200 or len({x["id"] for x in items}) != len(items):
        raise ValueError("manifest size/identity constraint")
    OUT.mkdir(parents=True, exist_ok=True)
    if OUT.resolve() != OUT:
        raise ValueError("output directory uses a symlink")
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for row in pool.map(fetch_one, items):
            print(json.dumps(row), flush=True)


if __name__ == "__main__":
    main()
