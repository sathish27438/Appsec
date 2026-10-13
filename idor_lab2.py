from flask import Flask, request, jsonify, session

app = Flask(__name__)

users_db = {
   "wiener":{
       "id" : 1,
       "password" : "1234556",
       "role" : "admin"

   },

   "carlos": {
       "id" : 2,
        "password" : "password",
        "role" : "user"
   }
}

def login_check(username, password):
    user = users_db.get(username)
    # If user exists AND the password matches, return True
    if user and password == user["password"]:
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
    # 1. Authenticate the session
    username = session.get('username')
    if not username:
        return jsonify({"message": "Not Authorized"}), 401
    
    # 2. Grab the raw payload
    payload = request.get_json()
    
    # 3. THE MASS ASSIGNMENT FLAW: Blindly loop through whatever the user sent
    for key, value in payload.items():
        users_db[username][key] = value
        
    # 4. Show the updated profile to prove it worked
    return jsonify(users_db[username]), 200
    