from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
import os

# Initialize Flask application
app = Flask(__name__)

# Define path to SQLite database file
db_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dataentry', 'location.db'))

# Configure SQLAlchemy to use SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy object with the Flask app
db = SQLAlchemy(app)

# Define Enum for location types (Danger, Safe Spot, Resource)
class LocationType(Enum):
    DANGER = 'Danger'
    SAFE = 'Safe Spot'
    RESOURCE = 'Resource'

# Define SQLAlchemy Model for locations
class Location(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    details = db.Column(db.String(500), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    location_type = db.Column(db.Enum(LocationType), nullable=False)

    def __repr__(self) -> str:
        return f"{self.name}"

# Route for the index page
@app.route("/")
def index():
    return render_template("index.html")

# Route for the map page
@app.route("/map")
def show_map():
    return render_template("map.html")

# Route for displaying resources (locations with location_type='RESOURCE')
@app.route("/resources")
def show_resources():
    entries = Location.query.filter_by(location_type='RESOURCE').all()
    return render_template("resources.html", entries=entries)

# Route for displaying safe spots (locations with location_type='SAFE')
@app.route("/safespots")
def show_safespots():
    entries = Location.query.filter_by(location_type='SAFE').all()
    return render_template("safespots.html", entries=entries)

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
