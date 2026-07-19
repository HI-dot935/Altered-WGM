import asyncio
import json
import sys
from typing import Dict

async def run_holehe_async(email: str) -> Dict:
    """
    Run holehe CLI and return a dict with site -> registration status.
    """
    try:
        # Use `python3 -m holehe` to run the CLI, with JSON output
        proc = await asyncio.create_subprocess_exec(
            sys.executable, "-m", "holehe",
            "--json",          # get JSON output (available in 1.59+)
            "--only-used",     # only show registered sites
            email,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")

        if proc.returncode != 0:
            return {"error": f"Holehe CLI failed: {stderr or stdout}"}

        # Parse JSON output
        try:
            data = json.loads(stdout)
        except json.JSONDecodeError:
            # Fallback: try to parse text output
            return parse_holehe_text(stdout)

        # Transform to our expected format
        results = {}
        for site, info in data.items():
            results[site] = {
                "registered": info.get("registered", False),
                "profile_url": info.get("profile_url") or None,
                "error": info.get("error", None)
            }
        return results

    except Exception as e:
        return {"error": f"Failed to run holehe: {str(e)}"}


def parse_holehe_text(output: str) -> Dict:
    """
    Fallback parser for non‑JSON output (older holehe versions).
    """
    results = {}
    for line in output.strip().split("\n"):
        if ":" not in line:
            continue
        site, status = line.split(":", 1)
        site = site.strip()
        status = status.strip().lower()
        results[site] = {
            "registered": "registered" in status,
            "profile_url": None,
            "error": None
        }
    return results


def run_holehe_sync(email: str) -> Dict:
    """
    Synchronous wrapper for the async function.
    """
    return asyncio.run(run_holehe_async(email))
