from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# Simulated user database
users = {
    "accounts": "password123",
    "admin": "supersecret"
}


def check_username_password(username, password):
    if username in users:
        time.sleep(0.1)
        if password == users.get(username):
            return True  # valid credentials
        else:
            return False  # wrong password
    else:
        return False  # wrong username


@app.route('/login', methods=['POST'])
def login():
    # your logic here
    data = request.get_json() or request.form
    
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    if check_username_password(username, password):
     return jsonify({"message": "Login successful"}), 302
    else:
     return jsonify({"message": "Invalid username or password"}), 200

if __name__ == '__main__':
    app.run(debug=True)