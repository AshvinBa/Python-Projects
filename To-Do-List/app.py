from flask import Flask , render_template , json

with open('config.json','r') as c:
    params = json.load(c)["params"]


local_server = True

app = Flask(__name__)

app.secret_key = 'your_secret_key'






















