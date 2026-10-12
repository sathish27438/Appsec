from flask import Flask, request, jsonify, session

app = Flask(__name__)

users_db = {
    "wiener": {
        "password": "1111", 
        "role": "admin",
        "message": {"id": "1", "text": "This is a test message"}
    },
    "carlos": {
        "password": "2222", 
        "role": "user",
        "message": {"id": "2", "text": "Hello world from Carlos"}
    }
}

def login_check(username, password):
    if username in users_db and password == users_db[username]["password"]:
        return True
    return False

### Retriving the message for a user based on their id value.

def get_message(requested_id):
    # Loop through all users in the database
    for username, data in users_db.items():
        # If the ID in their message matches the ID from the URL, return it
        if data["message"]["id"] == requested_id:
            return data["message"]
    return None


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or request.form
    username = data.get('username')
    password = data.get('password')

    if login_check(username, password):
        session['username'] = username
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@app.route('/message', methods=['GET'])
def message():
    user_id = request.args.get('id')
    username = session.get('username')
    if not user_id or not username:
        return jsonify({"error": "Missing id parameter"}), 400

    message = get_message(user_id)
    if message:
        return jsonify(message), 200
    else:
        return jsonify({"error": "Message not found"}), 404