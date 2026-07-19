import subprocess
import json
import sys

def run_holehe_sync(email: str) -> dict:
    """
    Run holehe CLI using the installed 'holehe' command (not python -m).
    Returns a dict with site -> registration info.
    """
    try:
        # Use 'holehe' directly (the console script) – it's in PATH inside venv
        cmd = ["holehe", "--json", "--only-used", email]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            return {"error": f"Holehe CLI failed: {result.stderr or result.stdout}"}

        data = json.loads(result.stdout)
        output = {}
        for site, info in data.items():
            output[site] = {
                "registered": info.get("registered", False),
                "profile_url": info.get("profile_url") or None,
                "error": info.get("error", None)
            }
        return output

    except subprocess.TimeoutExpired:
        return {"error": "Holehe scan timed out (30s)."}
    except json.JSONDecodeError:
        return {"error": f"Invalid JSON from holehe: {result.stdout[:200]}"}
    except FileNotFoundError:
        # Fallback: try using python -m as a last resort
        try:
            cmd = [sys.executable, "-m", "holehe", "--json", "--only-used", email]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode != 0:
                return {"error": f"Holehe (fallback) failed: {result.stderr or result.stdout}"}
            data = json.loads(result.stdout)
            output = {}
            for site, info in data.items():
                output[site] = {
                    "registered": info.get("registered", False),
                    "profile_url": info.get("profile_url") or None,
                    "error": info.get("error", None)
                }
            return output
        except Exception as e:
            return {"error": f"Both holehe commands failed: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
