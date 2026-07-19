import re
import dns.resolver
import requests

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def get_mx_records(domain):
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return [str(r.exchange) for r in answers]
    except Exception as e:
        return f"Error: {e}"

def check_hibp(email, api_key=None):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {"hibp-api-key": api_key} if api_key else {}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            return [b.get('Name', 'Unknown') for b in resp.json()]
        elif resp.status_code == 404:
            return []
        else:
            return f"Error: {resp.status_code}"
    except Exception as e:
        return f"Error: {e}"

def email_intel(email, hibp_api_key=None):
    report = {'email': email, 'valid': validate_email(email)}
    if report['valid']:
        domain = email.split('@')[1]
        report['mx_records'] = get_mx_records(domain)
        breaches = check_hibp(email, hibp_api_key)
        report['breaches'] = breaches if isinstance(breaches, list) else breaches
        report['breach_count'] = len(breaches) if isinstance(breaches, list) else 0
        report['username'] = email.split('@')[0]
    else:
        report['error'] = 'Invalid email format'
    return report
