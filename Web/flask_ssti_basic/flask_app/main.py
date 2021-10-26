from flask import Flask, request, render_template_string, render_template
import os

app = Flask(__name__)

with open(os.path.join("templates", "signed_up.html")) as file:
    signed_up_content = file.read()


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.post("/sign_up")
def signed_up():
    email = request.form.get("email", "N/A")
    return render_template_string(signed_up_content.format(email))
