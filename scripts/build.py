from __future__ import annotations

import hashlib
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "std_statistical_studio.html"
TARGETS = (
    ROOT / "dist" / "std_statistical_studio.html",
    ROOT / "docs" / "index.html",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if not SOURCE.is_file():
        raise SystemExit(f"Missing canonical source: {SOURCE}")

    source_bytes = SOURCE.read_bytes()
    if not source_bytes.startswith(b"<!doctype html>"):
        raise SystemExit("Canonical source is not a standalone HTML document.")

    for target in TARGETS:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOURCE, target)

    hashes = {target: sha256(target) for target in (SOURCE, *TARGETS)}
    if len(set(hashes.values())) != 1:
        raise SystemExit("Release targets are not byte-identical to the source.")

    print(f"BUILD PASS: {len(source_bytes)} bytes")
    print(f"SHA256: {hashes[SOURCE]}")
    for target in TARGETS:
        print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()
