from flask import Flask, request, jsonify , render_template, redirect
from werkzeug import datastructures
from pymongo import MongoClient
import os, json, redis 

# App
application = Flask(__name__)

# connect to MongoDB
mongoClient = MongoClient('mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_AUTHDB'])
db = mongoClient[os.environ['MONGODB_DATABASE']]

# connect to Redis
redisClient = redis.Redis(host=os.environ.get("REDIS_HOST", "localhost"), port=os.environ.get("REDIS_PORT", 6379), db=os.environ.get("REDIS_DB", 0))


@application.route('/', methods=['GET','POST'])
def game():
    guessing_game = db.GuessingGame.find_one()
    if request.method == "POST":
        game = db.GuessingGame.find()
        for ele in game:
            if len(ele['Game_Answer']) != 4:
                db.GuessingGame.update({}, {"$addToSet": {"Game_Answer": request.form['submit'] }} )
        return redirect("/")
    elif request.method == "GET":
        return render_template('index.html',title="Alphabet Guessing Game v1.0", guessing_game=guessing_game)

@application.route('/start_game', methods=['GET','POST'])
def start_game():
    guessing_game = db.GuessingGame.find_one()
    if request.method == "GET":
        return render_template('start.html',title="Alphabet Guessing Game v1.0", guessing_game=guessing_game)
    elif request.method == "POST":
        game = db.GuessingGame.find()
        for ele in game:
            while request.form["submit"] != ele["Game_Answer"][0] and ele["Game_Answer"][0] != ele["Player_Answer_Correct"][0]:
                db.GuessingGame.update({}, {"$inc": {"Count_Answer": 1}})
                return redirect('/start_game')
            db.GuessingGame.update({}, {"$set": {"Player_Answer_Correct.0": ele["Game_Answer"][0]}})
            while request.form["submit"] != ele["Game_Answer"][1] and ele["Game_Answer"][1] != ele["Player_Answer_Correct"][1]:
                db.GuessingGame.update({}, {"$inc": {"Count_Answer": 1}})
                return redirect('/start_game')
            db.GuessingGame.update({}, {"$set": {"Player_Answer_Correct.1": ele["Game_Answer"][1]}})
            while request.form["submit"] != ele["Game_Answer"][2] and ele["Game_Answer"][2] != ele["Player_Answer_Correct"][2]:
                db.GuessingGame.update({}, {"$inc": {"Count_Answer": 1}})
                return redirect('/start_game')
            db.GuessingGame.update({}, {"$set": {"Player_Answer_Correct.2": ele["Game_Answer"][2]}})
            while(request.form["submit"] != ele["Game_Answer"][3]) and ele["Game_Answer"][3] != ele["Player_Answer_Correct"][3]:
                db.GuessingGame.update({}, {"$inc": {"Count_Answer": 1}})
                return redirect('/start_game')
            db.GuessingGame.update({}, {"$set": {"Player_Answer_Correct.3": ele["Game_Answer"][3]}})
            db.GuessingGame.update({}, {"$set": {"Total_Count":ele["Count_Answer"] -4}})
        return redirect('/start_game')



if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("FLASK_DEBUG", True)
    ENVIRONMENT_PORT = os.environ.get("FLASK_PORT", 5000)
    application.run(host='0.0.0.0', port=ENVIRONMENT_PORT, debug=ENVIRONMENT_DEBUG)