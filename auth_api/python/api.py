import jwt
import hashlib

import mysql.connector
from flask import Flask
from flask import jsonify
from flask import request
from methods import Token, Restricted

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Ly8w3wjd7yXF64FiADFnxNs1ouPrGauB'

login = Token()
protected = Restricted()


cnx = mysql.connector.connect(user='secret', password='jOdznoyH6swQB9sTGdLUeeSrtejWkcw',
                              host='sre-bootcamp-selection-challenge.cabf3yhjqvmq.us-east-1.rds.amazonaws.com',
                              database='bootcamp_tht')
cursor = cnx.cursor()


# Just a health check
@app.route("/")
def url_root():
    return "OK"


# Just a health check
@app.route("/_health")
def url_health():
    return "OK"


# e.g. http://127.0.0.1:8000/login
@app.route("/login", methods=['POST'])
def url_login():
    username = request.form['username']
    password = request.form['password']
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    if result is None:
        return jsonify({"error": "Invalid username or password"}), 403
    stored_password = result[1]
    salt = result[2]
    hashed_password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
    if stored_password != hashed_password:
        return jsonify({"error": "Invalid username or password"}), 403

    res = {
        "data": login.generate_token(username, password)
    }

    return jsonify(res)


# # e.g. http://127.0.0.1:8000/protected
@app.route("/protected")
def url_protected():
    auth_token = request.headers.get('Authorization')
    if not auth_token:
        return jsonify({"error": "Token is missing"}), 401
    try:
        res = {
            "data": protected.access_data(auth_token)
        }
        return jsonify(res)

    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
