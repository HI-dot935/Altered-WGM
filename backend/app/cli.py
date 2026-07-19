#!/usr/bin/env python3
import argparse
import asyncio
import sys
import json
from .modules.email_check import email_intel
from .modules.phone_intel import phone_intel
from .modules.holehe_wrapper import run_holehe_async
from .modules.xposed_check import check_xposed
from .modules.username_check import check_username_sync
from .config import HIBP_API_KEY

async def run_scan(email=None, phone=None, username=None, domain=None, hibp_key=None, region="US"):
    results = {}
    if email:
        print(f"[*] Checking email: {email}")
        results['email'] = email_intel(email, hibp_key)
        print("[*] Running Holehe (120+ sites)...")
        results['holehe'] = await run_holehe_async(email)
        print("[*] Checking breaches via XposedOrNot...")
        results['xposed'] = check_xposed(email)
    if phone:
        print(f"[*] Checking phone: {phone}")
        results['phone'] = phone_intel(phone, region)
    if username:
        print(f"[*] Searching username across 150+ sites...")
        results['username'] = check_username_sync(username)
    if domain:
        print(f"[*] Reconning domain: {domain}")
        results['domain'] = domain_recon(domain)
    return results

def main():
    parser = argparse.ArgumentParser(description="Altered-WGM OSINT scanner")
    parser.add_argument("-e", "--email", help="Email address")
    parser.add_argument("-p", "--phone", help="Phone number (+1234567890)")
    parser.add_argument("-u", "--username", help="Username")
    parser.add_argument("-d", "--domain", help="Domain name")
    parser.add_argument("--hibp-key", default=HIBP_API_KEY, help="HIBP API key (optional)")
    parser.add_argument("--region", default="US", help="Region for phone")
    parser.add_argument("-j", "--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    if not any([args.email, args.phone, args.username, args.domain]):
        print("Error: at least one of -e, -p, -u, -d required", file=sys.stderr)
        sys.exit(1)

    results = asyncio.run(run_scan(args.email, args.phone, args.username, args.domain,
                                   args.hibp_key, args.region))

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        # Pretty print
        if 'email' in results:
            e = results['email']
            print(f"\n📧 Email: {e.get('email')} (valid: {e.get('valid')})")
            if e.get('valid'):
                print(f"   MX: {e.get('mx_records')}")
                print(f"   Breach count: {e.get('breach_count')}")
        if 'holehe' in results:
            h = results['holehe']
            if isinstance(h, dict) and "error" in h:
                print(f"\n🔍 Holehe error: {h['error']}")
            else:
                reg = sum(1 for v in h.values() if v.get('registered'))
                print(f"\n🔍 Deep Account Scan: {reg} registered out of {len(h)} sites")
                for site, info in list(h.items())[:15]:
                    if info.get('registered'):
                        url = info.get('profile_url') or f"https://{site}.com"
                        print(f"   ✅ {site} -> {url}")
        if 'xposed' in results:
            x = results['xposed']
            print(f"\n🔐 XposedOrNot: {x.get('breach_count', 0)} breaches found")
        if 'phone' in results:
            p = results['phone']
            print(f"\n📱 Phone: {p.get('number')} (valid: {p.get('valid')})")
            if p.get('valid'):
                print(f"   Type: {p.get('type')}, Location: {p.get('location')}, Carrier: {p.get('carrier')}")
        if 'username' in results:
            u = results['username']
            print(f"\n👤 Username: {u.get('username')}")
            print(f"   Found on {u.get('found_count')} out of {u.get('total_checked')} sites")
            for site in u.get('found_sites', [])[:15]:
                print(f"   ✅ {site['site']} -> {site['url']}")
            if u.get('found_count', 0) > 15:
                print(f"   ... and {u.get('found_count')-15} more")
        if 'domain' in results:
            d = results['domain']
            print(f"\n🌐 Domain: {d.get('domain')}")
            print(f"   MX records: {d.get('mx_records')}")

if __name__ == "__main__":
    main()
