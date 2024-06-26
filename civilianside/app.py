from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/map")
def show_map():
    return render_template("map.html")

@app.route("/resources")
def show_resources():
    return render_template("resources.html")

@app.route("/safespots")
def show_safespots():
    return render_template("safespots.html")

if __name__ == "__main__":
    app.run(debug=True)