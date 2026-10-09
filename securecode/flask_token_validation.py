from flask import Flask, request, jsonify
import secrets

app = Flask(__name__)

users = {
    "wiener": "peter",
    "carlos": "111111"
}

# Simple token storage — token maps to username
def token_create():
    return secrets.token_urlsafe(16)
reset_tokens = {}

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    # Generate token and store which user it belongs to
    data = request.get_json() or request.form
    username = data.get('username')
    if username in users:
        token = token_create()
        reset_tokens[token] = username  # Store the token with the associated username
        return jsonify({"message": "Password reset token generated", "token": token}), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/reset-password', methods=['POST'])  
def reset_password():
    data = request.get_json() or request.form
    token = data.get('token')
    username = data.get('username')
    new_password = data.get('new_password')
    
    # VULNERABLE — only checks token exists, not if it belongs to username
    if token in reset_tokens and username == reset_tokens[token]:  # FIXED: validate token owner
        users[username]["password"] = new_password  # FIXED: validate token owner
        return jsonify({"message": "Password reset successful"}), 200
    return jsonify({"error": "Invalid token"}), 400

if __name__ == '__main__':
    app.run(debug=True)


    
    # Vulnerability: This function does not check the username associated with the token
    # It only checks if the token is valid and not expired
   


