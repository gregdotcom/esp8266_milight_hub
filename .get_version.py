import os
import platform
import sys
from pathlib import Path
from subprocess import check_output

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
version_file = Path(dir_path) / "VERSION"

# http://stackoverflow.com/questions/11210104/check-if-a-program-exists-from-a-python-script
def is_tool(name):
    cmd = "where" if platform.system() == "Windows" else "which"
    try:
        check_output([cmd, name])
        return True
    except:
        return False

version = None

if version_file.exists():
    file_version = version_file.read_text(encoding="utf-8").strip()
    if file_version:
        version = file_version.encode()

if version is None and is_tool("git"):
    try:
        version = check_output(["git", "describe", "--always"]).rstrip()
    except:
        try:
            version = check_output(["git", "rev-parse", "--short", "HEAD"]).rstrip()
        except:
            pass
        pass

if version is None:
    version = "UNKNOWN".encode()

sys.stdout.write("-DMILIGHT_HUB_VERSION=%s %s" % (version.decode('utf-8'), ' '.join(sys.argv[1:])))
