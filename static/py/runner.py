# Loaded into Pyodide in the browser. Runs student code in a fresh namespace,
# captures output, feeds input() and classifies errors (syntax / runtime / timeout).
import builtins
import json
import linecache
import sys
import time
import traceback

import js

TIME_LIMIT = 5.0          # seconds of CPU time (time waiting for input is not counted)
OUTPUT_LIMIT = 200_000    # characters

SEED_FILES = {
    "students.csv": "Amira,72\nBen,58\nChen,91\nDara,64\nEli,85\n",
    "scores.txt": "12\n45\n33\n27\n",
    "products.csv": "P01,Pencil,120,50\nP02,Ruler,30,40\nP03,Eraser,15,25\nP04,Notebook,200,60\nP05,Glue stick,8,20\n",
    "rainfall.txt": "Jan,78\nFeb,61\nMar,55\nApr,49\nMay,52\nJun,40\nJul,35\nAug,48\nSep,57\nOct,83\nNov,90\nDec,85\n",
}

_state = {"start": 0.0, "events": 0, "chars": 0}


# BaseException so a student's `except Exception:` can't swallow them
class ProgramTimeout(BaseException):
    pass


class OutputLimit(BaseException):
    pass


class _Stream:
    def __init__(self, write, kind):
        self._write = write
        self._kind = kind

    def write(self, text):
        if text:
            _state["chars"] += len(text)
            if _state["chars"] > OUTPUT_LIMIT:
                raise OutputLimit("Too much output - is a loop printing forever?")
            self._write(text, self._kind)
        return len(text)

    def flush(self):
        pass


def _tracer(frame, event, arg):
    _state["events"] += 1
    if _state["events"] % 500 == 0 and time.time() - _state["start"] > TIME_LIMIT:
        raise ProgramTimeout(f"Program ran for more than {TIME_LIMIT:g} seconds - is there an infinite loop?")
    return _tracer


def _make_input(write, queue):
    def _input(prompt=""):
        prompt = str(prompt)
        if prompt:
            sys.stdout.write(prompt)
        if queue is not None:
            if not queue:
                raise EOFError("The test ran out of input values - your program called input() more times than expected")
            value = str(queue.pop(0))
        else:
            value = js.askInput(prompt)
            if value is None:
                raise KeyboardInterrupt
            value = str(value)
        write(value + "\n", "in")
        _state["start"] = time.time()   # don't count time spent typing
        return value
    return _input


def reset_seed_files():
    for name, text in SEED_FILES.items():
        with open(name, "w") as f:
            f.write(text)


def _format_runtime_error(exc):
    frames = [f for f in traceback.extract_tb(exc.__traceback__) if f.filename == "main.py"]
    text = "Traceback (most recent call last):\n"
    text += "".join(traceback.StackSummary.from_list(frames).format())
    text += "".join(traceback.format_exception_only(type(exc), exc))
    return text


def run_user(src, write, inputs_json=""):
    """Run src as main.py. Returns 'ok', 'syntax:Name', 'runtime:Name', 'timeout' or 'cancelled'."""
    queue = json.loads(inputs_json) if inputs_json else None
    reset_seed_files()
    linecache.cache["main.py"] = (len(src), None, src.splitlines(True), "main.py")

    saved = (sys.stdout, sys.stderr, builtins.input)
    sys.stdout = _Stream(write, "out")
    sys.stderr = _Stream(write, "err")
    builtins.input = _make_input(write, queue)
    _state.update(start=time.time(), events=0, chars=0)

    try:
        try:
            compiled = compile(src, "main.py", "exec")
        except SyntaxError as exc:
            write("".join(traceback.format_exception_only(type(exc), exc)), "err")
            return "syntax:" + type(exc).__name__

        namespace = {"__name__": "__main__", "__builtins__": builtins}
        sys.settrace(_tracer)
        try:
            exec(compiled, namespace)
        finally:
            sys.settrace(None)
        return "ok"
    except (ProgramTimeout, OutputLimit) as exc:
        write("\n" + str(exc) + "\n", "err")
        return "timeout"
    except KeyboardInterrupt:
        write("\nInput cancelled - program stopped.\n", "err")
        return "cancelled"
    except SystemExit:
        return "ok"
    except BaseException as exc:
        write(_format_runtime_error(exc), "err")
        return "runtime:" + type(exc).__name__
    finally:
        sys.settrace(None)
        sys.stdout, sys.stderr, builtins.input = saved


reset_seed_files()
