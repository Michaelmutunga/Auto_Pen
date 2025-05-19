import os
import json
from datetime import datetime
from jinja2 import Template
from weasyprint import HTML

RESULTS_FILE = 'results/scan_results.json'
EXPLOIT_LOG = 'logs/exploit_log.txt'
SUCCESSFUL_EXPLOITS = 'reports/successful_exploits.json'
POST_EXPLOIT_FILE = 'reports/post_exploitation_data.json'
REPORT_OUTPUT = f"reports/AutoPen_Report_{datetime.now().strftime('%Y-%m-%d')}.pdf"


def load_json(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"[!] Failed to load {filepath}: {e}")
        return []

def load_text(filepath):
    try:
        with open(filepath, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"[!] Failed to read {filepath}: {e}")
        return ""

def generate_html_report(scan_data, exploit_log, successes, post_data):
    template_str = '''
    <html>
    <head>
        <style>
            body { font-family: Arial; margin: 30px; }
            h1, h2 { color: #333366; }
            .section { margin-bottom: 40px; }
            .code { background-color: #f4f4f4; padding: 10px; font-family: monospace; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <h1>Auto-Pen Penetration Test Report</h1>
        <p><strong>Date:</strong> {{ date }}</p>

        <div class="section">
            <h2>1. Scan Results</h2>
            {% for host in scan_data %}
                <h3>Target: {{ host.ip }}</h3>
                <ul>
                    <li><strong>OS:</strong> {{ host.os }}</li>
                    <li><strong>Open Ports:</strong> {{ host.ports | join(', ') }}</li>
                </ul>
            {% endfor %}
        </div>

        <div class="section">
            <h2>2. Exploit Log</h2>
            <div class="code">{{ exploit_log }}</div>
        </div>

        <div class="section">
            <h2>3. Successful Exploits</h2>
            <ul>
            {% for item in successes %}
                <li>{{ item.ip }} - {{ item.exploit }} ({{ item.payload }})</li>
            {% endfor %}
            </ul>
        </div>

        <div class="section">
            <h2>4. Post-Exploitation Findings</h2>
            {% for session in post_data %}
                <h3>Session ID {{ session.session_id }} - {{ session.target }}</h3>
                <ul>
                    <li><strong>System Info:</strong> {{ session.sysinfo }}</li>
                    <li><strong>Users:</strong> {{ session.users }}</li>
                    <li><strong>Processes:</strong> {{ session.processes }}</li>
                    <li><strong>Files:</strong> {{ session.files }}</li>
                </ul>
            {% endfor %}
        </div>

        <div class="section">
            <h2>5. Recommendations</h2>
            <p>It is strongly advised to patch outdated software, close unused ports, and monitor any signs of intrusion. Prioritize CVEs identified in this test for remediation.</p>
        </div>
    </body>
    </html>
    '''
    template = Template(template_str)
    return template.render(
        date=datetime.now().strftime('%Y-%m-%d'),
        scan_data=scan_data,
        exploit_log=exploit_log,
        successes=successes,
        post_data=post_data
    )

def parse_scan_results():
    data = load_json(RESULTS_FILE)
    for entry in data:
        entry['ports'] = [p['port'] for p in entry.get('services', [])]
    return data

def generate_report():
    scan_data = parse_scan_results()
    exploit_log = load_text(EXPLOIT_LOG)
    successes = load_json(SUCCESSFUL_EXPLOITS)
    post_data = load_json(POST_EXPLOIT_FILE)

    html = generate_html_report(scan_data, exploit_log, successes, post_data)
    os.makedirs('reports', exist_ok=True)
    HTML(string=html).write_pdf(REPORT_OUTPUT)
    print(f"[+] Report generated: {REPORT_OUTPUT}")

if __name__ == '__main__':
    generate_report()

