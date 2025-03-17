import csv
import os
import shutil
import getpass
import statistics
import time


# CSV File Handling Class
class CSVHandler:
    @staticmethod
    def get_file_path(filename):
        # Get the folder where the current Python file is located
        script_dir = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(script_dir, filename)

    def read_csv(filename):
        try:
            file_path = CSVHandler.get_file_path(filename)
            
            with open(filename, mode='r', newline='', encoding= 'utf-8') as file:
                reader = csv.reader(file)
                data = []
                for row in reader:
                    row = [cell.strip() for cell in row]  # Strip whitespace from each item
                    data.append(row)
                return data
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return []
    
    @staticmethod
    def write_csv(filename, data, mode='a'):
        file_path = CSVHandler.get_file_path(filename)
        try:
            with open(filename, mode=mode, newline='', encoding= 'utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(data)
            print(f"Data written to {filename}: {data}")
        except Exception as e:
            print(f"An error occurred while writing to {filename}: {e}")


# Student Class
class Student:
    def __init__(self, first_name, last_name, email, course_id=None, grade=None, marks=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.courses = {}  # Dictionary to store courses and grades
        if course_id and grade and marks:
            self.add_course(course_id, grade, marks)

    def add_course(self, course_id, grade, marks):
        if course_id not in self.courses:
            self.courses[course_id] = {'grade': grade, 'marks': marks}
        else:
            print(f"Course {course_id} already exists for {self.first_name} {self.last_name}.")

    @staticmethod
    def load_students():
        file_path = CSVHandler.get_file_path('students.csv')
        students_data = CSVHandler.read_csv('students.csv')
        students = {}

        for data in students_data:
            first_name, last_name, email, course_id, grade, marks = data

            if email not in students:
                students[email] = Student(first_name, last_name, email)

            students[email].add_course(course_id, grade, marks)
        return list(students.values())


    def view_grades(self):
        """ Display grades of the logged-in student """
        user = session.get_user()

        if not user:
            print("[!] No user is logged in.")
            return
        if not isinstance(user, Student):
            print("[!] This functionality is available only for students.")
            return 
        student_found = False
        for student in Student.load_students():
            if student.email == user.email:
                student_found = True
                if not student.courses:
                    print(f"No courses found for {student.first_name} {student.last_name}.")
                else:
                    print("\n--- Your Grades ---")
                    print(f"Student: {student.first_name} {student.last_name} ({student.email})")
                    print("Courses and Grades:")
                    for course_id, details in student.courses.items():
                        print(f"{course_id}: Grade - {details['grade']}, Marks - {details['marks']}")
                break

        if not student_found:
            print("[!] Student not found.")
            return

    def update_student_record(self, course_id, new_grade, new_marks):
        # Check if the student is enrolled in the course
        if course_id in self.courses:
            self.courses[course_id]['grade'] = new_grade
            self.courses[course_id]['marks'] = new_marks
            print(f"Updated record for {self.first_name} {self.last_name} in course {course_id}.")
        else:
            print(f"Student is not enrolled in the course: {course_id}.")

    def display_records(self):
        print(f"Student: {self.first_name} {self.last_name} ({self.email})")
        print("Courses and Grades:")
        for course, details in self.courses.items():
            print(f"{course}: Grade - {details['Grade']}, Marks - {details['Marks']}")

# Course Class
class Course:
    def __init__(self, course_id, course_name, description, professor_email=None):
        self.professor_email = professor_email
        self.course_id = course_id
        self.course_name = course_name
        self.description = description

    def display_course(self):
        print(f"{self.course_id}: {self.course_name} - {self.description}")

    @staticmethod
    def load_courses():

        file_path = CSVHandler.get_file_path('courses.csv')
        courses_data = CSVHandler.read_csv('courses.csv')
        courses = []
        for data in courses_data:
            courses.append(Course(*data))
        return courses
    
    @staticmethod
    def add_course(course_list, course):
        course_list.append(course)
        print("Course added successfully!")
        # Save to file
        Course.save_courses(course_list)

    @staticmethod
    def save_courses(course_list):
        data = []
        for course in course_list:
            data.append([course.course_id, course.course_name, course.description, course.professor_email])
        CSVHandler.write_csv('courses.csv', data)

# Professor Class
class Professor:
    def __init__(self, name, email, rank, course_id):
        self.name = name
        self.email = email
        self.rank = rank
        self.course_id = course_id

    def display_professor(self):
        print(f"Professor: {self.name}, Email: {self.email}, Rank: {self.rank}, Course: {self.course_id}")

    @staticmethod
    def load_professors():
        file_path = CSVHandler.get_file_path('professors.csv')
        professors_data = CSVHandler.read_csv('professors.csv')
        professors = []
        for data in professors_data:
            professors.append(Professor(*data))
        return professors
    
    @staticmethod
    def save_professors(professor_list):
        data = []
        for professor in professor_list:
            data.append([professor.name, professor.email, professor.rank, professor.course_id])
        CSVHandler.write_csv('professors.csv', data)

    def get_students_by_course(self, course_id):
        """ Retrieve students enrolled in a given course """
        students_data = CSVHandler.read_csv('students.csv')
        enrolled_students = []

        for student_data in students_data:
            first_name, last_name, email, course_id_student, grade, marks = student_data
            if course_id_student == course_id:
                enrolled_students.append(f"{first_name} {last_name} - {email}")

        return enrolled_students
    
    @staticmethod
    def add_student_to_course(first_name, last_name, email, course_id, grade, marks):
        """ Add a new student record to the students.csv """
        student_data = [first_name, last_name, email, course_id, grade, marks]
        file_path = CSVHandler.get_file_path('students.csv')
        CSVHandler.write_csv(file_path, [student_data], mode="a")  # Append new student to the file

        print(f"[+] Student {first_name} {last_name} added successfully to course {course_id}.")
    
    @staticmethod
    def delete_student_record(email, file_path="students.csv"):
        """ Delete a student record by email from the students.csv file """
        try:
            students_data = CSVHandler.read_csv('students.csv')
            updated_data = []

            # Find the student record to delete and keep other records
            student_found = False
            for student in students_data:
                if student[2] != email:  # student[2] is the email field
                    updated_data.append(student)
                else:
                    student_found = True  # Mark that we found and removed the student

            # If student was found, update the CSV
            if student_found:
                CSVHandler.write_csv('students.csv', updated_data, mode='w')  # Overwrite the file with the updated data
                print(f"[+] Student with email {email} has been deleted.")
            else:
                print(f"[!] Student with email {email} not found.")
        except FileNotFoundError:
            print(f"[!] The file 'students.csv' was not found.")
        except Exception as e:
            print(f"[!] An error occurred while deleting the student: {e}")

class StudentStatistics:
    @staticmethod
    def display_statistics():
        students = CSVHandler.read_csv('students.csv')
        
        # Ensure that the students list is not empty
        if not students:
            print("No data available.")
            return
        
        # Assuming marks are in the 6th column (index 5)
        marks = []
        for student in students:
            try:
                marks.append(int(student[5]))  # Adjust index if necessary
            except ValueError:
                continue  # Skip rows with invalid marks

        if marks:
            avg_marks = sum(marks) / len(marks)
            median_marks = statistics.median(marks)
            max_marks = max(marks)
            min_marks = min(marks)

            print(f"Average Marks: {avg_marks:.2f}")
            print(f"Median Marks: {median_marks}")
            print(f"Highest Marks: {max_marks}")
            print(f"Lowest Marks: {min_marks}")
        else:
            print("No valid marks available.") 

#Text Security Class
class TextSecurity:
    """This class encrypts the text using Caesar cipher."""
    def __init__(self, shift):
        self.shifter = shift
        self.s = self.shifter % 26

    def _convert(self, text, s):
        result = ""
        for ch in text:
            if ch.isupper():
                result += chr((ord(ch) + s - 65) % 26 + 65)
            elif ch.islower():
                result += chr((ord(ch) + s - 97) % 26 + 97)
            else:
                result += ch  # keep non-alphabet chars (like #, _, numbers)
        return result

    def encrypt(self, text):
        return self._convert(text, self.shifter)

    def decrypt(self, text):
        return self._convert(text, 26 - self.s)

#LoginUser Class
class LoginUser:
    def __init__(self, email, password, role, shift=4):
        if not email:
            raise ValueError("Email cannot be empty.")
        self.email = email
        self.password = password
        self.role = role
        self.security = TextSecurity(shift)

    def encrypt_password(self):
        return self.security.encrypt(self.password)

    def decrypt_password(self, encrypted_password):
        return self.security.decrypt(encrypted_password)

    @staticmethod
    def register_user(email, password, role, file_path="login.csv", shift=4):
        file_path = CSVHandler.get_file_path(file_path)
        if not email:
            print("[!] Email cannot be empty.")
            return False
        
        if not LoginUser.is_unique_email(email, file_path):
            print("[!] Email already exists.")
            return False

        security = TextSecurity(shift)
        encrypted = security.encrypt(password)

        if os.path.exists(file_path):
            with open(file_path, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["email"] == email:
                        print("[!] User already exists.")
                        return False

        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if os.stat(file_path).st_size == 0:
                writer.writerow(["email", "password", "role"])  # header
            writer.writerow([email, encrypted, role])
            print("[+] User registered successfully.")
            return True
        
    @staticmethod
    def is_unique_email(email, file_path="login.csv"):
        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["email"] == email:
                        return False
            return True
        except FileNotFoundError:
            return True
        return True
    
    @staticmethod
    def login_user(email, password, file_path="login.csv", shift=4):
        file_path = CSVHandler.get_file_path(file_path)
        if not email:
            print("[!] Email cannot be empty.")
            return None
        security = TextSecurity(shift)
        try:
            with open(file_path, mode='r',encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if "email" in row:
                        if row["email"] == email:
                            decrypted = security.decrypt(row["password"])
                            if decrypted.strip() == password.strip():
                                print(f"[+] Login successful! Welcome, {email}")
                                print(f"Role: {row['role']}")
                                # The rest of the code
                            
                                if row["role"] == "student":
                                
                                    student_data = CSVHandler.read_csv('students.csv')
                                    for data in student_data:
                                        if data[2] == email:
                                            first_name, last_name, _, course_id, grade, marks = data
                                            return Student(first_name, last_name, email, course_id, grade, marks)
                                    
                                elif row["role"] == "professor":
                                    professor_data = CSVHandler.read_csv('professors.csv')  
                                    for data in professor_data:
                                        if data[1] == email:
                                            name, email, rank, course_id = data
                                            return Professor(name, email, rank, course_id)
                                else:
                                    print("[!] Invalid role.")
                                    return None
                            else:
                                print("[!] Incorrect password.")
                                return None
            print("[!] User not found.")
            return None
        except FileNotFoundError:
            print("[!] Login file not found.")
            return None

    @staticmethod
    def change_password(email, new_password, file_path="login.csv", shift=4):
        security = TextSecurity(shift)
        updated = False
        rows = []

        try:

            file_path = CSVHandler.get_file_path(file_path)
            print(f"Login CSV fiel path: {file_path}")

            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    #if row["email"] == email:
                    if row.get("email", "").strip() == email.strip():
                      row["password"] = security.encrypt(new_password)
                    updated = True
                    rows.append(row)

            if updated:
                with open(file_path, mode='w', newline='') as file:
                    fieldnames = ["email", "password", "role"]
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)
                print("[+] Password updated successfully.")
            else:
                print("[!] User not found.")
        except FileNotFoundError:
            print("[!] Login file not found.")
        except Exception as e:
            print(f"[!] An error occurred while updating the password in the CSV file: {e}")

#Session Class
class Session:
    """A simple session manager for tracking logged-in users."""
    def __init__(self):
        self.logged_in_user = None  # Stores the logged-in user object

    def set_user(self, user):
        """Set the currently logged-in user."""
        self.logged_in_user = user

    def get_user(self):
        """Get the currently logged-in user."""
        return self.logged_in_user

    def clear_user(self):
        """Clear the logged-in user."""
        self.logged_in_user = None

# Create a session instance
session = Session()

# Main Application

class CheckMyGrade:
    def __init__(self):
        self.courses_list = Course.load_courses()
        self.professors_list = Professor.load_professors()
        self.student_list = Student.load_students()

    def start(self):
        while True:
        
            if session.get_user():
                print(f"Welcome back, {session.get_user().email}!")
                self.logged_in_menu()
            else:
                choice = self.main_menu()
                if choice == '1':
                    self.login()
                elif choice == '2':
                    self.register()
                elif choice == '3':
                    print("Exiting...")
                    break
                else:
                    print("Invalid choice. Please try again.")

    def main_menu(self):
        columns = shutil.get_terminal_size().columns
        print("=================================".center(columns))
        print("San Jose State University".center(columns))
        print("Check My Grade Application".center(columns))
        print("================================".center(columns))
        print("\n\n Main Menu:")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice: ")
        return choice

    def login(self):

        if session.get_user():
            print(f"Welcome back, {session.get_user().email}!")
            return
        
        columns = shutil.get_terminal_size().columns
        print("=================================".center(columns))
        print("San Jose State University".center(columns))
        print("Check My Grade Application".center(columns))
        print("================================".center(columns))
        print("\n--- Login ---")
        email = input("Enter your email: ")
        password = getpass.getpass("Enter your password: ")

        user = LoginUser.login_user(email, password)

        if user:

            session.set_user(user)
            print("Login successful!")
            self.logged_in_menu()

        else:
            print("Login failed. Please try again.")

    def register(self):
        columns = shutil.get_terminal_size().columns
        print("=================================".center(columns))
        print("San Jose State University".center(columns))
        print("Check My Grade Application".center(columns))
        print("================================".center(columns))
        print("\n--- Register ---")
        email = input("Enter email: ")
        password = getpass.getpass("Enter password: ")
        role = input("Enter role (student/professor): ")
        
        # Register using LoginUser class
        if LoginUser.register_user(email, password, role):
            print(f"[+] Registration successful! You are now a {role}.")
        else:
            print("[!] Registration failed. Please try again.")

    def logged_in_menu(self):
        """ Show options based on the logged-in user role """
        columns = shutil.get_terminal_size().columns
        print("=================================".center(columns))
        print("San Jose State University".center(columns))
        print("Check My Grade Application".center(columns))
        print("================================".center(columns))
        while True:
            print("\nLogged In Menu:")
            if isinstance(session.get_user(), Student):
                print("Student Menu")
                print("1. View My Grades")
                print("2. View Course List")
                print("3. View Professor List")
                print("4. Change Password")
                print("5. Logout")
                choice = input("Enter your choice: ")

                if choice == "1":
                    self.view_grades()
                elif choice == "2":
                    self.view_courses()
                elif choice == "3":
                    self.view_professors()
                elif choice == "4":
                    new_password = getpass.getpass("Enter new password: ")
                    LoginUser.change_password(session.get_user().email, new_password)
                elif choice == "5":
                    self.logout()
                    break
                else:
                    print("[!] Invalid choice. Please try again.")
        
            elif isinstance(session.get_user(), Professor):
                print("---Professor Menu---")
                print("1. View Students List by Course")
                print("2. Add Student Course Record")
                print("3. Delete Student Record")
                print("4. Modify Student Course Record")
                print("5. Search Time")
                print("6. Display Grade by Course or Professor or Student")
                print("7. Display Statistics")
                print("8. Change Password")
                print("9. Logout")
                print("10. Add Course")
                print("11. Add Professor")
            
                choice = input("Enter your choice: ")

                if choice == "1":
                    self.view_students_by_course()
                elif choice == "2":
                    self.add_student_record()
                elif choice == "3":
                    email = input("Enter student's email to delete course for: ")
                    Professor.delete_student_record(email)
                elif choice == "4":
                    email_to_update = input("Enter student's email to update: ")

                    student = None

                    for s in self.student_list:
                        if s.email == email_to_update:
                            student = s
                            break

                    if student is None:
                        print(f"Student with email {email_to_update} not found.")
                    else:
                        course_to_update = input("Enter course ID to update: ")
                        new_grade = input("Enter new grade: ")
                        new_marks = input("Enter new marks: ")
                        student.update_student_record(course_to_update, new_grade, new_marks)

                elif choice == "5":
                    print("Sorting records...")
                    # Implement sorting logic here
                elif choice == "6": 
                    self.display_grades()
                elif choice == "7": 
                    StudentStatistics.display_statistics()
                elif choice == "8":
                    new_password = getpass.getpass("Enter new password: ")
                    LoginUser.change_password(session.get_user().email, new_password)
                elif choice == "9":
                    self.logout()
                    break
                elif choice == '10':
                    course_id = input("Enter course ID: ")
                    course_name = input("Enter course name: ")
                    description = input("Course Description: ")
                    course = Course(course_id, course_name, description)
                    Course.add_course(self.courses_list, course)
                elif choice == '11':
                    name = input("Enter professor name: ")
                    email = input("Enter professor email: ")
                    rank = input("Enter professor rank: ")
                    course_id = input("Enter course ID: ")
                    professor = Professor(name, email, rank, course_id)
                    Professor.save_professors([professor])
                else:
                    print("[!] Invalid choice. Please try again.")   

    def view_grades(self):
        """ Display grades of the logged-in student """
        if not session.get_user():
            print("[!] No user is logged in.")
            return

        if isinstance(session.get_user(), Student):
            session.get_user().view_grades()
            return
        else:   
            print("[!] This functionality is available only for students.")
            return
        
    def view_courses(self):
        """ Display all courses available """
        if not self.courses_list:
            print("No courses available.")
        print("\n--- Available Courses ---")
        for course in self.courses_list:
            course.display_course()
   
    def view_professors(self):
        """ Display all professors available """
        if not self.professors_list:
            print("No professors available.")
        print("\n--- Available Professors ---")
        for professor in self.professors_list:
            professor.display_professor() 

    def view_students_by_course(self):
        """ View the list of students enrolled in a specific course """
        if not session.get_user():
            print("[!] No user is logged in.")
            return

        if isinstance(session.get_user(), Professor):
            professor = session.get_user()
            print("\n--- View Students List by Course ---")
            course_id = input("Enter the course ID: ")

            enrolled_students = professor.get_students_by_course(course_id)
            if enrolled_students:
                print(f"\n--- Students enrolled in {course_id} ---")
                for student in enrolled_students:
                    print(student)
            else:
                print(f"[!] No students found for course {course_id}.")
        else:
            print("[!] This functionality is available only for professors.")  

    def add_student_record(self):
        """ Allow professor to add a new student record """
        if not session.get_user():
            print("[!] No user is logged in.")
            return

        if isinstance(session.get_user(), Professor):
            professor = session.get_user()
            print("\n--- Add Student Record ---")
            first_name = input("Enter student's first name: ")
            last_name = input("Enter student's last name: ")
            email = input("Enter student's email: ")
            course_id = input("Enter course ID: ")
            grade = input("Enter grade: ")
            marks = input("Enter marks: ")

            # Add student to the course
            Professor.add_student_to_course(first_name, last_name, email, course_id, grade, marks)
        else:
            print("[!] This functionality is available only for professors.")

    def display_grades(self):
        print("\n--- Display Grade Report---")
        print("1. View by Course ID")
        print("2. View by Professor Email")
        print("3. View by Student Email")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            course_id = input("Enter course ID: ")
            print(f"\n--- Grades for Course: {course_id} ---")
            found = False
            for student in self.student_list:
                if course_id in student.courses:
                    grade = student.courses[course_id]['grade']
                    marks = student.courses[course_id]['marks']
                    print(f"{student.first_name} {student.last_name} ({student.email}): Grade = {grade}, Marks = {marks}")
                    found = True
            if not found:
                print("No records found for this course.")

        elif choice == "2":
            prof_email = input("Enter professor's email: ")

            prof_courses = [
                prof.course_id for prof in self.professors_list if prof.email == prof_email
            ]

            if not prof_courses:
                print("No professor found with email {prof_email}.")
                return
            
            print(f"\n--- Grades for Courses taught by {prof_email} ---")
            found = False
            for student in self.student_list:
                for course_id in student.courses:
                    if course_id in student.courses:
                        grade = student.courses[course_id]['grade']
                        marks = student.courses[course_id]['marks']
                        print(f"{student.first_name} {student.last_name} ({student.email}) - {course_id}: Grade = {grade}, Marks = {marks}")
                        found = True
            if not found:
                print("No student grades found for this professor.")

        elif choice == "3":
            student_email = input("Enter student email: ")
            student = next((s for s in self.student_list if s.email == student_email), None)
            if student:
                print(f"\n--- Grades for Student: {student.first_name} {student.last_name} ({student.email}) ---")
                for course_id, data in student.courses.items():
                    print(f"{course_id}: Grade = {data['grade']}, Marks = {data['marks']}")
            else:
                print("Student not found.")
        else:
            print("Invalid choice.")

    def logout(self):
        """ Log out the current user """
        if session.get_user():
            print(f"[+] Logged out successfully. Goodbye, {session.get_user().email}.")
            session.clear_user()
        else:   
            print("No user is currently logged in.")
        return


if __name__ == "__main__":
    app = CheckMyGrade()
    app.start()


