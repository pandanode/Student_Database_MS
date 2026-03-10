# 🎓 Student Database Management System

A complete relational database project built with **MySQL + Python**, demonstrating real-world database design, CRUD operations, stored procedures, triggers, and analytics queries.

---

## 📦 Features

- **6 relational tables** with proper Primary & Foreign Key constraints
- **Full CRUD operations** via Python + mysql-connector
- **5 Stored Procedures** — student report, averages, attendance %, grade assignment, fee flagging
- **Auto-grade trigger** — automatically assigns A+/A/B+/B/C/F on INSERT
- **Analytics queries** — top performers, attendance defaulters, fee reports

---

## 🗄️ Database Schema

```
departments  ──< faculty
departments  ──< courses ──< grades
departments  ──< students ──< grades
                 students ──< attendance
                 students ──< fees
```

| Table | Purpose |
|---|---|
| `departments` | Academic departments |
| `faculty` | Faculty members |
| `courses` | Course catalog |
| `students` | Student records |
| `grades` | Marks & letter grades |
| `attendance` | Daily attendance |
| `fees` | Fee payment tracking |

---

## 🚀 Setup Instructions

### 1. Prerequisites
- MySQL 8.0+
- Python 3.8+

### 2. Install Python dependency
```bash
pip install mysql-connector-python
```

### 3. Run the SQL schema
Open MySQL Workbench and run:
```bash
source schema.sql
```

### 4. Update DB credentials in crud.py
```python
password="your_mysql_password"
```

### 5. Run the Python CRUD demo
```bash
python crud.py
```

---

## 📸 Sample Output

```
============================================================
  STUDENT DATABASE MANAGEMENT SYSTEM
============================================================

ID    Name                 Email                          Year   Dept
---------------------------------------------------------------------------
1     Tamanna Sharma       tamanna@student.com            3      Computer Applications
2     Riya Kapoor          riya@student.com               3      Computer Applications
3     Amit Verma           amit@student.com               2      Information Technology

📋 Report for Student ID: 1
------------------------------------------------------------
  Tamanna Sharma | Database Management Systems | Marks: 88.5 | Grade: A  | Sem: 5
  Tamanna Sharma | Python Programming          | Marks: 92.0 | Grade: A+ | Sem: 5

📊 Attendance for Student ID: 1
------------------------------------------------------------
  Database Management Systems: 66.7% ⚠️ LOW
  Python Programming: 100.0% ✅

🏆 Top Performers:
----------------------------------------
  1. Tamanna Sharma      Avg: 86.17  (3 courses)
  2. Riya Kapoor         Avg: 74.83  (3 courses)
```

---

## 🛠️ Tech Stack

- **Database**: MySQL 8.0
- **Language**: Python 3.x
- **Library**: mysql-connector-python

---

## 👩‍💻 Author

**Tamanna Sharma** — BCA Final Year, MIET Jammu  
[github.com/Tamanna-Sharma](https://github.com/Tamanna-Sharma)