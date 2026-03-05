from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from flask import render_template
from dotenv import load_dotenv
import os
load_dotenv() 
app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["student"]
collection = db["demo"]

def serialize_student(student):
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "age": student["age"],
        "hobbies": student.get("hobbies", [])
        
    }


@app.route('/')
def frontend():
    return render_template("index.html")

@app.route('/get', methods=["GET"])
def get_students():
    students = collection.find()
    return jsonify([serialize_student(s) for s in students])


@app.route('/add', methods=["POST"])
def add_student():
    data = request.json

    new_student = {
        "name": data.get("name"),
        "age": data.get("age"),
        "hobbies": data.get("hobbies")
    }

    result = collection.insert_one(new_student)

    return jsonify({
        "message": "Student added successfully",
        "id": str(result.inserted_id)
    }), 201


@app.route('/update/<id>', methods=["PUT"])
def update_student(id):
    data = request.json

    updated_data = {}

    if "name" in data:
        updated_data["name"] = data["name"]
    if "age" in data:
        updated_data["age"] = data["age"]
    if "hobbies" in data:
        updated_data["hobbies"] = data["hobbies"]

    result = collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": updated_data}
    )

    if result.matched_count == 0:
        return jsonify({"message": "Student not found"}), 404

    return jsonify({"message": "Student updated successfully"})


@app.route('/delete/<id>', methods=["DELETE"])
def delete_student(id):
    result = collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        return jsonify({"message": "Student not found"}), 404

    return jsonify({"message": "Student deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
