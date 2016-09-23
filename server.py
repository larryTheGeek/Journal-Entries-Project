import os 
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
import requests
import geocoder
from datetime import datetime
from model import db, connect_to_db, Trip, Preference, TripPreference
import json
import googlemaps
import pdb

@app.route('/')
def homepage():
    """Display the homepage to the user"""

    render_template("homepage.html")

def login():
    """Login the user"""

def register():
    """Register the user"""