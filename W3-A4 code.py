import sqlite3

class Course: # Course class to handle course-related operations
    def __init__(self, cou_id, cou_name, cou_credit, cou_departmen):# Constructor to initialize course details
        self.cou_id = cou_id
        self.cou_name = cou_name
        self.cou_credit = cou_credit
        self.cou_departmen = cou_departmen
      
    def append_course(self, conn):# Method to insert course into the database
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO Course (COU_ID, COU_NAME, COU_CREDIT, COU_DEPARTMEN)
                VALUES (?, ?, ?, ?);
            """, (self.cou_id, self.cou_name, self.cou_credit, self.cou_departmen))
            conn.commit()
            
            print(f"Course '{self.cou_name}' inserted successfully.")

        except sqlite3.IntegrityError as e:

            print(f"Error inserting course {self.cou_name}: {e}. (Check if Teacher T_ID={self.t_id} exists)")

class Teacher: # Teacher class to handle teacher-related operations
    def __init__(self, t_id, t_fname, t_lname, t_rank):
        self.t_id = t_id
        self.t_fname = t_fname
        self.t_lname = t_lname
        self.t_rank = t_rank

    def append_teacher(self, conn):# Method to insert teacher into the database
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Teacher (T_ID, T_FNAME, T_LNAME, T_RANK)
                VALUES (?, ?, ?, ?);
            """, (self.t_id, self.t_fname, self.t_lname, self.t_rank))
            conn.commit()
            print(f"Teacher '{self.t_fname} {self.t_lname}' inserted successfully.")
        except sqlite3.IntegrityError as e:
            print(f"Error inserting teacher {self.t_fname}: {e}")

class Student:# Student class to handle student-related operations
    def __init__(self, stu_id, stu_fname, stu_lname, stu_birthd):
        self.stu_id = stu_id
        self.stu_fname = stu_fname
        self.stu_lname = stu_lname
        self.stu_birthd = stu_birthd

    def append_student(self, conn):# Method to insert student into the database
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Student (STU_ID, STU_FNAME, STU_LNAME, STU_BIRTHD)
                VALUES (?, ?, ?, ?);
            """, (self.stu_id, self.stu_fname, self.stu_lname, self.stu_birthd))
            conn.commit()
            print(f"Student '{self.stu_fname} {self.stu_lname}' inserted successfully.")
        except sqlite3.IntegrityError as e:
            print(f"Error inserting student {self.stu_fname}: {e}")

class Designate:# Designate class to handle teacher-course assignments
    def __init__(self, cou_id, t_id):
        self.cou_id = cou_id
        self.t_id = t_id

    def append_designate(self, conn):# Method to insert designation into the database
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Designate (COU_ID, T_ID)
                VALUES (?, ?);
            """, (self.cou_id, self.t_id))
            conn.commit()
            print(f"Designation successful: Teacher {self.t_id} in Course {self.cou_id}.")
        except sqlite3.IntegrityError as e:
            print(f"Error enrolling Student {self.t_id} in Course {self.cou_id}: {e}")

class Enrollment:# Enrollment class to handle student-course enrollments
    def __init__(self, cou_id, stu_id):
        self.cou_id = cou_id
        self.stu_id = stu_id

    def append_enrollment(self, conn):# Method to insert enrollment into the database
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Assign (COU_ID, STU_ID)
                VALUES (?, ?);
            """, (self.cou_id, self.stu_id))
            conn.commit()
            print(f"Enrollment successful: Student {self.stu_id} in Course {self.cou_id}.")
        except sqlite3.IntegrityError as e:
            print(f"Error enrolling Student {self.stu_id} in Course {self.cou_id}: {e}")



def setup_college_database():# Function to setup the college database and tables
    
    conn = sqlite3.connect('college_database.db')# Connect to SQLite database (or create it if it doesn't exist)
    cursor = conn.cursor()# Create a cursor object to execute SQL commands
    
    cursor.execute("DROP TABLE IF EXISTS Assign;")# Drop existing tables to start fresh
    cursor.execute("DROP TABLE IF EXISTS Student;")
    cursor.execute("DROP TABLE IF EXISTS Course;")
    cursor.execute("DROP TABLE IF EXISTS Teacher;")
    cursor.execute("DROP TABLE IF EXISTS Designate;")

    cursor.execute("PRAGMA foreign_keys = ON;")# Enable foreign key support

    # --- 1. Create Teacher Table ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Teacher (
        T_ID INTEGER PRIMARY KEY,
        T_FNAME VARCHAR(255),
        T_LNAME VARCHAR(255),
        T_RANK VARCHAR(100)
    );
    """)
    

    # --- 2. Create Course Table ---
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Course (
        COU_ID INTEGER PRIMARY KEY,
        COU_NAME VARCHAR(255),
        COU_CREDIT VARCHAR(50),
        COU_DEPARTMEN VARCHAR(100)
    );
    """)
        
    # --- 3. Create Student Table ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Student (
        STU_ID INTEGER PRIMARY KEY,
        STU_FNAME VARCHAR(255),
        STU_LNAME VARCHAR(255),
        STU_BIRTHD VARCHAR(50) -- Stored as text for simplicity
    );
    """)
    

    # --- 4. Create Linking Table: Assign (Enrollment) ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Assign (
        -- Composite Primary Key made of two Foreign Keys
        COU_ID INTEGER,
        STU_ID INTEGER,
        
        PRIMARY KEY (COU_ID, STU_ID),
        FOREIGN KEY (COU_ID) REFERENCES Course(COU_ID),
        FOREIGN KEY (STU_ID) REFERENCES Student(STU_ID)
    );
    """)
    
    # --- 5 Create Linking Table: Designate (Designate) ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Designate (
        -- Composite Primary Key made of two Foreign Keys
        COU_ID INTEGER,
        T_ID INTEGER,
        
        PRIMARY KEY (COU_ID, T_ID),
        FOREIGN KEY (COU_ID) REFERENCES Course(COU_ID),
        FOREIGN KEY (T_ID) REFERENCES Teacher(T_ID)
    );
    """)


    # --- 6 Commit changes and close the connection ---
    conn.commit()
    conn.close()

def print_students_in_course(conn, course_id): #Function to print the list of students enrolled in a specific course.
   
    cursor = conn.cursor()# Create a cursor object
    
    #Query to get the course name
    course_name_query = cursor.execute("SELECT COU_NAME FROM Course WHERE COU_ID = ?", (course_id,)).fetchone()
    
    if not course_name_query:
        print(f"\n Course ID {course_id} not found.")
        return

    course_name = course_name_query[0]# Get the course name
    
    # Display header for the results
    print(f"\n--- Students Enrolled in Course {course_id}: {course_name} ---")

    #Query to get the enrolled students (using JOIN on the Assign table)
    query = """
    SELECT 
        S.STU_ID, 
        S.STU_FNAME, 
        S.STU_LNAME
    FROM 
        Student S
    JOIN 
        Assign A ON S.STU_ID = A.STU_ID
    WHERE 
        A.COU_ID = ?;
    """
    
    cursor.execute(query, (course_id,))
    students = cursor.fetchall()

    if not students:
        print("No students are currently enrolled in this course.")
    else:
        # Print results row by row
        for stu_id, fname, lname in students:
            print(f"ID: {stu_id} | Name: {fname} {lname}")

def print_teachers_for_course(conn, course_id): #Function to print the list of teachers assigned to a specific course.
    
    cursor = conn.cursor()
    
    #Query to get the course name
    course_name_query = cursor.execute("SELECT COU_NAME FROM Course WHERE COU_ID = ?", (course_id,)).fetchone()
    
    if not course_name_query:
        print(f"\n Course ID {course_id} not found.")
        return

    course_name = course_name_query[0]
    
    # Display header for the results
    print(f"\n--- Teachers Assigned to Course {course_id}: {course_name} ---")

    # Query to retrieve assigned teachers (JOIN on the Designate table)
    query = """
    SELECT 
        T.T_ID, 
        T.T_FNAME, 
        T.T_LNAME,
        T.T_RANK
    FROM 
        Teacher T
    JOIN 
        Designate D ON T.T_ID = D.T_ID
    WHERE 
        D.COU_ID = ?;
    """
    
    cursor.execute(query, (course_id,))
    teachers = cursor.fetchall()

    if not teachers:
        print("No teachers are currently assigned to this course.")
    else:
        # Print results row by row
        for t_id, fname, lname, rank in teachers:
            print(f"ID: {t_id} | Name: {fname} {lname} | Rank: {rank}")

def count_students_in_course(conn, course_id): #Function to count the total number of students enrolled in a specific course.
   
    cursor = conn.cursor()
    
    #Query to get the course name for output clarity
    course_name_query = cursor.execute("SELECT COU_NAME FROM Course WHERE COU_ID = ?", (course_id,)).fetchone()
    
    if not course_name_query:
        print(f"\n Course ID {course_id} not found.")
        return 0

    course_name = course_name_query[0]
    
    # Query to count the students in the linking table (Assign)
    query = """
    SELECT 
        COUNT(STU_ID) 
    FROM 
        Assign
    WHERE 
        COU_ID = ?;
    """
    
    cursor.execute(query, (course_id,))
    
    # Fetch the count result
    enrollment_count = cursor.fetchone()[0]

    # Display the result
    print(f"\n--- Enrollment Count for Course {course_id}: {course_name} ---")
    print(f"Total students enrolled: {enrollment_count}")
    
    return enrollment_count

def main():

    setup_college_database()# Setup the database and tables
    conn = sqlite3.connect('college_database.db')# Reconnect to the database to insert data

    Teacher(1, "Mohammad", "Norouzifard", "PhD").append_teacher(conn)
    Teacher(2, "Saveeta", "Bai", "PhD").append_teacher(conn)
    Teacher(3, "Arum", "Kumar", "PhD").append_teacher(conn)

    Course(800, "Professional Software Engineer", "80", "MSE").append_course(conn)
    Course(801, "Research Methods", "80", "MSE").append_course(conn)
    Course(802, "Quantum Computing", "80", "MSE").append_course(conn)

    Student(1000, "RONALDO", "NAZARIO", "2000-01-15").append_student(conn)
    Student(1001, "NEYMAR", "SANTOS", "1999-03-30").append_student(conn)
    Student(1002, "MARTA", "VIERIA", "2001-05-16").append_student(conn)
    Student(1003, "REBECA", "ANDRADE", "2001-07-01").append_student(conn)
    Student(1004, "MARIA", "BUENO", "2001-09-17").append_student(conn)

    Designate(800, 1).append_designate(conn) # Designate Teacher 1 to Course 800
    Designate(801, 1).append_designate(conn) # Designate Teacher 1 to Course 801
    Designate(801, 2).append_designate(conn) # Designate Teacher  to Course 801
    Designate(802, 3).append_designate(conn) # Designate Teacher 3 to Course 802

    Enrollment(800, 1000).append_enrollment(conn) # Enroll Student 1000 in Course 800
    Enrollment(801, 1000).append_enrollment(conn) # Enroll Student 1000 in Course 801
    Enrollment(800, 1001).append_enrollment(conn) # Enroll Student 1001 in Course 801
    Enrollment(801, 1001).append_enrollment(conn) # Enroll Student 1001 in Course 801
    Enrollment(800, 1002).append_enrollment(conn) # Enroll Student 1002 in Course 801

    count_students_in_course(conn, 800)# Count students enrolled in Course 800
    print_students_in_course(conn, 800)# Print students enrolled in Course 800
    print_teachers_for_course(conn, 801)# Print teachers assigned to Course 801
    
    conn.close()# Close the database connection
    
# Execute the setup function
if __name__ == "__main__":
    main()