import jwt

from flask import current_app


class Token:
    def __init__(self):
        pass

    @staticmethod
    def generate_token(username, password):
        payload = {
            'username': username,
            'pass': password
        }

        token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        return token


class Restricted:

    @staticmethod
    def access_data(authorization):
        if len(authorization.split(" ")) != 2:
            token = authorization
        else:
            bearer, token = authorization.split(" ")
            if bearer != "Bearer":
                raise Exception("Bad request")

        jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return 'You are under protected data'
