import os 
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
import requests
from datetime import datetime
import model
import json
import pdb

app = Flask(__name__)

app.secret_key = "Shhhhh"

@app.route('/')
def homepage():
    """Display the homepage to the user"""

    render_template("homepage.html")

def login():
    """Login the user"""

def register():
    """Register the user"""

def view_entries_by_tag():
    """Create a function that sorts the entries by user's input tag"""

if __name__ == "__main__":
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0', port=5000) #vagrant requires port to be 5000