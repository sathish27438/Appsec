from flask import Flask, request, jsonify, session

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-me"

users_db = {
    "wiener": {
        "password": "peter",
        "role": "user"
    },
    "carlos": {
        "password": "password",
        "role": "user"
    }
}

# Helper function for login check:
def login_check(username, password):
    # 1. Safely check if the username exists in your database dict
    if username in users_db:
        # 2. If it exists, verify the password matches
        if users_db[username]["password"] == password:
            return True
            
    return False

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or request.form
    username = data.get('username')
    password = data.get('password')
    if login_check(username,password):
        session['username'] = username
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'username' not in session:
        return jsonify({"message": "Unauthorized"}), 401
    
    payload = request.get_json()
    if not payload:
        return jsonify({"message": "No data provided"}), 400
        
    target_user = payload.get('id')
    new_password = payload.get('password')
    
    # 3. Write the logic here:
    # If target_user is a valid key in users_db, set that user's "password" to new_password.
    if target_user in users_db:
        users_db[target_user]["password"] = new_password

        return jsonify({"message": f"Profile for {target_user} updated successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)