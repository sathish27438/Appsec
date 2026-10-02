from flask import Flask, request, jsonify

app = Flask(__name__)

#simulate user database
users = {
    "wiener": "peter",
    "carlos": "111111"
}

failed_attempts = {}  # {ip: count}
MAX_ATTEMPTS = 3



def login_check(username, password):
    if username in users:
        if password == users.get(username):
            return True
        else:
            return False
    else:
        return False
        

   

    
@app.route('/login', methods=['POST'])  

def login():
    data = request.get_json() or request.form
        
    username = data.get('username')
    password = data.get('password')
    user_ip  = request.remote_addr

       # Check if IP is blocked
    if failed_attempts.get(user_ip, 0) >= MAX_ATTEMPTS:
        return jsonify({"message": "Too many attempts. Try again later."}), 429

    # Check credentials
    if login_check(username, password):
        failed_attempts[user_ip] = 0  # reset counter on success
        return jsonify({"message": "Login successful"}), 302
    else:
        failed_attempts[user_ip] = failed_attempts.get(user_ip, 0) + 1
        return jsonify({"message": "Invalid username or password"}), 200
    


if __name__ == '__main__':
        app.run(debug=True)

