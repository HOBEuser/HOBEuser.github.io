import random
import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

ID_FILE = "generated_ids.json"

# Function to load existing IDs or create an empty structure if the file doesn't exist
def load_ids():
    if os.path.exists(ID_FILE):
        with open(ID_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Error: Invalid JSON in file. Starting fresh.")
                return {}
    return {}

# Function to save IDs to the file
def save_ids(data):
    with open(ID_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Function to generate a unique ID
def generate_unique_id(base_id, existing_ids):
    while any(base_id == entry["unique_id"] for entry in existing_ids.values()):
        # Add two random digits if the ID already exists
        base_id += str(random.randint(10, 99))
    return base_id

@app.route('/')
def home():
    return "Welcome to the ID generation and checking server!"

@app.route('/generate_id', methods=['POST'])
def generate_id():
    data = request.get_json()
    if not data or not all(key in data for key in ('name', 'dob', 'key')):
        return jsonify({"error": "Invalid input, name, dob, and key are required"}), 400

    name = data['name']
    dob = data['dob']
    key = data['key']

    ALF = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
    stringToEncrypt = name.upper()
    ES = ""

    for currentCharacter in stringToEncrypt:
        position = ALF.find(currentCharacter)
        if position == -1:
            ES += currentCharacter
        else:
            newPosition = (position + key) % 26
            ES += ALF[newPosition]

    rand = random.randint(1000, 10000)
    base_id = dob + str(rand) + ES

    stored_ids = load_ids()
    unique_id = generate_unique_id(base_id, stored_ids)

    # Save the new ID in the stored IDs
    IDNum = len(stored_ids) + 1
    stored_ids[str(IDNum)] = {
        "unique_id": unique_id,
        "name": name
    }
    save_ids(stored_ids)

    return jsonify({"unique_id": unique_id, "IDNum": IDNum})

@app.route('/check_id', methods=['GET'])
def check_id():
    user_id = request.args.get('id')
    if not user_id:
        return jsonify({"error": "ID parameter is missing"}), 400

    stored_ids = load_ids()
    for entry in stored_ids.values():
        if entry["unique_id"] == user_id:
            return jsonify({"found": True, "ID": entry})

    return jsonify({"found": False, "message": "ID not found"})

if __name__ == '__main__':
    app.run(debug=True)
