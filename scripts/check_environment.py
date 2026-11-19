"""Report local tool availability. Installs nothing."""
from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys

REQUIRED_TOOLS: dict[str, list[str]] = {
    "Git": ["git", "--version"],
    "FFmpeg": ["ffmpeg", "-version"],
    "FFprobe": ["ffprobe", "-version"],
}
OPTIONAL_TOOLS: dict[str, list[str]] = {
    "Claude Code CLI": ["claude", "--version"],
    "Node": ["node", "--version"],
    "GitHub CLI": ["gh", "--version"],
    "Playwright CLI": ["playwright-cli", "--version"],
}
PYTHON_PACKAGES: dict[str, str] = {"pytest": "pytest", "Pillow": "PIL", "python-dotenv": "dotenv"}
MIN_PYTHON = (3, 11)


def first_line(command: list[str]) -> str:
    exe = shutil.which(command[0])
    if exe is None:
        return ""
    try:
        p = subprocess.run([exe, *command[1:]], capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"error: {exc}"
    lines = (p.stdout or p.stderr).strip().splitlines()
    return lines[0][:160] if lines else "(no output)"


def main() -> int:
    failed: list[str] = []
    py_ok = sys.version_info >= MIN_PYTHON
    print(f"[{'OK' if py_ok else 'FAIL'}] Python: {sys.version.split()[0]} ({sys.executable})")
    if not py_ok:
        failed.append("Python>=3.11")
    for group, tools, required in (("required", REQUIRED_TOOLS, True), ("optional", OPTIONAL_TOOLS, False)):
        for name, cmd in tools.items():
            line = first_line(cmd)
            if line:
                print(f"[OK] {name}: {line}")
            else:
                print(f"[{'MISSING' if required else 'OPTIONAL-MISSING'}] {name}: '{cmd[0]}' not on PATH")
                if required:
                    failed.append(name)
    for dist, module in PYTHON_PACKAGES.items():
        if importlib.util.find_spec(module) is None:
            print(f"[MISSING] Python package {dist} (pip install -r requirements.txt)")
            failed.append(dist)
        else:
            print(f"[OK] Python package {dist}")
    if failed:
        print("Missing required: " + ", ".join(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
