from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timezone
import json
import os

app = Flask(__name__)

# Where the real login should send people afterwards.
# Point this at whatever real inbox your targets actually use now
# (e.g. https://mail.google.com or https://outlook.office.com),
# since mail01.corp.local is no longer part of this project.
REAL_LOGIN_URL = os.environ.get("REAL_LOGIN_URL", "https://mail.google.com")

LOG_FILE = "events.log"


def log_event(event_type):
    """Append a JSON line with only the event type and timestamp.
    This function never reads request.form, so no submitted field
    (email, password, or anything else typed into the page) is ever
    accessed, logged, or stored anywhere. Safe for a public demo."""
    entry = {
        "event": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # DATA CAPTURE DISABLED: request.form is intentionally never
        # accessed here. Whatever was typed into the Email/Password
        # fields is discarded by the browser submit and never reaches
        # this app in any usable form. We only note that a demo
        # submission occurred, then move on to the awareness page.
        log_event("demo_form_submitted")
        return redirect(url_for("awareness"))
    log_event("page_viewed")
    return render_template("login.html")


@app.route("/awareness", methods=["GET"])
def awareness():
    return render_template("awareness.html", real_login_url=REAL_LOGIN_URL)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
