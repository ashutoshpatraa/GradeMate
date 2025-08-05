"""
GradeMate - Student Grade Management System
A modern GUI application inspired by Wuthering Waves aesthetic.
Built with CustomTkinter and MySQL for managing student data and marks.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
from db_config import db_config
import mysql.connector
from mysql.connector import Error

class GradeMateApp:
    def __init__(self, root):
        """
        Initialize the main application window with Wuthering Waves theme
        """
        self.root = root
        self.root.title("GradeMate - Student Grade Management System")
        self.root.geometry("1400x900")
        self.root.resizable(True, True)
        
        # Wuthering Waves Theme Colors
        self.colors = {
            'bg_primary': '#0A0A0A',      # Deep black background
            'bg_secondary': '#1A1A1A',    # Secondary dark
            'bg_tertiary': '#2A2A2A',     # Card background
            'accent_cyan': '#00FFF7',     # Glowing neon cyan
            'accent_blue': '#00BFFF',     # Bright blue
            'accent_purple': '#8A2BE2',   # Purple accent
            'text_primary': '#FFFFFF',    # Pure white text
            'text_secondary': '#CCCCCC',  # Light gray text
            'text_muted': '#808080',      # Muted gray
            'border': '#333333',          # Border color
            'success': '#00FF41',         # Success green
            'warning': '#FFD700',         # Warning gold
            'error': '#FF073A',           # Error red
            'hover': '#404040'            # Hover state
        }
        
        # Configure CustomTkinter appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configure root window
        self.root.configure(fg_color=self.colors['bg_primary'])
        
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
        
        # Configure Notebook (tabs) - Modern Design
        style.configure('TNotebook', 
                       background=self.colors['bg_primary'],
                       borderwidth=0,
                       tabmargins=[2, 5, 2, 0])
        style.configure('TNotebook.Tab',
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_muted'],
                       padding=[25, 15],
                       borderwidth=0,
                       focuscolor='none')
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['accent_blue']),
                           ('active', self.colors['hover'])],
                 foreground=[('selected', '#FFFFFF'),
                           ('active', self.colors['text_primary'])],
                 expand=[('selected', [1, 1, 1, 0])])
        
        # Configure Frame
        style.configure('TFrame',
                       background=self.colors['bg_primary'],
                       borderwidth=0)
        
        # Configure LabelFrame - Minimal & Clean
        style.configure('TLabelframe',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=0,
                       relief='flat')
        style.configure('TLabelframe.Label',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 12, 'bold'))
        
        # Modern Card Style
        style.configure('Card.TLabelframe',
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       borderwidth=1,
                       relief='flat')
        style.configure('Card.TLabelframe.Label',
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['accent_cyan'],
                       font=('Segoe UI', 13, 'bold'))
        
        # Configure Labels - Better Typography
        style.configure('TLabel',
                       background=self.colors['bg_primary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 11))
        
        # Configure Entry widgets - Modern Input Fields
        style.configure('TEntry',
                       fieldbackground=self.colors['bg_accent'],
                       background=self.colors['bg_accent'],
                       foreground=self.colors['text_primary'],
                       borderwidth=2,
                       relief='flat',
                       insertcolor=self.colors['accent_blue'],
                       font=('Segoe UI', 11))
        style.map('TEntry',
                 focuscolor=[('focus', self.colors['accent_blue'])],
                 bordercolor=[('focus', self.colors['accent_blue'])])
        
        # Configure Modern Buttons
        style.configure('TButton',
                       background=self.colors['accent_blue'],
                       foreground='#FFFFFF',
                       borderwidth=0,
                       relief='flat',
                       focuscolor='none',
                       font=('Segoe UI', 11, 'bold'),
                       padding=[20, 12])
        style.map('TButton',
                 background=[('active', self.colors['accent_purple']),
                           ('pressed', '#2563EB')])
        
        # Premium Button Styles
        style.configure('Primary.TButton',
                       background=self.colors['accent_blue'],
                       foreground='#FFFFFF',
                       font=('Segoe UI', 11, 'bold'),
                       padding=[25, 15])
        style.map('Primary.TButton',
                 background=[('active', '#2563EB'),
                           ('pressed', '#1D4ED8')])
        
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='#FFFFFF',
                       font=('Segoe UI', 11, 'bold'),
                       padding=[25, 15])
        style.map('Success.TButton',
                 background=[('active', '#38A169'),
                           ('pressed', '#2F855A')])
        
        style.configure('Warning.TButton',
                       background=self.colors['warning'],
                       foreground='#FFFFFF',
                       font=('Segoe UI', 11, 'bold'),
                       padding=[25, 15])
        style.map('Warning.TButton',
                 background=[('active', '#DD6B20'),
                           ('pressed', '#C05621')])
        
        style.configure('Secondary.TButton',
                       background=self.colors['bg_accent'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 11),
                       padding=[25, 15])
        style.map('Secondary.TButton',
                 background=[('active', self.colors['hover']),
                           ('pressed', self.colors['border'])])
        
        # Configure Modern Treeview
        style.configure('Treeview',
                       background=self.colors['bg_tertiary'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['bg_tertiary'],
                       borderwidth=0,
                       font=('Segoe UI', 10),
                       rowheight=35)
        style.configure('Treeview.Heading',
                       background=self.colors['bg_accent'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=0,
                       relief='flat')
        style.map('Treeview',
                 background=[('selected', self.colors['accent_blue'])],
                 foreground=[('selected', '#FFFFFF')])
        style.map('Treeview.Heading',
                 background=[('active', self.colors['hover'])])
        
        # Configure Modern Scrollbar
        style.configure('Vertical.TScrollbar',
                       background=self.colors['bg_accent'],
                       troughcolor=self.colors['bg_primary'],
                       borderwidth=0,
                       arrowcolor=self.colors['text_secondary'],
                       darkcolor=self.colors['bg_accent'],
                       lightcolor=self.colors['bg_accent'])
        style.map('Vertical.TScrollbar',
                 background=[('active', self.colors['accent_blue'])])
        
    def create_widgets(self):
        """
        Create and organize all GUI widgets with modern design
        """
        # Main container with better spacing
        main_container = ttk.Frame(self.root)
        main_container.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Modern Header Section
        self.create_header(main_container)
        
        # Create notebook for tabs with improved spacing
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill='both', expand=True, pady=(30, 20))
        
        # Create tabs
        self.create_student_tab()
        self.create_marks_tab()
        self.create_reports_tab()
        
        # Modern status bar
        self.create_status_bar(main_container)
    
    def create_header(self, parent):
        """
        Create modern header with proper branding
        """
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'], height=80)
        header_frame.pack(fill='x', pady=(0, 30))
        header_frame.pack_propagate(False)
        
        # Brand container
        brand_container = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        brand_container.pack(expand=True, fill='both')
        
        # App title with proper hierarchy
        title_label = tk.Label(brand_container, 
                              text="GradeMate",
                              font=('Segoe UI', 28, 'bold'),
                              bg=self.colors['bg_primary'],
                              fg=self.colors['accent_cyan'])
        title_label.pack(pady=(15, 5))
        
        # Subtitle with better typography
        subtitle_label = tk.Label(brand_container,
                                 text="Student Grade Management System",
                                 font=('Segoe UI', 14),
                                 bg=self.colors['bg_primary'],
                                 fg=self.colors['text_secondary'])
        subtitle_label.pack()
    
    def create_status_bar(self, parent):
        """
        Create modern status bar
        """
        status_frame = tk.Frame(parent, bg=self.colors['bg_tertiary'], height=50)
        status_frame.pack(fill='x')
        status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar()
        self.status_var.set("● Connected to Database")
        status_bar = tk.Label(status_frame, 
                             textvariable=self.status_var, 
                             bg=self.colors['bg_tertiary'],
                             fg=self.colors['success'],
                             font=('Segoe UI', 10),
                             anchor=tk.W)
        status_bar.pack(side=tk.LEFT, fill=tk.X, padx=25, pady=15)
    
    def create_student_tab(self):
        """
        Create enhanced student management tab
        """
        # Student tab frame
        student_frame = ttk.Frame(self.notebook)
        self.notebook.add(student_frame, text="Student Management")
        
        # Main container with better spacing
        container = ttk.Frame(student_frame)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Input frame with enhanced glassmorphism styling
        input_frame = ttk.LabelFrame(container, text="✨ Student Information", padding=25, style='Glass.TLabelframe')
        input_frame.pack(fill='x', pady=(0, 25))
        
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
        
        # Styled buttons with glassmorphism icons
        ttk.Button(button_frame, text="✨ Add Student", 
                  command=self.add_student, style='GlassSuccess.TButton').pack(side='left', padx=(0, 15))
        ttk.Button(button_frame, text="🔮 Update Student", 
                  command=self.update_student, style='Glass.TButton').pack(side='left', padx=(0, 15))
        ttk.Button(button_frame, text="� Delete Student", 
                  command=self.delete_student, style='GlassWarning.TButton').pack(side='left', padx=(0, 15))
        ttk.Button(button_frame, text="🌊 Clear Fields", 
                  command=self.clear_student_fields, style='GlassSecondary.TButton').pack(side='left', padx=(0, 15))
        
        # Students list frame with enhanced glassmorphism styling
        list_frame = ttk.LabelFrame(container, text="� Students Database", padding=20, style='Glass.TLabelframe')
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
        self.notebook.add(marks_frame, text="Marks Management")
        
        # Main container
        container = ttk.Frame(marks_frame)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Input frame with enhanced glassmorphism styling
        input_frame = ttk.LabelFrame(container, text="✨ Add Student Marks", padding=25, style='Glass.TLabelframe')
        input_frame.pack(fill='x', pady=(0, 25))
        
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
        
        # Styled glassmorphism buttons
        ttk.Button(button_frame, text="✨ Add Marks", 
                  command=self.add_marks, style='GlassSuccess.TButton').pack(side='left', padx=(0, 15))
        ttk.Button(button_frame, text="🌊 Clear Fields", 
                  command=self.clear_marks_fields, style='GlassSecondary.TButton').pack(side='left')
        
        # Marks list frame with glassmorphism
        list_frame = ttk.LabelFrame(container, text="� Marks Database", padding=20, style='Glass.TLabelframe')
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
        self.notebook.add(reports_frame, text="Reports & Analytics")
        
        # Main container
        container = ttk.Frame(reports_frame)
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Enhanced buttons frame with glassmorphism
        button_frame = ttk.LabelFrame(container, text="� Generate Reports", padding=20, style='Glass.TLabelframe')
        button_frame.pack(fill='x', pady=(0, 25))
        
        # Create button container for better layout
        btn_container = ttk.Frame(button_frame)
        btn_container.pack(expand=True)
        
        # Styled glassmorphism report buttons with enhanced icons
        ttk.Button(btn_container, text="� Student Averages", 
                  command=self.show_student_averages,
                  style='Glass.TButton').pack(side='left', padx=(0, 20))
        ttk.Button(btn_container, text="✨ Top Scorers", 
                  command=self.show_top_scorers,
                  style='GlassSuccess.TButton').pack(side='left', padx=(0, 20))
        ttk.Button(btn_container, text="� Generate Report Card", 
                  command=self.generate_report_card,
                  style='Glass.TButton').pack(side='left')
        
        # Enhanced report display frame with glassmorphism
        display_frame = ttk.LabelFrame(container, text="� Report Display", padding=20, style='Glass.TLabelframe')
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
        
        # Add welcome message with glassmorphism theme
        welcome_msg = """
✨ Welcome to GradeMate Reports & Analytics!

� Available Glassmorphism Reports:
• Student Averages - View all students with their average marks and grades
• Top Scorers - See the highest-performing students (Top 10)  
• Report Card - Generate detailed individual student report cards

� Click any glassmorphism button above to generate reports!

🌊 Enhanced Features:
• Advanced MySQL functions (AVG, ROUND, IF, JOIN)
• Real-time calculations with glassmorphism UI
• Professional formatting with glass effects
• Grade assignment (A+, A, B+, B, C, F)
• Pass/Fail status determination
• Smooth glassmorphism animations and effects
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
            self.status_var.set(f"✓ Student {name} added successfully")
            
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
                self.status_var.set(f"✓ Student {name} updated successfully")
            
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
                    self.status_var.set(f"✓ Student with roll number {roll_no} deleted")
            
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
            self.status_var.set(f"✓ Marks added for roll number {roll_no} in {subject}")
            
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
            self.status_var.set("✓ Student averages report generated successfully")
            
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
