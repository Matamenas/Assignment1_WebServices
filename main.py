from fastapi import FastAPI
from pydantic import BaseModel
import pymongo
from pymongo import MongoClient
import requests

app = FastAPI()

# MongoDB connection setup
client = pymongo.MongoClient("mongodb+srv://matasbagdonas02_db_user:hgjUPMIOCCxfysOh@webservicesassignment1.ymqk4vx.mongodb.net/?appName=WebServicesAssignment1")
db = client["WebServicesAssignment1"]
collection = db["products"]


class Product(BaseModel):
    ProductID: str
    Name: str
    UnitPrice: float
    StockQuantity: int
    Description: str

# Root of the API to test if the API is working fine
@app.get("/")
async def root():
    return {"message": "Hello, World!"}

# /getSingleProduct/productID
# Get Single Product EndPoint
@app.get("/getSingleProduct/{ProductID: str}")
async def get_single_product(ProductID: str):
    product = collection.find_one({"ProductID": ProductID}, {"_id": 0})
    if not product:
        return {"message": "Product not found"}
    else:
        return {"ProductID": product["ProductID"], "Name": product["Name"], "UnitPrice": product["UnitPrice"], "StockQuantity": product["StockQuantity"], "Description": product["Description"]}

# /getAll/
# Get All Products EndPoint
@app.get("/getAll")
async def get_all_products():
    products = list(collection.find({}, {"_id": 0}))
    return products


# Add a product to the database
@app.post("/addnew")
async def add_new_product(product: Product):
    collection.insert_one(product.dict())
    return {"message": "Product added successfully"}

# Delete a product from the database
@app.delete("/deleteproduct/{ProductID}")
async def delete_product(ProductID: str):
    result = collection.delete_one({"ProductID": ProductID})
    if result.deleted_count == 0:
        return {"message": "Product not found"}
    return {"message": "Product deleted successfully"}

# Get products starting with a specific letter
@app.get("/startsWith/{letter}")
async def get_products_starting_with(letter: str):
    products = list(collection.find({"Name": {"$regex": f"^{letter}"}}, {"_id": 0}))
    return products

# Paginataion EndPoint to get products in chunks of 10
@app.get("/paginate/{start_id}/{end_id}")
async def paginate(start_id: str, end_id: str):
    products = list(collection.find({"ProductID": {"$gte": start_id, "$lte": end_id}}, {"_id": 0}).limit(10))
    return products

# Convert all prices to Euros and return the updated products
@app.get("/convert/{ProductID}")
async def convert_price(ProductID: str):
    product = collection.find_one({"ProductID": ProductID}, {"_id": 0})

    if not product:
        return {"message": "Product not found"}

    # Exchange Rate API to convert USD to EUR
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    data = response.json()
    eur_rate = data["rates"]["EUR"]

    converted_price = product["UnitPrice"] * eur_rate

    return{
        "ProductID": product["ProductID"],
        "Name": product["Name"],
        "UnitPrice": round(converted_price, 2),
        "StockQuantity": product["StockQuantity"],
        "Description": product["Description"]
    }

