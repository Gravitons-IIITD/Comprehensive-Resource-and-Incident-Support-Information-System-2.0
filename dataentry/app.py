from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from enum import Enum

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///announce.db"
app.config["SQLALCHEMY_BINDS"] = {"location": "sqlite:///location.db"}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class LocationType(Enum):
    DANGER = 'Danger'
    SAFE = 'Safe Spot'
    RESOURCE = 'Resource'

class Announce(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)

    def __repr__(self) -> str:
        return f"{self.heading}"
    
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
        var = Location(name = name, details = details, longitude = longitude, latitude = latitude, location_type = location_type)
        db.session.add(var)
        db.session.commit()
    return render_template("location.html")

if __name__ == "__main__":
    app.run(debug=True)
