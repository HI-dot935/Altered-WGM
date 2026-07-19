from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from modules.email_check import email_intel
from modules.phone_intel import phone_intel
from modules.holehe_wrapper import run_holehe_sync
from modules.xposed_check import check_xposed
from modules.username_check import check_username_sync
from modules.domain_recon import domain_recon
from report_export import export_markdown
from config import HIBP_API_KEY
import io
from datetime import datetime

app = Flask(__name__, 
            template_folder='../../frontend',
            static_folder='../../frontend',
            static_url_path='')
CORS(app)

current_case = {'name': 'Altered-WGM Case', 'findings': []}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/email', methods=['POST'])
def email_lookup():
    data = request.get_json()
    email = data.get('email', '').strip()
    if not email:
        return jsonify({'error': 'Email required'}), 400
    try:
        result = email_intel(email, HIBP_API_KEY)
        current_case['findings'].append({
            'type': '📧 Email Intel',
            'query': email,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/phone', methods=['POST'])
def phone_lookup():
    data = request.get_json()
    phone = data.get('phone', '').strip()
    region = data.get('region', 'US')
    if not phone:
        return jsonify({'error': 'Phone required'}), 400
    try:
        result = phone_intel(phone, region)
        current_case['findings'].append({
            'type': '📱 Phone Intel',
            'query': phone,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/holehe', methods=['POST'])
def holehe_lookup():
    data = request.get_json()
    email = data.get('email', '').strip()
    if not email:
        return jsonify({'error': 'Email required'}), 400
    try:
        result = run_holehe_sync(email)
        if isinstance(result, dict) and 'error' in result:
            return jsonify(result), 500
        registered = sum(1 for v in result.values() if v.get('registered', False))
        summary = {
            'email': email,
            'total_checked': len(result),
            'registered_count': registered,
            'sites': result
        }
        current_case['findings'].append({
            'type': '🔍 Deep Account Scan (Holehe)',
            'query': email,
            'result': summary,
            'timestamp': datetime.now().isoformat()
        })
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/xposed', methods=['POST'])
def xposed_lookup():
    data = request.get_json()
    email = data.get('email', '').strip()
    if not email:
        return jsonify({'error': 'Email required'}), 400
    try:
        result = check_xposed(email)
        current_case['findings'].append({
            'type': '🔐 Breach Check (Xposed)',
            'query': email,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/username', methods=['POST'])
def username_lookup():
    data = request.get_json()
    username = data.get('username', '').strip()
    if not username:
        return jsonify({'error': 'Username required'}), 400
    try:
        result = check_username_sync(username)
        current_case['findings'].append({
            'type': '👤 Username Search (150+ sites)',
            'query': username,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/domain', methods=['POST'])
def domain_lookup():
    data = request.get_json()
    domain = data.get('domain', '').strip()
    if not domain:
        return jsonify({'error': 'Domain required'}), 400
    try:
        result = domain_recon(domain)
        current_case['findings'].append({
            'type': '🌐 Domain Recon',
            'query': domain,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/case', methods=['GET'])
def get_case():
    return jsonify(current_case)

@app.route('/api/case/clear', methods=['POST'])
def clear_case():
    current_case['findings'] = []
    return jsonify({'status': 'cleared'})

@app.route('/api/case/export', methods=['GET'])
def export_case():
    md = export_markdown(current_case)
    return send_file(
        io.BytesIO(md.encode('utf-8')),
        mimetype='text/markdown',
        as_attachment=True,
        download_name=f"altered_wgm_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8420, debug=True)
