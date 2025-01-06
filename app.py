from flask import Flask, request, render_template_string
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
    return render_template_string(html_template)

@app.route('/generate', methods=['POST'])
def generate_id():
    string_to_encrypt = request.form.get("name", "").upper()
    sa = int(request.form.get("key", 0))
    num = request.form.get("dob", "")

    if not string_to_encrypt or sa < 1 or sa > 25:
        return render_template_string(html_template, error="Invalid input. Ensure you provide a name and a key between 1 and 25.")

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
        return render_template_string(html_template, error="Date of birth is required.")

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

    return render_template_string(html_template, unique_id=unique_id, current_id_count=len(stored_ids))

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unique ID Generator</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body {
            padding-top: 50px;
        }
        .container {
            max-width: 600px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center">Unique ID Generator</h1>
        <form action="/generate" method="post">
            <div class="form-group">
                <label for="name">Name:</label>
                <input type="text" class="form-control" id="name" name="name" required>
            </div>
            <div class="form-group">
                <label for="key">Key (1-25):</label>
                <input type="number" class="form-control" id="key" name="key" min="1" max="25" required>
            </div>
            <div class="form-group">
                <label for="dob">Date of Birth (YYYYMMDD):</label>
                <input type="text" class="form-control" id="dob" name="dob" required>
            </div>
            <button type="submit" class="btn btn-primary">Generate ID</button>
        </form>
        {% if error %}
            <div class="alert alert-danger mt-3" role="alert">
                {{ error }}
            </div>
        {% endif %}
        {% if unique_id %}
            <div class="alert alert-success mt-3" role="alert">
                Unique ID: {{ unique_id }}<br>
                Total IDs Generated: {{ current_id_count }}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)

  
