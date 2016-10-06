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

@app.route('/new_entry')
def add_entry_to_db():
    entry_body = request.form["entry"]
    # add the entry to the model
    entry_id = Entry(entry_body=entry_body, entry_date=entry_date, username=username, tag=tag)

   db.session.add(entry_id)
   db.session.commit()

if __name__ == "__main__":
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0', port=5000) #vagrant requires port to be 5000