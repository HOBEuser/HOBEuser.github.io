from flask import Flask, render_template, request, jsonify
import random
import json
import os

app = Flask(__name__)

ID_FILE = "generated_ids.json"

def load_ids():
    if os.path.exists(ID_FILE):
        with open(ID_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Error: Invalid JSON in file. Starting fresh.")
                return {}
    return {}

def save_ids(data):
    with open(ID_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def generate_unique_id(base_id, existing_ids):
    while any(base_id == entry["unique_id"] for entry in existing_ids.values()):
        base_id += str(random.randint(10, 99))
    return base_id

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_id():
    string_to_encrypt = request.form.get("name", "").upper()
    sa = int(request.form.get("key", 0))
    num = request.form.get("dob", "")

    if not string_to_encrypt or sa < 1 or sa > 25:
        return render_template('index.html', error="Invalid input. Ensure you provide a name and a key between 1 and 25.")

    ALF = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
    es = ""

    for current_character in string_to_encrypt:
        position = ALF.find(current_character)
        if position == -1:
            es += current_character
        else:
            new_position = (position + sa) % 26
            es += ALF[new_position]

    rand = random.randint(1000, 10000)

    if not num:
        return render_template('index.html', error="Date of birth is required.")

    base_id = num + str(rand) + es
    stored_ids = load_ids()

    if not isinstance(stored_ids, dict):
        stored_ids = {}

    unique_id = generate_unique_id(base_id, stored_ids)

    id_num = len(stored_ids) + 1
    stored_ids[str(id_num)] = {
        "unique_id": unique_id,
        "name": string_to_encrypt
    }

    save_ids(stored_ids)

    return render_template('index.html', unique_id=unique_id, current_id_count=len(stored_ids))

if __name__ == '__main__':
    app.run(debug=True)
