from typing import Optional
import os
import platform
import subprocess
import sys
import shlex
from rich import print as rprint
from rich.markup import escape


def find_rye() -> Optional[str]:
    """Finds an executable `rye` on the PATH."""
    rye_name = "rye.exe" if platform.system() == "Windows" else "rye"
    path = os.environ.get("PATH", "").split(os.pathsep)
    for dir in path:
        rye_path = os.path.join(dir, rye_name)
        if os.path.isfile(rye_path) and os.access(rye_path, os.X_OK):
            return rye_path

    return None


def main(argv: list[str] = sys.argv[1:]) -> int:
    rye_path = find_rye()
    if not rye_path:
        rprint("[red]error[/red]: rye executable not found in PATH", file=sys.stderr)
        sys.exit(1)

    try:
        command = [rye_path, *argv]
        rprint(f"debug: running `{escape(shlex.join(command))}`")
        subprocess.run(command, check=True)
        return 0
    except subprocess.CalledProcessError as e:
        rprint(
            f"[red]error[/red]: `rye test` failed with exit code {e.returncode}",
            file=sys.stderr,
        )
        return e.returncode
