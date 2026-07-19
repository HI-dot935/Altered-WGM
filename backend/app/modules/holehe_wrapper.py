import asyncio
import pkgutil
import importlib
import inspect

# ----- Auto‑locate check_email anywhere in the holehe package -----
def find_check_email():
    """Search all holehe submodules for a function named 'check_email'."""
    try:
        import holehe
    except ImportError:
        raise ImportError("holehe is not installed.")
    
    # First, try common direct imports
    for attempt in [
        ("holehe", "check_email"),
        ("holehe.core", "check_email"),
        ("holehe.modules", "check_email"),
        ("holehe.holehe", "check_email"),
    ]:
        try:
            mod = importlib.import_module(attempt[0])
            if hasattr(mod, attempt[1]):
                return getattr(mod, attempt[1])
        except ImportError:
            continue
    
    # If not found, recursively scan all submodules
    for importer, modname, ispkg in pkgutil.walk_packages(
        path=holehe.__path__,
        prefix=holehe.__name__ + ".",
        onerror=lambda x: None
    ):
        try:
            mod = importlib.import_module(modname)
            for name, obj in inspect.getmembers(mod):
                if name == "check_email" and inspect.iscoroutinefunction(obj):
                    return obj
        except ImportError:
            continue
    
    raise ImportError(
        "Cannot find 'check_email' in holehe. "
        "Please run: python3 -c 'import holehe; print(holehe.__path__)' "
        "and share the output with me."
    )

check_email = find_check_email()

# ----- Wrapper functions (unchanged) -----
async def run_holehe_async(email):
    try:
        data = await check_email(email)
        results = {}
        for site, info in data.items():
            if info.get("rateLimit", False):
                continue
            registered = info.get("registered", False)
            other = info.get("other", {})
            profile_url = None
            if "profile" in other:
                profile_url = other["profile"]
            elif "url" in other:
                profile_url = other["url"]
            elif "link" in other:
                profile_url = other["link"]
            if registered and not profile_url:
                for v in other.values():
                    if isinstance(v, str) and (v.startswith("http://") or v.startswith("https://")):
                        profile_url = v
                        break
            results[site] = {
                "registered": registered,
                "profile_url": profile_url,
                "error": info.get("error", None)
            }
        return results
    except Exception as e:
        return {"error": f"Holehe failed: {str(e)}"}

def run_holehe_sync(email):
    return asyncio.run(run_holehe_async(email))
