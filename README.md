# 🕵️ Altered‑WGM – Ultimate OSINT Workbench

**Altered‑WGM** is a **self‑hosted, all‑in‑one OSINT platform** that combines the best of:

- **RAWS** – modular dashboard, case management, report export
- **Epieos** – email & phone intelligence
- **Holehe** – 120+ site account existence checker (with clickable profile links)
- **XposedOrNot** – free, keyless breach detection (no API key required)
- **Username Search** – checks **150+ platforms** asynchronously
- **Domain Recon** – DNS MX records

It provides a **goofy dark cyberpunk Web UI** with a sidebar for easy navigation, plus a **command‑line interface** for automation. Everything runs **locally** – your data stays private.

---

## ✨ Features

| Tool | Description |
|------|-------------|
| 📧 **Email Intel** | Validate email format, retrieve MX records, optional HIBP breach check, extract username |
| 📱 **Phone Intel** | Validate international phone numbers, identify type (mobile/landline), show location, carrier, timezone |
| 🔍 **Deep Account Scan** | Check if an email is registered on **120+ sites** (using Holehe) – shows profile links when available |
| 🔐 **Breach Check** | Uses **XposedOrNot** (completely free, no API key) to show known data breaches |
| 👤 **Username Search** | Check **150+ platforms** asynchronously for a given username – returns clickable profile URLs |
| 🌐 **Domain Recon** | DNS MX record lookup (extensible to WHOIS, subdomains, etc.) |
| 📂 **Case Management** | All queries are logged with timestamps; review, clear, or export as Markdown |
| 📥 **Export Report** | Generate a **Markdown** report with all findings in one file |
| 🖥️ **Web UI** | Dark sidebar layout, real‑time results, live case logging, export button |
| ⌨️ **CLI** | Run scans from the terminal – ideal for automation and scripting |
| 🐳 **Docker** | Containerised deployment, no dependency conflicts |

---

## 📦 Installation

### Prerequisites
- **Python 3.9 or higher**
- **pip** (Python package manager)
- (Optional) **Docker** for containerised deployment

### 1. Clone or download the repository
```bash
git clone https://github.com/yourusername/Altered-WGM.git
cd Altered-WGM

2. Run the startup script (creates virtual environment, installs dependencies, starts the web UI)
Linux / macOS:

bash
chmod +x run.sh
./run.sh
Windows:

batch
run.bat
The script will:

Create a Python virtual environment (.venv/).

Install all required packages.

Start the Flask web server at http://127.0.0.1:8420.

3. (Optional) Install the CLI globally
bash
source venv/bin/activate   # or `venv\Scripts\activate` on Windows
pip install -e .
Now you can run altered-wgm from anywhere.

🧭 Web UI Usage
Open http://127.0.0.1:8420 in your browser.

Sidebar – click any tool name to scroll directly to its card.

Each tool has its own card with an input field and a Scan / Search button.

Results appear immediately in the card’s result box.

Every query is automatically added to the Case Findings panel at the bottom.

Use Export Report to download a .md file with all logged findings.

Use Clear All to reset the case (findings are stored in memory only, so they reset when the app restarts).

⌨️ CLI Commands
After installing the package (pip install -e .), you can run scans from your terminal.

Basic usage
bash
altered-wgm -e target@example.com
This runs Email Intel, Deep Account Scan (Holehe), and Breach Check (Xposed) for the given email.

Full command reference
Command	Description
altered-wgm -e EMAIL	Run email, Holehe, and Xposed scans
altered-wgm -p PHONE	Run phone intel (use international format, e.g. +14155552671)
altered-wgm -u USERNAME	Run username search across 150+ sites
altered-wgm -d DOMAIN	Run domain recon (MX records)
altered-wgm -e EMAIL -u USERNAME -p PHONE	Combine multiple scans in one command
altered-wgm -e EMAIL -j	Output results in JSON format (for scripting)
altered-wgm -e EMAIL --hibp-key YOUR_KEY	Use your HIBP API key for breach detection
altered-wgm -e EMAIL --region US	Specify region for phone number parsing (default: US)
Example output (CLI)
text
[*] Checking email: target@example.com
[*] Running Holehe (120+ sites)...
[*] Checking breaches via XposedOrNot...

📧 Email: target@example.com (valid: True)
   MX: ['mail.example.com.']
   Breach count: 0

🔍 Deep Account Scan: 3 registered out of 120 sites
   ✅ Twitter -> https://twitter.com/target
   ✅ GitHub -> https://github.com/target
   ✅ Instagram -> https://instagram.com/target

🔐 XposedOrNot: 0 breaches found
🐳 Docker Usage
Build the image
bash
docker build -t altered-wgm .
Run the container (Web UI only)
bash
docker run -p 8420:8420 altered-wgm
Open http://127.0.0.1:8420 in your browser.

(The CLI is not available inside the container by default, but you can enter the container with docker exec -it <container-id> /bin/bash and run altered-wgm if you install it there.)

⚙️ Configuration
All settings are in backend/app/config.py.

Variable	Description
HIBP_API_KEY	Optional; get a free key from Have I Been Pwned. Leave None to skip HIBP checks.
No other configuration is required – XposedOrNot works keyless, and Holehe runs via subprocess (so it uses whatever version you have installed).

🧪 Testing
Web UI – Enter test@example.com in the Email Intel card. You should see valid: True, MX records, and breach_count: 0.

Deep Account Scan – Enter test@example.com; after 5‑15 seconds, you’ll see 0 registered out of 120 sites.

Username Search – Enter johndoe; after 10‑20 seconds, you’ll see a list of platforms where that username appears (if any).

CLI – Run altered-wgm -e test@example.com – you should see similar output without errors.

🛠️ Troubleshooting
ImportError: cannot import name 'check_email' from 'holehe'
Cause: Newer versions of holehe changed their internal structure.

Solution: The tool now uses the Holehe CLI (subprocess) instead of direct import, so this error no longer occurs. Ensure holehe is installed (pip install holehe).

If you still see issues, run python3 -m holehe --version to verify the CLI works.

ModuleNotFoundError: No module named 'aiohttp'
Install it manually: pip install aiohttp

Port 8420 already in use
Change the port in backend/app/main.py (last line) or kill the process:

bash
lsof -i :8420   # macOS/Linux
netstat -ano | findstr :8420   # Windows
Slow scans
The Deep Account Scan and Username Search query many sites asynchronously – network speed and site rate‑limiting affect performance. Be patient; they usually finish within 15‑20 seconds.

SSL certificate errors (on some networks)
The username search disables SSL verification (ssl=False) to avoid issues. If you still get errors, try updating aiohttp: pip install --upgrade aiohttp

holehe CLI not found
Ensure holehe is installed in your virtual environment: pip install holehe

Test with python3 -m holehe --help

📁 Project Structure
text
Altered-WGM/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # Flask app with all routes
│   │   ├── cli.py           # CLI entry point
│   │   ├── config.py        # Settings (HIBP key, etc.)
│   │   ├── report_export.py # Markdown report generator
│   │   └── modules/
│   │       ├── __init__.py
│   │       ├── email_check.py      # Email validation, MX, HIBP
│   │       ├── phone_intel.py      # Phone number analysis
│   │       ├── holehe_wrapper.py   # Holehe CLI wrapper (subprocess)
│   │       ├── xposed_check.py     # Keyless breach check via XposedOrNot
│   │       ├── username_check.py   # 150+ site async scanner
│   │       └── domain_recon.py     # DNS MX records
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html           # Main UI (sidebar + cards)
│   ├── styles.css           # Cyberpunk dark theme
│   └── app.js               # Frontend logic (spinners, API calls, scrolling)
├── setup.py                 # pip install entry point
├── run.sh / run.bat         # startup scripts
└── README.md                # this file
🤝 Contributing
Contributions are welcome! Feel free to open issues or pull requests for:

Additional OSINT modules (e.g., WHOIS, subdomain enumeration, social media scraping).

Improved UI/UX.

Enhanced report formats (PDF, HTML).

Performance optimizations.

⚠️ Disclaimer
This tool is for ethical and educational purposes only.
Do not use it for any illegal, malicious, or unauthorised activities.
Always comply with the terms of service of the platforms you query, and respect the privacy of individuals.
The authors assume no liability for any misuse.

📄 License
MIT – free to use and modify, with attribution
