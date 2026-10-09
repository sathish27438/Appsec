from flask import Flask, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'supersecretkey' # Required for Flask sessions to work

users = {
    "wiener": {"auth_code": "1111", "role": "admin", "password": "peter"},
    "carlos": {"auth_code": "2222", "role": "user", "password": "111111"}
}

def login_check(username, password):
    if username in users and password == users[username]["password"]:
        return True
    return False

def authenticate_2fa(username, auth_code):
    if username in users and auth_code == users[username]["auth_code"]:
        return True
    return False

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or request.form
    username = data.get('username')
    password = data.get('password')

    if login_check(username, password):
        # 1. Put the username into the Flask session waiting room
        session['pending_user'] = username
        return jsonify({"message": "Login successful. Please complete 2FA."}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@app.route('/login2', methods=['POST'])
def login2():
    data = request.get_json() or request.form
    auth_code = data.get('auth_code')

    # 2. Securely get the username from the session, NOT from the user data
    pending_user = session.get('pending_user')

    # 3. Check if they are actually in the waiting room
    if not pending_user:
        return jsonify({"message": "Please complete step 1 of login first"}), 401

    # 4. Verify the 2FA code using the pending_user variable
    if authenticate_2fa(pending_user, auth_code):
        # 5. Success! Give them the real session token
        session['username'] = pending_user
        
        # 6. Kick them out of the waiting room
        session.pop('pending_user', None)
        
        return jsonify({"message": "2FA successful. Access granted."}), 200
    else:
        return jsonify({"message": "Invalid authentication code"}), 401