from typing import Optional
import os
import platform
import subprocess
import sys
import shlex
from rich import print as rprint
from rich.markup import escape


def find_rye(verbose: bool) -> Optional[str]:
    """Finds an executable `rye` on the PATH."""
    path = os.environ.get("PATH", "").split(os.pathsep)
    if verbose:
        rprint("verbose: read path as", path)

    rye_name = "rye.exe" if platform.system() == "Windows" else "rye"
    for dir_path in path:
        rye_path = os.path.join(dir_path, rye_name)
        if os.access(rye_path, os.X_OK):
            return rye_path

    return None


def main(argv: list[str] = sys.argv[1:]) -> int:
    verbose = os.environ.get("RYE_PRECOMMIT_VERBOSE", "") != ""

    rye_path = find_rye(verbose)
    if not rye_path:
        rprint("[red]error[/red]: rye executable not found in PATH", file=sys.stderr)
        sys.exit(1)

    command = [rye_path, *argv]
    escaped_command = escape(shlex.join(command))

    try:
        if verbose:
            rprint(f"verbose: running `{escaped_command}`")
        subprocess.run(command, check=True)
        return 0
    except subprocess.CalledProcessError as e:
        rprint(
            f"[red]error[/red]: `{escaped_command}` failed with exit code {e.returncode}",
            file=sys.stderr,
        )
        return e.returncode
