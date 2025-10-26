from flask import Flask, render_template, request, jsonify,redirect,url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# MongoDB connection
mongo_url = os.getenv("mongo_url")
client = MongoClient(mongo_url)
db = client["database"]
collection = db["todo"]

# Routes
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get JSON data safely
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400

        # Insert into MongoDB
        collection.insert_one(data)

        # Fetch all todos
        todos = list(collection.find())
        for t in todos:
            t["_id"] = str(t["_id"])

        # Optionally return JSON if it's an API call
        return jsonify({"message": "Todo added", "todos": todos}), 201

    # GET request: render HTML template
    todos = list(collection.find())
    for t in todos:
        t["_id"] = str(t["_id"])
    return render_template("index.html", todos=todos)

@app.route("/delete/<string:task_id>",methods=["DELETE"])
def delete(task_id):
    result=collection.delete_one({"_id":ObjectId(task_id)})
    return redirect(url_for("home")) 



# Run the app
if __name__ == "__main__":
    app.run(debug=True)
