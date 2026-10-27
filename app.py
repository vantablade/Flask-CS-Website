"""Edexcel IGCSE Computer Science (4CP0) Paper 2 revision site.

Run with:  python app.py   then open http://127.0.0.1:5000
All Python examples run in the visitor's browser (Pyodide), never on the server.
"""
from flask import Flask, abort, render_template

from content import GROUPS, PAPER2_EXAMPLE, PLAYGROUND_EXAMPLES, TOPICS, get_topic
from exam_questions import QUESTIONS, TYPES, get_question

app = Flask(__name__)

TOPIC_TITLES = {t["slug"]: t["title"] for t in TOPICS}


@app.context_processor
def inject_globals():
    return {"all_topics": TOPICS, "groups": GROUPS, "question_types": TYPES,
            "topic_titles": TOPIC_TITLES, "question_count": len(QUESTIONS)}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/paper-2")
def paper2():
    return render_template("paper2.html", example=PAPER2_EXAMPLE)


@app.route("/playground")
def playground():
    return render_template("playground.html", examples=PLAYGROUND_EXAMPLES)


@app.route("/topic/<slug>")
def topic(slug):
    current = get_topic(slug)
    if current is None:
        abort(404)
    i = TOPICS.index(current)
    prev_topic = TOPICS[i - 1] if i > 0 else None
    next_topic = TOPICS[i + 1] if i < len(TOPICS) - 1 else None
    inline_questions = [q for q in QUESTIONS if q["lesson"] == slug]
    related_questions = [q for q in QUESTIONS if slug in q["topics"] and q["lesson"] != slug]
    return render_template("topic.html", topic=current,
                           prev_topic=prev_topic, next_topic=next_topic,
                           inline_questions=inline_questions,
                           related_questions=related_questions)


@app.route("/exam-questions")
def exam_library():
    return render_template("exam_library.html", questions=QUESTIONS,
                           total_marks=sum(q["marks"] for q in QUESTIONS))


@app.route("/exam-questions/<qid>")
def exam_question(qid):
    question = get_question(qid)
    if question is None:
        abort(404)
    i = QUESTIONS.index(question)
    prev_q = QUESTIONS[i - 1] if i > 0 else None
    next_q = QUESTIONS[i + 1] if i < len(QUESTIONS) - 1 else None
    return render_template("exam_question.html", q=question, prev_q=prev_q, next_q=next_q)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
