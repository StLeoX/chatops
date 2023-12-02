# Flask modules
from flask import Blueprint, render_template

core_bp = Blueprint("core", __name__, url_prefix="/")

