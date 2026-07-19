import asyncio
import json
import sys
from typing import Dict

async def run_holehe_async(email: str) -> Dict:
    try:
        proc = await asyncio.create_subprocess_exec(
            sys.executable, "-m", "holehe",
            "--json", "--only-used", email,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        stdout = stdout.decode("utf-8")
        if proc.returncode != 0:
            return {"error": f"Holehe failed: {stderr or stdout}"}
        data = json.loads(stdout)
        results = {}
        for site, info in data.items():
            results[site] = {
                "registered": info.get("registered", False),
                "profile_url": info.get("profile_url") or None,
                "error": info.get("error", None)
            }
        return results
    except Exception as e:
        return {"error": f"Failed: {str(e)}"}

def run_holehe_sync(email: str) -> Dict:
    return asyncio.run(run_holehe_async(email))
