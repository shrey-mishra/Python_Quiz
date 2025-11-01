import random
import datetime
import os
from getpass import getpass

# ---------- FILE NAMES ----------
USERS_FILE   = "users.txt"
QUESTIONS_FILE = "questions.txt"  
SCORES_FILE  = "scores.txt"

# ---------- INITIALISE FILES ----------
def init_files():
    # users.txt – default admin
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            f.write("admin:admin:admin:Admin:None:None:None\n")

    # questions.txt – create if missing
    if not os.path.exists(QUESTIONS_FILE):
        default_txt = """[CATEGORY:DSA]
Which data structure uses LIFO?|Queue|Stack|Array|Linked List|Stack
Time complexity of binary search?|O(n)|O(log n)|O(n²)|O(1)|O(log n)
Which is not a stable sorting algorithm?|Merge Sort|Bubble Sort|Quick Sort|Insertion Sort|Quick Sort
In a BST, left child is ___ right child.|Equal to|Greater than|Less than|None|Less than
Hash tables resolve collision using?|Linear Probing|Binary Search|Recursion|Stack|Linear Probing

[CATEGORY:DBMS]
Which is not a type of join?|Inner|Outer|Cross|Diagonal|Diagonal
Primary key ensures?|Uniqueness|Duplicates|Null values|Sorting|Uniqueness
SQL stands for?|Simple Query Language|Structured Query Language|Standard Query Language|Sequential Query Language|Structured Query Language
Normalization reduces?|Data Integrity|Redundancy|Speed|Size|Redundancy
Which is a DDL command?|SELECT|INSERT|CREATE|UPDATE|CREATE

[CATEGORY:PYTHON]
Which is mutable?|String|Tuple|List|Frozenset|List
Python is ____ typed.|Statically|Dynamically|Weakly|Strongly|Dynamically
To create a virtual environment?|python -m venv|pip install venv|virtualenv create|env create|python -m venv
Lambda is used for?|Loops|Anonymous functions|Classes|Files|Anonymous functions
Which is not a Python keyword?|pass|global|local|yield|local
"""
        with open(QUESTIONS_FILE, "w") as f:
            f.write(default_txt.strip() + "\n")

    # scores.txt
    if not os.path.exists(SCORES_FILE):
        open(SCORES_FILE, "w").close()

# ---------- LOAD QUESTIONS FROM TXT ----------
def load_questions():
    questions = {"DSA": [], "DBMS": [], "PYTHON": []}
    current_cat = None

    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if line.startswith("[CATEGORY:"):
                current_cat = line[10:-1]      # extract DSA / DBMS / PYTHON
                continue
            if current_cat not in questions:
                continue

            parts = line.split("|")
            if len(parts) != 6:
                continue
            q = parts[0]
            opts = parts[1:5]
            ans = parts[5]
            questions[current_cat].append({
                "question": q,
                "options": opts,
                "answer": ans
            })
    return questions

# ---------- USER / SCORE HANDLING (unchanged) ----------
def save_user(user_data):
    with open(USERS_FILE, "a") as f:
        f.write(":".join(user_data) + "\n")

def load_users():
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(":")
                if len(parts) >= 7:
                    username = parts[0]
                    users[username] = {
                        "password": parts[1],
                        "role": parts[2],
                        "name": parts[3],
                        "email": parts[4],
                        "branch": parts[5],
                        "year": parts[6],
                        "contact": parts[7] if len(parts) > 7 else ""
                    }
    return users

def update_user_in_file(username, updated_data):
    lines = []
    with open(USERS_FILE, "r") as f:
        lines = f.readlines()
    with open(USERS_FILE, "w") as f:
        for line in lines:
            if line.split(":")[0] == username:
                f.write(":".join(updated_data) + "\n")
            else:
                f.write(line)

def save_score(enrollment, category, marks, total, timestamp):
    with open(SCORES_FILE, "a") as f:
        f.write(f"{enrollment}:{category}:{marks}/{total}:{timestamp}\n")

def load_scores():
    scores = []
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r") as f:
            scores = [line.strip() for line in f]
    return scores

# ---------- REGISTRATION ----------
def register():
    print("\n=== User Registration ===")
    username = input("Enter username (enrollment no): ").strip()
    if username in load_users():
        print("Username already exists!")
        return None

    password = getpass("Enter password: ")
    name = input("Enter full name: ").strip()
    email = input("Enter email: ").strip()
    branch = input("Enter branch: ").strip()
    year = input("Enter year: ").strip()
    contact = input("Enter contact: ").strip()

    user_data = [username, password, "user", name, email, branch, year, contact]
    save_user(user_data)
    print("Registration successful!")
    return username

# ---------- LOGIN ----------
def login():
    print("\n=== Login ===")
    username = input("Username: ").strip()
    password = getpass("Password: ")
    users = load_users()

    if username in users and users[username]["password"] == password:
        print(f"Welcome, {users[username]['name']}!")
        return username, users[username]["role"]
    else:
        print("Invalid credentials!")
        return None, None

# ---------- QUIZ ----------
def attempt_quiz(username, user_info):
    questions = load_questions()
    print("\n=== Select Category ===")
    print("1. DSA\n2. DBMS\n3. PYTHON")
    choice = input("Choose (1-3): ").strip()

    cat_map = {"1": "DSA", "2": "DBMS", "3": "PYTHON"}
    if choice not in cat_map:
        print("Invalid choice!")
        return

    category = cat_map[choice]
    qlist = questions[category]
    if len(qlist) < 5:
        print("Not enough questions in this category!")
        return

    random.shuffle(qlist)
    selected = qlist[:5]

    score = 0
    print(f"\nStarting {category} Quiz (5 Questions)\n")
    for i, q in enumerate(selected, 1):
        print(f"Q{i}: {q['question']}")
        for j, opt in enumerate(q['options'], 1):
            print(f"  {j}. {opt}")
        ans = input("Your answer (1-4): ").strip()
        try:
            if q['options'][int(ans)-1] == q['answer']:
                score += 1
        except:
            pass
        print()

    total = len(selected)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_score(username, category, score, total, timestamp)
    print(f"Quiz Complete! Score: {score}/{total}")

# ---------- PROFILE ----------
def view_profile(user_info):
    print("\n=== Your Profile ===")
    print(f"Name     : {user_info['name']}")
    print(f"Email    : {user_info['email']}")
    print(f"Branch   : {user_info['branch']}")
    print(f"Year     : {user_info['year']}")
    print(f"Contact  : {user_info['contact']}")

def update_profile(username):
    users = load_users()
    user = users[username]
    print("\n=== Update Profile (Leave blank to keep current) ===")
  
    name = input(f"Name [{user['name']}]: ") or user['name']
    email = input(f"Email [{user['email']}]: ") or user['email']
    branch = input(f"Branch [{user['branch']}]: ") or user['branch']
    year = input(f"Year [{user['year']}]: ") or user['year']
    contact = input(f"Contact [{user['contact']}]: ") or user['contact']

    updated = [username, user['password'], user['role'], name, email, branch, year, contact]
    update_user_in_file(username, updated)
    print("Profile updated!")

# ---------- SCORES ----------
def view_scores(username):
    print("\n=== Your Scores ===")
    found = False
    for line in load_scores():
        parts = line.split(":")
        if parts[0] == username:
            print(f"Category: {parts[1]}, Score: {parts[2]}, Date: {parts[3]}")
            found = True
    if not found:
        print("No scores yet.")

# ---------- ADMIN ----------
def admin_panel():
    while True:
        print("\n=== Admin Panel ===")
        print("1. View All Scores")
        print("2. Logout")
        ch = input("Choose: ").strip()
        if ch == "1":
            print("\nAll User Scores:")
            for line in load_scores():
                print(line.replace(":", " | "))
        elif ch == "2":
            break

# ---------- USER MENU ----------
def user_menu(username):
    users = load_users()
    user_info = users[username]

    while True:
        print("\n=== Quiz Menu ===")
        print("1. Attempt Quiz")
        print("2. View Scores")
        print("3. View Profile")
        print("4. Update Profile")
        print("5. Logout")
        choice = input("Choose (1-5): ").strip()

        if choice == "1":
            attempt_quiz(username, user_info)
        elif choice == "2":
            view_scores(username)
        elif choice == "3":
            view_profile(user_info)
        elif choice == "4":
            update_profile(username)
            users = load_users()
            user_info = users[username]
        elif choice == "5":
            print("Logged out.")
            break

# ---------- MAIN ----------
def main():
    init_files()
    while True:
        print("\n" + "="*40)
        print("     QUIZ APPLICATION")
        print("="*40)
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose (1-3): ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            username, role = login()
            if username:
                if role == "admin":
                    admin_panel()
                else:
                    user_menu(username)
        elif choice == "3":
            print("Thank you!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()