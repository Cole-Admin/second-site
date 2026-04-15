from flask import Flask, render_template, request

app = Flask(__name__)

def ucitaj_bazu():
    baza = []

    with open("utakmice.txt", "r", encoding="utf-8") as f:
        for line in f:
            t = line.strip().split(":")

            name = t[0]
            matches = int(t[1])
            goals = int(t[2])
            conceded = int(t[3])
            wins = int(t[4])
            draws = int(t[5])
            losses = int(t[6])

            points = wins * 3 + draws
            gd = goals - conceded

            baza.append({
                "name": name,
                "matches": matches,
                "goals": goals,
                "conceded": conceded,
                "wins": wins,
                "draws": draws,
                "losses": losses,
                "points": points,
                "gd": gd
            })

    baza.sort(key=lambda x: (x["points"], x["gd"], x["goals"]), reverse=True)

    return baza


@app.route("/", methods=["GET", "POST"])
def home():
    table = ucitaj_bazu()
    search_result = None
    query = ""

    if request.method == "POST":
        query = request.form.get("ime").lower()

        for team in table:
            if team["name"].lower() == query:
                search_result = team
                break

    return render_template(
        "index.html",
        table=table[:10],
        search=search_result,
        query=query
    )

"""
Deploy cancelled
==> Deploying...
==> Setting WEB_CONCURRENCY=1 by default, based on available CPUs in the instance
Menu
==> Running 'gunicorn app:app'
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 644-501-992
127.0.0.1 - - [15/Apr/2026 14:03:28] "HEAD / HTTP/1.1" 200 -
==> No open ports detected on 0.0.0.0, continuing to scan...
==> Docs on specifying a port: https://render.com/docs/web-services#port-binding
==> No open ports detected on 0.0.0.0, continuing to scan...
==> Docs on specifying a port: https://render.com/docs/web-services#port-binding
==> No open ports detected on 0.0.0.0, continuing to scan...
==> Docs on specifying a port: https://render.com/docs/web-services#port-binding
==> No open ports detected on 0.0.0.0, continuing to scan...
==> Docs on specifying a port: https://render.com/docs/web-services#port-binding
"""
import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
