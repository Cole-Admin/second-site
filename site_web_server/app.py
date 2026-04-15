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


app.run(debug=True)