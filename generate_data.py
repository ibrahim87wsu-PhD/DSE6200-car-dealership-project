from pymongo import MongoClient
from faker import Faker
import random

fake = Faker()

client = MongoClient("mongodb://localhost:27017/")
db = client["car_dealership"]
collection = db["car_sales"]

# Delete old data first
collection.delete_many({})

brands_models = {
    "Toyota": ["Camry", "Corolla", "RAV4"],
    "Honda": ["Civic", "Accord", "CR-V"],
    "Ford": ["Focus", "Escape", "Mustang"],
    "BMW": ["3 Series", "X3", "X5"],
    "Chevrolet": ["Malibu", "Equinox", "Impala"]
}

statuses = ["Sold", "Available", "Pending"]

data = []

for i in range(7000):
    brand = random.choice(list(brands_models.keys()))
    model = random.choice(brands_models[brand])

    car = {
        "car_id": f"C{1000 + i}",
        "brand": brand,
        "model": model,
        "year": random.randint(2018, 2025),
        "price": random.randint(18000, 60000),
        "sale_date": fake.date_between(start_date="-2y", end_date="today").strftime("%Y-%m-%d"),
        "dealer_location": fake.city(),
        "customer_city": fake.city(),
        "salesperson": fake.name(),
        "status": random.choice(statuses)
    }

    data.append(car)

collection.insert_many(data)

print("7000 random car sales records inserted successfully into MongoDB.")