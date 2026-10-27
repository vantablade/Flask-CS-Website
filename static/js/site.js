// Browser-side Python runner (Pyodide), code editors, challenges, quizzes and progress.
(function () {
  "use strict";

  const PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/";
  const PROGRESS_KEY = "igcse-cs-p2-progress";

  // ---------------------------------------------------------------- progress
  function loadProgress() {
    try { return JSON.parse(localStorage.getItem(PROGRESS_KEY)) || {}; }
    catch (e) { return {}; }
  }
  function saveProgress(p) {
    try { localStorage.setItem(PROGRESS_KEY, JSON.stringify(p)); } catch (e) { /* storage blocked */ }
  }
  function recordProgress(slug, key, value) {
    const p = loadProgress();
    p[slug] = p[slug] || {};
    p[slug][key] = value;
    saveProgress(p);
  }

  // ----------------------------------------------------------------- pyodide
  const statusEl = document.getElementById("py-status");
  function setStatus(state, text) {
    if (!statusEl) return;
    statusEl.dataset.state = state;
    statusEl.querySelector("span").textContent = text;
  }

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = src;
      s.onload = resolve;
      s.onerror = () => reject(new Error("Could not load " + src));
      document.head.appendChild(s);
    });
  }

  let pyPromise = null;
  function loadPython() {
    if (!pyPromise) {
      setStatus("loading", "Loading Python…");
      pyPromise = (async () => {
        await loadScript(PYODIDE_URL + "pyodide.js");
        const py = await window.loadPyodide({ indexURL: PYODIDE_URL });
        const src = await (await fetch(window.SITE.runnerUrl)).text();
        py.runPython(src);
        setStatus("ready", "Python 3 ready");
        return py;
      })().catch((err) => {
        pyPromise = null;
        setStatus("error", "Python failed to load");
        throw err;
      });
    }
    return pyPromise;
  }

  // input() uses a browser prompt showing the last few lines of output
  let recentOutput = "";
  window.askInput = function (promptText) {
    const tail = recentOutput.split("\n").slice(-8).join("\n");
    const value = window.prompt(tail.trim() ? tail : (promptText || "Input:"), "");
    return value === null ? undefined : value;
  };

  function appendOutput(pre, text, kind) {
    const last = pre.lastChild;
    if (last && last.dataset && last.dataset.kind === kind) {
      last.textContent += text;
    } else {
      const span = document.createElement("span");
      span.className = "o-" + kind;
      span.dataset.kind = kind;
      span.textContent = text;
      pre.appendChild(span);
    }
  }

  async function runPython(src, pre, inputs) {
    const py = await loadPython();
    pre.textContent = "";
    recentOutput = "";
    let plain = "";
    const write = (text, kind) => {
      recentOutput += text;
      if (kind !== "err") plain += text;
      appendOutput(pre, text, kind);
    };
    const runUser = py.globals.get("run_user");
    try {
      const status = runUser(src, write, inputs ? JSON.stringify(inputs) : "");
      return { status: String(status), output: plain };
    } finally {
      runUser.destroy();
    }
  }

  // --------------------------------------------------------- error messages
  const ERROR_HINTS = {
    SyntaxError: "Check for a missing colon, bracket or quote, or = used where == was meant.",
    IndentationError: "The indentation (spaces at the start of the line) is wrong or inconsistent.",
    TabError: "Tabs and spaces are mixed. Use 4 spaces.",
    NameError: "A variable or function is used before it exists. Check the spelling.",
    TypeError: "An operation was used on the wrong data type, e.g. \"text\" + 5. Convert with str() or int().",
    ValueError: "The value can't be converted, e.g. int(\"abc\"). Validate input first.",
    ZeroDivisionError: "The program divided by zero.",
    IndexError: "A list or string index doesn't exist. Indexes run from 0 to len - 1.",
    KeyError: "That key isn't in the dictionary.",
    AttributeError: "That method doesn't exist for this data type. Check the spelling.",
    FileNotFoundError: "The file doesn't exist. Check the name. Only students.csv and scores.txt are built in.",
    EOFError: "The program asked for more input than was provided.",
    RecursionError: "A function kept calling itself with no stopping case.",
  };

  function describeStatus(status) {
    const [kind, name] = status.split(":");
    switch (kind) {
      case "ok":
        return { cls: "ok", label: "✓ Program finished", text: "" };
      case "syntax":
        return { cls: "syntax", label: "Syntax error",
          text: "<strong>Syntax error:</strong> the code breaks Python's grammar rules, so it couldn't start at all. " +
                (ERROR_HINTS[name] || "") };
      case "runtime":
        return { cls: "runtime", label: "Runtime error · " + name,
          text: "<strong>Runtime error (" + name + "):</strong> the program started but crashed while running. " +
                (ERROR_HINTS[name] || "Read the last line of the message for details.") };
      case "timeout":
        return { cls: "runtime", label: "Stopped", text: "Stopped automatically. Check that your loop condition eventually becomes False." };
      default:
        return { cls: "muted", label: "Cancelled", text: "" };
    }
  }

  const nextFrame = () => new Promise((r) => setTimeout(r, 30));

  // ------------------------------------------------------------- editors
  function makeEditor(textarea, opts) {
    const runKey = () => opts.onRun && opts.onRun();
    return window.CodeMirror.fromTextArea(textarea, Object.assign({
      mode: "python",
      lineNumbers: true,
      indentUnit: 4,
      tabSize: 4,
      matchBrackets: true,
      viewportMargin: Infinity,
      extraKeys: {
        Tab: (cm) => cm.somethingSelected() ? cm.indentSelection("add") : cm.replaceSelection("    ", "end"),
        "Shift-Tab": (cm) => cm.indentSelection("subtract"),
        "Ctrl-Enter": runKey,
        "Cmd-Enter": runKey,
      },
    }, opts.cm || {}));
  }

  function initRunner(el) {
    const textarea = el.querySelector("textarea");
    const original = textarea.value;
    const outBox = el.querySelector(".runner-out");
    const pre = outBox.querySelector("pre");
    const badge = outBox.querySelector(".badge");
    const explain = outBox.querySelector(".explain");
    const runBtn = el.querySelector("[data-action=run]");

    let busy = false;
    async function run() {
      if (busy) return;
      busy = true;
      runBtn.disabled = true;
      const label = runBtn.innerHTML;
      runBtn.textContent = pyPromise ? "Running…" : "Loading Python…";
      outBox.hidden = false;
      badge.className = "badge muted";
      badge.textContent = "running";
      explain.innerHTML = "";
      await nextFrame();
      try {
        const result = await runPython(editor.getValue(), pre);
        const d = describeStatus(result.status);
        badge.className = "badge " + d.cls;
        badge.textContent = d.label;
        explain.innerHTML = d.text;
        if (!pre.textContent) pre.innerHTML = '<span class="o-muted">(no output)</span>';
      } catch (err) {
        badge.className = "badge runtime";
        badge.textContent = "Error";
        pre.textContent = "Could not start Python in this browser. Check your internet connection and refresh.\n" + err;
      } finally {
        busy = false;
        runBtn.disabled = false;
        runBtn.innerHTML = label;
      }
    }

    const editor = makeEditor(textarea, { onRun: run, cm: el.dataset.height ? { viewportMargin: 10 } : {} });
    if (el.dataset.height) editor.setSize(null, el.dataset.height);

    runBtn.addEventListener("click", run);
    const resetBtn = el.querySelector("[data-action=reset]");
    if (resetBtn) resetBtn.addEventListener("click", () => {
      editor.setValue(original);
      outBox.hidden = true;
    });
    const clearBtn = el.querySelector("[data-action=clear]");
    if (clearBtn) clearBtn.addEventListener("click", () => { outBox.hidden = true; pre.textContent = ""; });

    el._editor = editor;
    if (el.dataset.challenge !== undefined) initChallenge(el, editor);
  }

  // ---------------------------------------------------------- challenges
  function initChallenge(el, editor) {
    const tests = JSON.parse(el.dataset.tests || "[]");
    const solution = JSON.parse(el.querySelector("script.solution").textContent);
    const results = el.querySelector(".check-results");
    const checkBtn = el.querySelector("[data-action=check]");
    const slug = el.dataset.progressSlug || document.body.dataset.slug;
    const id = el.dataset.challenge;

    el.querySelector("[data-action=solution]").addEventListener("click", () => {
      if (confirm("Replace your code with the model answer? Have a proper go yourself first!")) editor.setValue(solution);
    });

    checkBtn.addEventListener("click", async () => {
      checkBtn.disabled = true;
      checkBtn.textContent = "Checking…";
      results.hidden = false;
      results.innerHTML = '<p class="muted">Running tests…</p>';
      await nextFrame();
      const rows = [];
      let passed = 0;
      try {
        for (let i = 0; i < tests.length; i++) {
          const t = tests[i];
          const scratch = document.createElement("pre");
          const r = await runPython(editor.getValue(), scratch, t.inputs);
          const out = r.output.toLowerCase();
          const ok = r.status === "ok" && t.expect.every((e) => out.includes(e.toLowerCase())) &&
            !(t.reject || []).some((e) => out.includes(e.toLowerCase()));
          if (ok) passed++;
          rows.push({ t, ok, r, scratch });
          if (r.status.startsWith("syntax")) break;   // no point running the rest
        }
      } catch (err) {
        results.innerHTML = '<p class="fail">Python could not load: ' + escapeHtml(String(err)) + "</p>";
        checkBtn.disabled = false;
        checkBtn.textContent = "Check my code";
        return;
      }
      const all = passed === tests.length;
      let html = '<p class="' + (all ? "pass" : "fail") + '"><strong>' +
        (all ? "🎉 All " + tests.length + " tests passed!" : passed + " of " + tests.length + " tests passed") + "</strong></p><ol>";
      rows.forEach(({ t, ok, r, scratch }) => {
        const inputs = t.inputs.length ? "inputs " + t.inputs.map((v) => "<code>" + escapeHtml(JSON.stringify(v)) + "</code>").join(", ") : "no input";
        const show = (list) => list.map((e) => "<code>" + escapeHtml(e).replace(/\n/g, "↵") + "</code>").join(" and ");
        html += '<li class="' + (ok ? "pass" : "fail") + '">' + (ok ? "✓ " : "✗ ") +
          (t.label ? '<span class="tlabel">' + escapeHtml(t.label) + "</span> " : "") + inputs +
          ": expected output containing " + show(t.expect) +
          (t.reject && t.reject.length ? ", and not " + show(t.reject) : "");
        if (!ok) {
          const d = describeStatus(r.status);
          if (r.status !== "ok") html += ' <span class="badge ' + d.cls + '">' + escapeHtml(d.label) + "</span>";
          html += '<pre class="mini">' + scratch.innerHTML + "</pre>";
        }
        html += "</li>";
      });
      html += "</ol>";
      results.innerHTML = html;
      if (all) {
        const done = (loadProgress()[slug] || {}).challenges || [];
        if (!done.includes(id)) done.push(id);
        recordProgress(slug, "challenges", done);
        el.classList.add("solved");
      }
      checkBtn.disabled = false;
      checkBtn.textContent = "Check my code";
    });

    const done = (loadProgress()[slug] || {}).challenges || [];
    if (done.includes(id)) el.classList.add("solved");
  }

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  // ---------------------------------------------------------------- quiz
  function initQuiz(quiz) {
    const questions = quiz.querySelectorAll(".q");
    const scoreEl = quiz.querySelector(".quiz-score");
    let answered = 0, correct = 0;
    questions.forEach((q) => {
      const answer = Number(q.dataset.answer);
      q.querySelectorAll(".opt").forEach((btn, i) => {
        btn.addEventListener("click", () => {
          if (q.classList.contains("done")) return;
          q.classList.add("done");
          answered++;
          if (i === answer) correct++;
          btn.classList.add(i === answer ? "right" : "wrong");
          q.querySelectorAll(".opt")[answer].classList.add("right");
          q.querySelector(".why").hidden = false;
          scoreEl.textContent = "Score: " + correct + " / " + questions.length;
          if (answered === questions.length) {
            const slug = document.body.dataset.slug;
            const best = (loadProgress()[slug] || {}).quiz || 0;
            recordProgress(slug, "quiz", Math.max(best, correct));
            recordProgress(slug, "quizTotal", questions.length);
          }
        });
      });
    });
    quiz.querySelector("[data-action=retry]").addEventListener("click", () => {
      answered = 0; correct = 0;
      scoreEl.textContent = "";
      questions.forEach((q) => {
        q.classList.remove("done");
        q.querySelector(".why").hidden = true;
        q.querySelectorAll(".opt").forEach((b) => b.classList.remove("right", "wrong"));
      });
    });
  }

  // ------------------------------------------------------ mark schemes
  function initMarkScheme(box) {
    const qid = box.dataset.qid;
    const total = Number(box.dataset.total);
    const boxes = Array.from(box.querySelectorAll("input[type=checkbox]"));
    const nowEl = box.querySelector(".ms-now");
    const summaryScore = box.querySelector(".ms-score");
    const saved = ((loadProgress().exam || {}).ticks || {})[qid] || [];
    boxes.forEach((b, i) => { b.checked = saved.includes(i); });

    function update(save) {
      const mark = boxes.reduce((sum, b) => sum + (b.checked ? Number(b.dataset.marks) : 0), 0);
      nowEl.textContent = mark;
      summaryScore.textContent = boxes.some((b) => b.checked) ? "· " + mark + " / " + total : "";
      if (!save) return;
      const exam = loadProgress().exam || {};
      exam.ticks = exam.ticks || {};
      exam.marks = exam.marks || {};
      exam.ticks[qid] = boxes.map((b, i) => (b.checked ? i : -1)).filter((i) => i >= 0);
      exam.marks[qid] = mark;
      recordProgress("exam", "ticks", exam.ticks);
      recordProgress("exam", "marks", exam.marks);
    }
    boxes.forEach((b) => b.addEventListener("change", () => update(true)));
    box.querySelector("[data-action=ms-clear]").addEventListener("click", () => {
      boxes.forEach((b) => { b.checked = false; });
      update(true);
    });
    update(false);
  }

  // ------------------------------------------------- question library
  function showQuestionStatus() {
    const exam = loadProgress().exam || {};
    const solved = exam.challenges || [];
    const marks = exam.marks || {};
    document.querySelectorAll(".qcard").forEach((card) => {
      const qid = card.dataset.qid;
      const bits = [];
      if (solved.includes(qid)) bits.push("✓ Tests passed");
      if (marks[qid] !== undefined && marks[qid] > 0) bits.push("Self-marked " + marks[qid] + "/" + card.dataset.marks);
      const el = card.querySelector(".qstatus");
      if (bits.length) { el.textContent = bits.join(" · "); el.hidden = false; card.classList.add("attempted"); }
    });
    const summary = document.getElementById("library-summary");
    if (summary) {
      const cards = document.querySelectorAll(".qcard");
      const done = Array.from(cards).filter((c) => solved.includes(c.dataset.qid)).length;
      let got = 0, possible = 0;
      cards.forEach((c) => {
        if (marks[c.dataset.qid] !== undefined) { got += marks[c.dataset.qid]; possible += Number(c.dataset.marks); }
      });
      summary.textContent = "Tests passed on " + done + " of " + cards.length + " questions" +
        (possible ? " · self-marked " + got + " / " + possible + " marks on the questions you've marked" : "");
    }
  }

  function initLibrary() {
    const list = document.getElementById("question-list");
    if (!list) return;
    const state = { type: "", marks: "", topic: "" };
    const apply = () => {
      let shown = 0;
      list.querySelectorAll(".qcard").forEach((card) => {
        const m = Number(card.dataset.marks);
        const [lo, hi] = state.marks ? state.marks.split("-").map(Number) : [0, 999];
        const ok = (!state.type || card.dataset.type === state.type) &&
          m >= lo && m <= hi &&
          (!state.topic || card.dataset.topics.split(" ").includes(state.topic));
        card.hidden = !ok;
        if (ok) shown++;
      });
      document.getElementById("no-results").hidden = shown > 0;
    };
    document.querySelectorAll(".fgroup[data-filter]").forEach((group) => {
      group.querySelectorAll(".chip").forEach((chip) => chip.addEventListener("click", () => {
        group.querySelectorAll(".chip").forEach((c) => c.classList.remove("on"));
        chip.classList.add("on");
        state[group.dataset.filter] = chip.dataset.value;
        apply();
      }));
    });
    document.getElementById("topic-filter").addEventListener("change", (e) => { state.topic = e.target.value; apply(); });
  }

  // ------------------------------------------------------- index progress
  function showProgress() {
    const p = loadProgress();
    document.querySelectorAll("[data-topic-progress]").forEach((el) => {
      const t = p[el.dataset.topicProgress];
      if (!t) return;
      const bits = [];
      if (t.quizTotal) bits.push("Quiz " + t.quiz + "/" + t.quizTotal);
      if (t.challenges && t.challenges.length) bits.push(t.challenges.length + " solved");
      if (bits.length) {
        el.textContent = bits.join(" · ");
        el.hidden = false;
      }
    });
  }

  // --------------------------------------------------------- playground
  function initPlayground() {
    const select = document.getElementById("example-select");
    if (!select) return;
    const runner = document.querySelector(".playground [data-runner]");
    const examples = JSON.parse(document.getElementById("examples-data").textContent);
    select.addEventListener("change", () => {
      runner._editor.setValue(examples[select.value]);
      select.value = "";
    });
  }

  // --------------------------------------------------------------- boot
  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-runner]").forEach(initRunner);
    document.querySelectorAll(".quiz").forEach(initQuiz);
    document.querySelectorAll(".markscheme").forEach(initMarkScheme);
    showProgress();
    showQuestionStatus();
    initLibrary();
    initPlayground();
    const navToggle = document.getElementById("nav-toggle");
    if (navToggle) navToggle.addEventListener("click", () => document.body.classList.toggle("nav-open"));
    // Warm up Python in the background on pages that have code
    if (document.querySelector("[data-runner]")) setTimeout(() => loadPython().catch(() => {}), 800);
  });
})();
