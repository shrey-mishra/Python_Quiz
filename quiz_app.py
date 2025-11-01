import json
import random
import datetime
import os
from getpass import getpass

# File paths
USERS_FILE = "users.txt"
QUESTIONS_FILE = "questions.json"
SCORES_FILE = "scores.txt"

# Initialize files
def init_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            f.write("admin:admin:admin:Admin:None:None:None\n")  # default admin

    if not os.path.exists(QUESTIONS_FILE):
        default_questions = {
            "DSA": [
                {"question": "Which data structure uses LIFO?", "options": ["Queue", "Stack", "Array", "Linked List"], "answer": "Stack"},
                {"question": "Time complexity of binary search?", "options": ["O(n)", "O(log n)", "O(n^2)", "O(1)"], "answer": "O(log n)"},
                {"question": "Which is not a stable sorting algorithm?", "options": ["Merge Sort", "Bubble Sort", "Quick Sort", "Insertion Sort"], "answer": "Quick Sort"},
                {"question": "In a BST, left child is ___ right child.", "options": ["Equal to", "Greater than", "Less than", "None"], "answer": "Less than"},
                {"question": "Hash tables resolve collision using?", "options": ["Linear Probing", "Binary Search", "Recursion", "Stack"], "answer": "Linear Probing"}
            ],
            "DBMS": [
                {"question": "Which is not a type of join?", "options": ["Inner", "Outer", "Cross", "Diagonal"], "answer": "Diagonal"},
                {"question": "Primary key ensures?", "options": ["Uniqueness", "Duplicates", "Null values", "Sorting"], "answer": "Uniqueness"},
                {"question": "SQL stands for?", "options": ["Simple Query Language", "Structured Query Language", "Standard Query Language", "Sequential Query Language"], "answer": "Structured Query Language"},
                {"question": "Normalization reduces?", "options": ["Data Integrity", "Redundancy", "Speed", "Size"], "answer": "Redundancy"},
                {"question": "Which is a DDL command?", "options": ["SELECT", "INSERT", "CREATE", "UPDATE"], "answer": "CREATE"}
            ],
            "PYTHON": [
                {"question": "Which is mutable?", "options": ["String", "Tuple", "List", "Frozenset"], "answer": "List"},
                {"question": "Python is ____ typed.", "options": ["Statically", "Dynamically", "Weakly", "Strongly"], "answer": "Dynamically"},
                {"question": "To create a virtual environment?", "options": ["python -m venv", "pip install venv", "virtualenv create", "env create"], "answer": "python -m venv"},
                {"question": "Lambda is used for?", "options": ["Loops", "Anonymous functions", "Classes", "Files"], "answer": "Anonymous functions"},
                {"question": "Which is not a Python keyword?", "options": ["pass", "global", "local", "yield"], "answer": "local"}
            ]
        }
        with open(QUESTIONS_FILE, "w") as f:
            json.dump(default_questions, f, indent=2)

    if not os.path.exists(SCORES_FILE):
        open(SCORES_FILE, "w").close()

# Load questions
def load_questions():
    with open(QUESTIONS_FILE, "r") as f:
        return json.load(f)

# Save user
def save_user(user_data):
    with open(USERS_FILE, "a") as f:
        f.write(":".join(user_data) + "\n")

# Load all users
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

# Update user in file
def update_user_in_file(username, updated_data):
    lines = []
    with open(USERS_FILE, "r") as f:
        lines = f.readlines()
    with open(USERS_FILE, "w") as f:
        for line in lines:
            parts = line.strip().split(":")
            if parts[0] == username:
                f.write(":".join(updated_data) + "\n")
            else:
                f.write(line)

# Save score
def save_score(enrollment, category, marks, total, timestamp):
    with open(SCORES_FILE, "a") as f:
        f.write(f"{enrollment}:{category}:{marks}/{total}:{timestamp}\n")

# Load scores
def load_scores():
    scores = []
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, "r") as f:
            for line in f:
                scores.append(line.strip())
    return scores

# Registration
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

# Login
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

# Attempt Quiz
def attempt_quiz(username, user_info):
    questions = load_questions()
    print("\n=== Select Category ===")
    print("1. DSA\n2. DBMS\n3. PYTHON")
    choice = input("Choose (1-3): ").strip()

    categories = {"1": "DSA", "2": "DBMS", "3": "PYTHON"}
    if choice not in categories:
        print("Invalid choice!")
        return

    category = categories[choice]
    qlist = questions[category]
    random.shuffle(qlist)
    selected = qlist[:5]  # 5 random questions

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

# View Profile
def view_profile(user_info):
    print("\n=== Your Profile ===")
    print(f"Name     : {user_info['name']}")
    print(f"Email    : {user_info['email']}")
    print(f"Branch   : {user_info['branch']}")
    print(f"Year     : {user_info['year']}")
    print(f"Contact  : {user_info['contact']}")

# Update Profile
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

# View Scores
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

# Admin Panel
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

# User Menu
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
            users = load_users()  # reload
            user_info = users[username]
        elif choice == "5":
            print("Logged out.")
            break

# Main Program
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