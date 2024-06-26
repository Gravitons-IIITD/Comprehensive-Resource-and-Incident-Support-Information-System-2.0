import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from enum import Enum

app = Flask(__name__)

# Get the directory of the current script
basedir = os.path.abspath(os.path.dirname(__file__))

# Main database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "announce.db")

# Additional bind for location database
app.config["SQLALCHEMY_BINDS"] = {
    "location": "sqlite:///" + os.path.join(basedir, "location.db")
}

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'supersecretkey'
db = SQLAlchemy(app)

# Enum for LocationType
class LocationType(Enum):
    DANGER = 'Danger'
    SAFE = 'Safe Spot'
    RESOURCE = 'Resource'

# Model for announcements
class Announce(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)

    def __repr__(self) -> str:
        return f"{self.heading}"

# Model for locations with a specific bind key
class Location(db.Model):
    __bind_key__ = 'location'
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    details = db.Column(db.String(500), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    location_type = db.Column(db.Enum(LocationType), nullable=False)

    def __repr__(self) -> str:
        return f"{self.name}"

# Create all tables in the databases
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("indexentry.html")

@app.route("/announce", methods=["GET", "POST"])
def show_announce():
    if request.method == "POST":
        heading = request.form["heading"]
        content = request.form["content"]
        var = Announce(heading=heading, content=content)
        db.session.add(var)
        db.session.commit()
    return render_template("announce.html")

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

if __name__ == "__main__":
    app.run(debug=True)
