#!/usr/bin/env python3
"""
Zero-Daemon OCI Container Image Assembler & Artifact Registry V2 Pusher for Ideas-Mining Studio.
Layers the staged /app directory onto mirror.gcr.io/library/python:3.12-slim (linux/amd64)
and pushes directly to Artifact Registry via Docker Registry HTTP API v2.
"""
from __future__ import annotations

import gzip
import hashlib
import io
import json
import os
import subprocess
import sys
import tarfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone


def get_gcloud_token() -> str:
    env = os.environ.copy()
    existing = env.get("CLOUDSDK_METRICS_ENVIRONMENT", "")
    env["CLOUDSDK_METRICS_ENVIRONMENT"] = f"{existing} datacloud.antigravity".strip()
    return subprocess.check_output(
        ["gcloud", "auth", "print-access-token"], text=True, env=env
    ).strip()


def http_req(url: str, method: str = "GET", headers: dict | None = None, data: bytes | None = None):
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    return urllib.request.urlopen(req, timeout=180)


def blob_exists(dest_host: str, dest_repo: str, digest: str, token: str) -> bool:
    url = f"https://{dest_host}/v2/{dest_repo}/blobs/{digest}"
    try:
        with http_req(url, method="HEAD", headers={"Authorization": f"Bearer {token}"}) as resp:
            return resp.status == 200
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        raise


def upload_blob(dest_host: str, dest_repo: str, digest: str, payload: bytes, token: str) -> None:
    if blob_exists(dest_host, dest_repo, digest, token):
        print(f"  [cache-hit] Blob {digest[:19]}... ({len(payload)} bytes) already exists in {dest_repo}")
        return
    init_url = f"https://{dest_host}/v2/{dest_repo}/blobs/uploads/"
    with http_req(
        init_url,
        method="POST",
        headers={"Authorization": f"Bearer {token}", "Content-Length": "0"},
    ) as resp:
        loc = resp.headers.get("Location")
    if not loc:
        raise RuntimeError(f"Missing Location header from {init_url}")
    if loc.startswith("/"):
        loc = f"https://{dest_host}{loc}"
    sep = "&" if "?" in loc else "?"
    put_url = f"{loc}{sep}digest={urllib.parse.quote(digest)}"
    with http_req(
        put_url,
        method="PUT",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/octet-stream",
            "Content-Length": str(len(payload)),
        },
        data=payload,
    ) as resp:
        if resp.status not in (200, 201, 202, 204):
            raise RuntimeError(f"Unexpected blob PUT status {resp.status} for {digest}")
    print(f"  [uploaded]  Blob {digest[:19]}... ({len(payload)} bytes)")


def build_app_layer(stage_dir: str) -> tuple[bytes, str, str, int]:
    """Builds a deterministic tar + gzip layer placing stage_dir contents under app/."""
    tar_buf = io.BytesIO()
    mtime = int(time.time())
    with tarfile.open(fileobj=tar_buf, mode="w", format=tarfile.PAX_FORMAT) as tf:
        app_root = tarfile.TarInfo(name="app")
        app_root.type = tarfile.DIRTYPE
        app_root.mode = 0o755
        app_root.uid = 0
        app_root.gid = 0
        app_root.uname = "root"
        app_root.gname = "root"
        app_root.mtime = mtime
        tf.addfile(app_root)

        for root, dirs, files in os.walk(stage_dir):
            dirs[:] = sorted(d for d in dirs if d not in (".git", "__pycache__"))
            files.sort()
            rel_root = os.path.relpath(root, stage_dir)
            if rel_root != ".":
                arc_dir = os.path.join("app", rel_root).replace("\\", "/")
                ti = tarfile.TarInfo(name=arc_dir)
                ti.type = tarfile.DIRTYPE
                ti.mode = 0o755
                ti.uid = 0
                ti.gid = 0
                ti.uname = "root"
                ti.gname = "root"
                ti.mtime = mtime
                tf.addfile(ti)

            for fname in files:
                if fname in ("Dockerfile.runtime", "cloudbuild.yaml") or fname.endswith(".pyc"):
                    continue
                full_path = os.path.join(root, fname)
                if not os.path.isfile(full_path):
                    continue
                rel_path = os.path.relpath(full_path, stage_dir)
                arc_name = os.path.join("app", rel_path).replace("\\", "/")
                with open(full_path, "rb") as f:
                    raw = f.read()
                ti = tarfile.TarInfo(name=arc_name)
                ti.size = len(raw)
                ti.mode = 0o755 if fname.endswith((".py", ".sh", ".mjs")) else 0o644
                ti.uid = 0
                ti.gid = 0
                ti.uname = "root"
                ti.gname = "root"
                ti.mtime = mtime
                tf.addfile(ti, io.BytesIO(raw))

    uncompressed_bytes = tar_buf.getvalue()
    diff_id = "sha256:" + hashlib.sha256(uncompressed_bytes).hexdigest()

    gz_buf = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=gz_buf, compresslevel=6, mtime=mtime) as gz:
        gz.write(uncompressed_bytes)
    compressed_bytes = gz_buf.getvalue()
    layer_digest = "sha256:" + hashlib.sha256(compressed_bytes).hexdigest()
    return compressed_bytes, diff_id, layer_digest, len(compressed_bytes)


def main() -> None:
    if len(sys.argv) < 4:
        print("Usage: oci_push_ideas_mining.py <STAGE_DIR> <DEST_HOST> <DEST_REPO> <TAG> [TAG2...]", file=sys.stderr)
        sys.exit(1)

    stage_dir = sys.argv[1]
    dest_host = sys.argv[2]
    dest_repo = sys.argv[3]
    tags = sys.argv[4:]

    token = get_gcloud_token()
    base_registry = "https://mirror.gcr.io/v2/library/python"

    print("==> [OCI 1/4] Resolving mirror.gcr.io/library/python:3.12-slim (linux/amd64)...")
    with http_req(
        f"{base_registry}/manifests/3.12-slim",
        headers={
            "Accept": (
                "application/vnd.oci.image.index.v1+json, "
                "application/vnd.docker.distribution.manifest.list.v2+json"
            )
        },
    ) as resp:
        idx = json.loads(resp.read().decode())

    amd64_digest = None
    for m in idx.get("manifests", []):
        plat = m.get("platform", {})
        if plat.get("os") == "linux" and plat.get("architecture") == "amd64":
            amd64_digest = m["digest"]
            break
    if not amd64_digest:
        raise RuntimeError("Could not find linux/amd64 manifest in python:3.12-slim index")

    with http_req(
        f"{base_registry}/manifests/{amd64_digest}",
        headers={
            "Accept": (
                "application/vnd.oci.image.manifest.v1+json, "
                "application/vnd.docker.distribution.manifest.v2+json"
            )
        },
    ) as resp:
        base_manifest = json.loads(resp.read().decode())

    base_cfg_digest = base_manifest["config"]["digest"]
    with http_req(f"{base_registry}/blobs/{base_cfg_digest}") as resp:
        base_config = json.loads(resp.read().decode())

    print(f"==> [OCI 2/4] Syncing {len(base_manifest['layers'])} base layers to {dest_host}/{dest_repo}...")
    for layer in base_manifest["layers"]:
        ldigest = layer["digest"]
        if blob_exists(dest_host, dest_repo, ldigest, token):
            print(f"  [cache-hit] Base layer {ldigest[:19]}... ({layer['size']} bytes)")
            continue
        print(f"  [fetching]  Base layer {ldigest[:19]}... ({layer['size']} bytes) from mirror.gcr.io")
        with http_req(f"{base_registry}/blobs/{ldigest}") as resp:
            blob_bytes = resp.read()
        upload_blob(dest_host, dest_repo, ldigest, blob_bytes, token)

    print(f"==> [OCI 3/4] Assembling /app layer from {stage_dir}...")
    app_gz_bytes, app_diff_id, app_layer_digest, app_layer_size = build_app_layer(stage_dir)
    upload_blob(dest_host, dest_repo, app_layer_digest, app_gz_bytes, token)

    cfg_obj = base_config.setdefault("config", {})
    cfg_obj["WorkingDir"] = "/app"
    env_list = [e for e in cfg_obj.get("Env", []) if not e.startswith(("PORT=", "HOST="))]
    env_list.extend(["HOST=0.0.0.0", "PORT=8080"])
    cfg_obj["Env"] = env_list
    cfg_obj["ExposedPorts"] = {"8080/tcp": {}}
    cfg_obj["Cmd"] = ["python3", "server.py"]

    base_config["created"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    base_config.setdefault("rootfs", {"type": "layers", "diff_ids": []})["diff_ids"].append(app_diff_id)
    base_config.setdefault("history", []).append(
        {
            "created": base_config["created"],
            "created_by": "oci_push_ideas_mining.py COPY /app & CMD python3 server.py",
        }
    )

    new_cfg_bytes = json.dumps(base_config, separators=(",", ":")).encode("utf-8")
    new_cfg_digest = "sha256:" + hashlib.sha256(new_cfg_bytes).hexdigest()
    upload_blob(dest_host, dest_repo, new_cfg_digest, new_cfg_bytes, token)

    manifest_media_type = base_manifest.get("mediaType", "application/vnd.oci.image.manifest.v1+json")
    layer_media_type = base_manifest["layers"][0].get(
        "mediaType", "application/vnd.oci.image.layer.v1.tar+gzip"
    )
    cfg_media_type = base_manifest["config"].get(
        "mediaType", "application/vnd.oci.image.config.v1+json"
    )

    new_manifest = {
        "schemaVersion": 2,
        "mediaType": manifest_media_type,
        "config": {
            "mediaType": cfg_media_type,
            "digest": new_cfg_digest,
            "size": len(new_cfg_bytes),
        },
        "layers": list(base_manifest["layers"])
        + [
            {
                "mediaType": layer_media_type,
                "digest": app_layer_digest,
                "size": app_layer_size,
            }
        ],
    }
    manifest_bytes = json.dumps(new_manifest, indent=2).encode("utf-8")
    manifest_digest = "sha256:" + hashlib.sha256(manifest_bytes).hexdigest()

    print(f"==> [OCI 4/4] Pushing manifest ({manifest_digest[:19]}...) for tags {tags}...")
    for t in tags:
        m_url = f"https://{dest_host}/v2/{dest_repo}/manifests/{t}"
        with http_req(
            m_url,
            method="PUT",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": manifest_media_type,
                "Content-Length": str(len(manifest_bytes)),
            },
            data=manifest_bytes,
        ) as resp:
            print(f"  [pushed]    {dest_host}/{dest_repo}:{t} (HTTP {resp.status})")


if __name__ == "__main__":
    main()
