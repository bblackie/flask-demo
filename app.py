# app.py
'''
Import at the top of the file to avoid circular imports
'''
from flask import Flask
from flask import g
import sqlite3

app = Flask(__name__)



@app.route("/")
def home():




if __name__ == "__main__":
    app.run(debug=True)