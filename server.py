import os
from flask import Flask, render_template, request, flash, redirect, session, abort
from flask_debugtoolbar import DebugToolbarExtension
import requests
from datetime import datetime
from model import connect_to_db, db, User, Entry, Tag, EntryTag
import json
import pdb
from flask_login import login_required, current_user
from flask_bcrypt import Bcrypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from flask.ext.login import current_user,current_app

app = Flask(__name__)

app.secret_key = "Shhhhh"

bcrypt = Bcrypt(app)


@app.route('/')
def homepage():
    """Display the homepage to the user"""

    quote, quote_author = get_quotes_for_footer()

    if not session.get('logged_in'):
        return render_template("homepage.html",
                               quote=quote,
                               quote_author=quote_author)
    else:
        return render_template("entry.html",
                               quote=quote,
                               quote_author=quote_author)


@app.route('/login', methods=['POST'])
def handle_login():
    """Process login and store user in session."""

    # this function handles the form info from the homepage modal window
    username = request.form["username"]
    password = bcrypt.generate_password_hash(request.form.get("password"))

    # Check that the user exists.
    uq = User.query
    user_object = uq.filter_by(username=username).first()

    if user_object and bcrypt.check_password_hash(password, user_object.password):

        session["user_id"] = user_object.user_id
        session["logged_in"] = True

        flash("Hello again - You are logged in!")

        return redirect("/new_entry")

    else:
        flash("Incorrect login")
        return redirect("/")


@app.route('/register', methods=['POST'])
def register():
    """Register the user"""

    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    # password = bcrypt.generate_password_hash(request.form.get("password"))

    # Add the new user to the model
    new_user = User(username=username, password=password, email=email)

    # FIXME: grab the user_id to store in the session for later use.
    # user_id = db.session.query(User.user_id).filter_by(username=username).first()[0]
    # session['user_id']

    db.session.add(new_user)
    db.session.commit()

    flash("You have just registered! Login to start writing entries. Thank you!")
    quote, quote_author = get_quotes_for_footer()

    return render_template("entry.html",
                           quote=quote,
                           quote_author=quote_author)


@app.route('/new_entry')
def new_entry():
    """Displays new journal entry form."""

    quote, quote_author = get_quotes_for_footer()

    return render_template("entry.html",
                           quote=quote,
                           quote_author=quote_author)


@app.route('/entry', methods=['POST'])
def add_entry_to_db():
    """Save and redirect journal entries."""
    try:
        title = request.form["title"]
        body = request.form["journalBody"]
        tags = request.form.getlist('prof1')

        user_id = session['user_id']

        entry = Entry(entry_body=body, entry_title=title, user_id=user_id)

        # Need to consider entry_date
        # entry_id = Entry(body=entry_body, entry_date=entry_date, username=username, tag=tag)

        db.session.add(entry)
        db.session.commit()

        quote, quote_author = get_quotes_for_footer()

        return render_template("view_entries.html",
                           title=title,
                           body=body,
                           quote=quote,
                           quote_author=quote_author)
    except:
        
        quote, quote_author = get_quotes_for_footer()
        
        return render_template("error.html",
                                quote=quote,
                                quote_author=quote_author)


@app.route('/logout')
def logout_form():
    """Process logout form"""

    #Remove user from session
    session.clear()

    return redirect("/")


@app.route('/recover', methods=('GET', 'POST', ))
def recover_login_info():
    """When the user hits forgot password in the login modal, send them an email with their username or password"""
    token = request.args.get('token', None)
    form = ResetPassword(request.form)
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            token = user.get_token()
            print token
    return redirect("/")

# if token and verified_result:
#     is_verified_token = True
#     password_submit_form = ResetPasswordSubmit(request.form)
#     if password_submit_form.validate_on_submit():
#         verified_result.pasword = generate_password_hash(password_submit_form.password.data)
#         verified_result.is_active = True
#         db.session.add(verified_result)
#         db.session.commit()

#         flash("Password updated successfully!")
#         return redirect("/new_entry")


########################### Helper Functions ###################################

def get_quotes_for_footer():
    """Call this function in other routes to display fancy quote footer"""
    try:
        r = requests.get("http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en")
        quote = r.json()["quoteText"]
        print "\n\n this is the quote: ", quote

        quote_author = r.json()["quoteAuthor"]
        print "\n\n  this is the author: ", quote_author
    except:
        quote = unicode("Through perseverance many people win success out of what seemed destined to be certain failure.", "utf-8")
        quote_author = unicode("Benjamin Disraeli", "utf-8")

    return quote, quote_author


# def view_entries_by_tag():
#     """Create a function that sorts the entries by user's input tag"""

    # from view_entries.html have a navbar?/button? where the user can sort through their past entries 


if __name__ == "__main__":
    DebugToolbarExtension(app)

    connect_to_db(app)

    app.run(debug=True, host='0.0.0.0', port=5000) #vagrant requires port to be 5000
