"""All lesson content for the site.

Each topic is a dict:
  slug, title, group, spec, summary, icon
  sections:   list of {heading, body (HTML), code (runnable Python or None)}
  exam_tip:   HTML string
  quiz:       list of {q, options, answer (index), explain}
  challenges: list of {title, task, starter, solution, hint, tests}
              tests = [{"inputs": [...], "expect": [...substrings in output]}]
"""
from textwrap import dedent


def code(text):
    return dedent(text).strip("\n") + "\n"


def section(heading, body, example=None):
    return {"heading": heading, "body": body, "code": code(example) if example else None}


GROUPS = {
    "t1": "Topic 1 · Problem solving",
    "t2": "Topic 2 · Programming",
}


TOPICS = [
    # ------------------------------------------------------------------ basics
    {
        "slug": "basics",
        "title": "Variables, data types & I/O",
        "group": "t2",
        "spec": "2.1 · 2.3 · 2.4",
        "summary": "Variables, constants, the five data types, input(), print() and type conversion.",
        "sections": [
            section("Your first program", """
<p>A Python program is a list of instructions run <strong>in sequence</strong>, top to bottom.
<code>print()</code> displays output. Anything after a <code>#</code> is a <strong>comment</strong>,
which Python ignores. Comments are for the humans reading your code, and in Paper 2 you get marks
for making your code readable.</p>
<p>Edit the code below and press <kbd>Run</kbd> (or <kbd>Ctrl</kbd>+<kbd>Enter</kbd>).</p>
""", r'''
# This is a comment - Python ignores it
print("Hello, IGCSE!")
print("Paper 2 is", 3, "hours long")
print("Total marks:", 80)
'''),
            section("Variables and constants", """
<p>A <strong>variable</strong> is a named location in memory that stores a value which can
<em>change</em> while the program runs. You create one with an <strong>assignment</strong>
using <code>=</code>. Giving a variable its first value is called <strong>initialisation</strong>.</p>
<p>A <strong>constant</strong> holds a value that must <em>not</em> change. Python has no special
constant keyword, so by convention we write constants in <code>UPPER_CASE</code>.</p>
<ul>
<li>Use descriptive names like <code>total_price</code>, not <code>tp</code> or <code>x</code>.</li>
<li>Names can't start with a digit or contain spaces, and they are case-sensitive
(<code>Score</code> and <code>score</code> are different variables).</li>
</ul>
""", r'''
VAT_RATE = 0.2        # constant - UPPER_CASE, never changed
price = 50.0          # variable, initialised to 50.0
quantity = 3

total = price * quantity
total = total + total * VAT_RATE   # variables can be re-assigned

print("Total to pay:", total)
'''),
            section("The five data types", """
<p>The specification expects you to know these data types:</p>
<table>
<tr><th>Data type</th><th>Python</th><th>Example</th><th>Use for</th></tr>
<tr><td>Integer</td><td><code>int</code></td><td><code>16</code>, <code>-3</code></td><td>Whole numbers: counts, ages, scores</td></tr>
<tr><td>Real</td><td><code>float</code></td><td><code>1.75</code>, <code>3.0</code></td><td>Numbers with a decimal part: prices, measurements</td></tr>
<tr><td>Boolean</td><td><code>bool</code></td><td><code>True</code>, <code>False</code></td><td>Yes/no values: flags, conditions</td></tr>
<tr><td>Character</td><td><code>str</code> (length 1)</td><td><code>"A"</code></td><td>A single letter or symbol</td></tr>
<tr><td>String</td><td><code>str</code></td><td><code>"Ada"</code></td><td>Text: names, messages</td></tr>
</table>
<p>Python has no separate character type, so a character is just a string of length 1.
<code>type()</code> tells you what type a value is.</p>
""", r'''
age = 16               # integer
height = 1.75          # real (float)
is_student = True      # Boolean
grade = "A"            # character (string of length 1)
name = "Ada Lovelace"  # string

print(type(age))
print(type(height))
print(type(is_student))
print(type(grade))
print(type(name))
'''),
            section("Input and type conversion (casting)", """
<p><code>input()</code> shows a prompt and waits for the user to type something.
<strong><code>input()</code> always returns a string</strong>, even when the user types a number.
To do maths with it, convert (cast) it:</p>
<ul>
<li><code>int("42")</code> gives <code>42</code></li>
<li><code>float("3.5")</code> gives <code>3.5</code></li>
<li><code>str(42)</code> gives <code>"42"</code>, which you need when joining a number onto a string with <code>+</code></li>
<li><code>bool</code>: any non-empty string or non-zero number counts as <code>True</code></li>
</ul>
<p>When you run this, the browser pops up a box for each <code>input()</code>.</p>
""", r'''
name = input("What is your name? ")
age = int(input("How old are you? "))   # string -> integer

print("Hello " + name + "!")
print("Next year you will be", age + 1)
print("Age as a string: " + str(age))
'''),
            section("Formatting output", """
<p>There are a few ways to build output:</p>
<ul>
<li><strong>Commas</strong> in <code>print(a, b)</code> put a space between items and accept any type.</li>
<li><strong>Concatenation</strong> with <code>+</code> joins strings with no space added. Every part must be a string.</li>
<li><code>round(value, 2)</code> rounds to 2 decimal places.</li>
<li><code>sep=</code> changes the separator between items, and <code>end=</code> replaces the newline at the end.</li>
<li><strong>f-strings</strong> put values straight into text: <code>f"£{cost:.2f}"</code> shows exactly 2 decimal places.</li>
</ul>
""", r'''
price = 7.5
qty = 3
cost = price * qty

print("Cost: £" + str(cost))     # concatenation needs str()
print("Cost:", round(cost, 2))   # commas add a space
print(f"Cost: £{cost:.2f}")      # f-string, 2 decimal places

print("a", "b", "c", sep="-")
for i in range(5):
    print(i, end=" ")            # stay on the same line
print()
'''),
        ],
        "exam_tip": """Watch out for <code>input()</code> results being strings. <code>"5" + "3"</code> gives
<code>"53"</code>, not <code>8</code>. Forgetting <code>int()</code> is one of the most common mistakes in Paper 2.""",
        "quiz": [
            {"q": "What data type does <code>input()</code> return?",
             "options": ["Integer", "String", "Whatever the user typed", "Real"],
             "answer": 1,
             "explain": "input() always returns a string. Use int() or float() to convert it."},
            {"q": "Which data type is most suitable for storing whether a user is logged in?",
             "options": ["String", "Integer", "Boolean", "Character"],
             "answer": 2,
             "explain": "Logged in or not is a True/False value, so it's a Boolean."},
            {"q": "What is printed by <code>print(\"3\" + \"4\")</code>?",
             "options": ["7", "34", "3 4", "An error"],
             "answer": 1,
             "explain": "Both are strings, so + joins them (concatenation) and gives 34."},
            {"q": "Why should <code>VAT_RATE</code> be a constant rather than a variable?",
             "options": ["It runs faster", "Its value should not change while the program runs",
                         "Constants can store decimals", "Python requires it"],
             "answer": 1,
             "explain": "Constants hold values that stay the same, and UPPER_CASE tells other programmers not to change them."},
        ],
        "challenges": [
            {"title": "Rectangle area",
             "task": "Ask the user for the <strong>width</strong> and then the <strong>height</strong> of a rectangle "
                     "(whole numbers). Output the area in the form <code>Area: 20</code>.",
             "starter": code(r'''
# Ask for width and height, then print the area
'''),
             "solution": code(r'''
width = int(input("Enter the width: "))
height = int(input("Enter the height: "))
area = width * height
print("Area:", area)
'''),
             "hint": "Use int(input(...)) twice, multiply, then print(\"Area:\", area).",
             "tests": [{"inputs": ["4", "5"], "expect": ["Area: 20"]},
                       {"inputs": ["10", "3"], "expect": ["Area: 30"]}]},
        ],
    },
    # --------------------------------------------------------------- operators
    {
        "slug": "operators",
        "title": "Operators",
        "group": "t2",
        "spec": "2.5",
        "summary": "Arithmetic, relational and logical operators, with integer division and modulus.",
        "sections": [
            section("Arithmetic operators", """
<table>
<tr><th>Operator</th><th>Meaning</th><th>Example</th><th>Result</th></tr>
<tr><td><code>+</code></td><td>Addition</td><td><code>17 + 5</code></td><td>22</td></tr>
<tr><td><code>-</code></td><td>Subtraction</td><td><code>17 - 5</code></td><td>12</td></tr>
<tr><td><code>*</code></td><td>Multiplication</td><td><code>17 * 5</code></td><td>85</td></tr>
<tr><td><code>/</code></td><td>Real division (always a float)</td><td><code>17 / 5</code></td><td>3.4</td></tr>
<tr><td><code>//</code></td><td>Integer division (quotient)</td><td><code>17 // 5</code></td><td>3</td></tr>
<tr><td><code>%</code></td><td>Modulus (remainder)</td><td><code>17 % 5</code></td><td>2</td></tr>
<tr><td><code>**</code></td><td>Exponentiation (power)</td><td><code>17 ** 2</code></td><td>289</td></tr>
</table>
""", r'''
a = 17
b = 5
print("a + b  =", a + b)
print("a - b  =", a - b)
print("a * b  =", a * b)
print("a / b  =", a / b)     # real division -> float
print("a // b =", a // b)    # integer division
print("a % b  =", a % b)     # remainder
print("a ** 2 =", a ** 2)    # power
'''),
            section("Using // and % in practice", """
<p>Integer division and modulus come up a lot in exam questions:</p>
<ul>
<li><strong>Odd or even:</strong> <code>n % 2 == 0</code> means <code>n</code> is even.</li>
<li><strong>Divisible by:</strong> <code>n % 3 == 0</code> means <code>n</code> is a multiple of 3.</li>
<li><strong>Unit conversion:</strong> minutes into hours plus leftover minutes.</li>
<li><strong>Digits:</strong> <code>n % 10</code> is the last digit, and <code>n // 10</code> removes it.</li>
</ul>
""", r'''
total_minutes = 135
hours = total_minutes // 60
minutes = total_minutes % 60
print(total_minutes, "minutes =", hours, "h", minutes, "min")

for n in range(1, 8):
    if n % 2 == 0:
        print(n, "is even")
    else:
        print(n, "is odd")

number = 4721
print("Last digit:", number % 10)
print("Without last digit:", number // 10)
'''),
            section("Relational (comparison) operators", """
<p>These compare two values and always give a <strong>Boolean</strong> (<code>True</code> or <code>False</code>):</p>
<p><code>==</code> equal to, <code>!=</code> not equal to, <code>&lt;</code> less than,
<code>&lt;=</code> less than or equal, <code>&gt;</code> greater than, <code>&gt;=</code> greater than or equal.</p>
<p class="callout"><strong><code>=</code> is assignment, <code>==</code> is comparison.</strong>
Writing <code>if x = 5:</code> is a syntax error.</p>
""", r'''
score = 72
print(score == 72)
print(score != 72)
print(score > 50)
print(score <= 70)
print("apple" < "banana")   # strings compare alphabetically
'''),
            section("Logical (Boolean) operators", """
<p><code>and</code>, <code>or</code> and <code>not</code> combine Boolean values:</p>
<ul>
<li><code>A and B</code> is True only if <strong>both</strong> are True.</li>
<li><code>A or B</code> is True if <strong>at least one</strong> is True.</li>
<li><code>not A</code> flips True to False and back.</li>
</ul>
<p>This program prints the full truth table:</p>
""", r'''
print("A      B      | A and B  A or B  not A")
for a in [True, False]:
    for b in [True, False]:
        print(f"{a!s:6} {b!s:6} | {a and b!s:8} {a or b!s:7} {not a}")
'''),
            section("Order of operations", """
<p>Python follows BIDMAS: Brackets, Indices (<code>**</code>), Division/Multiplication
(<code>/ // % *</code>), then Addition/Subtraction. Comparisons come next, then <code>not</code>, <code>and</code>, <code>or</code>.
<strong>If in doubt, add brackets.</strong> They make your intention clear and prevent logic errors.</p>
""", r'''
print(2 + 3 * 4)        # 14, not 20
print((2 + 3) * 4)      # 20
a = 60
b = 80
print(a + b / 2)        # logic error if you wanted the average!
print((a + b) / 2)      # correct average
'''),
        ],
        "exam_tip": """For an average, always write <code>(a + b + c) / 3</code> with brackets. Without them only
<code>c</code> is divided, which is a classic <strong>logic error</strong> in "find and fix" questions.""",
        "quiz": [
            {"q": "What is <code>23 // 4</code>?", "options": ["5.75", "5", "3", "6"], "answer": 1,
             "explain": "Integer division gives the whole-number quotient: 4 goes into 23 five times."},
            {"q": "What is <code>23 % 4</code>?", "options": ["5", "3", "0.75", "4"], "answer": 1,
             "explain": "23 = 4 × 5 + 3, so the remainder is 3."},
            {"q": "What does <code>not (True and False)</code> evaluate to?",
             "options": ["True", "False", "None", "An error"], "answer": 0,
             "explain": "True and False is False, and not False is True."},
            {"q": "Which expression tests whether <code>n</code> is a multiple of 5?",
             "options": ["n / 5 == 0", "n // 5 == 0", "n % 5 == 0", "n % 5 == 5"], "answer": 2,
             "explain": "A multiple of 5 leaves no remainder when divided by 5."},
        ],
        "challenges": [
            {"title": "Seconds converter",
             "task": "Ask the user for a number of seconds (whole number). Output it as minutes and seconds "
                     "in the form <code>2 minutes and 5 seconds</code>.",
             "starter": code(r'''
seconds = int(input("Enter seconds: "))
# work out minutes and remaining seconds
'''),
             "solution": code(r'''
seconds = int(input("Enter seconds: "))
minutes = seconds // 60
remaining = seconds % 60
print(minutes, "minutes and", remaining, "seconds")
'''),
             "hint": "Use // 60 for the minutes and % 60 for the seconds left over.",
             "tests": [{"inputs": ["125"], "expect": ["2 minutes and 5 seconds"]},
                       {"inputs": ["60"], "expect": ["1 minutes and 0 seconds"]},
                       {"inputs": ["59"], "expect": ["0 minutes and 59 seconds"]}]},
        ],
    },
    # --------------------------------------------------------------- selection
    {
        "slug": "selection",
        "title": "Selection (if / elif / else)",
        "group": "t2",
        "spec": "2.2",
        "summary": "Making decisions with if, elif and else, nested selection and compound conditions.",
        "sections": [
            section("if and else", """
<p><strong>Selection</strong> means choosing which code to run based on a condition.
The indented block under <code>if</code> runs only when the condition is <code>True</code>,
otherwise the <code>else</code> block runs.</p>
<p>Don't forget the <strong>colon</strong> <code>:</code> and the <strong>indentation</strong> (4 spaces).
Python uses indentation to know which lines belong inside the <code>if</code>.</p>
""", r'''
age = int(input("Enter your age: "))

if age >= 18:
    print("You can vote.")
else:
    print("You can vote in", 18 - age, "years.")
print("This line always runs - it is not indented.")
'''),
            section("elif: more than two choices", """
<p><code>elif</code> ("else if") lets you check several conditions in order. Python runs the
<strong>first</strong> branch whose condition is True and skips the rest, so <strong>order matters</strong>.
Put the highest grade boundary first.</p>
""", r'''
mark = int(input("Enter your mark (0-100): "))

if mark >= 70:
    grade = "A"
elif mark >= 60:
    grade = "B"
elif mark >= 50:
    grade = "C"
elif mark >= 40:
    grade = "D"
else:
    grade = "U"

print("Grade:", grade)
'''),
            section("Compound conditions", """
<p>Combine conditions with <code>and</code> / <code>or</code>. A common use is checking that a
value is <strong>within a range</strong>. Python also lets you chain comparisons:
<code>1 &lt;= day &lt;= 31</code>.</p>
""", r'''
temperature = 23
is_raining = False

if temperature > 20 and not is_raining:
    print("Go to the beach!")
elif temperature > 20 or is_raining:
    print("Maybe the cinema?")

day = 31
if 1 <= day <= 31:
    print(day, "is a possible day of the month")
'''),
            section("Nested selection", """
<p>An <code>if</code> can sit inside another <code>if</code>. This is called <strong>nesting</strong>.
Each level is indented one more step.</p>
""", r'''
has_ticket = True
age = 15

if has_ticket:
    if age >= 18:
        print("Enjoy the film.")
    else:
        print("You need an adult with you.")
else:
    print("Please buy a ticket first.")
'''),
            section("Common mistakes", """
<ul>
<li><code>if x = 5:</code> is a <strong>syntax error</strong>. Use <code>==</code> to compare.</li>
<li>A missing colon after the condition is a <strong>syntax error</strong>.</li>
<li>Wrong <code>elif</code> order, such as testing <code>mark &gt;= 40</code> before <code>mark &gt;= 70</code>, is a <strong>logic error</strong> because everyone gets a D.</li>
<li><code>if answer == "yes" or "y":</code> is a <strong>logic error</strong> that is always True. Write <code>answer == "yes" or answer == "y"</code>.</li>
</ul>
""", r'''
answer = "no"

# BUG: "y" on its own is a non-empty string, so it counts as True
if answer == "yes" or "y":
    print("Buggy version thinks you said yes!")

# FIXED
if answer == "yes" or answer == "y":
    print("Fixed version thinks you said yes")
else:
    print("Fixed version knows you said no")
'''),
        ],
        "exam_tip": """When testing ranges, think about the <strong>boundaries</strong>: is it <code>&gt;</code> or
<code>&gt;=</code>? Check the question wording ("over 18" and "18 or over" are different).""",
        "quiz": [
            {"q": "With <code>mark = 75</code>, what grade does this give?<br><code>if mark &gt;= 40: grade = \"D\"<br>elif mark &gt;= 70: grade = \"A\"</code>",
             "options": ["A", "D", "Both", "Nothing"], "answer": 1,
             "explain": "75 >= 40 is True, so the first branch runs and elif is skipped. The order is wrong, which is a logic error."},
            {"q": "What is missing from <code>if score &gt; 50</code>?",
             "options": ["Brackets", "A colon", "A semicolon", "The word then"], "answer": 1,
             "explain": "Every if, elif, else, for, while and def line must end with a colon."},
            {"q": "Which condition is true only for ages 13 to 19 inclusive?",
             "options": ["age > 13 and age < 19", "age >= 13 or age <= 19",
                         "age >= 13 and age <= 19", "age == 13 and age == 19"], "answer": 2,
             "explain": "Both conditions must be true (and), and the boundaries are included (>=, <=)."},
        ],
        "challenges": [
            {"title": "Grade calculator",
             "task": "Ask for a mark. Output <code>Grade: A</code> for 70+, <code>B</code> for 60–69, <code>C</code> for 50–59, "
                     "<code>D</code> for 40–49 and <code>U</code> otherwise.",
             "starter": code(r'''
mark = int(input("Enter mark: "))
'''),
             "solution": code(r'''
mark = int(input("Enter mark: "))
if mark >= 70:
    print("Grade: A")
elif mark >= 60:
    print("Grade: B")
elif mark >= 50:
    print("Grade: C")
elif mark >= 40:
    print("Grade: D")
else:
    print("Grade: U")
'''),
             "hint": "Use an if / elif / else chain starting with the highest boundary.",
             "tests": [{"inputs": ["85"], "expect": ["Grade: A"]},
                       {"inputs": ["70"], "expect": ["Grade: A"]},
                       {"inputs": ["69"], "expect": ["Grade: B"]},
                       {"inputs": ["50"], "expect": ["Grade: C"]},
                       {"inputs": ["40"], "expect": ["Grade: D"]},
                       {"inputs": ["39"], "expect": ["Grade: U"]}]},
        ],
    },
    # --------------------------------------------------------------- iteration
    {
        "slug": "iteration",
        "title": "Repetition & iteration (loops)",
        "group": "t2",
        "spec": "2.2",
        "summary": "Count-controlled for loops, condition-controlled while loops, iterating over lists and nested loops.",
        "sections": [
            section("Count-controlled loops: for and range()", """
<p>A <strong>count-controlled</strong> loop repeats a <em>fixed</em> number of times.
In Python this is <code>for</code> with <code>range()</code>:</p>
<ul>
<li><code>range(5)</code> gives 0, 1, 2, 3, 4 (it stops <em>before</em> 5)</li>
<li><code>range(1, 6)</code> gives 1, 2, 3, 4, 5</li>
<li><code>range(10, 0, -2)</code> gives 10, 8, 6, 4, 2 (the third value is the step)</li>
</ul>
""", r'''
for i in range(5):
    print("Loop number", i)

print("--- 1 to 5 ---")
for i in range(1, 6):
    print(i)

print("--- countdown ---")
for i in range(10, 0, -2):
    print(i)
'''),
            section("Condition-controlled loops: while", """
<p>A <strong>condition-controlled</strong> loop repeats <em>while</em> a condition is True.
Use it when you don't know in advance how many repeats you'll need, for example
"keep asking until the password is right".</p>
<p>Something inside the loop must eventually make the condition False, otherwise you get an
<strong>infinite loop</strong>. This site stops programs that run for more than 5 seconds.</p>
""", r'''
total = 0
number = int(input("Enter a number (0 to stop): "))
while number != 0:
    total = total + number
    number = int(input("Enter a number (0 to stop): "))
print("Total:", total)
'''),
            section("Iterating over a data structure", """
<p><strong>Iteration</strong> also means visiting each item of a data structure in turn.
A <code>for</code> loop can go straight through a list or a string with no counter needed.
If you <em>also</em> need the position, loop over <code>range(len(...))</code>.</p>
""", r'''
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print("I like", fruit)

for index in range(len(fruits)):
    print("Index", index, "holds", fruits[index])

for letter in "IGCSE":
    print(letter)
'''),
            section("Running totals, counters and averages", """
<p>Many Paper 2 tasks follow this pattern: <strong>initialise</strong> a total or counter
before the loop, <strong>update</strong> it inside the loop, then <strong>use</strong> it after.</p>
""", r'''
scores = [56, 78, 91, 43, 67, 88]
total = 0
count_passed = 0

for score in scores:
    total = total + score
    if score >= 50:
        count_passed = count_passed + 1

average = total / len(scores)
print("Total:", total)
print("Average:", round(average, 1))
print("Passed:", count_passed, "out of", len(scores))
'''),
            section("Nested loops", """
<p>A loop inside a loop: the <strong>inner</strong> loop runs completely for every single repeat of the
<strong>outer</strong> loop. You'll use this for times tables, grids and 2D lists.</p>
""", r'''
for row in range(1, 6):
    for col in range(1, 6):
        print(row * col, end="\t")
    print()   # new line after each row
'''),
        ],
        "exam_tip": """If a question says "until" or "keep asking", use a <code>while</code> loop. If it gives a fixed
number ("10 times", "each item"), use a <code>for</code> loop. Using the right kind of loop is part of good design.""",
        "quiz": [
            {"q": "What numbers does <code>range(2, 8, 2)</code> produce?",
             "options": ["2, 4, 6, 8", "2, 4, 6", "2, 3, 4, 5, 6, 7", "4, 6, 8"], "answer": 1,
             "explain": "Start at 2, step by 2, and stop before 8."},
            {"q": "Which type of loop is best for 'keep asking for a password until it is correct'?",
             "options": ["Count-controlled (for)", "Condition-controlled (while)", "Nested for", "No loop needed"],
             "answer": 1, "explain": "You don't know how many attempts it will take, so the loop is condition-controlled."},
            {"q": "How many times does <code>print</code> run?<br><code>for i in range(3):<br>&nbsp;&nbsp;for j in range(4):<br>&nbsp;&nbsp;&nbsp;&nbsp;print(i, j)</code>",
             "options": ["7", "12", "3", "4"], "answer": 1,
             "explain": "The inner loop runs 4 times for each of the 3 outer repeats: 3 × 4 = 12."},
        ],
        "challenges": [
            {"title": "Keep adding",
             "task": "Keep asking the user for whole numbers until they enter <code>0</code>. "
                     "Then output the total in the form <code>Total: 18</code>.",
             "starter": code(r'''
total = 0
'''),
             "solution": code(r'''
total = 0
number = int(input("Number (0 to stop): "))
while number != 0:
    total = total + number
    number = int(input("Number (0 to stop): "))
print("Total:", total)
'''),
             "hint": "Read the first number before the while loop, and read the next number at the end of each loop.",
             "tests": [{"inputs": ["5", "10", "3", "0"], "expect": ["Total: 18"]},
                       {"inputs": ["0"], "expect": ["Total: 0"]},
                       {"inputs": ["-4", "4", "7", "0"], "expect": ["Total: 7"]}]},
        ],
    },
    # ------------------------------------------------------------------- lists
    {
        "slug": "lists",
        "title": "Data structures: lists, 2D lists & records",
        "group": "t2",
        "spec": "2.4",
        "summary": "One-dimensional arrays (lists), two-dimensional arrays and records.",
        "sections": [
            section("One-dimensional lists (arrays)", """
<p>A <strong>list</strong> stores many values under one name. Each item has an <strong>index</strong>,
and <strong>indexes start at 0</strong>. Lists are Python's version of the arrays in the specification.</p>
<ul>
<li><code>items[0]</code> is the first item, and <code>items[-1]</code> is the last</li>
<li><code>len(items)</code> is the number of items</li>
<li><code>items.append(x)</code> adds to the end, and <code>items.insert(i, x)</code> inserts at position i</li>
<li><code>items.remove(x)</code> removes the first x, and <code>items.pop(i)</code> removes and returns the item at index i</li>
<li><code>x in items</code> is True if x is in the list</li>
</ul>
""", r'''
names = ["Amira", "Ben", "Chen"]
print(names[0])          # first item
print(names[-1])         # last item
print(len(names))

names.append("Dara")
names[1] = "Bella"       # change an item
names.insert(0, "Zak")
print(names)

names.remove("Chen")
print(names)
print("Dara" in names)
'''),
            section("Creating and filling lists", """
<p>You'll often build a list in a loop, or create a list of a fixed size filled with a default value.</p>
""", r'''
squares = []
for n in range(1, 6):
    squares.append(n * n)
print(squares)

totals = [0] * 5        # five zeros
totals[2] = 99
print(totals)

print("Largest:", max(squares), "Smallest:", min(squares), "Sum:", sum(squares))
'''),
            section("Two-dimensional lists", """
<p>A <strong>2D list</strong> is a list of lists, like a table or grid. Access an item with
<strong>two indexes</strong>: <code>grid[row][column]</code>. Use nested loops to visit every item.</p>
""", r'''
# 3 students x 4 test scores
scores = [
    [65, 72, 80, 58],
    [90, 85, 88, 94],
    [45, 60, 52, 49],
]

print("Student 1, test 3:", scores[1][2])   # row 1, column 2

for row in range(len(scores)):
    total = 0
    for col in range(len(scores[row])):
        total = total + scores[row][col]
    print("Student", row, "total:", total)
'''),
            section("Records", """
<p>A <strong>record</strong> groups related data of <em>different</em> types about one thing, such as a
student's name (string), age (integer) and enrolled status (Boolean). Each item in a record is a
<strong>field</strong>. In Python you can store a record as a list, and a table of records as a 2D list.</p>
""", r'''
# Each record: [name, age, enrolled]
students = [
    ["Amira", 16, True],
    ["Ben", 15, False],
    ["Chen", 16, True],
]

for student in students:
    name = student[0]
    age = student[1]
    enrolled = student[2]
    if enrolled:
        print(name, "is", age, "and enrolled")
'''),
            section("Index out of range", """
<p>Asking for an index that doesn't exist causes a <strong>runtime error</strong>
(<code>IndexError</code>). A list of length 4 has indexes 0–3 only. This is often an
<em>off-by-one</em> mistake in a loop.</p>
""", r'''
items = [10, 20, 30, 40]
for i in range(len(items) + 1):   # BUG: one too many
    print(items[i])
'''),
        ],
        "exam_tip": """Exam questions often say "do not use built-in functions such as <code>max()</code> or
<code>sort()</code>". Then you must write the algorithm yourself with a loop. Practise both ways.""",
        "quiz": [
            {"q": "<code>colours = [\"red\", \"green\", \"blue\"]</code>. What is <code>colours[1]</code>?",
             "options": ["red", "green", "blue", "IndexError"], "answer": 1,
             "explain": "Indexes start at 0, so index 1 is the second item."},
            {"q": "In <code>grid[2][0]</code>, which number is the row?",
             "options": ["2", "0", "Neither", "Both"], "answer": 0,
             "explain": "The first index picks the inner list (the row) and the second picks the item in it (the column)."},
            {"q": "What is a record?",
             "options": ["A list where every item has the same type", "A group of related fields, possibly of different types",
                         "A file on disk", "A sorted list"], "answer": 1,
             "explain": "A record groups related data about one entity, and its fields can have different data types."},
        ],
        "challenges": [
            {"title": "Highest score (no max!)",
             "task": "Using a loop and <strong>without</strong> using <code>max()</code>, find the highest value in "
                     "<code>scores</code> and output it as <code>Highest: 92</code>.",
             "starter": code(r'''
scores = [45, 78, 92, 61, 88]
'''),
             "solution": code(r'''
scores = [45, 78, 92, 61, 88]
highest = scores[0]
for score in scores:
    if score > highest:
        highest = score
print("Highest:", highest)
'''),
             "hint": "Start with highest = scores[0], then replace it whenever you find a bigger score.",
             "tests": [{"inputs": [], "expect": ["Highest: 92"]}]},
        ],
    },
    # ----------------------------------------------------------------- strings
    {
        "slug": "strings",
        "title": "String manipulation",
        "group": "t2",
        "spec": "2.4",
        "summary": "Length, indexing, slicing, case conversion, searching, splitting and character codes.",
        "sections": [
            section("Indexing, length and slicing", """
<p>A string is a sequence of characters, so you can index it like a list (starting at 0).</p>
<ul>
<li><code>len(s)</code> is the number of characters</li>
<li><code>s[0]</code> is the first character, and <code>s[-1]</code> is the last</li>
<li><code>s[start:end]</code> is a <strong>substring</strong> from <code>start</code> up to (not including) <code>end</code></li>
</ul>
<p>Strings are <strong>immutable</strong>: you can't change <code>s[0] = "X"</code>, you have to build a new string.</p>
""", r'''
word = "COMPUTER"
print(len(word))
print(word[0], word[-1])
print(word[0:4])     # COMP
print(word[4:])      # UTER
print(word[:3])      # COM
print(word[::-1])    # reversed
'''),
            section("Case conversion and tidying", """
<p><code>upper()</code>, <code>lower()</code> and <code>title()</code> return converted copies.
<code>strip()</code> removes spaces from both ends. To compare input ignoring case, convert both sides:
<code>answer.lower() == "yes"</code>.</p>
""", r'''
name = "  ada LOVELACE  "
print("[" + name + "]")
print("[" + name.strip() + "]")
print(name.strip().upper())
print(name.strip().lower())
print(name.strip().title())

text = "I like cats. Cats are great."
print(text.replace("cats", "dogs"))
'''),
            section("Searching and testing strings", """
<ul>
<li><code>"cat" in s</code> is True if the substring appears</li>
<li><code>s.find("x")</code> gives the position of the first match, or <code>-1</code> if it isn't found</li>
<li><code>s.index("x")</code> is like find but causes a runtime error if there's no match</li>
<li><code>s.count("x")</code> counts the matches</li>
<li><code>s.isdigit()</code>, <code>s.isalpha()</code>, <code>s.isupper()</code> and <code>s.islower()</code> test the characters</li>
</ul>
""", r'''
email = "student@school.org"
print("@" in email)
print(email.find("@"))
print(email.find("#"))
print(email.count("o"))

username = email[:email.find("@")]
print("Username:", username)

print("12345".isdigit(), "12a45".isdigit())
print("Hello".isalpha(), "Hello!".isalpha())
'''),
            section("split() and join()", """
<p><code>split()</code> breaks a string into a <strong>list</strong>, which you'll use a lot with CSV files.
<code>",".join(list)</code> does the opposite.</p>
""", r'''
line = "Amira,16,72"
parts = line.split(",")
print(parts)
name = parts[0]
score = int(parts[2])
print(name, "scored", score)

sentence = "the quick brown fox"
words = sentence.split()      # split on spaces
print(len(words), "words")
print("-".join(words))
'''),
            section("Character codes: ord() and chr()", """
<p>Every character has a numeric code (ASCII/Unicode). <code>ord("A")</code> is 65 and <code>chr(65)</code> is <code>"A"</code>.
This lets you build ciphers like the <strong>Caesar cipher</strong>, which shifts every letter along the alphabet.</p>
""", r'''
print(ord("A"), ord("Z"), ord("a"))
print(chr(72) + chr(105))

message = "HELLO WORLD"
shift = 3
encrypted = ""
for letter in message:
    if letter.isalpha():
        position = ord(letter) - ord("A")
        new_position = (position + shift) % 26   # wrap Z back to A
        encrypted = encrypted + chr(new_position + ord("A"))
    else:
        encrypted = encrypted + letter
print(encrypted)
'''),
        ],
        "exam_tip": """Remember that slicing stops <em>before</em> the end index: <code>"HELLO"[1:3]</code> is
<code>"EL"</code>. When in doubt, run a quick test in the playground.""",
        "quiz": [
            {"q": "What is <code>\"PYTHON\"[2:5]</code>?", "options": ["YTH", "THO", "THON", "YTHO"], "answer": 1,
             "explain": "Indexes 2, 3 and 4 are T, H and O. It stops before index 5."},
            {"q": "What does <code>\"banana\".find(\"z\")</code> return?",
             "options": ["0", "None", "-1", "An error"], "answer": 2,
             "explain": "find() returns -1 when the substring isn't found."},
            {"q": "What does <code>\"a,b,c\".split(\",\")</code> return?",
             "options": ["\"abc\"", "[\"a\", \"b\", \"c\"]", "[\"a,b,c\"]", "3"], "answer": 1,
             "explain": "split() returns a list of the pieces between the separators."},
        ],
        "challenges": [
            {"title": "Vowel counter",
             "task": "Ask the user for a word and output how many vowels (a, e, i, o, u, either case) it contains, "
                     "in the form <code>Vowels: 5</code>.",
             "starter": code(r'''
word = input("Enter a word: ")
'''),
             "solution": code(r'''
word = input("Enter a word: ")
vowels = 0
for letter in word.lower():
    if letter in "aeiou":
        vowels = vowels + 1
print("Vowels:", vowels)
'''),
             "hint": "Loop through word.lower() and check if each letter is in \"aeiou\".",
             "tests": [{"inputs": ["education"], "expect": ["Vowels: 5"]},
                       {"inputs": ["rhythm"], "expect": ["Vowels: 0"]},
                       {"inputs": ["AppLE"], "expect": ["Vowels: 2"]}]},
        ],
    },
    # ------------------------------------------------------------- subprograms
    {
        "slug": "subprograms",
        "title": "Subprograms: functions & procedures",
        "group": "t2",
        "spec": "2.6",
        "summary": "Functions vs procedures, parameters, return values, local and global scope, and library modules.",
        "sections": [
            section("Why use subprograms?", """
<p>A <strong>subprogram</strong> is a named block of code that does one task and can be <strong>called</strong> whenever it's needed.
The benefits you should be able to state:</p>
<ul>
<li><strong>Reuse:</strong> write the code once and call it many times, so there's less repetition</li>
<li><strong>Decomposition:</strong> a big problem is split into small, manageable parts</li>
<li><strong>Easier testing and debugging:</strong> each subprogram can be tested on its own</li>
<li><strong>Maintainability:</strong> fix or change the code in one place</li>
<li><strong>Teamwork:</strong> different programmers can write different subprograms</li>
</ul>
"""),
            section("Procedures and functions", """
<p>Both are defined with <code>def</code>:</p>
<ul>
<li>A <strong>procedure</strong> carries out a task but does <strong>not return</strong> a value.</li>
<li>A <strong>function</strong> <strong>returns</strong> a value with <code>return</code>, which the calling code can store or use.</li>
</ul>
<p>A subprogram must be defined <em>before</em> the line that calls it runs.</p>
""", r'''
# Procedure - does something, returns nothing
def show_banner(title):
    print("=" * 20)
    print(title.upper())
    print("=" * 20)

# Function - calculates and returns a value
def area_of_circle(radius):
    return 3.14159 * radius ** 2

show_banner("circle calculator")
a = area_of_circle(5)
print("Area:", round(a, 2))
print("Double area:", round(area_of_circle(5) * 2, 2))
'''),
            section("Parameters and arguments", """
<p><strong>Parameters</strong> are the variables listed in the <code>def</code> line. <strong>Arguments</strong>
are the actual values passed in when calling it. A function can take several parameters and can also return
several values.</p>
""", r'''
def calculate_pay(hours, rate):
    pay = hours * rate
    if hours > 40:
        pay = pay + (hours - 40) * rate * 0.5   # overtime bonus
    return pay

def min_max(numbers):
    return min(numbers), max(numbers)

print(calculate_pay(35, 12.0))
print(calculate_pay(45, 12.0))

low, high = min_max([7, 2, 9, 4])
print("Lowest", low, "highest", high)
'''),
            section("Local and global variables", """
<p>A <strong>local</strong> variable is created inside a subprogram and exists only while it runs.
A <strong>global</strong> variable is created in the main program and can be read anywhere.
To <em>change</em> a global inside a function you need the <code>global</code> keyword, but passing
parameters and returning values is usually better practice.</p>
""", r'''
score = 0            # global

def add_points(points):
    global score
    score = score + points

def double(n):
    result = n * 2   # 'result' is local
    return result

add_points(10)
add_points(5)
print("Score:", score)
print(double(21))
print(result)        # runtime error - result only existed inside double()
'''),
            section("Pre-existing subprograms and libraries", """
<p>Python has <strong>built-in</strong> subprograms (<code>len</code>, <code>print</code>, <code>round</code>, <code>int</code>...)
and <strong>library modules</strong> you <code>import</code>. Common ones:</p>
<ul>
<li><code>random</code>: <code>random.randint(1, 6)</code> (inclusive of both ends), <code>random.random()</code>, <code>random.choice(list)</code></li>
<li><code>math</code>: <code>math.sqrt()</code>, <code>math.pi</code>, <code>math.floor()</code>, <code>math.ceil()</code></li>
<li><code>time</code>: <code>time.time()</code> for timing</li>
</ul>
""", r'''
import random
import math

dice = random.randint(1, 6)
print("You rolled", dice)
print("Random choice:", random.choice(["rock", "paper", "scissors"]))

print("Square root of 50:", math.sqrt(50))
print("Pi:", math.pi)
print("Floor of 4.7:", math.floor(4.7), " Ceil of 4.2:", math.ceil(4.2))
'''),
        ],
        "exam_tip": """If a question asks for a <em>function</em> that "returns" something, use <code>return</code>, not
<code>print</code>. Printing inside the function instead of returning loses marks.""",
        "quiz": [
            {"q": "What is the key difference between a function and a procedure?",
             "options": ["Functions use def, procedures don't", "A function returns a value",
                         "Procedures can take parameters", "There is no difference"], "answer": 1,
             "explain": "A function returns a value to the caller. A procedure just carries out a task."},
            {"q": "In <code>def greet(name):</code>, what is <code>name</code>?",
             "options": ["An argument", "A parameter", "A global variable", "A return value"], "answer": 1,
             "explain": "Variables in the def line are parameters. The values you pass in when calling are arguments."},
            {"q": "Which value can <code>random.randint(1, 3)</code> NOT return?",
             "options": ["1", "2", "3", "0"], "answer": 3,
             "explain": "randint includes both ends, so it returns 1, 2 or 3."},
        ],
        "challenges": [
            {"title": "Largest of three",
             "task": "Write a function <code>largest(a, b, c)</code> that <strong>returns</strong> the biggest of three numbers "
                     "(don't use <code>max()</code>). The main program reads three whole numbers and prints "
                     "<code>Largest: X</code>.",
             "starter": code(r'''
def largest(a, b, c):
    # your code here
    return 0

x = int(input("First: "))
y = int(input("Second: "))
z = int(input("Third: "))
print("Largest:", largest(x, y, z))
'''),
             "solution": code(r'''
def largest(a, b, c):
    biggest = a
    if b > biggest:
        biggest = b
    if c > biggest:
        biggest = c
    return biggest

x = int(input("First: "))
y = int(input("Second: "))
z = int(input("Third: "))
print("Largest:", largest(x, y, z))
'''),
             "hint": "Assume a is biggest, then compare b and c with it.",
             "tests": [{"inputs": ["3", "9", "5"], "expect": ["Largest: 9"]},
                       {"inputs": ["10", "2", "7"], "expect": ["Largest: 10"]},
                       {"inputs": ["-1", "-5", "-3"], "expect": ["Largest: -1"]}]},
        ],
    },
    # ------------------------------------------------------------------- files
    {
        "slug": "files",
        "title": "File handling",
        "group": "t2",
        "spec": "2.3",
        "summary": "Reading and writing text files and processing comma-separated (CSV) data.",
        "sections": [
            section("Opening files", """
<p>Programs use files to keep data after the program ends. <code>open(filename, mode)</code> opens a file:</p>
<table>
<tr><th>Mode</th><th>Meaning</th></tr>
<tr><td><code>"r"</code></td><td>Read. The file must exist, or you get a <code>FileNotFoundError</code>.</td></tr>
<tr><td><code>"w"</code></td><td>Write. Creates the file, and <strong>wipes</strong> it if it already exists.</td></tr>
<tr><td><code>"a"</code></td><td>Append. Adds to the end of the file and keeps what's already there.</td></tr>
</table>
<p>Always <code>close()</code> a file when you're finished, or use a <code>with</code> block, which closes it automatically.</p>
<p class="callout">On this site you have a pretend disk that already contains <code>students.csv</code> and
<code>scores.txt</code>. Files you create stay until you refresh the page.</p>
"""),
            section("Reading a file", """
<p><code>read()</code> gets the whole file as one string, <code>readline()</code> gets one line, and
<code>readlines()</code> gets a list of lines. The simplest approach is to loop over the file line by line.
Each line ends with <code>"\\n"</code>, so use <code>strip()</code> to remove it.</p>
""", r'''
file = open("scores.txt", "r")
contents = file.read()
file.close()
print(contents)

print("--- line by line ---")
with open("scores.txt", "r") as file:
    for line in file:
        print("Line:", line.strip())
'''),
            section("Writing and appending", """
<p><code>write()</code> doesn't add a newline for you, so add <code>"\\n"</code> yourself.
Remember that <code>write()</code> only accepts strings, so convert numbers with <code>str()</code>.</p>
""", r'''
with open("shopping.txt", "w") as file:
    file.write("milk\n")
    file.write("bread\n")

with open("shopping.txt", "a") as file:
    file.write("eggs\n")
    file.write(str(12) + "\n")

with open("shopping.txt", "r") as file:
    print(file.read())
'''),
            section("Processing CSV files", """
<p>A <strong>CSV</strong> (comma-separated values) file stores one record per line, with fields separated by commas.
Read each line, <code>strip()</code> it, <code>split(",")</code> it, then convert the numeric fields.</p>
<pre class="filebox"><span>students.csv</span>
Amira,72
Ben,58
Chen,91
Dara,64
Eli,85</pre>
""", r'''
students = []
with open("students.csv", "r") as file:
    for line in file:
        fields = line.strip().split(",")
        name = fields[0]
        score = int(fields[1])
        students.append([name, score])

for record in students:
    if record[1] >= 70:
        print(record[0], "got a distinction with", record[1])
print(len(students), "records loaded")
'''),
            section("Writing CSV data", """
<p>To save records, join the fields with commas and write one line per record.</p>
""", r'''
results = [["Amira", 72, "Pass"], ["Ben", 38, "Fail"]]

with open("results.csv", "w") as file:
    for record in results:
        line = record[0] + "," + str(record[1]) + "," + record[2]
        file.write(line + "\n")

with open("results.csv", "r") as file:
    print(file.read())
'''),
        ],
        "exam_tip": """Paper 2 file questions give you a data file. Check whether it has a <strong>header row</strong>
(skip it with <code>file.readline()</code> before the loop) and remember to <code>strip()</code> each line before splitting.""",
        "quiz": [
            {"q": "Which mode adds data to the end of an existing file?",
             "options": ["\"r\"", "\"w\"", "\"a\"", "\"x\""], "answer": 2,
             "explain": "\"a\" means append. \"w\" would wipe the file first."},
            {"q": "Why do we use <code>strip()</code> on each line read from a file?",
             "options": ["To convert it to a number", "To remove the newline character and spaces at the ends",
                         "To split it into fields", "To close the file"], "answer": 1,
             "explain": "Each line ends with \\n, and strip() removes it so comparisons and conversions work."},
            {"q": "<code>file.write(42)</code> causes which kind of error?",
             "options": ["Syntax error", "Runtime error (TypeError)", "Logic error", "No error"], "answer": 1,
             "explain": "write() needs a string. Passing an integer crashes while running, which is a TypeError."},
        ],
        "challenges": [
            {"title": "Class average",
             "task": "Read every record from <code>students.csv</code> (name,score) and output the average score in "
                     "the form <code>Average: 74.0</code>.",
             "starter": code(r'''
total = 0
count = 0
'''),
             "solution": code(r'''
total = 0
count = 0
with open("students.csv", "r") as file:
    for line in file:
        fields = line.strip().split(",")
        total = total + int(fields[1])
        count = count + 1
print("Average:", total / count)
'''),
             "hint": "Loop over the file, split each line on commas and add int(fields[1]) to the total.",
             "tests": [{"inputs": [], "expect": ["Average: 74"]}]},
        ],
    },
    # -------------------------------------------------------------- validation
    {
        "slug": "validation",
        "title": "Validation & authentication",
        "group": "t2",
        "spec": "2.3",
        "summary": "Presence, length, range, type, lookup and format checks, plus a simple login system.",
        "sections": [
            section("What is validation?", """
<p><strong>Validation</strong> is an automatic check that input data is <em>sensible and reasonable</em> before
the program uses it. It can't check that data is <em>correct</em>: a valid age of 15 could still be the wrong age.
(Checking the data is correct, for example by typing a password twice, is called <em>verification</em>.)</p>
<table>
<tr><th>Check</th><th>What it does</th><th>Example</th></tr>
<tr><td>Presence</td><td>Something was entered</td><td><code>name != ""</code></td></tr>
<tr><td>Length</td><td>The right number of characters</td><td><code>len(password) &gt;= 8</code></td></tr>
<tr><td>Range</td><td>A number between limits</td><td><code>0 &lt;= mark &lt;= 100</code></td></tr>
<tr><td>Type</td><td>The right data type</td><td><code>text.isdigit()</code></td></tr>
<tr><td>Lookup</td><td>The value is in a list of allowed values</td><td><code>size in ["S", "M", "L"]</code></td></tr>
<tr><td>Format</td><td>Matches a pattern</td><td>Contains an <code>@</code>, starts with a letter...</td></tr>
</table>
"""),
            section("Validating with a while loop", """
<p>The standard pattern is: ask, and <strong>while</strong> the input is invalid, show an error and ask again.
Note the order below: the type check (<code>isdigit</code>) must come <em>before</em> <code>int()</code>,
or bad input would cause a runtime error.</p>
""", r'''
age_text = input("Enter your age (11-18): ")
while not age_text.isdigit() or not (11 <= int(age_text) <= 18):
    print("Invalid - please enter a whole number from 11 to 18")
    age_text = input("Enter your age (11-18): ")
age = int(age_text)
print("Accepted age:", age)
'''),
            section("Presence, length and lookup checks", """
<p>Several checks can be combined. Using a validation <strong>function</strong> keeps the main program tidy.</p>
""", r'''
def valid_username(name):
    if name == "":                      # presence check
        print("Username cannot be blank")
        return False
    if len(name) < 3 or len(name) > 12: # length check
        print("Username must be 3-12 characters")
        return False
    return True

username = input("Choose a username: ")
while not valid_username(username):
    username = input("Choose a username: ")

size = input("T-shirt size (S/M/L): ").upper()
while size not in ["S", "M", "L"]:      # lookup check
    size = input("Please enter S, M or L: ").upper()

print("Welcome", username, "- size", size)
'''),
            section("Using try / except for type checks", """
<p>Another way to handle input that might not be a number is to <em>try</em> the conversion and catch the
runtime error. This also works for negative numbers and decimals, which <code>isdigit()</code> rejects.</p>
""", r'''
valid = False
while not valid:
    try:
        price = float(input("Enter a price: "))
        valid = True
    except ValueError:
        print("That is not a number, try again")
print("Price with VAT:", round(price * 1.2, 2))
'''),
            section("Authentication", """
<p><strong>Authentication</strong> confirms who a user is, usually by checking a username and password against
stored values. Good systems limit the number of attempts.</p>
""", r'''
USERS = [["admin", "Pa55word"], ["maya", "cats123"]]
MAX_ATTEMPTS = 3

attempts = 0
logged_in = False
while attempts < MAX_ATTEMPTS and not logged_in:
    username = input("Username: ")
    password = input("Password: ")
    for record in USERS:
        if record[0] == username and record[1] == password:
            logged_in = True
    attempts = attempts + 1
    if not logged_in:
        print("Incorrect.", MAX_ATTEMPTS - attempts, "attempts left")

if logged_in:
    print("Access granted. Hello", username)
else:
    print("Account locked")
'''),
        ],
        "exam_tip": """When asked to "validate" an input, you need a <strong>loop</strong>. A single <code>if</code>
only checks once, so a user could enter bad data a second time.""",
        "quiz": [
            {"q": "Checking that a mark is between 0 and 100 is which validation check?",
             "options": ["Presence", "Length", "Range", "Lookup"], "answer": 2,
             "explain": "The value must fall between a lower and an upper limit, so it's a range check."},
            {"q": "Checking that a colour is one of \"red\", \"green\" or \"blue\" is which check?",
             "options": ["Format", "Lookup", "Type", "Range"], "answer": 1,
             "explain": "The value is compared against a list of allowed values, so it's a lookup check."},
            {"q": "Can validation guarantee data is correct?",
             "options": ["Yes, always", "No, only that it is reasonable", "Only for numbers", "Only with try/except"],
             "answer": 1, "explain": "Validation checks data is sensible. Valid data can still be wrong."},
        ],
        "challenges": [
            {"title": "Valid mark",
             "task": "Keep asking for a mark until the user enters a <strong>whole number from 0 to 100</strong>. "
                     "Reject non-numbers too. Then output <code>Accepted: 42</code>.",
             "starter": code(r'''
mark = input("Enter a mark (0-100): ")
'''),
             "solution": code(r'''
mark = input("Enter a mark (0-100): ")
while not mark.isdigit() or int(mark) > 100:
    print("Invalid mark")
    mark = input("Enter a mark (0-100): ")
print("Accepted:", int(mark))
'''),
             "hint": "Check mark.isdigit() first. isdigit() is False for \"-5\", so you only need to check the upper limit after that.",
             "tests": [{"inputs": ["150", "-5", "abc", "42"], "expect": ["Accepted: 42"]},
                       {"inputs": ["0"], "expect": ["Accepted: 0"]},
                       {"inputs": ["101", "100"], "expect": ["Accepted: 100"]}]},
        ],
    },
    # ------------------------------------------------------------------ errors
    {
        "slug": "errors",
        "title": "Types of errors & debugging",
        "group": "t2",
        "spec": "2.1",
        "summary": "Syntax, runtime and logic errors: how to spot them, read error messages and fix them.",
        "sections": [
            section("The three types of error", """
<table>
<tr><th>Error type</th><th>What happens</th><th>Examples</th></tr>
<tr><td><strong>Syntax error</strong></td><td>The code breaks the <em>rules (grammar)</em> of the language.
The program <strong>won't start at all</strong>.</td><td>Missing colon, missing bracket or quote, bad indentation, misspelt keyword (<code>whlie</code>)</td></tr>
<tr><td><strong>Runtime error</strong></td><td>The code is valid but <strong>crashes while running</strong> because it tried to do something impossible.</td>
<td>Dividing by zero, converting <code>"abc"</code> to int, index out of range, opening a file that doesn't exist</td></tr>
<tr><td><strong>Logic error</strong></td><td>The program runs and finishes but gives the <strong>wrong result</strong>. There's no error message, which makes these the hardest to find.</td>
<td>Wrong operator (<code>&lt;</code> instead of <code>&lt;=</code>), missing brackets in an average, wrong order of <code>elif</code>, an off-by-one loop</td></tr>
</table>
<p>When you run code on this site, the output panel <strong>labels the error type</strong> for you. Try each example below.</p>
"""),
            section("Syntax errors", """
<p>Python reads the whole program before running any of it, so <em>nothing</em> runs if there's a syntax error,
not even the first <code>print</code>. The message shows the line and a <code>^</code> near the problem.
The real mistake is sometimes on the line <em>before</em> the one reported, for example an unclosed bracket.</p>
<p>Run this, read the message, fix it, and run again:</p>
""", r'''
print("This never prints, even though it is fine")
score = 75
if score > 50
    print("Pass")
'''),
            section("Runtime errors", """
<p>The program starts and runs normally until it reaches the bad line, so earlier output <em>does</em> appear.
Python then prints a <strong>traceback</strong>. Read it from the <strong>bottom up</strong>: the last line names the error
type, and the line above it shows which line of your code caused it.</p>
""", r'''
scores = [80, 65, 90]
print("Number of scores:", len(scores))
print("First score:", scores[0])
print("Fourth score:", scores[3])     # there is no index 3!
print("This line is never reached")
'''),
            section("Common runtime errors", """
<table>
<tr><th>Error</th><th>Cause</th><th>Example</th></tr>
<tr><td><code>NameError</code></td><td>Using a variable or function that doesn't exist (often a typo)</td><td><code>print(totl)</code></td></tr>
<tr><td><code>TypeError</code></td><td>An operation on the wrong type</td><td><code>"Age: " + 16</code></td></tr>
<tr><td><code>ValueError</code></td><td>The right type but an impossible value</td><td><code>int("twelve")</code></td></tr>
<tr><td><code>ZeroDivisionError</code></td><td>Dividing by zero</td><td><code>total / 0</code></td></tr>
<tr><td><code>IndexError</code></td><td>A list or string index that doesn't exist</td><td><code>items[10]</code></td></tr>
<tr><td><code>FileNotFoundError</code></td><td>Opening a missing file for reading</td><td><code>open("nope.txt")</code></td></tr>
</table>
<p>Uncomment one line at a time (delete the <code>#</code>) and run to see each error:</p>
""", r'''
age = 16
print("Program started")
# print(agee)               # NameError
# print("Age: " + age)      # TypeError
# print(int("twelve"))      # ValueError
# print(10 / 0)             # ZeroDivisionError
# print([1, 2, 3][5])       # IndexError
# open("missing.txt", "r")  # FileNotFoundError
print("Program finished")
'''),
            section("Logic errors", """
<p>No crash and no message, just the wrong answer. You find logic errors by <strong>testing</strong> with data where you
already know the expected result, and by <strong>tracing</strong> the code. This program should print the
average of 60, 70 and 80 (which is 70) and count the scores of 70 or more (which is 2). Can you spot both logic errors?</p>
""", r'''
a = 60
b = 70
c = 80
average = a + b + c / 3
print("Average:", average)

count = 0
for score in [a, b, c]:
    if score > 70:
        count = count + 1
print("Scores of 70 or more:", count)
'''),
            section("Debugging techniques", """
<ul>
<li><strong>Read the error message</strong>: the error type and line number tell you most of what you need.</li>
<li><strong>Add print statements</strong> to show variable values at key points.</li>
<li><strong>Use a trace table</strong> to dry-run the code by hand (see <a href="/topic/testing">Testing</a>).</li>
<li><strong>Test small parts</strong>: run each subprogram or section on its own.</li>
<li><strong>Comment out</strong> lines to isolate which part causes the problem.</li>
<li><strong>Use test data</strong> with known answers, including normal, boundary and erroneous values.</li>
</ul>
""", r'''
def average(numbers):
    total = 0
    for n in numbers:
        total = total + n
        print("DEBUG: n =", n, "total =", total)   # debug print
    return total / len(numbers)

print("Average:", average([4, 8, 15]))
'''),
            section("Handling runtime errors with try / except", """
<p>Instead of letting a runtime error crash the program, you can <strong>catch</strong> it with
<code>try</code> / <code>except</code> and respond sensibly.</p>
""", r'''
numbers = [10, 5, 0, 2]
for n in numbers:
    try:
        print("100 /", n, "=", 100 / n)
    except ZeroDivisionError:
        print("Cannot divide by zero - skipped")

try:
    data = open("missing.txt", "r")
except FileNotFoundError:
    print("File not found - check the filename")
'''),
        ],
        "exam_tip": """Paper 2 often gives you a program containing errors to <strong>find and fix</strong>. Fix the
<strong>syntax errors</strong> first so it runs, then the <strong>runtime</strong> crashes, then test carefully with
known data to catch the <strong>logic errors</strong>. Don't rewrite the whole program, just correct the faulty lines.""",
        "quiz": [
            {"q": "<code>for i in range(10)</code> with no colon is a...",
             "options": ["Syntax error", "Runtime error", "Logic error", "Not an error"], "answer": 0,
             "explain": "It breaks Python's grammar rules, so the program won't start."},
            {"q": "A program to find the average divides by 2 instead of 3. It runs without crashing. This is a...",
             "options": ["Syntax error", "Runtime error", "Logic error", "Type error"], "answer": 2,
             "explain": "It runs but produces the wrong result, which is a logic error."},
            {"q": "<code>int(input())</code> crashes when the user types <code>hello</code>. This is a...",
             "options": ["Syntax error", "Runtime error", "Logic error", "Not an error"], "answer": 1,
             "explain": "The code is valid but fails while running, with a ValueError."},
            {"q": "Which type of error produces no error message?",
             "options": ["Syntax", "Runtime", "Logic", "All produce messages"], "answer": 2,
             "explain": "Logic errors give wrong results silently, so you must test to find them."},
            {"q": "<code>print(\"Total: \" + 50)</code> raises which error?",
             "options": ["NameError", "ValueError", "TypeError", "SyntaxError"], "answer": 2,
             "explain": "You can't use + to join a string and an integer. Use str(50) or a comma."},
        ],
        "challenges": [
            {"title": "Find and fix",
             "task": "This program should ask for <strong>3</strong> scores and print their average "
                     "(e.g. <code>Average: 70.0</code>). It contains one <strong>syntax</strong>, one <strong>runtime</strong> "
                     "and one <strong>logic</strong> error. Fix all three.",
             "starter": code(r'''
total = 0
for i in range(3)
    score = input("Enter score: ")
    total = total + score
average = total / 2
print("Average:", average)
'''),
             "solution": code(r'''
total = 0
for i in range(3):                       # syntax: missing colon
    score = int(input("Enter score: "))  # runtime: str + int TypeError
    total = total + score
average = total / 3                      # logic: divide by 3, not 2
print("Average:", average)
'''),
             "hint": "Run it and fix the errors one at a time: the colon, then int(), then the divisor.",
             "tests": [{"inputs": ["60", "70", "80"], "expect": ["Average: 70"]},
                       {"inputs": ["10", "20", "30"], "expect": ["Average: 20"]}]},
        ],
    },
    # ----------------------------------------------------------------- testing
    {
        "slug": "testing",
        "title": "Testing & trace tables",
        "group": "t2",
        "spec": "2.1",
        "summary": "Normal, boundary and erroneous test data, test plans, trace tables and dry runs.",
        "sections": [
            section("Why test?", """
<p>Testing shows that a program works as intended and handles unexpected input without crashing.
It's how you find <strong>logic errors</strong>, which produce no error messages. A <strong>test plan</strong> lists each test with
its purpose, the test data, the <strong>expected</strong> result and the <strong>actual</strong> result.</p>
"""),
            section("Types of test data", """
<p>Example: a program accepts an exam mark from <strong>0 to 100</strong>.</p>
<table>
<tr><th>Type</th><th>Meaning</th><th>Example data</th><th>Expected result</th></tr>
<tr><td><strong>Normal</strong></td><td>Typical, valid data the program should accept</td><td>45, 72</td><td>Accepted</td></tr>
<tr><td><strong>Boundary</strong></td><td>Values at the edges of the valid range (and just outside)</td><td>0, 100 (and -1, 101)</td><td>0 and 100 accepted, -1 and 101 rejected</td></tr>
<tr><td><strong>Erroneous</strong></td><td>Invalid data the program should reject without crashing</td><td>"abc", -20, 250, blank</td><td>Rejected with a message</td></tr>
</table>
<p>The program below runs a mini test plan on a validation function automatically:</p>
""", r'''
def is_valid_mark(text):
    return text.isdigit() and 0 <= int(text) <= 100

tests = [
    # (type, data, expected)
    ("Normal",    "45",  True),
    ("Normal",    "72",  True),
    ("Boundary",  "0",   True),
    ("Boundary",  "100", True),
    ("Boundary",  "101", False),
    ("Erroneous", "abc", False),
    ("Erroneous", "",    False),
    ("Erroneous", "-20", False),
]

print(f"{'Type':10} {'Data':6} {'Expected':9} {'Actual':7} Result")
for test_type, data, expected in tests:
    actual = is_valid_mark(data)
    result = "PASS" if actual == expected else "FAIL"
    print(f"{test_type:10} {data!r:6} {expected!s:9} {actual!s:7} {result}")
'''),
            section("Trace tables", """
<p>A <strong>trace table</strong> records the value of each variable, line by line, as you <strong>dry run</strong>
(work through by hand) an algorithm. It's used to work out what an algorithm does, to predict its output, and to find logic errors.</p>
<p>Code being traced:</p>
<pre class="filebox">total = 0
for i in range(1, 5):
    total = total + i * 2
print(total)</pre>
<table>
<tr><th>i</th><th>total</th><th>Output</th></tr>
<tr><td></td><td>0</td><td></td></tr>
<tr><td>1</td><td>2</td><td></td></tr>
<tr><td>2</td><td>6</td><td></td></tr>
<tr><td>3</td><td>12</td><td></td></tr>
<tr><td>4</td><td>20</td><td></td></tr>
<tr><td></td><td></td><td>20</td></tr>
</table>
<p>You can make Python print its own trace table to check your hand trace:</p>
""", r'''
total = 0
print("i  | total")
print("---+------")
print("   |", total)
for i in range(1, 5):
    total = total + i * 2
    print(i, " |", total)
print("Output:", total)
'''),
            section("Try a trace", """
<p>Dry-run this on paper first. What are the values of <code>a</code>, <code>b</code> and <code>c</code> each time
round the loop? Then press Run to check.</p>
""", r'''
a = 1
b = 1
print("count | a  | b  | c")
for count in range(5):
    c = a + b
    a = b
    b = c
    print(f"{count:5} | {a:2} | {b:2} | {c:2}")
'''),
        ],
        "exam_tip": """For boundary testing, give the values <strong>exactly on</strong> the boundary (and ideally just
outside it). For a range of 1–10, that's 1 and 10 (and 0 and 11).""",
        "quiz": [
            {"q": "A program accepts ages 18 to 65. Which is <strong>boundary</strong> data?",
             "options": ["30", "65", "\"forty\"", "200"], "answer": 1,
             "explain": "65 is right on the upper edge of the valid range."},
            {"q": "Entering <code>\"hello\"</code> when a number is expected is which kind of test data?",
             "options": ["Normal", "Boundary", "Erroneous", "Extreme"], "answer": 2,
             "explain": "It's invalid data the program should reject without crashing."},
            {"q": "What is a trace table used for?",
             "options": ["Storing data in a file", "Tracking variable values while dry-running an algorithm",
                         "Listing syntax errors", "Drawing flowcharts"], "answer": 1,
             "explain": "Trace tables record how variables change, step by step."},
        ],
        "challenges": [],
    },
    # -------------------------------------------------------------- algorithms
    {
        "slug": "algorithms",
        "title": "Searching & sorting algorithms",
        "group": "t1",
        "spec": "1.1",
        "summary": "Linear search, binary search, bubble sort and merge sort, coded and compared.",
        "sections": [
            section("Linear search", """
<p>Check each item <strong>in turn</strong> from the start until the target is found or the list ends.</p>
<ul><li>Works on <strong>unsorted</strong> lists.</li><li>Simple, but slow for large lists: it may check every item.</li></ul>
""", r'''
def linear_search(items, target):
    for index in range(len(items)):
        print("Checking index", index, "->", items[index])
        if items[index] == target:
            return index
    return -1

numbers = [31, 8, 72, 15, 42, 7, 99]
position = linear_search(numbers, 42)
if position != -1:
    print("Found at index", position)
else:
    print("Not found")
'''),
            section("Binary search", """
<p>Only works on a <strong>sorted</strong> list. Look at the <strong>middle</strong> item:</p>
<ol><li>If it's the target, you're done.</li>
<li>If the target is smaller, throw away the upper half. If it's larger, throw away the lower half.</li>
<li>Repeat on the half that's left until the item is found or nothing remains.</li></ol>
<p>Each step halves the list, so it's much faster than linear search on large lists: about 10 checks for 1,000 items.</p>
""", r'''
def binary_search(items, target):
    low = 0
    high = len(items) - 1
    while low <= high:
        mid = (low + high) // 2
        print(f"low={low} high={high} mid={mid} -> {items[mid]}")
        if items[mid] == target:
            return mid
        elif target < items[mid]:
            high = mid - 1        # discard upper half
        else:
            low = mid + 1         # discard lower half
    return -1

numbers = [3, 8, 15, 21, 34, 42, 57, 63, 78, 91]
print("Result:", binary_search(numbers, 57))
'''),
            section("Bubble sort", """
<p>Go through the list comparing each <strong>adjacent pair</strong> and <strong>swap</strong> them if they're in the wrong order.
After each <strong>pass</strong> the largest remaining value has "bubbled" to the end. Stop when a whole pass makes no swaps.</p>
<ul><li>Simple to code, and sorts in place without needing extra memory.</li><li>Slow for large lists.</li></ul>
""", r'''
def bubble_sort(items):
    n = len(items)
    swapped = True
    pass_number = 0
    while swapped:
        swapped = False
        pass_number = pass_number + 1
        for i in range(n - 1):
            if items[i] > items[i + 1]:
                temp = items[i]              # swap using a temporary variable
                items[i] = items[i + 1]
                items[i + 1] = temp
                swapped = True
        n = n - 1   # the last item is now in place
        print("After pass", pass_number, ":", items)
    return items

bubble_sort([5, 1, 4, 2, 8, 3])
'''),
            section("Merge sort", """
<p>A <strong>divide and conquer</strong> algorithm:</p>
<ol><li><strong>Divide</strong>: keep splitting the list in half until each sub-list has one item.</li>
<li><strong>Merge</strong>: combine pairs of sub-lists into sorted lists by repeatedly taking the smaller front item.</li></ol>
<ul><li>Much faster than bubble sort on large lists.</li><li>Needs extra memory for the sub-lists, and is more complex to code (often recursive).</li></ul>
""", r'''
def merge_sort(items, depth=0):
    print("  " * depth + "split", items)
    if len(items) <= 1:
        return items
    mid = len(items) // 2
    left = merge_sort(items[:mid], depth + 1)
    right = merge_sort(items[mid:], depth + 1)
    merged = merge(left, right)
    print("  " * depth + "merge", merged)
    return merged

def merge(left, right):
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i = i + 1
        else:
            result.append(right[j])
            j = j + 1
    while i < len(left):          # copy any leftovers
        result.append(left[i])
        i = i + 1
    while j < len(right):
        result.append(right[j])
        j = j + 1
    return result

print("Sorted:", merge_sort([38, 27, 43, 3, 9, 82, 10]))
'''),
            section("Comparing efficiency", """
<p>The <strong>efficiency</strong> of an algorithm is how much time (number of steps) or memory it needs as the input grows.
This program counts the comparisons each algorithm makes:</p>
""", r'''
import random

def linear_count(items, target):
    count = 0
    for item in items:
        count = count + 1
        if item == target:
            break
    return count

def binary_count(items, target):
    low, high, count = 0, len(items) - 1, 0
    while low <= high:
        count = count + 1
        mid = (low + high) // 2
        if items[mid] == target:
            break
        elif target < items[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return count

for size in [10, 100, 1000, 10000]:
    data = list(range(size))
    target = random.randint(0, size - 1)
    print(f"{size:6} items: linear {linear_count(data, target):6} checks, "
          f"binary {binary_count(data, target):3} checks")
'''),
        ],
        "exam_tip": """Know the <strong>conditions</strong> for each algorithm: binary search needs sorted data.
Be ready to explain the steps in words and to show the state of the list after each pass of a bubble sort.""",
        "quiz": [
            {"q": "What must be true before you can use a binary search?",
             "options": ["The list has an even length", "The list is sorted", "The list contains numbers", "The list is small"],
             "answer": 1, "explain": "Binary search discards halves based on order, so the data must be sorted."},
            {"q": "After the first pass of a bubble sort (ascending), where is the largest value?",
             "options": ["At the start", "In the middle", "At the end", "Anywhere"], "answer": 2,
             "explain": "The largest value is swapped along until it reaches the end."},
            {"q": "Which sort uses 'divide and conquer'?",
             "options": ["Bubble sort", "Merge sort", "Linear sort", "Neither"], "answer": 1,
             "explain": "Merge sort splits the list into halves and merges them back in order."},
            {"q": "Roughly how many checks does a binary search need in the worst case for 1,000 sorted items?",
             "options": ["1000", "500", "10", "100"], "answer": 2,
             "explain": "2¹⁰ = 1024, and each check halves the list, so about 10 checks."},
        ],
        "challenges": [
            {"title": "Linear search",
             "task": "Ask the user for a number to find in <code>data</code>. Using a linear search (not <code>in</code> or "
                     "<code>index()</code>), output <code>Found at index X</code> or <code>Not found</code>.",
             "starter": code(r'''
data = [14, 3, 27, 42, 8, 19]
target = int(input("Number to find: "))
'''),
             "solution": code(r'''
data = [14, 3, 27, 42, 8, 19]
target = int(input("Number to find: "))
found = False
index = 0
while index < len(data) and not found:
    if data[index] == target:
        found = True
    else:
        index = index + 1
if found:
    print("Found at index", index)
else:
    print("Not found")
'''),
             "hint": "Loop through the indexes. Stop when data[index] == target, and use a found flag.",
             "tests": [{"inputs": ["42"], "expect": ["Found at index 3"]},
                       {"inputs": ["14"], "expect": ["Found at index 0"]},
                       {"inputs": ["5"], "expect": ["Not found"]}]},
        ],
    },
    # ---------------------------------------------------------------- thinking
    {
        "slug": "thinking",
        "title": "Computational thinking & readable code",
        "group": "t1",
        "spec": "1.2 · 2.1",
        "summary": "Decomposition, abstraction, flowcharts and pseudocode, and writing maintainable code.",
        "sections": [
            section("Decomposition and abstraction", """
<ul>
<li><strong>Decomposition</strong> means breaking a problem down into smaller sub-problems that are easier to solve.
Each part often becomes a subprogram.</li>
<li><strong>Abstraction</strong> means removing unnecessary detail and focusing on what matters. A map of the
London Underground leaves out real distances and streets because passengers only need the stations and connections.</li>
<li>An <strong>algorithm</strong> is a precise sequence of steps that solves a problem. It can be written as a
<strong>flowchart</strong>, <strong>pseudocode</strong> or <strong>program code</strong>.</li>
</ul>
"""),
            section("Flowchart symbols", """
<table>
<tr><th>Symbol</th><th>Meaning</th></tr>
<tr><td>Rounded rectangle (terminator)</td><td>Start / Stop</td></tr>
<tr><td>Parallelogram</td><td>Input / Output</td></tr>
<tr><td>Rectangle</td><td>Process (e.g. <code>total = total + 1</code>)</td></tr>
<tr><td>Diamond</td><td>Decision, with Yes/No branches</td></tr>
<tr><td>Rectangle with double sides</td><td>Subprogram call</td></tr>
<tr><td>Arrow</td><td>Direction of flow</td></tr>
</table>
<p>A loop in a flowchart is a decision whose arrow points back up to an earlier step.</p>
"""),
            section("From design to code", """
<p>Example problem: <em>"A quiz has 3 questions. Ask each one, keep score, and say 'Well done' if the
user gets 2 or more."</em> Decomposed into: store the questions → ask each question → check the answer and update the
score → output the result.</p>
""", r'''
QUESTIONS = [
    ["What is 7 * 8?", "56"],
    ["What data type is True?", "boolean"],
    ["What symbol starts a comment?", "#"],
]

def ask_question(question, answer):
    """Ask one question; return True if answered correctly."""
    reply = input(question + " ")
    return reply.strip().lower() == answer

def run_quiz():
    score = 0
    for record in QUESTIONS:
        if ask_question(record[0], record[1]):
            print("Correct!")
            score = score + 1
        else:
            print("Wrong - the answer was", record[1])
    return score

final_score = run_quiz()
print("You scored", final_score, "out of", len(QUESTIONS))
if final_score >= 2:
    print("Well done")
'''),
            section("Writing maintainable code", """
<p>Paper 2 awards marks for code that other people can read and maintain. Use these four techniques:</p>
<ul>
<li><strong>Comments</strong> explain the purpose of code sections and any tricky logic</li>
<li><strong>Descriptive names</strong> for variables, constants and subprograms (<code>total_cost</code> not <code>tc</code>)</li>
<li><strong>Indentation</strong> shows the structure (Python requires it anyway)</li>
<li><strong>White space</strong>: blank lines between sections and spaces around operators</li>
</ul>
<p>Both programs below do the same thing. Which would you rather fix?</p>
""", r'''
# ----- Hard to maintain -----
a=[3,7,2]
b=0
for c in a:b=b+c
print(b/len(a))

# ----- Easy to maintain -----
# Calculate the mean number of goals per match
goals_per_match = [3, 7, 2]
total_goals = 0

for goals in goals_per_match:
    total_goals = total_goals + goals

mean_goals = total_goals / len(goals_per_match)
print("Mean goals per match:", mean_goals)
'''),
        ],
        "exam_tip": """Even when your code works, you can lose marks for poor readability. Before moving on to the next
question, add a comment for each section and rename any single-letter variables (loop counters like <code>i</code> are fine).""",
        "quiz": [
            {"q": "Breaking a problem down into smaller parts is called...",
             "options": ["Abstraction", "Decomposition", "Iteration", "Validation"], "answer": 1,
             "explain": "Decomposition splits a problem into smaller sub-problems."},
            {"q": "Which flowchart symbol represents a decision?",
             "options": ["Rectangle", "Parallelogram", "Diamond", "Oval"], "answer": 2,
             "explain": "A diamond has Yes/No (True/False) exits."},
            {"q": "Which of these does NOT make code more maintainable?",
             "options": ["Comments", "Descriptive variable names", "Putting everything on one line", "Consistent indentation"],
             "answer": 2, "explain": "Cramming code onto one line makes it harder to read and maintain."},
        ],
        "challenges": [],
    },
]


PAPER2_EXAMPLE = code(r'''
# Cinema ticket calculator
ADULT_PRICE = 8
CHILD_PRICE = 5
CHILD_AGE_LIMIT = 16


def get_valid_age():
    """Keep asking until a whole number from 0 to 120 is entered."""
    age = input("Enter age: ")
    while not age.isdigit() or int(age) > 120:
        print("Please enter an age from 0 to 120")
        age = input("Enter age: ")
    return int(age)


tickets = int(input("How many tickets? "))
total_cost = 0

for person in range(tickets):
    age = get_valid_age()
    if age < CHILD_AGE_LIMIT:
        total_cost = total_cost + CHILD_PRICE
    else:
        total_cost = total_cost + ADULT_PRICE

print("Total cost: £" + str(total_cost))
''')


PLAYGROUND_EXAMPLES = {
    "Blank": "",
    "Number guessing game": code(r'''
import random

secret = random.randint(1, 20)
guesses = 0
guess = 0
print("I'm thinking of a number from 1 to 20")
while guess != secret:
    guess = int(input("Your guess: "))
    guesses = guesses + 1
    if guess < secret:
        print("Too low")
    elif guess > secret:
        print("Too high")
print("Correct! You took", guesses, "guesses")
'''),
    "Read students.csv": code(r'''
with open("students.csv", "r") as file:
    for line in file:
        name, score = line.strip().split(",")
        print(name.ljust(8), "#" * (int(score) // 5), score)
'''),
    "Times table": code(r'''
number = int(input("Which times table? "))
for i in range(1, 13):
    print(i, "x", number, "=", i * number)
'''),
    "Bubble sort": code(r'''
items = [9, 4, 7, 1, 8, 2]
for p in range(len(items) - 1):
    for i in range(len(items) - 1 - p):
        if items[i] > items[i + 1]:
            items[i], items[i + 1] = items[i + 1], items[i]
    print("Pass", p + 1, items)
'''),
}


_BY_SLUG = {t["slug"]: t for t in TOPICS}


def get_topic(slug):
    return _BY_SLUG.get(slug)
