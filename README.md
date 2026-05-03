# 🎓 Smart Student Management System (SSMS)

A terminal-based Student Management System built with **pure Python** — no external libraries required. Designed to manage student records, calculate grades, generate class reports, and export data — all from a clean command-line interface.

---

## 🚀 Features

- **Add Students** — Store name, class, roll number, subjects, marks, and attendance
- **Smart Roll Number Validation** — Roll number format enforced by class (e.g., Class 10 → `1001`, `1002`)
- **Search Students** — Search by roll number or name; handles duplicate names with class-level disambiguation
- **Update Marks** — Add new subjects, update existing marks, or remove subjects
- **Display Marksheet** — Auto-calculates percentage, grade (A–F), and pass/fail status
- **Class Report** — Shows class-wide stats: highest/lowest marks, average score, failed count, top 3 rankers
- **Export Report** — Saves class report as a `.txt` file with timestamp
- **Top Rankers** — Displays top 3 students of any class sorted by percentage
- **Admin Delete** — Password-protected student deletion

---

## 🧠 Concepts Used

| Concept | Where Used |
|---|---|
| Dictionaries | Core data store (`students` dict) |
| Functions & Modularity | Each feature is its own isolated function |
| Input Validation | Roll number format, negative marks, class range |
| String Methods | `.strip()`, `.lower()`, `.split()`, `.isdigit()` |
| List Operations | `zip()`, `append()`, `pop()`, `index()` |
| Sorting with Lambda | `sorted()` with `key=lambda` for ranking |
| File I/O | `open()`, `write()`, `Path`, `os` for export |
| `datetime` module | Timestamps on creation and updates |
| Error Handling | `try/except ValueError` throughout |
| Conditional Logic | Grade logic, pass/fail, search disambiguation |

---

## 📁 Project Structure

```
Smart_Student_Management_System/
│
├── SSMS.py          # Main application — all modules in one file
└── README.md        # Project documentation
```

---

## ▶️ How to Run

**Requirements:** Python 3.7 or above. No pip installs needed.

```bash
# Step 1: Clone the repo
git clone https://github.com/YOUR_USERNAME/Smart-Student-Management-System.git

# Step 2: Navigate into the folder
cd Smart-Student-Management-System

# Step 3: Run the program
python SSMS.py
```

> On some systems use `python3` instead of `python`

---

## 🖥️ Menu Options

```
Smart Student Management System
1. Add Student
2. Search Student
3. Update Marks
4. Show All Students
5. Generate Class Report
6. Export Report (TXT)
7. Top Rankers
8. Delete Student (Admin)
9. Exit
```

---

## 📌 Sample Usage

**Adding a student:**
```
Enter Student Name: Rahul Sharma
Enter Class (1–12): 10
Roll No. format for Class 10: 1001, 1002 ...
Enter Roll Number: 1001
Enter Attendance Percentage: 85
Enter Subjects (comma separated): Maths, Science, English
Enter Marks (comma separated): 88, 76, 91
✅ Student added successfully
```

**Viewing marksheet output:**
```
===== MARKSHEET =====
Name: Rahul Sharma
Class: 10
Attendance: 85 %
Maths : 88
Science : 76
English : 91
Percentage: 85.0
Grade: B
Status: PASS
======================
```

---

## 🔐 Admin Access

To delete a student record, admin credentials are required:

```
Username: admin
Password: admin@123
```

---

## ⚠️ Troubleshooting

| Problem | Fix |
|---|---|
| `python: command not found` | Use `python3 SSMS.py` instead |
| `SyntaxError` on run | Make sure you're on Python 3.7+ — check with `python --version` |
| Export file not found | The `.txt` file saves in the same folder as `SSMS.py` — check there first, then `~/Downloads` |
| Marks not saving after program exits | Data is stored in memory (no database) — this is by design for simplicity |
| Roll number rejected | Format must match class — Class 10 → starts with `10` (e.g., `1001`, `1002`) |
| `Invalid numeric input` error | Make sure marks and attendance are numbers, not text |

---

## 💡 Design Decisions

- **No external libraries** — Entire project uses Python's standard library only (`datetime`, `os`, `pathlib`)
- **In-memory storage** — Data lives in a Python dictionary during runtime; intentionally kept simple (no SQLite/CSV persistence) to keep focus on core Python logic
- **Modular functions** — Each menu option maps to its own function, keeping code readable and maintainable
- **Smart search** — If two students share the same name, the system asks for class → then roll number to resolve ambiguity

---

## 🛠️ Possible Extensions (Future Scope)

- [ ] CSV/JSON persistence to save data between sessions
- [ ] SQLite database integration
- [ ] GUI using `tkinter`
- [ ] Web interface using Flask
- [ ] PDF marksheet generation using `reportlab`

---

## 👨‍💻 Author

Built as a Python project to demonstrate core programming concepts — data structures, modular design, file I/O, and input validation — without relying on any third-party packages.
