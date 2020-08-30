from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars_data
import urllib3
from urllib3.util.retry import Retry 

# Create an instance of Flask
app1 = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app1, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app1.route("/")
def home():

    nasa_mars_data = mongo.db.collection.find_one()
    
    return render_template("index.html",  nasa_mars_data_html= nasa_mars_data)
#----------------------news scrape-----------------------
# Route that will trigger the scrape function
@app1.route("/scrape")
def scrape():

    # Run the scrape function
    News_data = scrape_mars_data.scrape_news()
    jpl_img = scrape_mars_data.scrape_jpl()
    hemisphere_images_url= scrape_mars_data.scrape_hemsp() 
    mars_table = scrape_mars_data.mars_facts() 
    print("\n-------------------------------------")
    print(News_data)
    print(jpl_img)
    print(hemisphere_images_url)
    # print(mars_table)
    print("----------------------------------\n") 

    fina_dict= {"mars_title":News_data[0],
                "mars_para":News_data[1],
                "Featured_imag_url":jpl_img, 
                "hemisphere_images":hemisphere_images_url,
                "mars_facts":mars_table
                }

# fina_dict= {"mars_title":News_data[0],
#                 "mars_para":News_data[1],
#                 "Featured_imag_url":jpl_img, 
#                 "hemisphere_images":hemisphere_images_url,
#                 "mars_facts":mars_table}
     
    mongo.db.collection.update({},fina_dict , upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app1.run(debug=True)