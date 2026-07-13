"""
Optional PythonAnywhere wrapper for the Lundy Loop pack.
ONLY needed if you choose Option B in DEPLOY_PYTHONANYWHERE.txt.
Option A (static file mapping) needs no code at all and is recommended.
"""
from flask import Flask, send_from_directory
import os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "LundyLoop")
app = Flask(__name__)

@app.route("/")
@app.route("/lundy/")
def index():
    return send_from_directory(BASE, "index.html")

@app.route("/lundy/<path:filename>")
def files(filename):
    return send_from_directory(BASE, filename)
