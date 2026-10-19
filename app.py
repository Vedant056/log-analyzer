from flask import Flask, render_template_string
from Log_Analyzer import analyze_logs

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Security Log Analyzer</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            background: #f4f6f8;
            color: #202a35;
        }
        h1 { color: #173b65; }
        .card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin: 16px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th { background: #173b65; color: white; }
    </style>
</head>
<body>
    <h1>Security Log Analyzer 1</h1>
    <p>SSH authentication log analysis dashboard</p>

    <div class="card">
        <h2>Summary</h2>
        <p>Generated: {{ report.generated }}</p>
        <p>Total IPs analyzed: {{ report.total_ips }}</p>
        <p>Suspicious IPs: {{ report.suspicious_ips }}</p>
    </div>

    <div class="card">
        <h2>Failed Login Attempts</h2>
        <table>
            <tr><th>IP Address</th><th>Attempts</th><th>Status</th></tr>
            {% for item in report.results %}
            <tr>
                <td>{{ item.ip }}</td>
                <td>{{ item.attempts }}</td>
                <td>{{ item.status }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""


@app.route("/")
def home():
    report = analyze_logs("sample_auth.log")

    if "error" in report:
        return report["error"], 500

    return render_template_string(HTML, report=report)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
