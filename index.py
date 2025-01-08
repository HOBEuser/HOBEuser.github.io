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
    <script>
        function generateUniqueID() {
            const name = document.getElementById('name').value.trim().toUpperCase();
            const key = parseInt(document.getElementById('key').value);
            const dob = document.getElementById('dob').value.trim();

            if (!name || isNaN(key) || key < 1 || key > 25 || !dob) {
                alert("Invalid input. Ensure you provide a name, a key between 1 and 25, and a date of birth.");
                return;
            }

            const ALF = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ";
            let encryptedName = "";

            for (let i = 0; i < name.length; i++) {
                const currentCharacter = name[i];
                const position = ALF.indexOf(currentCharacter);
                if (position === -1) {
                    encryptedName += currentCharacter;
                } else {
                    const newPosition = (position + key) % 26;
                    encryptedName += ALF[newPosition];
                }
            }

            const rand = Math.floor(Math.random() * 9000) + 1000;
            const uniqueID = dob + rand + encryptedName;

            document.getElementById('result').innerHTML = `
                <div class="alert alert-success mt-3" role="alert">
                    Unique ID: ${uniqueID}<br>
                </div>
            `;
        }
    </script>
</head>
<body>
    <div class="container">
        <h1 class="text-center">Unique ID Generator</h1>
        <form onsubmit="event.preventDefault(); generateUniqueID();">
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
        <div id="result"></div>
    </div>
</body>
</html>

