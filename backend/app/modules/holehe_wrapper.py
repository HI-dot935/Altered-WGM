import subprocess
import json
import sys

def run_holehe_sync(email: str) -> dict:
    """
    Run holehe CLI and parse JSON output.
    Uses synchronous subprocess with timeout to avoid hanging.
    """
    try:
        cmd = [sys.executable, "-m", "holehe", "--json", "--only-used", email]
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
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
