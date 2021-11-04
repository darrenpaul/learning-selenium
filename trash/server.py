from modules import instagram_bot
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/api/v1/start-driver')
def start_driver():
    instagram_bot.start()
    return 'Hello, World!'
