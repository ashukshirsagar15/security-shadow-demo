
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Shadow | Network Monitor</title>

    <style>
        :root {
            --bg: #0b1120;
            --panel: #111b2e;
            --border: #24334a;
            --text: #e5edf8;
            --muted: #8da2bd;
            --green: #4ade80;
            --yellow: #facc15;
            --red: #f87171;
            --blue: #60a5fa;
        }

        * { box-sizing: border-box; }

        body {
            margin: 0;
            background: var(--bg);
            color: var(--text);
            font-family: Arial, sans-serif;
        }

        header {
            padding: 24px 5%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            border-bottom: 1px solid var(--border);
        }

        h1 { margin: 0; font-size: 24px; letter-spacing: 1px; }
        h1 span { color: var(--green); }
        .subtitle { color: var(--muted); margin-top: 8px; font-size: 13px; }

        .status {
            color: var(--green);
            font-size: 13px;
            white-space: nowrap;
        }

        main { padding: 28px 5%; }

        .section-title {
            font-size: 17px;
            margin: 0 0 18px;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 16px;
            margin-bottom: 30px;
        }

        .card, .panel {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 12px;
        }

        .card { padding: 20px; }
        .card-label { color: var(--muted); font-size: 13px; }
        .card-value { font-size: 30px; font-weight: bold; margin-top: 12px; }
        .card-note { color: var(--muted); font-size: 12px; margin-top: 8px; }

        .panel { overflow: hidden; margin-bottom: 24px; }
        .panel-header {
            padding: 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            gap: 12px;
            flex-wrap: wrap;
        }

        .panel-header h2 { margin: 0; font-size: 16px; }
        .panel-header p { color: var(--muted); font-size: 12px; margin: 6px 0 0; }

        .table-wrap { overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; text-align: left; }
        th, td {
            padding: 15px 20px;
            border-bottom: 1px solid var(--border);
            font-size: 13px;
            white-space: nowrap;
        }
        th { color: var(--muted); font-weight: normal; }
        tbody tr:last-child td { border-bottom: none; }
        .empty { text-align: center; color: var(--muted); padding: 36px 20px; }

        .badge {
            display: inline-block;
            padding: 5px 9px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: bold;
        }
        .low { color: var(--green); background: #123526; }
        .medium { color: var(--yellow); background: #3b3212; }
        .high, .critical { color: var(--red); background: #401d27; }

        footer {
            padding: 10px 5% 28px;
            color: var(--muted);
            font-size: 12px;
        }

        @media (max-width: 900px) {
            .cards { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        }
        @media (max-width: 520px) {
            header { align-items: flex-start; flex-direction: column; }
            .cards { grid-template-columns: 1fr 1fr; gap: 10px; }
            .card { padding: 14px; }
            .card-value { font-size: 24px; }
            main { padding-top: 20px; }
        }
    </style>
</head>

<body>
    <header>
        <div>
            <h1>SECURITY <span>SHADOW</span></h1>
            <div class="subtitle">PUBLIC SECURITY DEMO · SIMULATED DATA</div>
        </div>
        <div class="status">● DASHBOARD ONLINE</div>
    </header>

    <main>
        <h2 class="section-title">Overview</h2>

        <section class="cards">
            <article class="card">
                <div class="card-label">Active Connections</div>
                <div class="card-value" id="active">—</div>
                <div class="card-note">3 illustrative connections</div>
            </article>

            <article class="card">
                <div class="card-label">Processes with Connections</div>
                <div class="card-value" id="processes">—</div>
                <div class="card-note">Unique processes observed</div>
           </article>
            <article class="card">
                <div class="card-label">High-Risk Connections</div>
                <div class="card-value" id="high">—</div>
                <div class="card-note">HIGH or CRITICAL</div>
            </article>

            <article class="card">
                <div class="card-label">Monitoring Status</div>
                <div class="card-value" style="font-size: 20px; color: var(--blue);">READY</div>
                <div class="card-note">Demo mode active</div>
            </article>
        </section>

        <section class="panel">
            <div class="panel-header">
                <div>
                    <h2>Network Connections</h2>
                    <p>Process and remote endpoint information</p>
                </div>
                <span class="badge low">SIMULATED DEMO DATA</span>
            </div>
            <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap; padding:16px 20px;">
                   <label for="riskFilter" style="font-weight:600;">Filter by risk:</label>
                   <select id="riskFilter" style="padding:10px 14px; border-radius:8px; background:#111c30; color:#ffffff; border:1px solid #263650;">
                     <option value="ALL">All Levels</option>
                     <option value="LOW">Low Risk</option>
                     <option value="MEDIUM">Medium Risk</option>
                     <option value="HIGH">High Risk</option>
                     <option value="CRITICAL">Critical Risk</option>
                   </select>
                   <span id="filterCount" style="color:#8eafd9;">Showing all connections</span>
            </div>

            <div class="table-wrap">
                <table>
                    <thead>
                        <tr>
                            <th>PROCESS</th>
                            <th>PID</th>
                            <th>REMOTE ADDRESS</th>
                            <th>PORT</th>
                            <th>RISK</th>
                            <th>LEVEL</th>
                        </tr>
                    </thead>
                    <tbody id="connections">
                        <tr>
                            <td colspan="6" class="empty">
                                Dashboard interface ready. Waiting for backend integration.
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>

        <section class="panel">
            <div class="panel-header">
                <div>
                    <h2>Recent Alerts</h2>
                    <p>Connections requiring further investigation</p>
                </div>
            </div>
            <div id="alerts" class="empty">No live alert data received yet.</div>
        </section>
        
            </div>
        </section>

        <!-- Connection Details Panel -->
        <div id="connectionDetails" class="panel"
             style="display:none; margin-top:16px;">
            <div class="panel-header">
                <h2>Connection Details</h2>
                <button id="closeDetails" type="button">Close</button>
            </div>
           <div id="detailsContent" style="padding:16px 20px; white-space:pre-line;"></div>
        </div>

        <section class="panel">
            <div class="panel-header">
                <div>
                    <h2>Recent Alerts</h2>
    </main>

    <footer>
        Security Shadow · Public demonstration · All displayed security data is simulated

<script>
    function safeText(value) {
        return String(value ?? "").replace(/[&<>"']/g, char => ({
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;"
        })[char]);
    }

    async function updateDashboard() {
        try {
            const response = await fetch("/api/connections");

            if (!response.ok) {
                throw new Error("API error: " + response.status);
            }

            const data = await response.json();
            const connections = data.connections || [];
            const selectedRisk = document.getElementById("riskFilter")?.value || "ALL";

            const processes = new Set(
                connections.map(c => `${c.process}:${c.pid}`)
            );

            const highRisk = connections.filter(c =>
                ["HIGH", "CRITICAL"].includes(c.risk_level)
            );

            document.getElementById("active").textContent = connections.length;
            document.getElementById("processes").textContent = processes.size;
            document.getElementById("high").textContent = highRisk.length;

           
           const filteredConnections = selectedRisk === "ALL"
            ? connections
            : connections.filter(c => c.risk_level === selectedRisk);

           document.getElementById("filterCount").textContent =
              `Showing ${filteredConnections.length} of ${connections.length} connections`;

           document.getElementById("connections").innerHTML =
              filteredConnections.length
                 ? filteredConnections.map(c => {
                      const level = String(c.risk_level || "LOW").toLowerCase();
                     return `<tr class="connection-row"
                     style="cursor:pointer;"
                     data-process="${safeText(c.process)}"
                     data-pid="${safeText(c.pid)}">
                      <td>${safeText(c.process)}</td>
                      <td>${safeText(c.pid)}</td>
                      <td>${safeText(c.remote_ip)}</td>
                      <td>${safeText(c.remote_port)}</td>
                      <td>${safeText(c.risk_score)}/100</td>
                      <td><span class="badge ${safeText(level)}">
                          ${safeText(c.risk_level)}
                      </span></td>
                    </tr>`;
                 }).join("")
                 : `<tr><td colspan="6" class="empty">
                   No connections match this risk level.
                  </td></tr>`;
                  
           document.querySelectorAll(".connection-row").forEach(row => {
             row.addEventListener("click", () => {
                  const processName = row.dataset.process;
                  const pid = row.dataset.pid;
                  const connection = connections.find(c =>
                      c.process === processName && String(c.pid) === pid
                  );

                  if (!connection) return;

                  document.getElementById("detailsContent").textContent =
                     `Process: ${connection.process}\n` +
                     `PID: ${connection.pid}\n` +
                     `Remote address: ${connection.remote_ip}:${connection.remote_port}\n` +
                     `Risk score: ${connection.risk_score}/100\n` +
                     `Risk level: ${connection.risk_level}\n` +
                     `Reasons: ${(connection.reasons || []).join("; ")}`;

                  document.getElementById("connectionDetails").style.display = "block";
             });
           });

            const alerts = document.getElementById("alerts");

            if (highRisk.length === 0) {
                alerts.className = "empty";
                alerts.textContent =
                    "No HIGH or CRITICAL connections in the current snapshot.";
            } else {
                alerts.className = "";
                alerts.innerHTML = highRisk.map(c => `
                    <div style="padding:14px 20px; border-bottom:1px solid var(--border)">
                        <strong>${safeText(c.process)}</strong>
                        — ${safeText(c.remote_ip)}:${safeText(c.remote_port)}
                        <span class="badge ${safeText(String(c.risk_level).toLowerCase())}">
                            ${safeText(c.risk_level)}
                        </span>
                        <div style="color:var(--muted); margin-top:6px; font-size:12px">
                            Score: ${safeText(c.risk_score)}/100 ·
                            ${safeText((c.reasons || []).join("; "))}
                        </div>
                    </div>
                `).join("");
            }

            document.querySelector(".panel-header .badge").textContent =
                "SIMULATED DATA CONNECTED";

            document.querySelector(".status").textContent =
                "● DATA CONNECTED";

        } catch (error) {
            console.error("Dashboard update failed:", error);
            document.querySelector(".status").textContent =
                "● DATA CONNECTION ERROR";
        }
    }
document.getElementById("closeDetails")?.addEventListener("click", () => {
    document.getElementById("connectionDetails").style.display = "none";
});
    updateDashboard();
    setInterval(updateDashboard, 5000);
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(DASHBOARD_HTML)


@app.route("/api/status")
def status():
    return jsonify({
        "project": "Security Shadow",
        "status": "running",
        "live_data_connected": False
    })


@app.route("/api/connections")
def api_connections():
    # Simulated data for the public demo only.
    # These entries do not represent real computers.
    demo_connections = [
        {
            "process": "chrome.exe",
            "pid": 1840,
            "remote_ip": "192.0.2.10",
            "remote_port": 443,
            "status": "ESTABLISHED",
            "risk_score": 0,
            "risk_level": "LOW",
            "reasons": ["No suspicious indicators detected"]
        },
        {
            "process": "unknown_app.exe",
            "pid": 2256,
            "remote_ip": "198.51.100.20",
            "remote_port": 4444,
            "status": "ESTABLISHED",
            "risk_score": 70,
            "risk_level": "HIGH",
            "reasons": [
                "Suspicious port indicator",
                "Unknown process combined with non-standard port"
            ]
        },
        {
            "process": "file_sync_demo.exe",
            "pid": 3100,
            "remote_ip": "203.0.113.15",
            "remote_port": 443,
            "status": "ESTABLISHED",
            "risk_score": 20,
            "risk_level": "MEDIUM",
            "reasons": [
                "Illustrative demo alert requiring investigation"
            ]
        }
    ]

    return jsonify({
        "mode": "public_demo",
        "count": len(demo_connections),
        "connections": demo_connections
    })


if __name__ == "__main__":
    import os

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False,
        use_reloader=False
    )
