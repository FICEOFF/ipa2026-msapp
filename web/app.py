import os
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")

client = MongoClient(mongo_uri)
mydb = client[db_name]
mycol = mydb["routers"]

@app.route("/", methods=["GET"])
def main():
    return render_template("index.html", data=mycol.find({}, {"password": 0}))

@app.route("/add", methods=["POST"])
def add_router():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")
    mycol.insert_one({"ip": ip, "username": username, "password": password})
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete_router():
    try:
        id = request.form.get("id")
        mycol.delete_one({"_id": ObjectId(id)})
    except Exception:
        pass
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
