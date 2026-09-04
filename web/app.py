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
db = client[db_name]
routers = db["routers"]
interface_status = db["interface_status"]

@app.route("/", methods=["GET"])
def main():
    data = routers.find({}, {"password": 0})
    return render_template("index.html", data=data)

@app.route("/add", methods=["POST"])
def add_router():
    try:
        ip = request.form.get("ip")
        username = request.form.get("username")
        password = request.form.get("password")
        routers.insert_one({"ip": ip, "username": username, "password": password})
    except Exception:
        pass
    return redirect("/")

@app.route("/detail", methods=["GET"])
def router_detail():
    ip = request.args.get("ip")
    data = interface_status.find({"router_ip": ip}).sort("timestamp", -1).limit(3)
    return render_template("router_detail.html", router_ip=ip, data=data)

@app.route("/delete", methods=["POST"])
def delete_router():
    try:
        id = request.form.get("id")
        routers.delete_one({"_id": ObjectId(id)})
    except Exception:
        pass
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
