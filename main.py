from random import randint
from flask import Flask, redirect, url_for, request, render_template
import db
import socket

app = Flask(__name__)

quiz_id = 0
question_id = 0
score = 0

def index():
    global quiz_id, question_id, score
    if request.method == "GET":
        question_id = 0
        score = 0

        return render_template("index.html", questions=db.get_quizes())
    
    if request.method == "POST":
        quiz_id = request.form.get("quiz")
        return redirect(url_for("test"))


def test():
    global question_id, score
    try:
        question = db.get_questions(quiz_id)[question_id]
    except IndexError:
        return redirect(url_for("result"))
    

    if request.method == "GET":
        return render_template("test.html", question=question)

    if request.method == "POST":
        question_id += 1
        user_answer = request.form.get("answer")
        if user_answer == question[1]:
            score += 1
            text = "Правильно"
        else:
            score -= 1
            text = "Неправильно"

        return render_template("test.html", text_result = text)
        

def result():
    global score
    return render_template("result.html", text_score=score)

app.add_url_rule("/", "index", index, methods=["GET", "POST"])
app.add_url_rule("/test", "test", test, methods=["GET", "POST"])
app.add_url_rule("/result", "result", result)


local_ip = socket.gethostbyname( socket.gethostname() )

app.run(debug=True, host=local_ip, port=5000)