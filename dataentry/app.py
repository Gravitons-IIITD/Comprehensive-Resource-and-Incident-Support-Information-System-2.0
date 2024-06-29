import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from enum import Enum

app = Flask(__name__)

# Get the directory of the current script
basedir = os.path.abspath(os.path.dirname(__file__))

# Main database configuration for announcements
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "announce.db")

# Additional bind for location database
app.config["SQLALCHEMY_BINDS"] = {
    "location": "sqlite:///" + os.path.join(basedir, "location.db")
}

# Disable SQLAlchemy modification tracking to suppress warnings
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Secret key for session management (replace with your actual secret key)
app.secret_key = 'supersecretkey'

# Initialize SQLAlchemy object with the Flask app
db = SQLAlchemy(app)

# Enum for LocationType to categorize locations
class LocationType(Enum):
    DANGER = 'Danger'
    SAFE = 'Safe Spot'
    RESOURCE = 'Resource'

# Model for announcements stored in the main database
class Announce(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)

    def __repr__(self) -> str:
        return f"{self.heading}"

# Model for locations stored in the 'location' database
class Location(db.Model):
    __bind_key__ = 'location'  # Bind this model to the 'location' database
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    details = db.Column(db.String(500), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    location_type = db.Column(db.Enum(LocationType), nullable=False)

    def __repr__(self) -> str:
        return f"{self.name}"

# Create all tables in the databases (announce.db and location.db)
with app.app_context():
    db.create_all()

# Route for the index page
@app.route("/")
def index():
    return render_template("indexentry.html")

# Route for handling announcements (GET and POST methods)
@app.route("/announce", methods=["GET", "POST"])
def show_announce():
    if request.method == "POST":
        heading = request.form["heading"]
        content = request.form["content"]
        var = Announce(heading=heading, content=content)
        db.session.add(var)
        db.session.commit()
    return render_template("announce.html")

# Route for handling locations (GET and POST methods)
@app.route("/location", methods=["GET", "POST"])
def show_location():
    if request.method == "POST":
        name = request.form["name"]
        details = request.form["details"]
        longitude = request.form["longitude"]
        latitude = request.form["latitude"]
        location_type_str = request.form["dropdown"]
        location_type = LocationType[location_type_str.upper()]
        var = Location(name=name, details=details, longitude=longitude, latitude=latitude, location_type=location_type)
        db.session.add(var)
        db.session.commit()
    return render_template("location.html")

# Run the Flask application in debug mode
if __name__ == "__main__":
    app.run(debug=True)
