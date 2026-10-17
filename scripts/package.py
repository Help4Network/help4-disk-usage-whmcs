"""Build WHMCS-only archives independently of either native panel checkout."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MODULES = {
    "cpanel": ("help4_disk_usage", ("help4_disk_usage.php", "hooks.php", "templates/clientarea.tpl")),
    "plesk": ("help4_disk_usage_plesk", ("help4_disk_usage_plesk.php", "hooks.php", "templates/clientarea.tpl",
              "lib/Scope.php", "lib/Health.php", "lib/Report.php", "lib/Transport.php", "lib/Native.php", "lib/View.php")),
}
DOCUMENTS = ("README.md", "CHANGELOG.md", "LICENSE", "licenses/plesk-LICENSE", "VERSION", "components.json", "SECURITY.md",
             "docs/install.md", "docs/upgrade.md", "docs/compatibility.md", "docs/validation.md",
             "docs/cpanel.md", "docs/plesk.md", "docs/cpanel-file-workflows.md")


def safe(path, directory=False):
    metadata = path.lstat()
    if stat.S_ISLNK(metadata.st_mode) or getattr(metadata, "st_file_attributes", 0) & 0x400:
        raise RuntimeError("Link or reparse point in package source")
    if os.name == "nt" and not hasattr(metadata, "st_file_attributes"):
        raise RuntimeError("Windows reparse metadata unavailable")
    if not (stat.S_ISDIR(metadata.st_mode) if directory else stat.S_ISREG(metadata.st_mode)):
        raise RuntimeError("Unexpected package source object")


def inventory(root):
    safe(root, True)
    found = set()
    for child in sorted(root.iterdir()):
        metadata = child.lstat()
        if stat.S_ISLNK(metadata.st_mode) or getattr(metadata, "st_file_attributes", 0) & 0x400:
            raise RuntimeError("Link or reparse point before traversal")
        if stat.S_ISDIR(metadata.st_mode):
            found.update(child.name + "/" + name for name in inventory(child))
        else:
            safe(child)
            found.add(child.name)
    return found


def build(destination=None, component="all"):
    if component not in ("all", *MODULES):
        raise ValueError("Unknown component")
    safe(ROOT, True)
    safe(ROOT / "modules", True)
    safe(ROOT / "modules/addons", True)
    for name in DOCUMENTS:
        current = ROOT
        for part in Path(name).parts[:-1]:
            current /= part
            safe(current, True)
        safe(ROOT / name)
    version = (ROOT / "VERSION").read_text(encoding="ascii").strip()
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        raise RuntimeError("Invalid distribution version")
    metadata = json.loads((ROOT / "components.json").read_text(encoding="utf-8"))
    if metadata.get("distribution_version") != version or metadata.get("schema") != 1:
        raise RuntimeError("Component manifest mismatch")
    if inventory(ROOT / "modules/addons") != {
        module + "/" + name for module, names in MODULES.values() for name in names
    }:
        raise RuntimeError("Unexpected or incomplete addon inventory")
    entries = {name: (ROOT / name).read_bytes() for name in DOCUMENTS}
    for backend, (module, names) in MODULES.items():
        config = (ROOT / "modules/addons" / module / (module + ".php")).read_text(encoding="utf-8")
        declared = re.search(r"const H4DU_VERSION = '([^']+)'", config) if backend == "cpanel" else re.search(r"'version' => '([^']+)'", config)
        if not declared or declared[1] != metadata["components"][backend]["version"] or metadata["components"][backend]["module"] != module:
            raise RuntimeError("Addon version/identity mismatch")
        if component not in ("all", backend):
            continue
        for name in names:
            path = "modules/addons/" + module + "/" + name
            entries[path] = (ROOT / path).read_bytes()
    entries["SHA256SUMS"] = "".join(hashlib.sha256(data).hexdigest() + "  " + name + "\n"
                                  for name, data in sorted(entries.items())).encode("ascii")
    destination = Path(destination) if destination else ROOT / "dist"
    destination.mkdir(parents=True, exist_ok=True)
    safe(destination, True)
    suffix = "" if component == "all" else "-" + component
    archive = destination / ("help4-disk-usage-whmcs" + suffix + "-" + version + ".zip")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=destination, prefix=".whmcs-", suffix=".zip", delete=False) as stream:
            temporary = Path(stream.name)
        with zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as package:
            for name, data in sorted(entries.items()):
                info = zipfile.ZipInfo(name, (2026, 10, 17, 0, 0, 0))
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                package.writestr(info, data)
        digest = hashlib.sha256(temporary.read_bytes()).hexdigest()
        temporary.replace(archive)
        archive.with_suffix(".zip.sha256").write_text(digest + "  " + archive.name + "\n", encoding="ascii")
        return archive, digest
    finally:
        if temporary and temporary.exists():
            temporary.unlink()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--component", choices=("all", "cpanel", "plesk"), default="all")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    archive, digest = build(args.output, args.component)
    print(str(archive) + "\nSHA256 " + digest)
