from flask import Blueprint


vuln_bp = Blueprint("vuln_bp", __name__)

from . import blueprint

