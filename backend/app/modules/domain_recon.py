import dns.resolver

def domain_recon(domain):
    results = {"domain": domain}
    try:
        mx = dns.resolver.resolve(domain, 'MX')
        results['mx_records'] = [str(r.exchange) for r in mx]
    except Exception as e:
        results['mx_records'] = f"Error: {e}"
    return results
