import platform
import subprocess
import sys


def main():
    rye_name = "rye.exe" if platform.system() == "Windows" else "rye"
    sys.exit(subprocess.call([rye_name, *sys.argv[1:]]))
