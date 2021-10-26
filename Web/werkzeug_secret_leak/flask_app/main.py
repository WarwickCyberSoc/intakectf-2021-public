from flask import Flask, render_template, request, json, session
from werkzeug.utils import redirect

app = Flask(__name__)
app.config["SECRET_KEY"] = "x?Xq9k4@yQMGxCGt"

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        unformatted_json = request.form["json"]

        try:
            parsed_json = json.loads(unformatted_json)
        except Exception as e:
            return render_template(
                "index.html", format_error=str(e), formatted_json=unformatted_json
            )

        return render_template(
            "index.html",
            formatted_json=json.dumps(parsed_json, sort_keys=True, indent=4),
        )
    else:
        if session.get("isAdmin", None) is None:
            session["isAdmin"] = False

        return render_template("index.html")

@app.route("/admin")
def admin_route():
    if session.get("isAdmin", False):
        return "WMG{d0n7_run_y0ur_fl45k_4pp5_1n_d3bu6_m0d3_f0r_pr0duc710n!}"
    else:
        return redirect("/")
