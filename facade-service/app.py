from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = b'\x07n\x91\\1+H\x1fK\x08U1U\xc2}:t\xda{\xd3\xbc\t\x94\x7f' 