# app.py
'''
Import at the top of the file to avoid circular imports
'''
from flask import Flask
import sqlite3
from flask import g

DATABASE = 'database.db'

app = Flask(__name__)

'''Function to get a database connection. This function will be called whenever we need to interact with the database.'''
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


'''Get the home route to display all the bikes in the database.'''
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


'''Function to query the database and return the results.'''
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

'''Home route to display all the bikes in the database.'''
@app.route("/")
def home():
    
    sql = '''
        SELECT Makers.Name AS Maker, Bikes.Model, Bikes.Cost, Bikes.Description
        FROM Bikes
        JOIN Makers
        ON Bikes.MakerID = Makers.MakerID;
        '''
    results = query_db(sql)
    return str(results)


@app.route("/bikes")
def bikes():
    sql = '''
        SELECT BikeID, Model
        FROM Bikes;
        '''
    results = query_db(sql)
    return str(results)


@app.route("/bikes/<int:bike_id>")
def bike(bike_id):
    sql = '''
        SELECT Makers.Name AS Maker, Bikes.Model, Bikes.Cost, Bikes.Description
        FROM Bikes
        JOIN Makers
        ON Bikes.MakerID = Makers.MakerID
        WHERE Bikes.BikeID = ?;
        '''
    result = query_db(sql, (bike_id,), one=True)
    return str(result) if result else ("Bike not found", 404)


'''Run the Flask app.'''
if __name__ == "__main__":
    app.run(debug=True)