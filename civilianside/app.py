from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from enum import Enum
import os

# Initialize Flask application
app = Flask(__name__)

# Define base directory and database paths
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dataentry'))
location_db_file_path = os.path.join(basedir, 'location.db')
announce_db_file_path = os.path.join(basedir, 'announce.db')

# Configure SQLAlchemy to use the SQLite databases with binds
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{announce_db_file_path}'
app.config['SQLALCHEMY_BINDS'] = {
    'location': f'sqlite:///{location_db_file_path}'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secret key for session management 
app.secret_key = 'supersecretkey'

# Initialize SQLAlchemy object with the Flask app
db = SQLAlchemy(app)

# Define Enum for location types (Danger, Safe Spot, Resource)
class LocationType(Enum):
    DANGER = 'Danger'
    SAFE = 'Safe Spot'
    RESOURCE = 'Resource'

# Define SQLAlchemy Model for locations
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

# Model for announcements stored in the main database
class Announce(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)

    def __repr__(self) -> str:
        return f"{self.heading}"

# Route for the index page
@app.route("/")
def index():
    entries = Announce.query.all()[::-1]
    return render_template("index.html", entries = entries)

# Route for the map page
@app.route("/map")
def show_map():
    danger  = Location.query.filter_by(location_type='DANGER').all()
    safe = Location.query.filter_by(location_type='SAFE').all()
    resource = Location.query.filter_by(location_type='RESOURCE').all()
    return render_template("map.html", danger = danger, safe = safe, resource = resource)

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
