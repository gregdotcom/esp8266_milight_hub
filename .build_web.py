import os
import platform
import subprocess
from pathlib import Path

Import("env")

def is_tool(name):
    cmd = "where" if platform.system() == "Windows" else "which"
    try:
        subprocess.check_output([cmd, name])
        return True
    except Exception:
        return False

def run_command(command, cwd):
    completed = subprocess.run(
        command,
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True
    )

    if completed.stdout:
        print(completed.stdout)
    if completed.stderr:
        print(completed.stderr)

def build_web():
    if os.getenv("ESPMH_SKIP_WEB_BUILD") == "1":
        print("Skipping web build because ESPMH_SKIP_WEB_BUILD=1")
        return

    if not is_tool("npm"):
        print("WARNING: npm was not found. Using pre-built page.")
        return

    web_dir = Path("web2")
    npm_cmd = "npm.cmd" if platform.system() == "Windows" else "npm"
    install_cmd = [npm_cmd, "ci"] if (web_dir / "package-lock.json").exists() else [npm_cmd, "install"]

    print("Attempting to build webpage...")

    try:
        if not (web_dir / "node_modules").exists():
            run_command(install_cmd, web_dir)
        run_command([npm_cmd, "run", "build"], web_dir)
    except OSError as e:
        print("Encountered error OSError building webpage:", e)
        if e.filename:
            print("Filename is", e.filename)
        print("WARNING: Failed to build web package. Using pre-built page.")
    except subprocess.CalledProcessError as e:
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        print("Encountered error CalledProcessError building webpage:", e)
        print("WARNING: Failed to build web package. Using pre-built page.")
    except Exception as e:
        print("Encountered error", type(e).__name__, "building webpage:", e)
        print("WARNING: Failed to build web package. Using pre-built page.")

build_web()
