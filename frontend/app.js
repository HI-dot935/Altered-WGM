// DOM refs
const inputs = {
    email: document.getElementById('emailInput'),
    phone: document.getElementById('phoneInput'),
    holehe: document.getElementById('holeheInput'),
    xposed: document.getElementById('xposedInput'),
    username: document.getElementById('usernameInput'),
    domain: document.getElementById('domainInput')
};
const btns = {
    email: document.getElementById('emailBtn'),
    phone: document.getElementById('phoneBtn'),
    holehe: document.getElementById('holeheBtn'),
    xposed: document.getElementById('xposedBtn'),
    username: document.getElementById('usernameBtn'),
    domain: document.getElementById('domainBtn')
};
const results = {
    email: document.getElementById('emailResult'),
    phone: document.getElementById('phoneResult'),
    holehe: document.getElementById('holeheResult'),
    xposed: document.getElementById('xposedResult'),
    username: document.getElementById('usernameResult'),
    domain: document.getElementById('domainResult')
};

const findingsList = document.getElementById('findingsList');
const statusMsg = document.getElementById('statusMsg');

// Helper: format result as key:value
function formatResult(data) {
    if (typeof data === 'string') return data;
    let html = '';
    for (const [k, v] of Object.entries(data)) {
        let val = v;
        if (Array.isArray(v)) val = v.join(', ');
        else if (typeof v === 'object' && v !== null) val = JSON.stringify(v);
        html += `<span style="color:#ff00c8;">${k}</span>: <span style="color:#00ffc8;">${val}</span><br>`;
    }
    return html;
}

// Helper: format Holehe with links
function formatHoleheResult(data) {
    if (data.error) return `❌ ${data.error}`;
    let html = `<span style="color:#ffaa00;">📊 ${data.total_checked} sites checked, ${data.registered_count} registered</span><br><br>`;
    const sites = data.sites || {};
    let count = 0;
    for (const [site, info] of Object.entries(sites)) {
        if (count++ >= 20) { html += `<span style="color:#666;">... and more</span>`; break; }
        const status = info.registered ? '✅' : '❌';
        const color = info.registered ? '#00ffc8' : '#666';
        let link = '';
        if (info.registered) {
            const url = info.profile_url || `https://${site}.com`;
            link = ` <a href="${url}" target="_blank">🔗</a>`;
        }
        html += `<span style="color:#ffaa00;">${site}</span>: <span style="color:${color};">${status} ${info.registered ? 'REGISTERED' : 'not found'}</span>${link}<br>`;
    }
    return html;
}

// Helper: format Username results
function formatUsernameResult(data) {
    if (data.error) return `❌ ${data.error}`;
    let html = `<span style="color:#ffaa00;">👤 ${data.username} – found on ${data.found_count} out of ${data.total_checked} sites</span><br><br>`;
    const sites = data.found_sites || [];
    if (sites.length === 0) {
        html += `<span style="color:#666;">No profiles found.</span>`;
        return html;
    }
    sites.slice(0, 30).forEach(s => {
        html += `<span style="color:#00ffc8;">✅ ${s.site}</span> → <a href="${s.url}" target="_blank" style="color:#ff00c8;">${s.url}</a><br>`;
    });
    if (sites.length > 30) {
        html += `<span style="color:#666;">... and ${sites.length - 30} more</span>`;
    }
    return html;
}

function showStatus(msg, type='success') {
    statusMsg.innerHTML = `<div class="status-msg ${type}">${msg}</div>`;
    setTimeout(() => { statusMsg.innerHTML = ''; }, 5000);
}

async function lookup(type) {
    const input = inputs[type];
    const resultDiv = results[type];
    const btn = btns[type];
    const query = input.value.trim();
    if (!query) { resultDiv.innerHTML = '⚠️ Please enter a value.'; return; }
    btn.disabled = true;
    resultDiv.innerHTML = '⏳ scanning...';
    const endpoints = {
        email: '/api/email',
        phone: '/api/phone',
        holehe: '/api/holehe',
        xposed: '/api/xposed',
        username: '/api/username',
        domain: '/api/domain'
    };
    const payloads = {
        email: { email: query },
        phone: { phone: query, region: 'US' },
        holehe: { email: query },
        xposed: { email: query },
        username: { username: query },
        domain: { domain: query }
    };
    try {
        const res = await fetch(endpoints[type], {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payloads[type])
        });
        const data = await res.json();
        if (res.ok) {
            if (type === 'holehe') {
                resultDiv.innerHTML = formatHoleheResult(data);
            } else if (type === 'username') {
                resultDiv.innerHTML = formatUsernameResult(data);
            } else {
                resultDiv.innerHTML = formatResult(data);
            }
            await loadFindings();
            showStatus(`✅ ${type} scan done!`);
        } else {
            resultDiv.innerHTML = `❌ Error: ${data.error || 'Unknown'}`;
            showStatus(`❌ Scan failed`, 'error');
        }
    } catch (e) {
        resultDiv.innerHTML = `💥 Network error: ${e.message}`;
        showStatus(`💥 ${e.message}`, 'error');
    }
    btn.disabled = false;
}

async function loadFindings() {
    const res = await fetch('/api/case');
    const data = await res.json();
    if (!data.findings || data.findings.length === 0) {
        findingsList.innerHTML = '<p class="empty">✨ Nothing yet – run a scan!</p>';
        return;
    }
    let html = '';
    data.findings.slice().reverse().forEach(f => {
        let summary = '';
        if (f.result && typeof f.result === 'object') {
            if (f.result.valid !== undefined) summary = f.result.valid ? '✅ Valid' : '❌ Invalid';
            else if (f.result.registered_count !== undefined) summary = `✅ ${f.result.registered_count}/${f.result.total_checked} sites`;
            else if (f.result.breach_count !== undefined) summary = `🔐 ${f.result.breach_count} breaches`;
            else if (f.result.found_count !== undefined) summary = `👤 ${f.result.found_count}/${f.result.total_checked} sites`;
            else if (f.result.error) summary = '⚠️ ' + f.result.error;
            else summary = Object.keys(f.result).join(', ');
        } else {
            summary = String(f.result).slice(0, 60);
        }
        html += `
            <div class="finding-item">
                <span class="query">${f.query}</span>
                <span class="type">${f.type}</span>
                <span class="time">${f.timestamp.slice(0,19)}</span>
                <div class="summary">${summary}</div>
            </div>
        `;
    });
    findingsList.innerHTML = html;
}

async function clearFindings() {
    if (!confirm('🧹 Clear all findings?')) return;
    await fetch('/api/case/clear', { method: 'POST' });
    await loadFindings();
    showStatus('🗑️ All cleared.');
}

function exportReport() {
    window.location.href = '/api/case/export';
    showStatus('📥 Report download started.');
}

// Bind buttons
Object.keys(btns).forEach(key => {
    btns[key].addEventListener('click', () => lookup(key));
    inputs[key].addEventListener('keypress', e => { if (e.key === 'Enter') lookup(key); });
});

document.getElementById('clearBtn').addEventListener('click', clearFindings);
document.getElementById('exportBtn').addEventListener('click', exportReport);

// Initial load
loadFindings();
