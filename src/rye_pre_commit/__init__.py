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
    for dir in path:
        rye_path = os.path.join(dir, rye_name)
        if os.path.isfile(rye_path) and os.access(rye_path, os.X_OK):
            return rye_path

    return None


def main(argv: list[str] = sys.argv[1:]) -> int:
    verbose = "--rye-precommit-verbose" in argv
    if verbose:
        argv = [i for i in argv if i != "--rye-precommit-verbose"]

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
