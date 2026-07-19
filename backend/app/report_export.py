from datetime import datetime

def format_value(v):
    if isinstance(v, dict):
        return "\n".join(f"  - {k}: {format_value(v)}" for k, v in v.items())
    elif isinstance(v, list):
        return ", ".join(str(x) for x in v[:5]) + ("..." if len(v) > 5 else "")
    else:
        return str(v)

def export_markdown(case):
    md = f"# 🕵️ Altered-WGM Investigation Report\n"
    md += f"**Case:** {case['name']}\n"
    md += f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
    if not case['findings']:
        md += "No findings recorded yet.\n"
    else:
        for idx, f in enumerate(case['findings'], 1):
            md += f"## Finding #{idx}: {f['type']}\n"
            md += f"- **Query**: `{f['query']}`\n"
            md += f"- **Time**: {f['timestamp']}\n"
            md += "**Details**:\n"
            for k, v in f['result'].items():
                if k == 'sites' and isinstance(v, dict):
                    md += f"- **{k}**:\n"
                    for site, info in list(v.items())[:10]:
                        status = "✅ REGISTERED" if info.get('registered') else "❌ Not found"
                        profile = info.get('profile_url', '')
                        if profile:
                            md += f"  - {site}: {status} – {profile}\n"
                        else:
                            md += f"  - {site}: {status}\n"
                    if len(v) > 10:
                        md += f"  - ... and {len(v)-10} more sites\n"
                elif k == 'found_sites' and isinstance(v, list):
                    md += f"- **{k}**:\n"
                    for site in v[:10]:
                        md += f"  - {site['site']}: {site['url']}\n"
                    if len(v) > 10:
                        md += f"  - ... and {len(v)-10} more\n"
                else:
                    md += f"- **{k}**: {format_value(v)}\n"
            md += "\n"
    return md
