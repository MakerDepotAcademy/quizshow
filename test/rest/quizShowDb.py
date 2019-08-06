import datetime
import json
from flask import Flask, request, render_template
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify

db_connect = create_engine('sqlite:///quizShow.db')
app = Flask(__name__, template_folder="templates")
api = Api(app)

@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5002/

    :return:        the rendered template 'index.html'
    """
    return render_template('index.html')

class StartGame(Resource):
    def start():
        return render_template('start.html')

    def get(self):
        r = {'game': 'Quiz Show',
            'status': 'Started',
            'time': datetime.datetime.utcnow(),
            'teamID': 6,
            'teamName': "Bad Dogs"}
        return jsonify(r)

    def post(self):
        if request.headers['Content-Type'] == 'application/json':
            data = json.dumps(request.json)
            game = request.json['game']
            teamID = request.json['teamID']
            teamName = request.json['teamName']
            return "Message: " + json.dumps(request.json)
        else:
            return "Unsupported Message Type"

class EndGame(Resource):
    def end():
        return render_template('endGame.html')

    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from name_that_movie")
        result = {'name_that_movie': [dict(zip(tuple(query.keys()), i))
                                      for i in query.cursor]}
        return jsonify(result)

    def post(self):
        if request.headers['Content-Type'] == 'application/json':
            data = json.dumps(request.json)
            game = request.json['game']
            teamID = request.json['teamID']
            teamName = request.json['teamName']
            return "Message: " + json.dumps(request.json)
        else:
            return "Unsupported Message Type"

class Reset(Resource):
    def reset():
        return render_template('reset.html')

    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from name_that_movie")
        result = {'name_that_movie': [dict(zip(tuple(query.keys()), i))
                                      for i in query.cursor]}
        return jsonify(result)

    def post(self):
        if request.headers['Content-Type'] == 'application/json':
            data = json.dumps(request.json)
            game = request.json['game']
            teamID = request.json['teamID']
            teamName = request.json['teamName']
            return "Message: " + json.dumps(request.json)
        else:
            return "Unsupported Message Type"

class Pause(Resource):
    def pause():
        return render_template('pause.html')

    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from name_that_movie")
        result = {'name_that_movie': [dict(zip(tuple(query.keys()), i))
                                      for i in query.cursor]}
        return jsonify(result)

    def post(self):
        if request.headers['Content-Type'] == 'application/json':
            data = json.dumps(request.json)
            game = request.json['game']
            teamID = request.json['teamID']
            teamName = request.json['teamName']
            return "Message: " + json.dumps(request.json)
        else:
            return "Unsupported Message Type"

class Resume(Resource):
    def start():
        return render_template('resume.html')

    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from name_that_movie")
        result = {'name_that_movie': [dict(zip(tuple(query.keys()), i))
                                      for i in query.cursor]}
        return jsonify(result)

    def post(self):
        if request.headers['Content-Type'] == 'application/json':
            data = json.dumps(request.json)
            game = request.json['game']
            teamID = request.json['teamID']
            teamName = request.json['teamName']
            return "Message: " + json.dumps(request.json)
        else:
            return "Unsupported Message Type"

class Score(Resource):
    def score():
        return render_template('score.html')

    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from name_that_movie")
        result = {'name_that_movie': [dict(zip(tuple(query.keys()), i))
                                      for i in query.cursor]}
        return jsonify(result)

class DataDump(Resource):
    def dataDump():
        return render_template('dataDump.html')

    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from name_that_movie")
        result = {'name_that_movie': [dict(zip(tuple(query.keys()), i))
                                      for i in query.cursor]}
        return jsonify(result)

class GoTimeTrivia(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from go_time_trivia")
        return {'go_time_trivia': [i[0] for i in query.cursor.fetchall()]}

class GoTimeTriviaQuestion(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute('''SELECT
                g.rowid,
                g.QUESTION,
                g.yellow,
                g.green,
                g.red,
                g.blue,
                g.correct_answer
            FROM
                go_time_trivia AS g
            WHERE
                g.has_been_used = 0
            ORDER BY
                RANDOM() ASC
            LIMIT 1
        ''')
        result = {'trivia_question': [dict(zip(tuple(query.keys()), i))
                           for i in query.cursor]}
        return jsonify(result)

class NameThatMovie(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from name_that_movie")
        result = {'name_that_movie': [dict(zip(tuple(query.keys()), i))
                                      for i in query.cursor]}
        return jsonify(result)

class NameThatTune(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select * from name_that_tune")
        result = {'name_that_tune': [dict(zip(tuple(query.keys()), i))
                                      for i in query.cursor]}
        return jsonify(result)

api.add_resource(GoTimeTrivia, '/GoTimeTrivia')
api.add_resource(StartGame, '/GoTimeTrivia/StartGame')
api.add_resource(EndGame, '/GoTimeTrivia/EndGame')
api.add_resource(Reset, '/GoTimeTrivia/Reset')
api.add_resource(Pause, '/GoTimeTrivia/Pause')
api.add_resource(Resume, '/GoTimeTrivia/Resume')
api.add_resource(Score, '/GoTimeTrivia/Score')

api.add_resource(NameThatMovie, '/NameThatMovie')
api.add_resource(NameThatTune, '/NameThatTune')
api.add_resource(GoTimeTriviaQuestion, '/GoTimeTrivia/GetQuestion')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port='5002')
