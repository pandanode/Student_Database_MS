# ============================================================
#  STUDENT DATABASE MANAGEMENT SYSTEM — CRUD Operations
#  Author : Tamanna Sharma
#  GitHub : github.com/Tamanna-Sharma/student-database-system
# ============================================================

import mysql.connector
from mysql.connector import Error

# ── DB Connection ─────────────────────────────────────────────
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="porsche718~1!@",   # ← change this
        database="student_db"
    )

# ============================================================
#  CREATE Operations
# ============================================================

def add_student(name, email, phone, dept_id, year):
    """Insert a new student record"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO students (name, email, phone, dept_id, year)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, phone, dept_id, year))
        conn.commit()
        print(f"✅ Student '{name}' added with ID: {cursor.lastrowid}")
        return cursor.lastrowid
    except Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close(); conn.close()

def add_grade(student_id, course_id, marks, semester):
    """Insert grade — trigger auto-assigns letter grade"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO grades (student_id, course_id, marks, semester)
            VALUES (%s, %s, %s, %s)
        """, (student_id, course_id, marks, semester))
        conn.commit()
        print(f"✅ Grade added for student {student_id} | Marks: {marks}")
    except Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close(); conn.close()

def mark_attendance(student_id, course_id, att_date, status="Present"):
    """Record attendance for a student"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO attendance (student_id, course_id, att_date, status)
            VALUES (%s, %s, %s, %s)
        """, (student_id, course_id, att_date, status))
        conn.commit()
        print(f"✅ Attendance marked: Student {student_id} → {status} on {att_date}")
    except Error as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close(); conn.close()

# ============================================================
#  READ Operations
# ============================================================

def get_all_students():
    """Retrieve all students with department name"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT s.student_id, s.name, s.email, s.year, d.dept_name
            FROM students s
            JOIN departments d ON s.dept_id = d.dept_id
            ORDER BY s.student_id
        """)
        students = cursor.fetchall()
        print(f"\n{'ID':<5} {'Name':<20} {'Email':<30} {'Year':<6} {'Dept'}")
        print("-" * 75)
        for s in students:
            print(f"{s['student_id']:<5} {s['name']:<20} {s['email']:<30} {s['year']:<6} {s['dept_name']}")
        return students
    finally:
        cursor.close(); conn.close()

def get_student_report(student_id):
    """Get full academic report using stored procedure"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("GetStudentReport", [student_id])
        print(f"\n📋 Report for Student ID: {student_id}")
        print("-" * 60)
        for result in cursor.stored_results():
            for row in result.fetchall():
                print(f"  {row['name']} | {row['course_name']} | "
                      f"Marks: {row['marks']} | Grade: {row['grade']} | Sem: {row['semester']}")
    finally:
        cursor.close(); conn.close()

def get_attendance_report(student_id):
    """Get attendance % per course using stored procedure"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc("GetAttendance", [student_id])
        print(f"\n📊 Attendance for Student ID: {student_id}")
        print("-" * 60)
        for result in cursor.stored_results():
            for row in result.fetchall():
                flag = "⚠️ LOW" if row['attendance_pct'] < 75 else "✅"
                print(f"  {row['course_name']}: {row['attendance_pct']}% {flag}")
    finally:
        cursor.close(); conn.close()

def get_top_performers():
    """Get top 3 students by average marks"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT s.name, ROUND(AVG(g.marks), 2) AS avg_marks,
                   COUNT(g.course_id) AS courses
            FROM students s
            JOIN grades g ON s.student_id = g.student_id
            GROUP BY s.name
            ORDER BY avg_marks DESC
            LIMIT 3
        """)
        print("\n🏆 Top Performers:")
        print("-" * 40)
        for i, row in enumerate(cursor.fetchall(), 1):
            print(f"  {i}. {row['name']:<20} Avg: {row['avg_marks']}  ({row['courses']} courses)")
    finally:
        cursor.close(); conn.close()

def get_fee_defaulters():
    """Get students with pending/overdue fees"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT s.name, f.amount, f.status
            FROM fees f
            JOIN students s ON f.student_id = s.student_id
            WHERE f.status != 'Paid'
        """)
        rows = cursor.fetchall()
        print("\n💰 Fee Defaulters:")
        print("-" * 40)
        for row in rows:
            print(f"  {row['name']:<20} ₹{row['amount']}  [{row['status']}]")
    finally:
        cursor.close(); conn.close()

# ============================================================
#  UPDATE Operations
# ============================================================

def update_student_year(student_id, new_year):
    """Promote student to next year"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE students SET year = %s WHERE student_id = %s
        """, (new_year, student_id))
        conn.commit()
        if cursor.rowcount:
            print(f"✅ Student {student_id} promoted to Year {new_year}")
        else:
            print(f"⚠️  No student found with ID {student_id}")
    finally:
        cursor.close(); conn.close()

def update_fee_status(student_id, new_status):
    """Update fee payment status"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE fees SET status = %s, paid_on = CURDATE()
            WHERE student_id = %s AND status != 'Paid'
        """, (new_status, student_id))
        conn.commit()
        print(f"✅ Fee status updated to '{new_status}' for student {student_id}")
    finally:
        cursor.close(); conn.close()

# ============================================================
#  DELETE Operations
# ============================================================

def delete_student(student_id):
    """Remove student and all related records"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Delete child records first (FK constraint order)
        for table in ['attendance', 'grades', 'fees']:
            cursor.execute(f"DELETE FROM {table} WHERE student_id = %s", (student_id,))
        cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        conn.commit()
        print(f"✅ Student {student_id} and all related records deleted.")
    except Error as e:
        conn.rollback()
        print(f"❌ Error: {e}")
    finally:
        cursor.close(); conn.close()

# ============================================================
#  MAIN DEMO — runs all operations
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  STUDENT DATABASE MANAGEMENT SYSTEM")
    print("=" * 60)

    # READ — show all students
    get_all_students()

    # READ — full report for student 1
    get_student_report(1)

    # READ — attendance for student 1
    get_attendance_report(1)

    # READ — top performers
    get_top_performers()

    # READ — fee defaulters
    get_fee_defaulters()

    # CREATE — add new student
    add_student("Neha Rawat", "neha.rawat@student.com", "9111222333", 1, 2)

    # CREATE — add grade (trigger auto-assigns letter)
    add_grade(student_id=1, course_id=5, marks=85.0, semester=5)

    # UPDATE — promote student 4 to year 2
    update_student_year(4, 2)

    # UPDATE — mark student 3 fee as paid
    update_fee_status(3, "Paid")

    print("\n✅ All CRUD operations completed successfully!")