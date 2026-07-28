from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "std_statistical_studio.html"
DIST = ROOT / "dist" / "std_statistical_studio.html"
PAGES = ROOT / "docs" / "index.html"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS: {message}")


def main() -> None:
    for path in (SOURCE, DIST, PAGES):
        require(path.is_file(), f"{path.relative_to(ROOT)} exists")

    require(len({digest(SOURCE), digest(DIST), digest(PAGES)}) == 1,
            "source, dist, and Pages HTML are byte-identical")

    html = DIST.read_text(encoding="utf-8")
    require(html.lower().startswith("<!doctype html>"), "standalone HTML doctype")
    require("STD Statistical Studio v0.6" in html, "v0.6 product title")
    require(html.count('registerProcedure("') == 39,
            "39 procedures registered")
    require(sum(html.count(f'id:"nelson.rule_{number}"') for number in range(1, 7)) == 6,
            "Nelson Rules 1-6 registered")
    require("switch(state.activeProc)" not in html,
            "no monolithic active-procedure switch")
    require("procedure_version" in html, "Result IR records procedure version")
    require("function validateProcedure(proc)" in html,
            "generic procedure validator present")
    require("function runSelfTests()" in html, "statistical self-test present")
    require("function studentizedRangeCriticalApprox" in html,
            "post-hoc simultaneous CI critical value present")

    for guardrail in (
        "Do not calculate statistics.",
        "Do not invent specifications.",
        "Do not infer causality.",
        "Return only schema-compliant JSON.",
    ):
        require(guardrail in html, f"LLM guardrail: {guardrail}")

    require("Vue.createApp" not in html and "ReactDOM" not in html,
            "no React or Vue runtime")
    require("fetch(" not in html and "WebSocket(" not in html,
            "no backend transport")

    print("RELEASE VERIFICATION PASS")


if __name__ == "__main__":
    main()
