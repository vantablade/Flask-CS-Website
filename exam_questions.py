"""Exam-style question library (original questions written in the style of Paper 2).

Each question is a dict:
  id, file, title, type (key of TYPES), marks, topics (lesson slugs)
  lesson:      optional slug of the lesson the question is shown inside
  scenario:    HTML task description
  files:       data files the question uses (seeded in static/py/runner.py)
  starter, solution, hint
  tests:       [{"inputs": [...], "expect": [...], "reject": [...], "label": ...}]
  mark_scheme: [{"group": str, "points": [(marks, text), ...]}]  - must total `marks`
"""
from content import code

TYPES = {
    "amend": "Amend code",
    "fix": "Find & fix errors",
    "complete": "Complete the code",
    "rearrange": "Rearrange lines",
    "write": "Write a program",
    "extended": "Extended program",
}

READABILITY = {"group": "Readability & maintainability", "points": [
    (2, "Comments explain the purpose of each section of code (1 mark for some, 2 for consistently)"),
    (2, "Descriptive names for variables, constants and subprograms (1 mark for mostly, 2 for throughout)"),
    (2, "Sensible layout: consistent indentation, white space between sections, no redundant code"),
]}


QUESTIONS = [
    # ------------------------------------------------------------------ amend
    {
        "id": "cinema-discount", "file": "ticket", "title": "Child ticket discount",
        "type": "amend", "marks": 3, "topics": ["selection", "basics"], "lesson": "selection",
        "scenario": """
<p>A cinema charges £9.50 per ticket. The program below asks for the customer's age and displays the price.</p>
<p><strong>Amend the program</strong> so that customers <strong>under 12</strong> pay <strong>half price</strong>.
The price must be displayed to <strong>2 decimal places</strong>, e.g. <code>Price: £4.75</code>.</p>""",
        "starter": code(r'''
# Cinema ticket price
TICKET_PRICE = 9.50

age = int(input("Enter age: "))
price = TICKET_PRICE
print("Price: £" + str(price))
'''),
        "solution": code(r'''
# Cinema ticket price
TICKET_PRICE = 9.50
CHILD_AGE_LIMIT = 12

age = int(input("Enter age: "))
if age < CHILD_AGE_LIMIT:
    price = TICKET_PRICE / 2
else:
    price = TICKET_PRICE
print(f"Price: £{price:.2f}")
'''),
        "hint": "Wrap the price calculation in an if / else, and use an f-string with :.2f for the output.",
        "tests": [{"inputs": ["8"], "expect": ["Price: £4.75"]},
                  {"inputs": ["12"], "expect": ["Price: £9.50"], "label": "Boundary"},
                  {"inputs": ["11"], "expect": ["Price: £4.75"], "label": "Boundary"},
                  {"inputs": ["40"], "expect": ["Price: £9.50"]}],
        "mark_scheme": [{"group": "Marking points", "points": [
            (1, "Selection with the correct condition (age < 12, or age <= 11)"),
            (1, "Price halved for children and full price otherwise"),
            (1, "Price output to exactly 2 decimal places"),
        ]}],
    },
    {
        "id": "countdown", "file": "countdown", "title": "Rocket countdown",
        "type": "amend", "marks": 2, "topics": ["iteration"], "lesson": "iteration",
        "scenario": """
<p>The program prints the numbers 1 to 10.</p>
<p><strong>Amend the program</strong> so that it prints a countdown from <strong>20 down to 0 in steps of 4</strong>
(20, 16, 12, 8, 4, 0), each on its own line, and then prints <code>Lift off!</code> once at the end.</p>""",
        "starter": code(r'''
for number in range(1, 11):
    print(number)
'''),
        "solution": code(r'''
for number in range(20, -1, -4):
    print(number)
print("Lift off!")
'''),
        "hint": "range(start, stop, step). The stop value is not included, so to reach 0 you must stop at -1.",
        "tests": [{"inputs": [], "expect": ["20\n16\n12\n8\n4\n0\nLift off!"]}],
        "mark_scheme": [{"group": "Marking points", "points": [
            (1, "range() with the correct start, stop and negative step"),
            (1, "Lift off! printed once, after (not inside) the loop"),
        ]}],
    },
    {
        "id": "pin-validation", "file": "pin", "title": "Validate a PIN",
        "type": "amend", "marks": 4, "topics": ["validation", "strings"], "lesson": "validation",
        "scenario": """
<p>The program asks the user to set a PIN, but accepts anything.</p>
<p><strong>Amend the program</strong> so that it keeps asking until the PIN is <strong>exactly 4 characters long</strong>
and contains <strong>only digits</strong>. Display <code>Invalid PIN</code> each time an invalid PIN is entered.</p>""",
        "starter": code(r'''
pin = input("Enter a 4-digit PIN: ")
print("PIN set to", pin)
'''),
        "solution": code(r'''
pin = input("Enter a 4-digit PIN: ")
while len(pin) != 4 or not pin.isdigit():
    print("Invalid PIN")
    pin = input("Enter a 4-digit PIN: ")
print("PIN set to", pin)
'''),
        "hint": "Use a while loop whose condition is True when the PIN is invalid: wrong length OR not all digits.",
        "tests": [{"inputs": ["12", "12a4", "12345", "0420"], "expect": ["Invalid PIN", "PIN set to 0420"], "label": "Erroneous then normal"},
                  {"inputs": ["9999"], "expect": ["PIN set to 9999"], "reject": ["Invalid"], "label": "Normal"}],
        "mark_scheme": [{"group": "Marking points", "points": [
            (1, "A condition-controlled loop is used to repeat the input"),
            (1, "Length check: exactly 4 characters"),
            (1, "Type check: only digits (e.g. isdigit())"),
            (1, "Error message displayed and PIN re-entered inside the loop"),
        ]}],
    },
    # -------------------------------------------------------------------- fix
    {
        "id": "fix-basket", "file": "basket", "title": "Shopping basket errors",
        "type": "fix", "marks": 5, "topics": ["errors", "iteration"], "lesson": "errors",
        "scenario": """
<p>This program should ask for the price and quantity of <strong>3</strong> items, display the total cost of the basket,
and then display <code>Free delivery</code> if the total is <strong>£50 or more</strong>.</p>
<p>There are <strong>5 errors</strong> in the program (a mix of syntax, runtime and logic errors). <strong>Find and correct them.</strong></p>""",
        "starter": code(r'''
# Shopping basket total
DELIVERY_THRESHOLD = 50
total = 0

for item in range(2):
    price = float(input("Price: "))
    quantity = input("Quantity: ")
    total = total + price * quantity

print("Total: £" + total)
if total > DELIVERY_THRESHOLD
    print("Free delivery")
'''),
        "solution": code(r'''
# Shopping basket total
DELIVERY_THRESHOLD = 50
total = 0

for item in range(3):                         # logic: 3 items, not 2
    price = float(input("Price: "))
    quantity = int(input("Quantity: "))       # runtime: convert to int
    total = total + price * quantity

print("Total: £" + str(total))                # runtime: str + float
if total >= DELIVERY_THRESHOLD:               # syntax: colon; logic: "or more" is >=
    print("Free delivery")
'''),
        "hint": "Fix the syntax error first so the program runs. Then test with a basket that totals exactly £50.",
        "tests": [{"inputs": ["10", "2", "5", "1", "25", "1"], "expect": ["£50", "Free delivery"], "label": "Boundary"},
                  {"inputs": ["1.5", "2", "2", "1", "10", "1"], "expect": ["£15"], "reject": ["Free delivery"], "label": "Normal"}],
        "mark_scheme": [{"group": "One mark per error corrected", "points": [
            (1, "Loop repeats 3 times: range(3)"),
            (1, "Quantity converted to an integer"),
            (1, "Total converted to a string (or output with a comma / f-string)"),
            (1, "Missing colon added to the if statement"),
            (1, "Comparison changed to >= so exactly £50 gets free delivery"),
        ]}],
    },
    {
        "id": "fix-binary-search", "file": "library_search", "title": "Library binary search errors",
        "type": "fix", "marks": 4, "topics": ["algorithms", "errors"], "lesson": "algorithms",
        "scenario": """
<p>A school library stores book IDs in a sorted list. The program should use a <strong>binary search</strong> to find
the position of a book ID entered by the user, or display <code>Book not found</code>.</p>
<p>There are <strong>4 errors</strong> in the program. <strong>Find and correct them.</strong></p>""",
        "starter": code(r'''
book_ids = [102, 145, 167, 203, 256, 301, 388, 412, 459, 500]

target = int(input("Enter book ID: "))
low = 0
high = len(book_ids)
found = False

while low <= high and not found:
    mid = (low + high) / 2
    if book_ids[mid] == target:
        found = True
    elif target < book_ids[mid]
        high = mid + 1
    else:
        low = mid + 1

if found:
    print("Book found at position", mid)
else:
    print("Book not found")
'''),
        "solution": code(r'''
book_ids = [102, 145, 167, 203, 256, 301, 388, 412, 459, 500]

target = int(input("Enter book ID: "))
low = 0
high = len(book_ids) - 1          # last valid index
found = False

while low <= high and not found:
    mid = (low + high) // 2       # integer division
    if book_ids[mid] == target:
        found = True
    elif target < book_ids[mid]:  # missing colon
        high = mid - 1            # discard the upper half
    else:
        low = mid + 1

if found:
    print("Book found at position", mid)
else:
    print("Book not found")
'''),
        "hint": "Indexes run from 0 to len - 1, list indexes must be integers, and when the target is smaller you move high below mid.",
        "tests": [{"inputs": ["388"], "expect": ["position 6"]},
                  {"inputs": ["102"], "expect": ["position 0"], "label": "First item"},
                  {"inputs": ["500"], "expect": ["position 9"], "label": "Last item"},
                  {"inputs": ["150"], "expect": ["Book not found"], "reject": ["found at"]},
                  {"inputs": ["999"], "expect": ["Book not found"], "reject": ["found at"]}],
        "mark_scheme": [{"group": "One mark per error corrected", "points": [
            (1, "high initialised to len(book_ids) - 1"),
            (1, "Integer division // used to calculate mid"),
            (1, "Colon added after the elif condition"),
            (1, "high = mid - 1 when the target is in the lower half"),
        ]}],
    },
    # --------------------------------------------------------------- complete
    {
        "id": "complete-temperatures", "file": "temperatures", "title": "Weekly temperatures",
        "type": "complete", "marks": 6, "topics": ["lists", "iteration"], "lesson": "lists",
        "scenario": """
<p>The list holds the midday temperature for each day of one week.</p>
<p><strong>Complete the program</strong> so that it outputs the <strong>mean</strong> temperature to 1 decimal place, the
<strong>highest</strong> temperature, and the <strong>number of days above the mean</strong>.</p>
<p>You must <strong>not</strong> use the built-in functions <code>max()</code>, <code>sum()</code> or <code>sorted()</code>.</p>""",
        "starter": code(r'''
# Daily midday temperatures for one week (degrees C)
temperatures = [18.5, 21.0, 19.5, 24.0, 22.5, 17.0, 20.5]

total = 0
highest = temperatures[0]
days_above = 0

# Calculate the total and find the highest temperature
for temp in temperatures:
    # ---- complete this section ----
    pass

mean = total / len(temperatures)

# Count the days above the mean
# ---- complete this section ----

print("Mean:", round(mean, 1))
print("Highest:", highest)
print("Days above mean:", days_above)
'''),
        "solution": code(r'''
# Daily midday temperatures for one week (degrees C)
temperatures = [18.5, 21.0, 19.5, 24.0, 22.5, 17.0, 20.5]

total = 0
highest = temperatures[0]
days_above = 0

# Calculate the total and find the highest temperature
for temp in temperatures:
    total = total + temp
    if temp > highest:
        highest = temp

mean = total / len(temperatures)

# Count the days above the mean
for temp in temperatures:
    if temp > mean:
        days_above = days_above + 1

print("Mean:", round(mean, 1))
print("Highest:", highest)
print("Days above mean:", days_above)
'''),
        "hint": "The count needs a second loop, because you can't know the mean until the first loop has finished.",
        "tests": [{"inputs": [], "expect": ["Mean: 20.4", "Highest: 24.0", "Days above mean: 4"]}],
        "mark_scheme": [{"group": "Marking points", "points": [
            (1, "Each temperature added to the running total"),
            (1, "Each temperature compared with highest"),
            (1, "highest updated when a larger value is found"),
            (1, "A second loop over the list after the mean is calculated"),
            (1, "Correct comparison with the mean (temp > mean)"),
            (1, "days_above incremented correctly"),
        ]}],
    },
    {
        "id": "complete-stock-file", "file": "stock_report", "title": "Stock report from a file",
        "type": "complete", "marks": 6, "topics": ["files", "strings"], "lesson": "files",
        "scenario": """
<p>A shop stores its products in <code>products.csv</code>. Each line holds
<code>code,name,stock level,reorder level</code>, for example <code>P02,Ruler,30,40</code>.</p>
<p><strong>Complete the program</strong> so that it displays the <strong>name</strong> of every product whose stock level is
<strong>below</strong> its reorder level, followed by the number of products that need reordering.</p>""",
        "files": ["products.csv"],
        "starter": code(r'''
# Stock report
reorder_count = 0

file = open("products.csv", "r")
for line in file:
    # Split the line into its four fields
    fields =

    name = fields[1]
    stock =
    reorder_level = int(fields[3])

    # Display the product if its stock is below the reorder level


file.close()
print("Products to reorder:", reorder_count)
'''),
        "solution": code(r'''
# Stock report
reorder_count = 0

file = open("products.csv", "r")
for line in file:
    # Split the line into its four fields
    fields = line.strip().split(",")

    name = fields[1]
    stock = int(fields[2])
    reorder_level = int(fields[3])

    # Display the product if its stock is below the reorder level
    if stock < reorder_level:
        print(name)
        reorder_count = reorder_count + 1

file.close()
print("Products to reorder:", reorder_count)
'''),
        "hint": "Remove the newline with strip() before split(\",\"), and convert the stock to an integer before comparing.",
        "tests": [{"inputs": [], "expect": ["Ruler", "Eraser", "Glue stick", "Products to reorder: 3"], "reject": ["Pencil", "Notebook"]}],
        "mark_scheme": [{"group": "Marking points", "points": [
            (1, "Newline removed from the line (strip())"),
            (1, "Line split on commas"),
            (1, "Stock level converted to an integer"),
            (1, "Correct comparison: stock < reorder_level"),
            (1, "Product name displayed when it needs reordering"),
            (1, "reorder_count incremented inside the selection"),
        ]}],
    },
    {
        "id": "complete-functions", "file": "grades", "title": "Mean and grade functions",
        "type": "complete", "marks": 5, "topics": ["subprograms", "selection"], "lesson": "subprograms",
        "scenario": """
<p>The main program reads three marks and uses two functions. <strong>Complete both functions.</strong></p>
<ul>
<li><code>calculate_mean(numbers)</code> must <strong>return</strong> the mean of a list of numbers.</li>
<li><code>get_grade(mark)</code> must <strong>return</strong> <code>Distinction</code> for 70 or more, <code>Merit</code> for 55 to
under 70, <code>Pass</code> for 40 to under 55, and <code>Fail</code> below 40.</li>
</ul>
<p>Do not change the main program.</p>""",
        "starter": code(r'''
def calculate_mean(numbers):
    # Return the mean of the numbers in the list
    pass


def get_grade(mark):
    # Return the grade for the mark
    pass


# ---- Main program (do not change) ----
marks = []
for i in range(3):
    marks.append(int(input("Enter mark: ")))
mean_mark = calculate_mean(marks)
print("Mean mark:", round(mean_mark, 1))
print("Grade:", get_grade(mean_mark))
'''),
        "solution": code(r'''
def calculate_mean(numbers):
    # Return the mean of the numbers in the list
    total = 0
    for number in numbers:
        total = total + number
    return total / len(numbers)


def get_grade(mark):
    # Return the grade for the mark
    if mark >= 70:
        return "Distinction"
    elif mark >= 55:
        return "Merit"
    elif mark >= 40:
        return "Pass"
    else:
        return "Fail"


# ---- Main program (do not change) ----
marks = []
for i in range(3):
    marks.append(int(input("Enter mark: ")))
mean_mark = calculate_mean(marks)
print("Mean mark:", round(mean_mark, 1))
print("Grade:", get_grade(mean_mark))
'''),
        "hint": "Both functions must use return, not print. Check the grade boundaries from the highest down.",
        "tests": [{"inputs": ["70", "80", "90"], "expect": ["Mean mark: 80", "Grade: Distinction"]},
                  {"inputs": ["69", "70", "69"], "expect": ["Grade: Merit"], "label": "Boundary"},
                  {"inputs": ["55", "55", "55"], "expect": ["Grade: Merit"], "label": "Boundary"},
                  {"inputs": ["40", "50", "45"], "expect": ["Grade: Pass"]},
                  {"inputs": ["10", "20", "39"], "expect": ["Grade: Fail"]}],
        "mark_scheme": [{"group": "Marking points", "points": [
            (1, "calculate_mean totals the numbers in the list"),
            (1, "calculate_mean returns total / number of items"),
            (1, "get_grade tests the boundaries in a sensible order with the correct operators"),
            (1, "All four grades produced correctly"),
            (1, "Both functions return their result rather than printing it"),
        ]}],
    },
    # -------------------------------------------------------------- rearrange
    {
        "id": "rearrange-bubble", "file": "heights", "title": "Rearrange a bubble sort",
        "type": "rearrange", "marks": 5, "topics": ["algorithms", "iteration"], "lesson": "algorithms",
        "scenario": """
<p>The lines of a program that bubble sorts a list of heights into <strong>ascending</strong> order have been jumbled up.
The indentation of each line is already correct.</p>
<p><strong>Rearrange the lines</strong> so the program works and prints the list after each pass. Do not add or remove lines
(you may delete the first comment).</p>""",
        "starter": code(r'''
# Rearrange these lines into the correct order
            heights[i + 1] = temp
    swapped = False
heights = [162, 148, 175, 151, 169]
            swapped = True
    print(heights)
        if heights[i] > heights[i + 1]:
while swapped:
            temp = heights[i]
    for i in range(len(heights) - 1):
swapped = True
            heights[i] = heights[i + 1]
'''),
        "solution": code(r'''
heights = [162, 148, 175, 151, 169]
swapped = True
while swapped:
    swapped = False
    for i in range(len(heights) - 1):
        if heights[i] > heights[i + 1]:
            temp = heights[i]
            heights[i] = heights[i + 1]
            heights[i + 1] = temp
            swapped = True
    print(heights)
'''),
        "hint": "Start with the two lines that aren't indented. A swap needs the temp line first.",
        "tests": [{"inputs": [], "expect": ["[148, 162, 151, 169, 175]", "[148, 151, 162, 169, 175]"]}],
        "mark_scheme": [{"group": "Marking points", "points": [
            (1, "List and swapped flag initialised before the while loop"),
            (1, "swapped set to False at the start of every pass"),
            (1, "for loop inside the while loop, with the if inside the for loop"),
            (1, "Swap lines in the correct order (temp first) and swapped set to True"),
            (1, "print inside the while loop but after the for loop"),
        ]}],
    },
    {
        "id": "rearrange-login", "file": "login", "title": "Rearrange a login check",
        "type": "rearrange", "marks": 4, "topics": ["validation", "iteration"], "lesson": "validation",
        "scenario": """
<p>The lines of a login program have been jumbled. The user has <strong>3 attempts</strong> in total to enter the password.
After a wrong attempt it displays <code>Wrong password</code>. At the end it displays <code>Access granted</code> or
<code>Access denied</code>.</p>
<p><strong>Rearrange the lines</strong> so the program works. The indentation of each line is already correct.</p>""",
        "starter": code(r'''
    guess = input("Password: ")
if guess == PASSWORD:
attempts = 0
    print("Access denied")
while guess != PASSWORD and attempts < 2:
PASSWORD = "Secret42"
    print("Wrong password")
    print("Access granted")
guess = input("Password: ")
else:
    attempts = attempts + 1
'''),
        "solution": code(r'''
PASSWORD = "Secret42"
attempts = 0
guess = input("Password: ")
while guess != PASSWORD and attempts < 2:
    attempts = attempts + 1
    print("Wrong password")
    guess = input("Password: ")
if guess == PASSWORD:
    print("Access granted")
else:
    print("Access denied")
'''),
        "hint": "The first guess happens before the loop, and the re-guess is the last line inside it.",
        "tests": [{"inputs": ["Secret42"], "expect": ["Access granted"], "reject": ["Wrong"]},
                  {"inputs": ["abc", "Secret42"], "expect": ["Wrong password", "Access granted"]},
                  {"inputs": ["a", "b", "Secret42"], "expect": ["Access granted"], "label": "Third attempt"},
                  {"inputs": ["a", "b", "c"], "expect": ["Access denied"], "reject": ["granted"]}],
        "mark_scheme": [{"group": "Marking points", "points": [
            (1, "Constant, counter and first input before the loop"),
            (1, "Counter incremented and message shown inside the loop"),
            (1, "New guess input as the last step inside the loop"),
            (1, "if / else after the loop to show the outcome"),
        ]}],
    },
    # ------------------------------------------------------------------ write
    {
        "id": "password-strength", "file": "password_strength", "title": "Password strength checker",
        "type": "write", "marks": 8, "topics": ["strings", "selection", "iteration"], "lesson": "strings",
        "scenario": """
<p><strong>Write a program</strong> that asks the user for a password and rates its strength using four rules:</p>
<ol><li>at least 8 characters long</li><li>contains an uppercase letter</li>
<li>contains a lowercase letter</li><li>contains a digit</li></ol>
<p>Output <code>Strength: Strong</code> if all four rules are met, <code>Strength: Medium</code> if 2 or 3 are met, and
<code>Strength: Weak</code> otherwise. Also display a message for each rule that is <strong>not</strong> met.</p>""",
        "starter": code(r'''
# Password strength checker
'''),
        "solution": code(r'''
# Password strength checker
MIN_LENGTH = 8

password = input("Enter a password: ")

# Check each character for the three character rules
has_upper = False
has_lower = False
has_digit = False
for character in password:
    if character.isupper():
        has_upper = True
    elif character.islower():
        has_lower = True
    elif character.isdigit():
        has_digit = True

# Count the rules met and report any that were not
rules_met = 0
if len(password) >= MIN_LENGTH:
    rules_met = rules_met + 1
else:
    print("Rule not met: at least", MIN_LENGTH, "characters")
if has_upper:
    rules_met = rules_met + 1
else:
    print("Rule not met: an uppercase letter")
if has_lower:
    rules_met = rules_met + 1
else:
    print("Rule not met: a lowercase letter")
if has_digit:
    rules_met = rules_met + 1
else:
    print("Rule not met: a digit")

if rules_met == 4:
    strength = "Strong"
elif rules_met >= 2:
    strength = "Medium"
else:
    strength = "Weak"
print("Strength:", strength)
'''),
        "hint": "Use three Boolean flags set while looping through the characters, then count how many rules are True.",
        "tests": [{"inputs": ["Passw0rdX"], "expect": ["Strength: Strong"]},
                  {"inputs": ["password"], "expect": ["Strength: Medium"]},
                  {"inputs": ["Ab1"], "expect": ["Strength: Medium"]},
                  {"inputs": ["PASS1"], "expect": ["Strength: Medium"]},
                  {"inputs": ["pass"], "expect": ["Strength: Weak"]},
                  {"inputs": [""], "expect": ["Strength: Weak"], "label": "Erroneous"}],
        "mark_scheme": [{"group": "Marking points", "points": [
            (1, "Password input"),
            (1, "Length check (at least 8)"),
            (1, "Loop through each character of the password"),
            (1, "Uppercase letter detected"),
            (1, "Lowercase letter detected"),
            (1, "Digit detected"),
            (1, "Correct Strong / Medium / Weak classification"),
            (1, "A message for each rule that is not met"),
        ]}],
    },
    {
        "id": "caesar-cipher", "file": "caesar", "title": "Caesar cipher encryption",
        "type": "write", "marks": 10, "topics": ["strings", "subprograms", "validation"],
        "scenario": """
<p><strong>Write a program</strong> that encrypts a message using a Caesar cipher. The program must:</p>
<ul>
<li>ask the user for a message</li>
<li>ask for a shift and validate it, so that only a <strong>whole number from 1 to 25</strong> is accepted</li>
<li>use a <strong>function</strong> <code>encrypt(message, shift)</code> that <strong>returns</strong> the encrypted message</li>
<li>shift letters only, keeping their case, and wrap around from Z back to A</li>
<li>leave spaces, digits and punctuation unchanged</li>
<li>output the result in the form <code>Encrypted: Khoor, Zruog!</code></li>
</ul>""",
        "starter": code(r'''
# Caesar cipher
'''),
        "solution": code(r'''
# Caesar cipher
MIN_SHIFT = 1
MAX_SHIFT = 25


def encrypt(message, shift):
    """Return the message encrypted with a Caesar cipher."""
    result = ""
    for character in message:
        if character.isupper():
            result = result + chr((ord(character) - ord("A") + shift) % 26 + ord("A"))
        elif character.islower():
            result = result + chr((ord(character) - ord("a") + shift) % 26 + ord("a"))
        else:
            result = result + character   # spaces, digits, punctuation
    return result


def get_shift():
    """Keep asking until a whole number from 1 to 25 is entered."""
    shift = input("Enter shift (1-25): ")
    while not shift.isdigit() or not (MIN_SHIFT <= int(shift) <= MAX_SHIFT):
        print("Invalid shift")
        shift = input("Enter shift (1-25): ")
    return int(shift)


message = input("Enter message: ")
shift = get_shift()
print("Encrypted:", encrypt(message, shift))
'''),
        "hint": "Convert a letter to 0-25 with ord(letter) - ord(\"A\"), add the shift, use % 26 to wrap, then convert back with chr().",
        "tests": [{"inputs": ["Hello, World!", "3"], "expect": ["Encrypted: Khoor, Zruog!"]},
                  {"inputs": ["xyz", "0", "30", "abc", "2"], "expect": ["Encrypted: zab"], "label": "Invalid shifts, then wrap-around"},
                  {"inputs": ["Zebra 99", "25"], "expect": ["Encrypted: Ydaqz 99"], "label": "Boundary"}],
        "mark_scheme": [{"group": "Marking points", "points": [
            (1, "Message input"),
            (1, "Shift input"),
            (1, "Validation loop re-prompts until the shift is valid"),
            (1, "Type check: non-numeric shifts rejected without crashing"),
            (1, "Range check: 1 to 25"),
            (1, "encrypt function with message and shift parameters that returns the result"),
            (1, "Loop through each character of the message"),
            (1, "Letters shifted using ord() and chr()"),
            (1, "Wrap-around handled (e.g. % 26)"),
            (1, "Case preserved and non-letters unchanged"),
        ]}],
    },
    {
        "id": "rainfall-analysis", "file": "rainfall", "title": "Annual rainfall analysis",
        "type": "write", "marks": 12, "topics": ["files", "lists", "algorithms"],
        "scenario": """
<p>The file <code>rainfall.txt</code> holds one line per month in the form <code>Jan,78</code> (month, rainfall in mm).</p>
<p><strong>Write a program</strong> that reads the file and outputs:</p>
<ul>
<li><code>Total rainfall: 733 mm</code></li>
<li>the mean monthly rainfall to 1 decimal place, e.g. <code>Mean: 61.1 mm</code></li>
<li>the wettest and driest months, e.g. <code>Wettest month: Nov (90 mm)</code> and <code>Driest month: ...</code></li>
<li>the number of months with above-mean rainfall, e.g. <code>Months above mean: 4</code></li>
</ul>
<p>You must <strong>not</strong> use <code>max()</code>, <code>min()</code>, <code>sum()</code> or <code>sorted()</code>.</p>""",
        "files": ["rainfall.txt"],
        "starter": code(r'''
# Rainfall analysis
'''),
        "solution": code(r'''
# Rainfall analysis
months = []
rainfall = []

# Read each month and its rainfall into two parallel lists
with open("rainfall.txt", "r") as file:
    for line in file:
        fields = line.strip().split(",")
        months.append(fields[0])
        rainfall.append(int(fields[1]))

# Total, wettest and driest in one pass
total = 0
wettest = 0
driest = 0
for i in range(len(rainfall)):
    total = total + rainfall[i]
    if rainfall[i] > rainfall[wettest]:
        wettest = i
    if rainfall[i] < rainfall[driest]:
        driest = i
mean = total / len(rainfall)

# Count months above the mean
above_mean = 0
for amount in rainfall:
    if amount > mean:
        above_mean = above_mean + 1

print("Total rainfall:", total, "mm")
print("Mean:", round(mean, 1), "mm")
print("Wettest month:", months[wettest], "(" + str(rainfall[wettest]) + " mm)")
print("Driest month:", months[driest], "(" + str(rainfall[driest]) + " mm)")
print("Months above mean:", above_mean)
'''),
        "hint": "Store the month names and the amounts in two lists with matching indexes, and keep track of the index of the wettest and driest month.",
        "tests": [{"inputs": [], "expect": ["Total rainfall: 733", "Mean: 61.1", "Wettest month: Nov",
                                            "Driest month: Jul", "Months above mean: 4"]}],
        "mark_scheme": [{"group": "Marking points", "points": [
            (1, "File opened for reading"),
            (1, "Loop reads every line"),
            (1, "Each line stripped and split on the comma"),
            (1, "Rainfall converted to an integer"),
            (1, "Months and rainfall stored in a suitable data structure"),
            (1, "Total calculated"),
            (1, "Mean calculated and output to 1 decimal place"),
            (1, "Wettest month found without max()"),
            (1, "Driest month found without min()"),
            (1, "Months above the mean counted after the mean is known"),
            (1, "Outputs include month names and use the required format"),
            (1, "File closed (or a with block used)"),
        ]}],
    },
    # --------------------------------------------------------------- extended
    {
        "id": "fitness-tracker", "file": "fitness", "title": "Weekly fitness tracker",
        "type": "extended", "marks": 20, "topics": ["validation", "lists", "subprograms", "selection", "thinking"],
        "scenario": """
<p>A fitness app records the number of steps a user walks each day for one week. <strong>Write a program</strong> that:</p>
<ul>
<li>asks for the steps for each day using the day name, e.g. <code>Steps on Mon: </code></li>
<li>validates each entry as a <strong>whole number from 0 to 50000</strong>, displaying an error message and asking again
until it's valid</li>
<li>stores the seven values in a list</li>
<li>outputs <code>Total steps: ...</code> and <code>Average: ...</code> (to 1 decimal place)</li>
<li>outputs the best day and its steps, e.g. <code>Best day: Wed (15000)</code>. If there's a tie, use the first day.
Don't use <code>max()</code>.</li>
<li>outputs how many days met the 10,000-step goal, e.g. <code>Goal met on 4 days</code></li>
<li>outputs an award: <code>Award: Gold</code> (all 7 days), <code>Silver</code> (5–6 days), <code>Bronze</code> (3–4 days),
otherwise <code>Award: Keep going!</code></li>
</ul>
<p>Your program must use <strong>at least two subprograms</strong>. Marks are also given for readability.</p>""",
        "starter": code(r'''
# Weekly fitness tracker
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
GOAL = 10000
MAX_STEPS = 50000

# Write your program below
'''),
        "solution": code(r'''
# Weekly fitness tracker
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
GOAL = 10000
MAX_STEPS = 50000


def get_steps(day):
    """Ask for a day's steps until a whole number from 0 to MAX_STEPS is entered."""
    steps = input("Steps on " + day + ": ")
    while not steps.isdigit() or int(steps) > MAX_STEPS:
        print("Invalid - enter a whole number from 0 to", MAX_STEPS)
        steps = input("Steps on " + day + ": ")
    return int(steps)


def find_best_day(step_counts):
    """Return the index of the first day with the most steps."""
    best = 0
    for i in range(1, len(step_counts)):
        if step_counts[i] > step_counts[best]:
            best = i
    return best


def get_award(days_met):
    """Return the award for the number of days the goal was met."""
    if days_met == 7:
        return "Gold"
    elif days_met >= 5:
        return "Silver"
    elif days_met >= 3:
        return "Bronze"
    else:
        return "Keep going!"


# ---- Main program ----
weekly_steps = []
for day in DAYS:
    weekly_steps.append(get_steps(day))

# Total steps and number of days the goal was met
total = 0
days_met = 0
for steps in weekly_steps:
    total = total + steps
    if steps >= GOAL:
        days_met = days_met + 1

best = find_best_day(weekly_steps)

print("Total steps:", total)
print("Average:", round(total / len(DAYS), 1))
print("Best day:", DAYS[best], "(" + str(weekly_steps[best]) + ")")
print("Goal met on", days_met, "days")
print("Award:", get_award(days_met))
'''),
        "hint": "Decompose it: one function to get a valid day's steps, one to find the best day, and one for the award.",
        "tests": [{"inputs": ["12000", "8000", "15000", "10000", "9000", "11000", "7000"],
                   "expect": ["Total steps: 72000", "Average: 10285.7", "Best day: Wed (15000)", "Goal met on 4 days", "Award: Bronze"],
                   "label": "Normal week"},
                  {"inputs": ["abc", "-5", "60000", "10000", "10000", "10000", "10000", "10000", "10000", "10000"],
                   "expect": ["Invalid", "Total steps: 70000", "Best day: Mon", "Goal met on 7 days", "Award: Gold"],
                   "label": "Erroneous entries, tie for best"},
                  {"inputs": ["10000", "20000", "10000", "10000", "10000", "5", "5"],
                   "expect": ["Total steps: 60010", "Best day: Tue (20000)", "Goal met on 5 days", "Award: Silver"],
                   "label": "Boundary: exactly the goal"},
                  {"inputs": ["0", "0", "0", "0", "0", "0", "50000"],
                   "expect": ["Total steps: 50000", "Best day: Sun", "Goal met on 1 days", "Award: Keep going!"],
                   "label": "Boundary: 0 and 50000"}],
        "mark_scheme": [{"group": "Functionality", "points": [
            (1, "Constants used for the goal and the maximum"),
            (1, "Loop over the 7 days with the day name shown in the prompt"),
            (1, "Validation loop re-prompts until the value is valid"),
            (1, "Non-numeric input rejected without crashing"),
            (1, "Range check 0 to 50000 (both ends accepted)"),
            (1, "Steps stored in a list"),
            (1, "Total calculated correctly"),
            (1, "Average output to 1 decimal place"),
            (1, "Best day found without max(), using the first day on a tie"),
            (1, "Best day name and its steps output"),
            (1, "Days meeting the goal counted (>= 10000)"),
            (1, "Award selection with the correct boundaries"),
            (1, "At least two subprograms using parameters and/or return values"),
            (1, "All outputs in the required format"),
        ]}, READABILITY],
    },
    {
        "id": "cinema-booking", "file": "cinema_booking", "title": "Cinema seat booking",
        "type": "extended", "marks": 20, "topics": ["lists", "validation", "iteration", "subprograms", "thinking"],
        "scenario": """
<p>A small cinema has <strong>5 rows (A–E)</strong> of <strong>8 seats</strong>. Seats cost £6 in rows A–B, £8 in rows C–D
and £10 in row E. <strong>Write a program</strong> that:</p>
<ul>
<li>stores the seating plan in a <strong>2D list</strong>, with every seat free at the start</li>
<li>repeatedly asks <code>Row (A-E) or X to finish: </code>, accepting upper or lower case</li>
<li>displays <code>Invalid row</code> for anything other than A–E or X, then asks for the row again</li>
<li>asks for a seat number and validates it as a whole number from 1 to 8, asking again until it's valid</li>
<li>displays <code>Seat already booked</code> if the seat is taken. Otherwise it books the seat, adds its price to the total,
and displays e.g. <code>Booked C5</code></li>
<li>when X is entered, displays the seating plan with one row per line, e.g. <code>A OOXOOOOO</code>
(<code>O</code> = free, <code>X</code> = booked), then <code>Seats booked: 2</code> and <code>Total cost: £16</code></li>
</ul>
<p>Use subprograms where appropriate. Marks are also given for readability.</p>""",
        "starter": code(r'''
# Cinema seat booking
ROWS = "ABCDE"
SEATS_PER_ROW = 8

# Write your program below
'''),
        "solution": code(r'''
# Cinema seat booking
ROWS = "ABCDE"
SEATS_PER_ROW = 8
FREE = "O"
BOOKED = "X"


def row_price(row_index):
    """Return the ticket price for a row (0 = row A)."""
    if row_index <= 1:
        return 6
    elif row_index <= 3:
        return 8
    else:
        return 10


def get_seat_number():
    """Keep asking until a seat number from 1 to SEATS_PER_ROW is entered."""
    seat = input("Seat (1-8): ")
    while not seat.isdigit() or not (1 <= int(seat) <= SEATS_PER_ROW):
        print("Invalid seat")
        seat = input("Seat (1-8): ")
    return int(seat)


def show_plan(plan):
    """Display each row letter followed by its seats."""
    for row_index in range(len(plan)):
        line = ROWS[row_index] + " "
        for seat in plan[row_index]:
            line = line + seat
        print(line)


# ---- Main program ----
plan = []
for row_index in range(len(ROWS)):
    plan.append([FREE] * SEATS_PER_ROW)

total_cost = 0
seats_booked = 0

row = input("Row (A-E) or X to finish: ").upper()
while row != "X":
    if len(row) != 1 or row not in ROWS:
        print("Invalid row")
    else:
        row_index = ROWS.index(row)
        seat = get_seat_number()
        if plan[row_index][seat - 1] == BOOKED:
            print("Seat already booked")
        else:
            plan[row_index][seat - 1] = BOOKED
            total_cost = total_cost + row_price(row_index)
            seats_booked = seats_booked + 1
            print("Booked", row + str(seat))
    row = input("Row (A-E) or X to finish: ").upper()

show_plan(plan)
print("Seats booked:", seats_booked)
print("Total cost: £" + str(total_cost))
'''),
        "hint": "Convert the row letter to an index with ROWS.index(row), and remember seat 1 is index 0.",
        "tests": [{"inputs": ["A", "3", "e", "8", "X"],
                   "expect": ["Booked A3", "A OOXOOOOO", "E OOOOOOOX", "Seats booked: 2", "Total cost: £16"],
                   "label": "Normal, lower-case row"},
                  {"inputs": ["C", "5", "C", "5", "Z", "B", "0", "9", "1", "x"],
                   "expect": ["Seat already booked", "Invalid row", "B XOOOOOOO", "C OOOOXOOO", "Seats booked: 2", "Total cost: £14"],
                   "label": "Double booking and invalid input"},
                  {"inputs": ["D", "abc", "2", "X"], "expect": ["Booked D2", "Seats booked: 1", "Total cost: £8"],
                   "label": "Erroneous seat"},
                  {"inputs": ["X"], "expect": ["A OOOOOOOO", "E OOOOOOOO", "Seats booked: 0", "Total cost: £0"],
                   "label": "No bookings"}],
        "mark_scheme": [{"group": "Functionality", "points": [
            (1, "2D list created for 5 rows of 8 free seats"),
            (1, "Booking loop repeats until X is entered"),
            (1, "X (and row letters) accepted in either case"),
            (1, "Row validated as A to E"),
            (1, "Row letter converted to a list index"),
            (1, "Seat validated as 1 to 8, including non-numeric input"),
            (1, "Seat number converted to an index (minus 1)"),
            (1, "Already-booked seats detected and reported"),
            (1, "Seat marked as booked in the 2D list"),
            (1, "Correct price for each row"),
            (1, "Running total and count of seats booked"),
            (1, "Seating plan displayed using nested iteration"),
            (1, "Plan shows row letters with O / X in the required format"),
            (1, "Subprograms used appropriately"),
        ]}, READABILITY],
    },
    {
        "id": "stock-menu", "file": "stock_system", "title": "Stationery stock system",
        "type": "extended", "marks": 15, "topics": ["files", "subprograms", "algorithms", "iteration"],
        "scenario": """
<p>A school shop keeps its stock in <code>products.csv</code>, one product per line:
<code>code,name,stock level,reorder level</code>. <strong>Write a program</strong> that:</p>
<ul>
<li>reads the file <strong>once</strong> into a suitable data structure at the start</li>
<li>repeatedly displays a menu, <code>1 Search for a product</code>, <code>2 Low stock report</code> and <code>3 Quit</code>,
until the user chooses 3, then displays <code>Goodbye</code></li>
<li>displays <code>Invalid option</code> for any other choice</li>
<li><strong>Option 1</strong> asks for a product code (upper or lower case) and displays e.g. <code>Ruler: 30 in stock</code>,
or <code>Product not found</code> just once if there's no match</li>
<li><strong>Option 2</strong> displays the name of every product below its reorder level, then e.g. <code>Products to reorder: 3</code></li>
</ul>
<p>Use a subprogram for each menu option. Marks are also given for readability.</p>""",
        "files": ["products.csv"],
        "starter": code(r'''
# Stationery stock system
# products.csv fields: code, name, stock level, reorder level
STOCK_FILE = "products.csv"

# Write your program below
'''),
        "solution": code(r'''
# Stationery stock system
# products.csv fields: code, name, stock level, reorder level
STOCK_FILE = "products.csv"


def load_products(filename):
    """Read the file into a list of [code, name, stock, reorder_level] records."""
    products = []
    with open(filename, "r") as file:
        for line in file:
            fields = line.strip().split(",")
            products.append([fields[0], fields[1], int(fields[2]), int(fields[3])])
    return products


def search_product(products):
    """Linear search for a product code entered by the user."""
    code = input("Enter product code: ").upper()
    found = False
    for record in products:
        if record[0] == code:
            print(record[1] + ":", record[2], "in stock")
            found = True
    if not found:
        print("Product not found")


def low_stock_report(products):
    """Display every product below its reorder level."""
    count = 0
    for record in products:
        if record[2] < record[3]:
            print(record[1])
            count = count + 1
    print("Products to reorder:", count)


# ---- Main program ----
products = load_products(STOCK_FILE)
choice = ""
while choice != "3":
    print("1 Search for a product")
    print("2 Low stock report")
    print("3 Quit")
    choice = input("Choose an option: ")
    if choice == "1":
        search_product(products)
    elif choice == "2":
        low_stock_report(products)
    elif choice != "3":
        print("Invalid option")
print("Goodbye")
'''),
        "hint": "Load the file into a 2D list in a function that returns it, then pass that list to each menu function.",
        "tests": [{"inputs": ["1", "p02", "3"], "expect": ["Ruler: 30 in stock", "Goodbye"], "reject": ["Product not found"],
                   "label": "Lower-case search"},
                  {"inputs": ["1", "P99", "2", "3"], "expect": ["Product not found", "Glue stick", "Products to reorder: 3", "Goodbye"]},
                  {"inputs": ["7", "3"], "expect": ["Invalid option", "Goodbye"], "label": "Erroneous option"}],
        "mark_scheme": [{"group": "Functionality", "points": [
            (1, "File read once into a list of records"),
            (1, "Numeric fields converted to integers"),
            (1, "Menu repeats until option 3"),
            (1, "Invalid options reported"),
            (1, "Product code search is case-insensitive"),
            (1, "Linear search through all records"),
            (1, "Found product output in the required format"),
            (1, "Product not found shown once, only when there is no match"),
            (1, "Low stock compares stock with reorder level"),
            (1, "Number of products to reorder output"),
            (1, "A subprogram for each menu option"),
        ]}, {"group": "Readability & maintainability", "points": [
            (1, "Comments explain the purpose of the code"),
            (1, "Descriptive names for variables, constants and subprograms"),
            (1, "Consistent layout and white space"),
            (1, "Data passed using parameters and return values rather than globals"),
        ]}],
    },
]

for _number, _q in enumerate(QUESTIONS, start=1):
    _q["number"] = _number
    _q["filename"] = f"Q{_number:02d}_{_q['file']}.py"
    _q.setdefault("files", [])
    _q.setdefault("lesson", None)

_BY_ID = {q["id"]: q for q in QUESTIONS}


def get_question(qid):
    return _BY_ID.get(qid)
