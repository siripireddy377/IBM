
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
from flask_cors import CORS  
from functions import calculate_office_footprint  

app = Flask(__name__)
CORS(app)  

try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    db = client["carbon_tracker"]
    client.server_info()  
    print("✅ Connected to MongoDB")
except Exception as e:
    print(f"❌ MongoDB Connection Failed: {e}")


users_collection = db["users"]
footprints_collection = db["footprints"]


@app.route("/")
def home():
    return render_template("index.html")  

@app.route("/add_user", methods=["POST"])
def add_user():
    try:
        data = request.json
        if "user_id" not in data or "company_name" not in data:
            return jsonify({"error": "Missing required fields"}), 400
        
        user_data = {
            "user_id": data["user_id"],
            "company_name": data["company_name"],
            "timestamp": datetime.utcnow()
        }
        users_collection.insert_one(user_data)
        return jsonify({"message": "User registered successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/add_footprint", methods=["POST"])
def add_footprint():
    try:
        data = request.json
        required_fields = [
            "user_id",
            "company_name",
            "electricity_usage",
            "business_travel",
            "office_waste",
            "water_consumption"
        ]
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400
        
        total_emissions = calculate_office_footprint(
            data["electricity_usage"],
            data["business_travel"],
            data["office_waste"],
            data["water_consumption"]
        )

        footprint_data = {
            "user_id": data["user_id"],
            "company_name": data["company_name"],
            "electricity_usage": data["electricity_usage"],
            "business_travel": data["business_travel"],
            "office_waste": data["office_waste"],
            "water_consumption": data["water_consumption"],
            "total_emissions": total_emissions,
            "timestamp": datetime.utcnow()
        }

        footprints_collection.insert_one(footprint_data)
        return jsonify({"message": "Data saved successfully!", "total_emissions": total_emissions}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_footprints/<user_id>/<company_name>", methods=["GET"])
def get_footprints(user_id, company_name):
    try:
        data = list(footprints_collection.find(
            {"user_id": user_id, "company_name": company_name}, {"_id": 0}
        ))
        if not data:
            return jsonify({"message": "No data found for this user"}), 404
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
