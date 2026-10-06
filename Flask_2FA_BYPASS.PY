from flask import Flask, request, jsonify, session

app = Flask(__name__)

users = {
    "wiener": "peter",
    "carlos": "111111"
}

app.secret_key = 'supersecretkey'

def login_check(username, password):
    if username in users:
        if password == users.get(username):
            return True
        else:
            return False
    else:
        return False

code = 1111

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() or request.form
        username = data.get('username')
        password = data.get('password')
        # check credentials, set session
        if login_check(username, password):
            session['username'] = username
            return jsonify({"message": "Login successful"}), 302
    # check credentials, set session
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@app.route('/login2')
def login2():
    # show 2FA page but never validate
    return jsonify({"message": "2FA page"}), 200

@app.route('/my-account')
def my_account():
    # accessible without 2FA completion - the vulnerability
    if 'username' in session:
        return jsonify({"message": "Welcome to your account, {}".format(session['username'])}), 200
    else:
        return jsonify({"message": "Unauthorized"}), 401
    pass


if __name__ == '__main__':
    app.run(debug=True)