import requests

def check_xposed(email):
    url = f"https://api.xposedornot.com/v1/breaches/{email}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "breaches": data.get("breaches", []),
                "breach_count": len(data.get("breaches", []))
            }
        elif resp.status_code == 404:
            return {"breaches": [], "breach_count": 0}
        else:
            return {"error": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"error": str(e)}
