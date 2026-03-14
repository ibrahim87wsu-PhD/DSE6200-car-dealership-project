from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["car_dealership"]
collection = db["car_sales"]

@app.route("/")
def index():
    cars = list(collection.find().sort("_id", -1).limit(50))
    return render_template("index.html", cars=cars)

@app.route("/add", methods=["GET", "POST"])
def add_car():
    if request.method == "POST":
        new_car = {
            "car_id": request.form["car_id"],
            "brand": request.form["brand"],
            "model": request.form["model"],
            "year": int(request.form["year"]),
            "price": int(request.form["price"]),
            "sale_date": request.form["sale_date"],
            "dealer_location": request.form["dealer_location"],
            "customer_city": request.form["customer_city"],
            "salesperson": request.form["salesperson"],
            "status": request.form["status"]
        }
        collection.insert_one(new_car)
        return redirect(url_for("index"))
    return render_template("add_car.html")

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit_car(id):
    car = collection.find_one({"_id": ObjectId(id)})

    if request.method == "POST":
        updated_car = {
            "car_id": request.form["car_id"],
            "brand": request.form["brand"],
            "model": request.form["model"],
            "year": int(request.form["year"]),
            "price": int(request.form["price"]),
            "sale_date": request.form["sale_date"],
            "dealer_location": request.form["dealer_location"],
            "customer_city": request.form["customer_city"],
            "salesperson": request.form["salesperson"],
            "status": request.form["status"]
        }
        collection.update_one({"_id": ObjectId(id)}, {"$set": updated_car})
        return redirect(url_for("index"))

    return render_template("edit_car.html", car=car)

@app.route("/delete/<id>")
def delete_car(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("index"))

@app.route("/analytics", methods=["GET", "POST"])
def analytics():
    results = []
    selected_year = None

    if request.method == "POST":
        selected_year = int(request.form["year"])

        pipeline = [
            {"$match": {"year": selected_year}},
            {"$group": {"_id": "$brand", "total_sales": {"$sum": "$price"}}},
            {"$sort": {"total_sales": -1}}
        ]

        results = list(collection.aggregate(pipeline))

    return render_template("analytics.html", results=results, selected_year=selected_year)

if __name__ == "__main__":
    app.run(debug=True)