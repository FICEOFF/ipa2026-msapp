from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://mongo:27017/")
mydb = client["ipa2026"]
mycol = mydb["routers"]

@app.route("/")
def main():
    return render_template("index.html", data=mycol.find({}, {"password": 0}))

@app.route("/add", methods=["POST"])
def add_router():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")
    mycol.insert_one({"ip": ip, "username": username, "password": password})
    return redirect(url_for("main"))

@app.route("/delete", methods=["POST"])
def delete_router():
    try:
        id = request.form.get("id")
        mycol.delete_one({"_id": ObjectId(id)})
    except Exception:
        pass
    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
