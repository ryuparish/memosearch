from flask import Flask, render_template, request
import numpy as np
import os
import json

# Using the gui folder as the template folder (where we get the templates for the Flask application)
app = Flask(__name__, template_folder=os.path.abspath("../gui/"))


@app.route("/detect", methods=["GET", "POST"])
def detect():
    if request.method == "GET":
        return render_template("object.html")

    if request.method == "POST":
        path = request.form["path"]
        return render_template("object.html")


app.run()
