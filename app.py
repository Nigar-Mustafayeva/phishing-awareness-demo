"""
Flask landing page for GoPhish credential-harvest simulation.

IMPORTANT (for your report, and to keep this ethical/legal):
- Only run this against accounts/users your team/org has explicitly authorized.
- Never store real passwords in plaintext beyond what's needed to demonstrate
  the simulation; for a portfolio project, hash or just log a boolean
  "submitted credentials" event instead of the actual password if you can.
- GoPhish appends tracking params to the landing URL, e.g. ?rid=XXXXXX.
  Capture that "rid" so you can tie a submission back to a specific
  simulated recipient in your GoPhish campaign results.
"""

from flask import Flask, request, render_template, redirect
from datetime import datetime
import csv
import os

app = Flask(__name__)

LOG_FILE = "submissions.csv"


def log_submission(rid, email, password_submitted, ip):
    """Log that a submission happened. Stores whether a password was
    submitted, not the password itself -- adjust if your report needs
    the literal value for demonstration purposes in a controlled lab."""
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "rid", "email", "password_submitted", "ip"])
        writer.writerow([
            datetime.utcnow().isoformat(),
            rid,
            email,
            bool(password_submitted),
            ip,
        ])


@app.route("/", methods=["GET"])
def landing():
    # GoPhish appends ?rid=<recipient_id> to the URL it emails out.
    rid = request.args.get("rid", "unknown")
    return render_template("login.html", rid=rid)


@app.route("/submit", methods=["POST"])
def submit():
    rid = request.form.get("rid", "unknown")
    email = request.form.get("email", "")
    password = request.form.get("password", "")

    log_submission(rid, email, bool(password), request.remote_addr)

    # Redirect to GoPhish's landing page tracking endpoint or your own
    # "you have been phished" training page. For GoPhish integration,
    # you'd typically let GoPhish's own hosted page record the submit
    # event; if hosting your own page, redirect to an educational page.
    return redirect("/trained")


@app.route("/trained")
def trained():
    return render_template("trained.html")


if __name__ == "__main__":
    # For local/lab testing only. Put behind gunicorn + nginx for real use.
    app.run(host="0.0.0.0", port=8080, debug=False)
