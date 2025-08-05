# GradeMate
A clean, educational GUI application designed to help manage student data, marks, and generate comprehensive reports.

## Features

### Student Management
- **Add Students**: Register new students with roll number, name, and class
- **View Students**: Display all registered students in an organized table
- **Update Students**: Modify existing student information
- **Delete Students**: Remove students and their associated marks
- **Input Validation**: Ensures data integrity with proper validation

### Marks Management
- **Add Marks**: Record subject-wise marks for students (0-100 scale)
- **View Marks**: Display all marks with student names using SQL JOIN
- **Subject Tracking**: Track multiple subjects per student
- **Automatic Validation**: Ensures marks are within valid range

### Reports & Analytics
- **Student Averages**: Calculate and display average percentage using MySQL AVG() and ROUND() functions
- **Top Scorers**: Show top-performing students using ORDER BY
- **Report Cards**: Generate detailed individual report cards with grades and status
- **Grade Calculation**: Automatic grade assignment using MySQL IF() function
- **Statistics**: Display comprehensive academic statistics

### Technical Features
- **MySQL Integration**: Uses advanced MySQL functions (AVG, ROUND, IF, CONCAT, etc.)
- **JOIN Operations**: Combines student and marks tables for comprehensive reports
- **Clean GUI**: Organized tabbed interface using tkinter
- **Error Handling**: Robust error handling and user feedback
- **Database Validation**: Foreign key constraints and data integrity

## How to Run

### Prerequisites
1. **Python 3.7 or higher** installed on your system
2. **MySQL Server** installed and running
3. **mysql-connector-python** package

### Installation Steps

1. **Clone or download the project**:
   ```bash
   git clone https://github.com/your-username/GradeMate.git
   cd GradeMate
   ```

2. **Install required Python package**:
   ```bash
   pip install mysql-connector-python
   ```

3. **Set up MySQL** (see MySQL Setup section below)

4. **Configure database connection**:
   - Open `db_config.py`
   - Update the database credentials if needed:
     ```python
     # Default configuration
     host='localhost'
     user='root'
     password=''  # Enter your MySQL password
     database='grademate'
     ```

5. **Run the application**:
   ```bash
   python main.py
   ```

## MySQL Setup Steps

### Step 1: Install MySQL
- Download MySQL Community Server from [mysql.com](https://dev.mysql.com/downloads/mysql/)
- Install MySQL with default settings
- Remember the root password you set during installation

### Step 2: Start MySQL Service
- **Windows**: Start MySQL from Services or MySQL Workbench
- **Linux/Mac**: `sudo systemctl start mysql` or `brew services start mysql`

### Step 3: Create Database (Automatic)
The application will automatically:
- Create the `grademate` database if it doesn't exist
- Create the required tables (`students` and `marks`)
- Set up proper relationships and constraints

### Step 4: Database Schema
The application creates these tables:

```sql
-- Students table
CREATE TABLE students (
    roll_no INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    class INT NOT NULL
);

-- Marks table with foreign key relationship
CREATE TABLE marks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    roll_no INT,
    subject VARCHAR(50) NOT NULL,
    marks INT NOT NULL CHECK (marks >= 0 AND marks <= 100),
    FOREIGN KEY (roll_no) REFERENCES students(roll_no) ON DELETE CASCADE
);
```

### Step 5: Test Connection
- Launch the application
- If connection fails, check:
  - MySQL service is running
  - Credentials in `db_config.py` are correct
  - Firewall settings allow MySQL connections

## Usage Guide

### Adding Students
1. Go to "Student Management" tab
2. Enter roll number, name, and class
3. Click "Add Student"
4. Student appears in the list below

### Recording Marks
1. Go to "Marks Management" tab
2. Enter student roll number, subject, and marks (0-100)
3. Click "Add Marks"
4. Marks appear in the list with student name

### Generating Reports
1. Go to "Reports & Analytics" tab
2. Choose from:
   - **Student Averages**: View all students with their average marks and grades
   - **Top Scorers**: See highest-performing students
   - **Report Card**: Generate individual student report (enter roll number when prompted)

## MySQL Functions Used

The application demonstrates various MySQL functions:

- **AVG()**: Calculate average marks per student
- **ROUND()**: Round averages to 2 decimal places
- **IF()**: Conditional grade assignment and pass/fail status
- **COUNT()**: Count number of subjects per student
- **MAX()**: Find highest marks
- **CONCAT()**: Combine strings for formatted output
- **ORDER BY**: Sort results by marks (descending)
- **JOIN**: Combine student and marks tables
- **GROUP BY**: Group marks by student for calculations

## File Structure

```
GradeMate/
├── main.py           # Main application with GUI
├── db_config.py      # Database configuration and connection
├── README.md         # This documentation file
└── LICENSE           # Project license
```

## Educational Value

This project is designed for Class 12 Informatics Practices students and demonstrates:

- **Python Programming**: Object-oriented programming, GUI development
- **Database Management**: MySQL integration, CRUD operations
- **SQL Functions**: Advanced MySQL functions and queries
- **Software Design**: Clean architecture, error handling, user experience
- **Real-world Application**: Practical school management system

## Troubleshooting

### Common Issues

1. **"Failed to connect to database"**
   - Check if MySQL service is running
   - Verify credentials in `db_config.py`
   - Ensure MySQL is installed properly

2. **"Access denied for user 'root'"**
   - Update password in `db_config.py`
   - Check MySQL user permissions

3. **"No module named 'mysql.connector'"**
   - Install the package: `pip install mysql-connector-python`

4. **Application window too small**
   - The window is resizable - drag corners to resize
   - Application is responsive and adapts to different screen sizes

### Technical Support
- Ensure Python 3.7+ is installed
- All code is well-commented for learning purposes
- Database tables are created automatically on first run

## License
This project is open source and available under the MIT License.
