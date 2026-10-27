"""Edexcel IGCSE Computer Science (4CP0) Paper 2 revision site.

Run with:  python app.py   then open http://127.0.0.1:5000
All Python examples run in the visitor's browser (Pyodide), never on the server.
"""
from flask import Flask, abort, render_template

from content import GROUPS, PAPER2_EXAMPLE, PLAYGROUND_EXAMPLES, TOPICS, get_topic

app = Flask(__name__)


@app.context_processor
def inject_topics():
    return {"all_topics": TOPICS, "groups": GROUPS}


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
    return render_template("topic.html", topic=current,
                           prev_topic=prev_topic, next_topic=next_topic)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
