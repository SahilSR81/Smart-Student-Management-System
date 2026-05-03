# =====================================================
# Smart Student Management System (SSMS)
# =====================================================

from datetime import datetime
import os
from pathlib import Path

# =====================================================
# GLOBAL DATA STORE
# =====================================================
# Key   : roll number (string)
# Value : student record (dictionary)
students = {}

# =====================================================
# UTILITY FUNCTIONS MODULE
# Purpose: Percentage, Grade, Pass/Fail calculation
# =====================================================

def calculate_percentage(marks_list):
    # Calculate average percentage from marks list
    return sum(marks_list) / len(marks_list) if marks_list else 0.0


def calculate_grade(percentage):
    # Return grade based on percentage thresholds
    if percentage >= 90: return 'A'
    if percentage >= 75: return 'B'
    if percentage >= 60: return 'C'
    if percentage >= 40: return 'D'
    return 'F'


def calculate_status(percentage, attendance):
    # Pass if percentage >= 40% and attendance >= 75%
    return 'PASS' if percentage >= 40 and attendance >= 75 else 'FAIL'

# =====================================================
# VALIDATION MODULE
# Purpose: Validate roll number format
# =====================================================

def validate_roll_number(roll, class_number):
    # Validate roll number format: first 2 digits = class, rest = serial
    if not roll.isdigit():
        return False, "Roll number must contain only digits"
    if len(roll) < 3:
        return False, "Roll number too short"
    class_part = int(roll[:2])  # First 2 digits represent class
    serial_part = int(roll[2:])  # Remaining digits represent serial number
    if class_part != class_number:
        return False, f"Roll No. must start with class number {class_number:02d}"
    if serial_part <= 0:
        return False, "Roll No. serial must be greater than 0"
    return True, ""

# =====================================================
# ADD STUDENT MODULE
# Purpose: Add new student + store subjects & marks
# =====================================================

def add_student():
    try:
        student_name = input("Enter Student Name: ").strip()
        class_number = int(input("Enter Class (1–12): "))
        if class_number < 1 or class_number > 12:
            print("Class must be between 1 and 12")
            return

        print(f"Roll No. format for Class {class_number}: {class_number:02d}01, {class_number:02d}02 ...")
        roll_number = input("Enter Roll Number: ").strip()
        valid, message = validate_roll_number(roll_number, class_number)
        if not valid:
            print(message)
            return

        if roll_number in students:
            print("Student already exists")
            return

        attendance = int(input("Enter Attendance Percentage: "))
        if attendance < 0:
            print("Attendance cannot be negative")
            return

        print("You can add up to 12 subjects")
        # Parse subjects and marks from comma-separated input
        subject_list = [s.strip() for s in input("Enter Subjects (comma separated): ").split(',') if s.strip()]
        marks_list = list(map(int, input("Enter Marks (comma separated): ").split(',')))

        # Validate subject and marks count match and within limit
        if len(subject_list) != len(marks_list) or len(subject_list) > 12:
            print("Subject/marks count mismatch or limit exceeded")
            return
        if any(mark < 0 for mark in marks_list):
            print("Marks cannot be negative")
            return

        # Store student record in dictionary
        students[roll_number] = {
            'name': student_name,
            'class': class_number,
            'attendance': attendance,
            'records': {'subjects': subject_list, 'marks': marks_list},
            'created_on': datetime.now(),
            'last_updated': None
        }

        print("Student added successfully")
        print("Use this roll number for all future operations →", roll_number)

    except ValueError:
        print("Invalid numeric input")

# =====================================================
# UPDATE MARKS MODULE
# Purpose: Update / Add / Remove subject marks
# =====================================================

def update_marks():
    try:
        roll_number = input("Enter Roll Number: ").strip()
        student = students.get(roll_number)
        if not student:
            print("Student not found")
            return

        subject_list = student['records']['subjects']
        marks_list = student['records']['marks']

        print("1. Add/Update Marks")
        print("2. Remove Subject")
        choice = input("Enter choice: ").strip()

        if choice == '1':
            # Add or update subject marks
            new_subjects = [s.strip() for s in input("Enter Subjects: ").split(',') if s.strip()]
            new_marks = list(map(int, input("Enter Marks: ").split(',')))
            if any(mark < 0 for mark in new_marks):
                print("Marks cannot be negative")
                return

            # Update existing subject or add new one
            for subject, mark in zip(new_subjects, new_marks):
                if subject in subject_list:
                    index = subject_list.index(subject)
                    old_mark = marks_list[index]
                    marks_list[index] = mark
                    print(f"Updated {subject}: {old_mark} To {mark}")
                else:
                    subject_list.append(subject)
                    marks_list.append(mark)
                    print(f"Added {subject} with marks {mark}")

        elif choice == '2':
            # Remove subjects from student record
            remove_subjects = [s.strip() for s in input("Subjects to remove: ").split(',') if s.strip()]
            for subject in remove_subjects:
                if subject in subject_list:
                    index = subject_list.index(subject)
                    subject_list.pop(index)
                    marks_list.pop(index)  # Remove corresponding mark
                    print(f"Removed {subject}")
                else:
                    print(f"{subject} not found")
        else:
            print("Invalid choice")
            return

        # Update timestamp after modification
        student['last_updated'] = datetime.now()
        print("Marks updated successfully")

    except ValueError:
        print("Invalid numeric input")

# =====================================================
# SEARCH STUDENT MODULE
# Purpose: Search student by roll or name
# =====================================================

def search_student():
    search_key = input("Search by Roll No. or Name: ").strip()
    search_key_lower = search_key.lower()
    
    # Check if search is by roll number (exact match)
    if search_key in students:
        display_student(search_key)
        return
    
    # Search by name
    matching_students = []
    for roll_number, student in students.items():
        if student['name'].lower() == search_key_lower:
            matching_students.append(roll_number)
    
    if not matching_students:
        print("Student not found")
    elif len(matching_students) == 1:
        # Only one student found, display directly
        display_student(matching_students[0])
    else:
        # Multiple students with same name found - ask for class
        print(f"Multiple students found with name '{search_key}'")
        try:
            class_number = int(input("Enter Class (1–12): "))
            if class_number < 1 or class_number > 12:
                print("Invalid class")
                return
            
            # Filter students by class
            class_matching_students = []
            for roll in matching_students:
                if students[roll]['class'] == class_number:
                    class_matching_students.append(roll)
            
            if not class_matching_students:
                print(f"No student found with name '{search_key}' in Class {class_number}")
            elif len(class_matching_students) == 1:
                # Only one student in this class, display directly
                display_student(class_matching_students[0])
            else:
                # Multiple students with same name in same class
                print(f"Multiple students found with name '{search_key}' in Class {class_number}:")
                for roll in class_matching_students:
                    student = students[roll]
                    print(f"  Roll No.: {roll}, Class: {student['class']}")
                roll_number = input("Enter Roll No. to view details: ").strip()
                if roll_number in students:
                    # Display student even if roll number is from different class
                    display_student(roll_number)
                else:
                    print("Invalid Roll No.")
        except ValueError:
            print("Invalid input")

# =====================================================
# DISPLAY STUDENT MODULE
# Purpose: Display student marksheet
# =====================================================

def display_student(roll_number=None):
    if roll_number is None:
        roll_number = input("Enter Roll Number: ").strip()

    student = students.get(roll_number)
    if not student:
        print("Student not found")
        return

    print("\n===== MARKSHEET =====")
    print("Name:", student['name'])
    print("Class:", student['class'])
    print("Attendance:", student['attendance'], "%")
    print("Created:", student['created_on'])
    print("Last Updated:", student['last_updated'])

    # Collect all marks and display subject-wise
    all_marks = []
    for subject, mark in zip(student['records']['subjects'], student['records']['marks']):
        print(subject, ":", mark)
        all_marks.append(mark)

    # Calculate and display results
    percentage = calculate_percentage(all_marks)
    print("Percentage:", round(percentage, 2))
    print("Grade:", calculate_grade(percentage))
    print("Status:", calculate_status(percentage, student['attendance']))
    print("======================\n")

# =====================================================
# TOP RANKERS SEARCH MODULE
# Purpose: Show top 3 students class-wise
# =====================================================

def show_top_rankers():
    try:
        class_number = int(input("Enter Class (1–12): "))
        if class_number < 1 or class_number > 12:
            print("Invalid class")
            return

        # Collect all students from specified class
        class_students = []
        for roll_number, student in students.items():
            if student['class'] == class_number:
                percentage = calculate_percentage(student['records']['marks'])
                class_students.append({
                    'roll': roll_number,
                    'name': student['name'],
                    'class': class_number,
                    'attendance': student['attendance'],
                    'percentage': percentage
                })

        if not class_students:
            print("No students found in this class")
            return

        # Sort by percentage in descending order
        class_students.sort(key=lambda x: x['percentage'], reverse=True)

        print(f"\n🏆 Top 3 Rankers - Class {class_number}")
        print("--------------------------------")

        for rank, student in enumerate(class_students[:3], start=1):
            print(f"Rank {rank}")
            print("Name       :", student['name'])
            print("Roll No    :", student['roll'])
            print("Class      :", student['class'])
            print("Percentage :", round(student['percentage'], 2))
            print("Attendance :", student['attendance'], "%")
            print("--------------------------------")

    except ValueError:
        print("Invalid input")

# =====================================================
# CLASS REPORT MODULE
# Purpose: Show overall class statistics
# =====================================================

def class_report():
    if not students:
        print("No data available")
        return

    try:
        class_number = int(input("Enter Class (1–12): "))
        if class_number < 1 or class_number > 12:
            print("Invalid class")
            return

        class_students = {}
        for roll_number, student in students.items():
            if student['class'] == class_number:
                class_students[roll_number] = student

        if not class_students:
            print(f"No students found in Class {class_number}")
            return

        # Collect statistics for class report
        all_marks = []
        ranked_students = []
        failed_count = 0
        
        for roll_number, student in class_students.items():
            marks = student['records']['marks']
            all_marks.extend(marks)  # Collect all marks for class statistics
            percentage = calculate_percentage(marks)
            status = calculate_status(percentage, student['attendance'])
            
            ranked_students.append({
                'roll': roll_number,
                'name': student['name'],
                'percentage': percentage
            })
            
            if status == 'FAIL':
                failed_count += 1

        # Sort students by percentage for ranking
        ranked_students.sort(key=lambda x: x['percentage'], reverse=True)

        print(f"\nClass {class_number} Report:")
        print("-------------")
        print("Total Students:", len(class_students))
        print("Highest Marks in Class:", max(all_marks))
        print("Lowest Marks in Class:", min(all_marks))
        print("Average Score:", round(sum(all_marks) / len(all_marks), 2))
        print("Failed Students:", failed_count)

        print(f"\n🏆 Top 3 Rankers - Class {class_number}")
        print("--------------------------------")
        for rank, student in enumerate(ranked_students[:3], start=1):
            print(f"Rank {rank}")
            print("Name       :", student['name'])
            print("Roll No    :", student['roll'])
            print("Percentage :", round(student['percentage'], 2), "%")
            print("--------------------------------")

    except ValueError:
        print("Invalid input")

# =====================================================
# EXPORT REPORT MODULE
# Purpose: Export class report to TXT file
# =====================================================

def export_report():
    if not students:
        print("No data to export")
        return

    try:
        class_number = int(input("Enter Class (1–12) to export report: "))
        if class_number < 1 or class_number > 12:
            print("Invalid class")
            return

        class_students = {}
        for roll_number, student in students.items():
            if student['class'] == class_number:
                class_students[roll_number] = student

        if not class_students:
            print(f"No students found in Class {class_number}")
            return

        # Generate filename with timestamp
        filename = f"class_{class_number}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Try multiple locations for file writing
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            script_dir = os.getcwd()  # Fallback to current directory if __file__ not available
        
        possible_dirs = [
            os.getcwd(),  # Current directory
            str(Path.home() / "Downloads"),  # User's Downloads folder
            str(Path.home() / "Documents"),  # User's Documents folder
            script_dir  # Script directory
        ]
        
        # Find first writable directory
        file_path = None
        for directory in possible_dirs:
            try:
                test_path = os.path.join(directory, filename)
                # Test write permissions
                with open(test_path, 'w', encoding='utf-8') as test_file:
                    test_file.write("")  # Write empty file to test permissions
                os.remove(test_path)  # Remove test file
                file_path = test_path
                break
            except (PermissionError, OSError):
                continue
        
        if file_path is None:
            print("Error: Cannot write to any accessible directory.")
            print("Please check file permissions or close any files that might be open.")
            return

        # Calculate statistics for export
        all_marks = []
        ranked_students = []
        failed_count = 0

        for roll_number, student in class_students.items():
            marks = student['records']['marks']
            all_marks.extend(marks)
            percentage = calculate_percentage(marks)
            status = calculate_status(percentage, student['attendance'])
            
            ranked_students.append({
                'roll': roll_number,
                'name': student['name'],
                'percentage': percentage
            })
            
            if status == 'FAIL':
                failed_count += 1

        ranked_students.sort(key=lambda x: x['percentage'], reverse=True)

        # Write report to file
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(f"Class {class_number} Report\n")
                file.write(f"Generated on: {datetime.now()}\n")
                file.write("=" * 50 + "\n\n")
                file.write(f"Total Students: {len(class_students)}\n")
                file.write(f"Highest Marks in Class: {max(all_marks)}\n")
                file.write(f"Lowest Marks in Class: {min(all_marks)}\n")
                file.write(f"Average Score: {round(sum(all_marks) / len(all_marks), 2)}\n")
                file.write(f"Failed Students: {failed_count}\n\n")
                
                file.write(f"🏆 Top 3 Rankers - Class {class_number}\n")
                file.write("-" * 50 + "\n")
                for rank, student in enumerate(ranked_students[:3], start=1):
                    file.write(f"Rank {rank}\n")
                    file.write(f"Name       : {student['name']}\n")
                    file.write(f"Roll No    : {student['roll']}\n")
                    file.write(f"Percentage : {round(student['percentage'], 2)}%\n")
                    file.write("-" * 50 + "\n")

            print("Report exported successfully")
            print("File location:", file_path)
        
        except PermissionError:
            print("Error: Permission denied. The file may be open in another program.")
            print("Please close the file and try again, or check file permissions.")
        except OSError as e:
            print(f"Error writing file: {e}")
            print("Please check file permissions or disk space.")

    except ValueError:
        print("Invalid input")

# =====================================================
# ADMIN DELETE MODULE
# Purpose: Delete student record (admin only)
# =====================================================

def delete_student():
    # Admin authentication required
    if input("Username: ") == 'admin' and input("Password: ") == 'intern@2025':
        roll_number = input("Enter Roll Number to delete: ").strip()
        if roll_number in students:
            del students[roll_number]
            print("Student deleted")
        else:
            print("Student not found")
    else:
        print("Unauthorized access")

# =====================================================
# MAIN MENU MODULE
# =====================================================

def main():
    # Main menu loop
    while True:
        print("\nSmart Student Management System")
        print("1. Add Student")
        print("2. Search Student")
        print("3. Update Marks")
        print("4. Show All Students")
        print("5. Generate Class Report")
        print("6. Export Report (TXT)")
        print("7. Top Rankers")
        print("8. Delete Student (Admin)")
        print("9. Exit")

        choice = input("Enter choice: ").strip()
        if choice == '1': add_student()
        elif choice == '2': search_student()
        elif choice == '3': update_marks()
        elif choice == '4':
            # Display all students
            for roll in students:
                display_student(roll)
        elif choice == '5': class_report()
        elif choice == '6': export_report()
        elif choice == '7': show_top_rankers()
        elif choice == '8': delete_student()
        elif choice == '9': break  # Exit program
        else: print("Invalid choice")


# Entry point of the program
if __name__ == '__main__':
    main()
