from flask import Flask, request, jsonify, session

app = Flask(__name__)

users_db = {
    "wiener": {"password": "peter", 
               "role": "admin",
               "message" : {
                   "id": 1,
                   "content": "This is a secret message for wiener. Only wiener should be able to see this message."
               }
               },
    "carlos": {"password": "111111", 
               "role": "user",
               "message" : {
                   "id": 2,
                   "content": "This is a secret message for carlos. Only carlos should be able to see this message."
               }
            }}

def login_check(username, password):
    if username in users_db and password == users_db[username]["password"]:
        return True
    return False

## Login route that sets the session username

def message_check(username, message_id):
    if username in users_db and message_id == users_db[username]["message"]["id"]:
        return True
    return False

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

@app.route('/message/<int:message_id>', methods=['GET'])
def get_message(message_id):
    username = session.get('username')
    if not username:
        return jsonify({"message": "Unauthorized"}), 401

    # Call the security function you wrote
    if message_check(username, message_id):
        return jsonify(users_db[username]["message"]), 200
    else:
        return jsonify({"message": "Message not found or access denied"}), 404

