from flask import Flask, request, jsonify
import requests


app = Flask(__name__)

@app.route('/fetch', methods=['POST'])
def fetch():
    data = request.get_json() or request.form
    url = data.get('url')  # user controls this — the vulnerability
    response = requests.get(url, timeout=5)
    
    # Return the fetched data so the attacker can see the internal response
    return response.text, response.status_code

if __name__ == '__main__':
    app.run(port=5002)

