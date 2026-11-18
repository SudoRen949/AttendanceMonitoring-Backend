import os
import requests
from flask_cors import CORS
from dotenv import load_dotenv
from flask import Flask, request, abort

load_dotenv()

app = Flask(__name__)

CORS(app, resources={
	r"/api/*": {
		"origins": [
			#"http://localhost:8080",
			#"http://127.0.0.1:8080",
			#"http://0.0.0.0:8080",
			
			#"http://localhost:8082",
			#"http://127.0.0.1:8082",
			#"http://0.0.0.0:8082",
			
			"https://amsys.wasmer.app",
			"https://amsys-2.wasmer.app"
		]
	}
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

