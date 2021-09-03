from flask import Flask, render_template, redirect
from jinja2 import Template
from splinter import browser
from flask_pymongo import PyMongo
import scrape_mars


# Create an instance of our Flask app.
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

mongo.db.mars_page.drop()

# Set route
@app.route("/")
def home():
    mars_page = mongo.db.mars_page.find_one()
    return render_template("index.html", mars_page = mars_page)

# Set route
@app.route("/scrape")
def scraper():
    mars_page = mongo.db.mars_page
    mars_page_data = scrape_mars.scrape()
    mars_page.update({}, mars_page_data, upsert=True)
    return redirect("/", code=302)

 
if __name__ == "__main__":
    app.run(debug=True)
