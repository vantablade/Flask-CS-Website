# Paper 2 Python: IGCSE Computer Science revision site

A Flask site for Pearson Edexcel International GCSE Computer Science (4CP0) **Paper 2**.
Every lesson has editable Python examples that run in the browser, plus quizzes and auto-checked coding challenges.

## Run it

```
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000.

## How it works

- `app.py`: Flask routes (home, `/paper-2`, `/playground`, `/topic/<slug>`).
- `content.py`: **all lesson content**: topics, sections, code examples, quizzes and challenges with tests.
  To add a topic, add a dict to `TOPICS`.
- `exam_questions.py`: the exam-style question library (amend, fix, complete, rearrange, write, and extended
  15–20 mark programs). Each question has tests, a model answer and a mark scheme. A question with `lesson` set also
  appears inside that lesson. These are original questions, not Pearson past-paper questions.
- `static/py/runner.py`: loaded into [Pyodide](https://pyodide.org) (Python compiled to WebAssembly) in the browser.
  It runs student code, sends `input()` to a browser prompt, labels errors as syntax or runtime, and stops
  infinite loops after 5 seconds. Student code never runs on the server.
- `static/js/site.js`: CodeMirror editors, the run and check buttons, quizzes, and progress saved in `localStorage`.

The first run downloads Pyodide (~10 MB) from a CDN, so it needs an internet connection. After that the browser caches it.

Don't name any file `flask.py`: Python would import it instead of the real Flask package.
