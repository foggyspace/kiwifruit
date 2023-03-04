from flask import render_template, request

from . import vuln_bp


@vuln_bp.route("/home")
def home():
    return render_template("home/home.html")
