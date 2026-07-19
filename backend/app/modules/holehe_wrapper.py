import asyncio
from holehe import check_email

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
