"""
GradeMate - Student Grade Management System
A GUI application built with Python tkinter and MySQL for managing student data and marks.
Enhanced with Wuthering Waves inspired midnight black theme.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from db_config import db_config
import mysql.connector
from mysql.connector import Error

class GradeMateApp:
    def __init__(self, root):
        """
        Initialize the main application window with WuWa midnight theme
        """
        self.root = root
        self.root.title("GradeMate - Student Grade Management System")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # WuWa Midnight Theme Colors
        self.colors = {
            'bg_primary': '#0D1117',      # Deep midnight black
            'bg_secondary': '#161B22',    # Slightly lighter black
            'bg_tertiary': '#21262D',     # Card background
            'accent_blue': '#58A6FF',     # Bright blue accent
            'accent_purple': '#8B5CF6',   # Purple accent
            'accent_cyan': '#79C0FF',     # Cyan accent
            'text_primary': '#F0F6FC',    # Primary white text
            'text_secondary': '#8B949E',  # Secondary gray text
            'border': '#30363D',          # Border color
            'success': '#3FB950',         # Success green
            'warning': '#F85149',         # Warning red
            'hover': '#262C36'            # Hover state
        }
        
        # Configure root window
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Apply custom theme
        self.setup_theme()
        
        # Connect to database
        self.connection = db_config.create_connection()
        if not self.connection:
            messagebox.showerror("Database Error", "Failed to connect to database. Please check your MySQL configuration.")
            self.root.destroy()
            return
        
        # Create main interface
        self.create_widgets()
    
    def setup_theme(self):
        """
        Setup WuWa midnight theme for ttk widgets
        """
        style = ttk.Style()
        
        # Configure main theme
        style.theme_use('clam')
        
        # Configure Notebook (tabs)
        style.configure('TNotebook', 
                       background=self.colors['bg_primary'],
                       borderwidth=0)
        style.configure('TNotebook.Tab',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_secondary'],
                       padding=[20, 8],
                       borderwidth=0)
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['bg_tertiary']),
                           ('active', self.colors['hover'])],
                 foreground=[('selected', self.colors['accent_blue']),
                           ('active', self.colors['text_primary'])])
        
        # Configure Frame
        style.configure('TFrame',
                       background=self.colors['bg_primary'],
                       borderwidth=0)
        
        # Configure LabelFrame
        style.configure('TLabelframe',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['accent_cyan'],
                       borderwidth=1,
                       relief='solid')
        style.configure('TLabelframe.Label',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['accent_cyan'],
                       font=('Segoe UI', 10, 'bold'))
        
        # Configure Labels
        style.configure('TLabel',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 9))
        
        # Configure Entry widgets
        style.configure('TEntry',
                       fieldbackground=self.colors['bg_tertiary'],
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       relief='solid',
                       insertcolor=self.colors['accent_blue'])
        style.map('TEntry',
                 focuscolor=[('focus', self.colors['accent_blue'])])
        
        # Configure Buttons
        style.configure('TButton',
                       background=self.colors['accent_blue'],
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 9, 'bold'),
                       padding=[15, 8])
        style.map('TButton',
                 background=[('active', self.colors['accent_purple']),
                           ('pressed', self.colors['accent_cyan'])])
        
        # Configure Treeview
        style.configure('Treeview',
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['bg_tertiary'],
                       borderwidth=0,
                       font=('Segoe UI', 9))
        style.configure('Treeview.Heading',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['accent_cyan'],
                       font=('Segoe UI', 9, 'bold'),
                       borderwidth=1,
                       relief='solid')
        style.map('Treeview',
                 background=[('selected', self.colors['accent_blue'])],
                 foreground=[('selected', 'white')])
        
        # Configure Scrollbar
        style.configure('Vertical.TScrollbar',
                       background=self.colors['bg_secondary'],
                       troughcolor=self.colors['bg_primary'],
                       borderwidth=0,
                       arrowcolor=self.colors['text_secondary'],
                       darkcolor=self.colors['bg_secondary'],
                       lightcolor=self.colors['bg_secondary'])
        style.map('Vertical.TScrollbar',
                 background=[('active', self.colors['accent_blue'])])
        
        # Configure special button styles
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='white')
        style.map('Success.TButton',
                 background=[('active', '#2EA043')])
        
        style.configure('Warning.TButton',
                       background=self.colors['warning'],
                       foreground='white')
        style.map('Warning.TButton',
                 background=[('active', '#DA3633')])
        
        style.configure('Secondary.TButton',
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       relief='solid')
        style.map('Secondary.TButton',
                 background=[('active', self.colors['hover'])])
    
    def create_widgets(self):
        """
        Create and organize all GUI widgets with enhanced styling
        """
        # Create main container with padding
        main_container = ttk.Frame(self.root)
        main_container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Title frame with gradient-like effect
        title_frame = tk.Frame(main_container, bg=self.colors['bg_secondary'], height=60)
        title_frame.pack(fill='x', pady=(0, 15))
        title_frame.pack_propagate(False)
        
        # App title
        title_label = tk.Label(title_frame, 
                              text="🎓 GradeMate",
                              font=('Segoe UI', 18, 'bold'),
                              bg=self.colors['bg_secondary'],
                              fg=self.colors['accent_cyan'])
        title_label.pack(side='left', padx=20, pady=15)
        
        # Subtitle
        subtitle_label = tk.Label(title_frame,
                                 text="Student Grade Management System",
                                 font=('Segoe UI', 10),
                                 bg=self.colors['bg_secondary'],
                                 fg=self.colors['text_secondary'])
        subtitle_label.pack(side='left', padx=(0, 20), pady=15)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill='both', expand=True, pady=(0, 10))
        
        # Create tabs
        self.create_student_tab()
        self.create_marks_tab()
        self.create_reports_tab()
        
        # Enhanced status bar
        status_frame = tk.Frame(main_container, bg=self.colors['bg_secondary'], height=35)
        status_frame.pack(fill='x')
        status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar()
        self.status_var.set("🟢 Ready - Database Connected")
        status_bar = tk.Label(status_frame, 
                             textvariable=self.status_var, 
                             bg=self.colors['bg_secondary'],
                             fg=self.colors['text_secondary'],
                             font=('Segoe UI', 9),
                             anchor=tk.W)
        status_bar.pack(side=tk.LEFT, fill=tk.X, padx=15, pady=8)
    
    def create_student_tab(self):
        """
        Create enhanced student management tab
        """
        # Student tab frame
        student_frame = ttk.Frame(self.notebook)
        self.notebook.add(student_frame, text="👥 Student Management")
        
        # Main container with better spacing
        container = ttk.Frame(student_frame)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Input frame with enhanced styling
        input_frame = ttk.LabelFrame(container, text="📝 Student Information", padding=20)
        input_frame.pack(fill='x', pady=(0, 20))
        
        # Configure grid weights for responsive design
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=2)
        
        # Roll Number with icon
        ttk.Label(input_frame, text="🆔 Roll Number:").grid(row=0, column=0, sticky='w', padx=(0, 10), pady=8)
        self.roll_entry = ttk.Entry(input_frame, width=25, font=('Segoe UI', 10))
        self.roll_entry.grid(row=0, column=1, sticky='ew', padx=(0, 20), pady=8)
        
        # Name with icon
        ttk.Label(input_frame, text="👤 Name:").grid(row=0, column=2, sticky='w', padx=(0, 10), pady=8)
        self.name_entry = ttk.Entry(input_frame, width=35, font=('Segoe UI', 10))
        self.name_entry.grid(row=0, column=3, sticky='ew', padx=0, pady=8)
        
        # Class with icon
        ttk.Label(input_frame, text="🏫 Class:").grid(row=1, column=0, sticky='w', padx=(0, 10), pady=8)
        self.class_entry = ttk.Entry(input_frame, width=25, font=('Segoe UI', 10))
        self.class_entry.grid(row=1, column=1, sticky='ew', padx=(0, 20), pady=8)
        
        # Enhanced buttons frame
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=(15, 0))
        
        # Styled buttons with icons
        ttk.Button(button_frame, text="➕ Add Student", 
                  command=self.add_student, style='Success.TButton').pack(side='left', padx=(0, 10))
        ttk.Button(button_frame, text="✏️ Update Student", 
                  command=self.update_student).pack(side='left', padx=(0, 10))
        ttk.Button(button_frame, text="🗑️ Delete Student", 
                  command=self.delete_student, style='Warning.TButton').pack(side='left', padx=(0, 10))
        ttk.Button(button_frame, text="🧹 Clear Fields", 
                  command=self.clear_student_fields, style='Secondary.TButton').pack(side='left', padx=(0, 10))
        
        # Students list frame with enhanced styling
        list_frame = ttk.LabelFrame(container, text="📋 Students Database", padding=15)
        list_frame.pack(fill='both', expand=True)
        
        # Create frame for treeview and scrollbar
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill='both', expand=True)
        
        # Enhanced Treeview for students
        columns = ('Roll No', 'Name', 'Class')
        self.student_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=12)
        
        # Define headings with better formatting
        self.student_tree.heading('Roll No', text='🆔 Roll Number')
        self.student_tree.heading('Name', text='👤 Student Name')
        self.student_tree.heading('Class', text='🏫 Class')
        
        # Configure columns
        self.student_tree.column('Roll No', width=120, anchor='center')
        self.student_tree.column('Name', width=300, anchor='w')
        self.student_tree.column('Class', width=100, anchor='center')
        
        # Enhanced scrollbar
        scrollbar_students = ttk.Scrollbar(tree_frame, orient='vertical', command=self.student_tree.yview)
        self.student_tree.configure(yscrollcommand=scrollbar_students.set)
        
        self.student_tree.pack(side='left', fill='both', expand=True)
        scrollbar_students.pack(side='right', fill='y')
        
        # Bind selection event
        self.student_tree.bind('<<TreeviewSelect>>', self.on_student_select)
        
        # Load students
        self.load_students()
    
    def create_marks_tab(self):
        """
        Create enhanced marks management tab
        """
        # Marks tab frame
        marks_frame = ttk.Frame(self.notebook)
        self.notebook.add(marks_frame, text="📊 Marks Management")
        
        # Main container
        container = ttk.Frame(marks_frame)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Input frame with enhanced styling
        input_frame = ttk.LabelFrame(container, text="📝 Add Student Marks", padding=20)
        input_frame.pack(fill='x', pady=(0, 20))
        
        # Configure grid weights
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(3, weight=2)
        
        # Roll Number with icon
        ttk.Label(input_frame, text="🆔 Roll Number:").grid(row=0, column=0, sticky='w', padx=(0, 10), pady=8)
        self.marks_roll_entry = ttk.Entry(input_frame, width=25, font=('Segoe UI', 10))
        self.marks_roll_entry.grid(row=0, column=1, sticky='ew', padx=(0, 20), pady=8)
        
        # Subject with icon
        ttk.Label(input_frame, text="📚 Subject:").grid(row=0, column=2, sticky='w', padx=(0, 10), pady=8)
        self.subject_entry = ttk.Entry(input_frame, width=30, font=('Segoe UI', 10))
        self.subject_entry.grid(row=0, column=3, sticky='ew', padx=0, pady=8)
        
        # Marks with icon
        ttk.Label(input_frame, text="📈 Marks (0-100):").grid(row=1, column=0, sticky='w', padx=(0, 10), pady=8)
        self.marks_entry = ttk.Entry(input_frame, width=25, font=('Segoe UI', 10))
        self.marks_entry.grid(row=1, column=1, sticky='ew', padx=(0, 20), pady=8)
        
        # Buttons frame
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=(15, 0))
        
        # Styled buttons
        ttk.Button(button_frame, text="➕ Add Marks", 
                  command=self.add_marks, style='Success.TButton').pack(side='left', padx=(0, 10))
        ttk.Button(button_frame, text="🧹 Clear Fields", 
                  command=self.clear_marks_fields, style='Secondary.TButton').pack(side='left')
        
        # Marks list frame
        list_frame = ttk.LabelFrame(container, text="📋 Marks Database", padding=15)
        list_frame.pack(fill='both', expand=True)
        
        # Create frame for treeview and scrollbar
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill='both', expand=True)
        
        # Enhanced Treeview for marks
        columns = ('Roll No', 'Student Name', 'Subject', 'Marks')
        self.marks_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=14)
        
        # Define headings with icons
        self.marks_tree.heading('Roll No', text='🆔 Roll No')
        self.marks_tree.heading('Student Name', text='👤 Student Name')
        self.marks_tree.heading('Subject', text='📚 Subject')
        self.marks_tree.heading('Marks', text='📈 Marks')
        
        # Configure columns
        self.marks_tree.column('Roll No', width=100, anchor='center')
        self.marks_tree.column('Student Name', width=250, anchor='w')
        self.marks_tree.column('Subject', width=200, anchor='w')
        self.marks_tree.column('Marks', width=100, anchor='center')
        
        # Enhanced scrollbar
        scrollbar_marks = ttk.Scrollbar(tree_frame, orient='vertical', command=self.marks_tree.yview)
        self.marks_tree.configure(yscrollcommand=scrollbar_marks.set)
        
        self.marks_tree.pack(side='left', fill='both', expand=True)
        scrollbar_marks.pack(side='right', fill='y')
        
        # Load marks
        self.load_marks()
    
    def create_reports_tab(self):
        """
        Create enhanced reports and analytics tab
        """
        # Reports tab frame
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="📈 Reports & Analytics")
        
        # Main container
        container = ttk.Frame(reports_frame)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Enhanced buttons frame
        button_frame = ttk.LabelFrame(container, text="📊 Generate Reports", padding=15)
        button_frame.pack(fill='x', pady=(0, 20))
        
        # Create button container for better layout
        btn_container = ttk.Frame(button_frame)
        btn_container.pack(expand=True)
        
        # Styled report buttons with icons
        ttk.Button(btn_container, text="📊 Student Averages", 
                  command=self.show_student_averages,
                  style='TButton').pack(side='left', padx=(0, 15))
        ttk.Button(btn_container, text="🏆 Top Scorers", 
                  command=self.show_top_scorers,
                  style='Success.TButton').pack(side='left', padx=(0, 15))
        ttk.Button(btn_container, text="📄 Generate Report Card", 
                  command=self.generate_report_card,
                  style='TButton').pack(side='left')
        
        # Enhanced report display frame
        display_frame = ttk.LabelFrame(container, text="📋 Report Display", padding=15)
        display_frame.pack(fill='both', expand=True)
        
        # Create frame for text widget and scrollbar
        text_frame = ttk.Frame(display_frame)
        text_frame.pack(fill='both', expand=True)
        
        # Enhanced Text widget for reports with better styling
        self.report_text = tk.Text(text_frame, 
                                  wrap='word', 
                                  height=22,
                                  bg=self.colors['bg_tertiary'],
                                  fg=self.colors['text_primary'],
                                  font=('Consolas', 10),
                                  insertbackground=self.colors['accent_blue'],
                                  selectbackground=self.colors['accent_blue'],
                                  selectforeground='white',
                                  borderwidth=0,
                                  padx=15,
                                  pady=15)
        
        # Enhanced scrollbar
        scrollbar_report = ttk.Scrollbar(text_frame, orient='vertical', command=self.report_text.yview)
        self.report_text.configure(yscrollcommand=scrollbar_report.set)
        
        self.report_text.pack(side='left', fill='both', expand=True)
        scrollbar_report.pack(side='right', fill='y')
        
        # Add welcome message
        welcome_msg = """
🎓 Welcome to GradeMate Reports & Analytics!

📊 Available Reports:
• Student Averages - View all students with their average marks and grades
• Top Scorers - See the highest-performing students (Top 10)
• Report Card - Generate detailed individual student report cards

🚀 Click any button above to generate reports!

✨ Features:
• Advanced MySQL functions (AVG, ROUND, IF, JOIN)
• Real-time calculations
• Professional formatting
• Grade assignment (A+, A, B+, B, C, F)
• Pass/Fail status determination
        """
        
        self.report_text.insert(tk.END, welcome_msg)
        self.report_text.config(state='disabled')  # Make it read-only initially
    
    def add_student(self):
        """
        Add new student to database
        """
        try:
            roll_no = int(self.roll_entry.get().strip())
            name = self.name_entry.get().strip()
            class_num = int(self.class_entry.get().strip())
            
            # Validation
            if not name:
                messagebox.showerror("Error", "Name cannot be empty")
                return
            
            if class_num < 1 or class_num > 12:
                messagebox.showerror("Error", "Class must be between 1 and 12")
                return
            
            cursor = self.connection.cursor()
            query = "INSERT INTO students (roll_no, name, class) VALUES (%s, %s, %s)"
            cursor.execute(query, (roll_no, name, class_num))
            self.connection.commit()
            
            messagebox.showinfo("Success", "Student added successfully!")
            self.clear_student_fields()
            self.load_students()
            self.status_var.set(f"✅ Student {name} added successfully")
            
        except ValueError:
            messagebox.showerror("Error", "Roll number and class must be valid numbers")
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Roll number already exists")
        except Error as e:
            messagebox.showerror("Database Error", f"Error adding student: {e}")
        finally:
            cursor.close()
    
    def update_student(self):
        """
        Update existing student information
        """
        try:
            roll_no = int(self.roll_entry.get().strip())
            name = self.name_entry.get().strip()
            class_num = int(self.class_entry.get().strip())
            
            # Validation
            if not name:
                messagebox.showerror("Error", "Name cannot be empty")
                return
            
            cursor = self.connection.cursor()
            query = "UPDATE students SET name = %s, class = %s WHERE roll_no = %s"
            cursor.execute(query, (name, class_num, roll_no))
            
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "Student not found")
            else:
                self.connection.commit()
                messagebox.showinfo("Success", "Student updated successfully!")
                self.clear_student_fields()
                self.load_students()
                self.status_var.set(f"✏️ Student {name} updated successfully")
            
        except ValueError:
            messagebox.showerror("Error", "Roll number and class must be valid numbers")
        except Error as e:
            messagebox.showerror("Database Error", f"Error updating student: {e}")
        finally:
            cursor.close()
    
    def delete_student(self):
        """
        Delete student from database
        """
        try:
            roll_no = int(self.roll_entry.get().strip())
            
            result = messagebox.askyesno("Confirm Delete", 
                                       f"Are you sure you want to delete student with roll number {roll_no}?\n"
                                       "This will also delete all their marks.")
            
            if result:
                cursor = self.connection.cursor()
                query = "DELETE FROM students WHERE roll_no = %s"
                cursor.execute(query, (roll_no,))
                
                if cursor.rowcount == 0:
                    messagebox.showerror("Error", "Student not found")
                else:
                    self.connection.commit()
                    messagebox.showinfo("Success", "Student deleted successfully!")
                    self.clear_student_fields()
                    self.load_students()
                    self.load_marks()  # Refresh marks list
                    self.status_var.set(f"🗑️ Student with roll number {roll_no} deleted")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid roll number")
        except Error as e:
            messagebox.showerror("Database Error", f"Error deleting student: {e}")
        finally:
            cursor.close()
    
    def add_marks(self):
        """
        Add marks for a student
        """
        try:
            roll_no = int(self.marks_roll_entry.get().strip())
            subject = self.subject_entry.get().strip()
            marks = int(self.marks_entry.get().strip())
            
            # Validation
            if not subject:
                messagebox.showerror("Error", "Subject cannot be empty")
                return
            
            if marks < 0 or marks > 100:
                messagebox.showerror("Error", "Marks must be between 0 and 100")
                return
            
            # Check if student exists
            cursor = self.connection.cursor()
            cursor.execute("SELECT name FROM students WHERE roll_no = %s", (roll_no,))
            if not cursor.fetchone():
                messagebox.showerror("Error", "Student not found. Please add student first.")
                return
            
            # Add marks
            query = "INSERT INTO marks (roll_no, subject, marks) VALUES (%s, %s, %s)"
            cursor.execute(query, (roll_no, subject, marks))
            self.connection.commit()
            
            messagebox.showinfo("Success", "Marks added successfully!")
            self.clear_marks_fields()
            self.load_marks()
            self.status_var.set(f"📈 Marks added for roll number {roll_no} in {subject}")
            
        except ValueError:
            messagebox.showerror("Error", "Roll number and marks must be valid numbers")
        except Error as e:
            messagebox.showerror("Database Error", f"Error adding marks: {e}")
        finally:
            cursor.close()
    
    def load_students(self):
        """
        Load and display all students
        """
        try:
            # Clear existing data
            for item in self.student_tree.get_children():
                self.student_tree.delete(item)
            
            cursor = self.connection.cursor()
            cursor.execute("SELECT roll_no, name, class FROM students ORDER BY roll_no")
            students = cursor.fetchall()
            
            for student in students:
                self.student_tree.insert('', 'end', values=student)
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading students: {e}")
        finally:
            cursor.close()
    
    def load_marks(self):
        """
        Load and display all marks with student names
        """
        try:
            # Clear existing data
            for item in self.marks_tree.get_children():
                self.marks_tree.delete(item)
            
            cursor = self.connection.cursor()
            query = """
            SELECT m.roll_no, s.name, m.subject, m.marks 
            FROM marks m 
            JOIN students s ON m.roll_no = s.roll_no 
            ORDER BY m.roll_no, m.subject
            """
            cursor.execute(query)
            marks = cursor.fetchall()
            
            for mark in marks:
                self.marks_tree.insert('', 'end', values=mark)
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error loading marks: {e}")
        finally:
            cursor.close()
    
    def on_student_select(self, event):
        """
        Handle student selection in treeview
        """
        selection = self.student_tree.selection()
        if selection:
            item = self.student_tree.item(selection[0])
            values = item['values']
            
            # Fill entry fields with selected student data
            self.roll_entry.delete(0, tk.END)
            self.roll_entry.insert(0, values[0])
            
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, values[1])
            
            self.class_entry.delete(0, tk.END)
            self.class_entry.insert(0, values[2])
    
    def clear_student_fields(self):
        """
        Clear all student input fields
        """
        self.roll_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.class_entry.delete(0, tk.END)
    
    def clear_marks_fields(self):
        """
        Clear all marks input fields
        """
        self.marks_roll_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.marks_entry.delete(0, tk.END)
    
    def show_student_averages(self):
        """
        Display student averages using MySQL AVG and ROUND functions
        """
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT 
                s.roll_no,
                s.name,
                s.class,
                COUNT(m.marks) as subjects_count,
                ROUND(AVG(m.marks), 2) as average_marks,
                IF(AVG(m.marks) >= 90, 'A+',
                   IF(AVG(m.marks) >= 80, 'A',
                      IF(AVG(m.marks) >= 70, 'B+',
                         IF(AVG(m.marks) >= 60, 'B',
                            IF(AVG(m.marks) >= 50, 'C', 'F'))))) as grade
            FROM students s
            LEFT JOIN marks m ON s.roll_no = m.roll_no
            GROUP BY s.roll_no, s.name, s.class
            HAVING COUNT(m.marks) > 0
            ORDER BY average_marks DESC
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Enable text widget for editing
            self.report_text.config(state='normal')
            
            # Display in report text widget with enhanced formatting
            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(tk.END, "📊 STUDENT AVERAGE MARKS REPORT\n")
            self.report_text.insert(tk.END, "═" * 70 + "\n\n")
            
            if results:
                header = f"{'Roll No':<8} {'Name':<25} {'Class':<6} {'Subjects':<9} {'Average':<8} {'Grade':<5}\n"
                self.report_text.insert(tk.END, header)
                self.report_text.insert(tk.END, "─" * 70 + "\n")
                
                for row in results:
                    # Add grade emoji
                    grade_emoji = "🏆" if row[5] == "A+" else "🥇" if row[5] == "A" else "🥈" if row[5] == "B+" else "🥉" if row[5] == "B" else "📋" if row[5] == "C" else "❌"
                    line = f"{row[0]:<8} {row[1]:<25} {row[2]:<6} {row[3]:<9} {row[4]:<8} {grade_emoji} {row[5]:<5}\n"
                    self.report_text.insert(tk.END, line)
                
                self.report_text.insert(tk.END, "\n📈 Report generated successfully!")
                self.report_text.insert(tk.END, f"\n📊 Total students with marks: {len(results)}")
            else:
                self.report_text.insert(tk.END, "❌ No marks data available.\n")
                self.report_text.insert(tk.END, "💡 Add some student marks first to generate reports!")
            
            # Disable text widget to make it read-only
            self.report_text.config(state='disabled')
            self.status_var.set("📊 Student averages report generated successfully")
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error generating report: {e}")
        finally:
            cursor.close()
    
    def show_top_scorers(self):
        """
        Display top scorers using ORDER BY
        """
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT 
                s.roll_no,
                s.name,
                s.class,
                ROUND(AVG(m.marks), 2) as average_marks,
                MAX(m.marks) as highest_marks,
                COUNT(m.marks) as subjects_count
            FROM students s
            JOIN marks m ON s.roll_no = m.roll_no
            GROUP BY s.roll_no, s.name, s.class
            HAVING COUNT(m.marks) > 0
            ORDER BY average_marks DESC
            LIMIT 10
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            # Display in report text widget
            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(tk.END, "TOP SCORERS REPORT\n")
            self.report_text.insert(tk.END, "="*70 + "\n\n")
            
            if results:
                header = f"{'Rank':<5} {'Roll No':<8} {'Name':<20} {'Class':<6} {'Average':<8} {'Highest':<8} {'Subjects':<8}\n"
                self.report_text.insert(tk.END, header)
                self.report_text.insert(tk.END, "-"*70 + "\n")
                
                for i, row in enumerate(results, 1):
                    line = f"{i:<5} {row[0]:<8} {row[1]:<20} {row[2]:<6} {row[3]:<8} {row[4]:<8} {row[5]:<8}\n"
                    self.report_text.insert(tk.END, line)
            else:
                self.report_text.insert(tk.END, "No marks data available.\n")
            
            self.status_var.set("Top scorers report generated")
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error generating report: {e}")
        finally:
            cursor.close()
    
    def generate_report_card(self):
        """
        Generate detailed report card for a specific student
        """
        # Get roll number from user
        roll_no = tk.simpledialog.askinteger("Report Card", "Enter student roll number:")
        if not roll_no:
            return
        
        try:
            cursor = self.connection.cursor()
            
            # Get student details
            cursor.execute("SELECT roll_no, name, class FROM students WHERE roll_no = %s", (roll_no,))
            student = cursor.fetchone()
            
            if not student:
                messagebox.showerror("Error", "Student not found")
                return
            
            # Get marks details with calculations
            query = """
            SELECT 
                subject,
                marks,
                IF(marks >= 90, 'A+',
                   IF(marks >= 80, 'A',
                      IF(marks >= 70, 'B+',
                         IF(marks >= 60, 'B',
                            IF(marks >= 50, 'C', 'F'))))) as grade,
                IF(marks >= 50, 'PASS', 'FAIL') as status
            FROM marks 
            WHERE roll_no = %s 
            ORDER BY subject
            """
            cursor.execute(query, (roll_no,))
            marks_data = cursor.fetchall()
            
            if not marks_data:
                messagebox.showinfo("Info", "No marks found for this student")
                return
            
            # Calculate statistics
            total_marks = sum(mark[1] for mark in marks_data)
            total_subjects = len(marks_data)
            average = total_marks / total_subjects if total_subjects > 0 else 0
            
            # Display report card
            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(tk.END, "STUDENT REPORT CARD\n")
            self.report_text.insert(tk.END, "="*50 + "\n\n")
            
            # Student info
            self.report_text.insert(tk.END, f"Roll Number: {student[0]}\n")
            self.report_text.insert(tk.END, f"Name: {student[1]}\n")
            self.report_text.insert(tk.END, f"Class: {student[2]}\n\n")
            
            # Marks table
            self.report_text.insert(tk.END, "SUBJECT-WISE MARKS:\n")
            self.report_text.insert(tk.END, "-"*50 + "\n")
            header = f"{'Subject':<20} {'Marks':<8} {'Grade':<6} {'Status':<6}\n"
            self.report_text.insert(tk.END, header)
            self.report_text.insert(tk.END, "-"*50 + "\n")
            
            for mark in marks_data:
                line = f"{mark[0]:<20} {mark[1]:<8} {mark[2]:<6} {mark[3]:<6}\n"
                self.report_text.insert(tk.END, line)
            
            # Summary
            self.report_text.insert(tk.END, "\n" + "="*50 + "\n")
            self.report_text.insert(tk.END, f"Total Subjects: {total_subjects}\n")
            self.report_text.insert(tk.END, f"Total Marks: {total_marks}/{total_subjects * 100}\n")
            self.report_text.insert(tk.END, f"Average Percentage: {average:.2f}%\n")
            
            overall_grade = "A+" if average >= 90 else "A" if average >= 80 else "B+" if average >= 70 else "B" if average >= 60 else "C" if average >= 50 else "F"
            self.report_text.insert(tk.END, f"Overall Grade: {overall_grade}\n")
            
            result = "PASS" if all(mark[1] >= 50 for mark in marks_data) else "FAIL"
            self.report_text.insert(tk.END, f"Result: {result}\n")
            
            self.status_var.set(f"Report card generated for {student[1]}")
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error generating report card: {e}")
        finally:
            cursor.close()
    
    def on_closing(self):
        """
        Handle application closing
        """
        if self.connection:
            db_config.close_connection()
        self.root.destroy()

def main():
    """
    Main function to run the application
    """
    root = tk.Tk()
    app = GradeMateApp(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the GUI main loop
    root.mainloop()

if __name__ == "__main__":
    # Import dialog for report card functionality
    import tkinter.simpledialog
    main()
