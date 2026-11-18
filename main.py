import os
import requests
from flask_cors import CORS
from dotenv import load_dotenv
from flask import Flask, request, abort

load_dotenv()

app = Flask(__name__)

CORS(app, resources={
	r"/*": {"origins": ["https://amsys.wasmer.app","https://amsys-2.wasmer.app"]},
	methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"]
})

@app.route("/api/<path:db_path>", methods=["GET"])
def get_value(db_path):
	db_url = "https://es-attendancesystem-default-rtdb.asia-southeast1.firebasedatabase.app/"
	secret = os.environ["FB_DATABASE_SECRET"]
	response = requests.get(
		f"{db_url}{db_path}.json",
		params={ "auth": secret },
		timeout=10
	)
	response.raise_for_status()
	return response.json()

@app.route("/api/<path:db_path>", methods=["PUT"])
def change_value(db_path):
	db_url = "https://es-attendancesystem-default-rtdb.asia-southeast1.firebasedatabase.app/"
	secret = os.environ["FB_DATABASE_SECRET"]
	data = request.get_data(as_text=True)
	if data is None:
		abort(400, "Expected a request body")
	response = requests.put(
		f"{db_url}{db_path}.json",
		params={ "auth": secret },
		json=data,
		timeout=10
	)
	response.raise_for_status()
	return response.json(), 200

@app.route("/api/<path:db_path>", methods=["DELETE"])
def delete_path(db_path):
	db_url = "https://es-attendancesystem-default-rtdb.asia-southeast1.firebasedatabase.app/"
	secret = os.environ["FB_DATABASE_SECRET"]
	response = requests.delete(
		f"{db_url}{db_path}.json",
		params={ "auth": secret },
		timeout=10
	)
	response.raise_for_status()
	return { "deleted": True }, 200

if __name__ == "__main__":
	app.run()

