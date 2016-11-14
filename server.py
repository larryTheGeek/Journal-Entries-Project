import os 
from flask import Flask, render_template, request, flash, redirect, session, abort
from flask_debugtoolbar import DebugToolbarExtension
import requests
from datetime import datetime
from model import User, Entry, Tag, EntryTag
import json
import pdb
from flask_login import login_required, current_user
# from flask_bcrypt import bcrypt

app = Flask(__name__)

app.secret_key = "Shhhhh"

@app.route('/')
def homepage():
    """Display the homepage to the user"""

    try:
        r = requests.get("http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en")
        quote = r.json()["quoteText"]
        print "\n\n this is the quote: ", quote

        quote_author = r.json()["quoteAuthor"]
        print "\n\n  this is the author: ", quote_author
    except:
        quote = unicode("Through perseverance many people win success out of what seemed destined to be certain failure.", "utf-8")
        quote_author = unicode("Benjamin Disraeli", "utf-8")

    if not session.get('logged_in'):
        return render_template("homepage.html", 
                                quote=quote, 
                                quote_author=quote_author)
    else: 
        return render_template("entry.html", 
                                quote=quote,
                                quote_author=quote_author)

@app.route('/register', methods=['POST'])
def register():
    """Register the user"""
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    #add the new user to the model
    new_user = User(username=username, password=password, email=email)

    db.session.add(new_user)
    db.session.commit()

    flash("You have just registered! Login to start writing entries. Thank you!")
    return redirect('/')

@app.route('/login', methods=['POST'])
def handle_login():
    """Login the user. Store user in session cookie"""
    #this function handles the form info from the homepage modal window 
    username = request.form["username"]
    print "\n\n\n username ", username
    password = request.form["password"]
    print "\n\n\n\n password ", password
    # password = bcrypt.generate_password_hash(request.form.get("password"))

    if request.form['password'] == password and request.form['username'] == username:
        session['logged_in'] = True

    else:
        flash("Incorrect login")
        return redirect('/login')


    flash("You are logged in!")
    return render_template("entry.html")


def view_entries_by_tag():
    """Create a function that sorts the entries by user's input tag"""

@app.route('/new_entry')
@login_required
def add_entry_to_db():
    entry_body = request.form["entry"]
    # add the entry to the model
    entry_id = Entry(entry_body=entry_body, entry_date=entry_date, username=username, tag=tag)

    db.session.add(entry_id)
    db.session.commit()

@app.route('/logout')
def logout_form():
    """Process logout form"""

    #Remove user from session
    session.clear()
    flash("Logged out")
    return render_template("/")

    

if __name__ == "__main__":
    DebugToolbarExtension(app)

    app.run(debug=True, host='0.0.0.0', port=5000) #vagrant requires port to be 5000