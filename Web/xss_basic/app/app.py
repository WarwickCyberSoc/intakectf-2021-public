#!/usr/bin/env python3

from flask import Flask, render_template, request, send_from_directory
import os
import secrets

app = Flask(__name__)

flag = "WMG{YOiNk_My_C00kiEs_NoW!}"
auth_cookie = "6b2a3d6dda4d0b27bbb82b8503339441"

with open(os.path.join("templates", "story_template.html"), "r") as story_file:
    story_template = story_file.read()

if not os.path.exists("stories"):
    os.mkdir("stories")


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/story", methods=["POST"])
def create_story():
    story = request.form.get("story", "").strip()
    if story == "":
        return "Please enter some content!"

    story_id = secrets.token_hex(16)
    with open(f"stories/{story_id}.html", "w") as story_file:
        story_file.write(story_template.format(story))

    return render_template("created.html", story_link=f"/stories/{story_id}")


@app.route("/stories/<story_id>")
def view_story(story_id: str):
    story_path = os.path.join("stories", f"{story_id}.html")
    if os.path.exists(story_path):
        return send_from_directory("stories", f"{story_id}.html", as_attachment=False)
    else:
        return "This story does not exist! We may have already reviewed it!"


@app.route("/admin")
def admin_page():
    if request.cookies.get("auth", "") != auth_cookie:
        return "You are not authenticated!"

    return flag
