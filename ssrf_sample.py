from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/admin')
def admin():
    return jsonify({
        "secret": "admin_password_123",
        "users": ["wiener", "carlos", "administrator"]
    }), 200

@app.route('/sample')
def sample():
    return jsonify({
        "secret": "we do not belive in you",
        "users": ["wiener", "carlos", "administrator"]
    }), 200
if __name__ == '__main__':
    app.run(port=5001)