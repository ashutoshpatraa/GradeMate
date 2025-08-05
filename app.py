"""
GradePulse - Futuristic Student Grade Tracker
A Wuthering Waves-inspired app with glassmorphism design
Built with CustomTkinter and MySQL
"""

import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class GradePulseApp:
    def __init__(self, root):
        """Initialize GradePulse with Wuthering Waves theme"""
        self.root = root
        self.root.title("GradePulse - Student Grade Tracker")
        self.root.geometry("1600x1000")
        self.root.resizable(True, True)
        
        # Wuthering Waves Dark Neon Palette
        self.colors = {
            'bg_primary': '#0f1117',      # Deep dark background
            'bg_secondary': '#141926',    # Slightly lighter dark
            'bg_glass': '#1a1f2e',        # Glass effect simulation
            'accent_neon': '#00ffff',     # Neon cyan primary
            'accent_purple': '#9d4edd',   # Soft neon purple
            'accent_glow': '#7209b7',     # Purple glow
            'text_primary': '#ffffff',    # Pure white
            'text_secondary': '#c8d6e5',  # Cool light gray
            'text_muted': '#8395a7',      # Muted blue-gray
            'success': '#00ff88',         # Neon green
            'warning': '#ffd700',         # Gold
            'danger': '#ff4757',          # Neon red
            'glow_cyan': '#00ffff40',     # Cyan with transparency
            'glow_purple': '#9d4edd40',   # Purple with transparency
            'card_border': '#2c3e50',     # Subtle border
            'sidebar_bg': '#111822'       # Sidebar background
        }
        
        # Configure CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Database connection
        self.connection = None
        self.connect_database()
        
        # Current user data
        self.user_id = "STU001"
        self.current_average = 0.0
        self.improvement_percent = 0.0
        self.subjects_data = []
        
        # Create main interface
        self.create_main_layout()
        self.load_user_data()
        
    def connect_database(self):
        """Connect to MySQL database"""
        try:
            # First connect without specifying database to create it if needed
            temp_connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='qwerty4954'
            )
            cursor = temp_connection.cursor()
            
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS gradepulse_db")
            cursor.close()
            temp_connection.close()
            
            # Now connect to the specific database
            self.connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='qwerty4954',
                database='gradepulse_db'
            )
            self.create_tables()
            print("✅ Connected to GradePulse database")
        except Error as e:
            print(f"❌ Database error: {e}")
            # Don't show error dialog, just continue without database
            print("⚠️ Running in offline mode - database features disabled")
            self.connection = None
    
    def create_tables(self):
        """Create necessary database tables"""
        if not self.connection:
            return
            
        cursor = self.connection.cursor()
        
        # Subjects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                marks DECIMAL(5,2) NOT NULL,
                max_marks DECIMAL(5,2) DEFAULT 100,
                weightage DECIMAL(5,2) DEFAULT 1.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Performance history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS performance_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                average_grade DECIMAL(5,2) NOT NULL,
                total_subjects INT NOT NULL,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        self.connection.commit()
        cursor.close()
    
    def create_main_layout(self):
        """Create the main Wuthering Waves themed layout"""
        # Configure root
        self.root.configure(fg_color=self.colors['bg_primary'])
        
        # Main container
        main_container = ctk.CTkFrame(
            self.root,
            fg_color=self.colors['bg_primary'],
            corner_radius=0
        )
        main_container.pack(fill='both', expand=True)
        
        # Create layout sections
        self.create_header(main_container)
        self.create_content_area(main_container)
        self.create_footer(main_container)
    
    def create_header(self, parent):
        """Create futuristic header with gradient effect"""
        header_frame = ctk.CTkFrame(
            parent,
            height=80,
            fg_color=self.colors['bg_secondary'],
            corner_radius=0
        )
        header_frame.pack(fill='x', padx=20, pady=(20, 0))
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill='both', expand=True, padx=30, pady=15)
        
        # Logo and title
        title_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        title_frame.pack(side='left', fill='y')
        
        # App title with modern style
        title_label = ctk.CTkLabel(
            title_frame,
            text="� GRADEMATE",
            font=ctk.CTkFont(family="Consolas", size=24, weight="bold"),
            text_color=self.colors['text_primary']
        )
        title_label.pack(side='left', padx=(0, 10))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="WUTHERING WAVES EDITION",
            font=ctk.CTkFont(family="SF Pro Text", size=10),
            text_color=self.colors['text_secondary']
        )
        subtitle_label.pack(side='left', padx=(10, 0))
        
        # User info on right
        user_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        user_frame.pack(side='right', fill='y')
        
        user_label = ctk.CTkLabel(
            user_frame,
            text=f"👤 {self.user_id}",
            font=ctk.CTkFont(family="JetBrains Mono", size=12),
            text_color=self.colors['text_primary']
        )
        user_label.pack(side='right', pady=10)
    
    def create_content_area(self, parent):
        """Create main content area with Wuthering Waves layout"""
        content_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            corner_radius=0
        )
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Configure grid for vertical sidebar layout
        content_frame.grid_columnconfigure(0, weight=0, minsize=280)  # Sidebar
        content_frame.grid_columnconfigure(1, weight=1, minsize=800)  # Main content
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Left vertical sidebar (Wuthering Waves style)
        self.create_vertical_sidebar(content_frame)
        
        # Main content area
        self.create_main_content(content_frame)
    
    def create_navigation(self, parent):
        """Create left navigation menu with modern card design"""
        nav_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_glass'],
            corner_radius=25,
            border_width=0
        )
        nav_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 15))
        
        # Navigation title
        nav_title = ctk.CTkLabel(
            nav_frame,
            text="📊 Dashboard",
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            text_color=self.colors['text_primary']
        )
        nav_title.pack(pady=(30, 20))
        
        # Recent subjects/grades
        recent_items = [
            ("� Mathematics", "92%", "+5.2% ↑", self.colors['success']),
            ("� Physics", "85%", "-1.8% ↓", self.colors['danger']),
            ("📙 Chemistry", "88%", "+2.4% ↑", self.colors['success'])
        ]
        
        for name, grade, change, color in recent_items:
            item_frame = ctk.CTkFrame(
                nav_frame,
                fg_color=self.colors['bg_primary'],
                corner_radius=15,
                height=60
            )
            item_frame.pack(fill='x', padx=20, pady=5)
            item_frame.pack_propagate(False)
            
            # Subject info
            info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            info_frame.pack(fill='both', expand=True, padx=15, pady=10)
            
            name_label = ctk.CTkLabel(
                info_frame,
                text=name,
                font=ctk.CTkFont(family="SF Pro Text", size=12, weight="bold"),
                text_color=self.colors['text_primary']
            )
            name_label.pack(side='left')
            
            change_label = ctk.CTkLabel(
                info_frame,
                text=change,
                font=ctk.CTkFont(family="SF Pro Text", size=10),
                text_color=color
            )
            change_label.pack(side='right')
            
            grade_label = ctk.CTkLabel(
                info_frame,
                text=grade,
                font=ctk.CTkFont(family="SF Pro Text", size=11),
                text_color=self.colors['text_secondary']
            )
            grade_label.pack(side='right', padx=(0, 10))
        
        # Add subject button
        add_subject_btn = ctk.CTkButton(
            nav_frame,
            text="➕ ADD SUBJECT",
            command=self.show_add_subject_dialog,
            font=ctk.CTkFont(family="SF Pro Text", size=12, weight="bold"),
            fg_color=self.colors['accent_purple'],
            hover_color=self.colors['accent_glow'],
            text_color=self.colors['text_primary'],
            corner_radius=15,
            height=40
        )
        add_subject_btn.pack(fill='x', padx=20, pady=(30, 20))
    
    def create_vertical_sidebar(self, parent):
        """Create Wuthering Waves style vertical sidebar"""
        sidebar = ctk.CTkFrame(
            parent,
            fg_color=self.colors['sidebar_bg'],
            corner_radius=25,
            border_width=1,
            border_color=self.colors['accent_neon']
        )
        sidebar.grid(row=0, column=0, sticky='nsew', padx=(0, 20))
        
        # Sidebar header with avatar
        header_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        header_frame.pack(fill='x', padx=20, pady=(30, 40))
        
        # User avatar circle
        avatar_frame = ctk.CTkFrame(
            header_frame,
            fg_color=self.colors['accent_neon'],
            corner_radius=35,
            width=70,
            height=70
        )
        avatar_frame.pack()
        avatar_frame.pack_propagate(False)
        
        avatar_label = ctk.CTkLabel(
            avatar_frame,
            text="👤",
            font=ctk.CTkFont(size=28),
            text_color=self.colors['bg_primary']
        )
        avatar_label.pack(expand=True)
        
        # User name
        user_name = ctk.CTkLabel(
            header_frame,
            text="Student Portal",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            text_color=self.colors['text_primary']
        )
        user_name.pack(pady=(10, 5))
        
        # User ID
        user_id = ctk.CTkLabel(
            header_frame,
            text=self.user_id,
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color=self.colors['accent_neon']
        )
        user_id.pack()
        
        # Navigation menu
        nav_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        nav_frame.pack(fill='x', padx=20, pady=20)
        
        # Menu items with Wuwa style
        menu_items = [
            ("🏠", "Dashboard", True),
            ("📚", "Subjects", False),
            ("📊", "Analytics", False),
            ("🏆", "Performance", False),
            ("⚙️", "Settings", False)
        ]
        
        for icon, text, is_active in menu_items:
            self.create_sidebar_item(nav_frame, icon, text, is_active)
        
        # Add subject button at bottom
        add_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        add_frame.pack(side='bottom', fill='x', padx=20, pady=30)
        
        add_button = ctk.CTkButton(
            add_frame,
            text="➕ ADD SUBJECT",
            command=self.show_add_subject_dialog,
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            fg_color=self.colors['accent_neon'],
            hover_color=self.colors['accent_purple'],
            text_color=self.colors['bg_primary'],
            corner_radius=15,
            height=45
        )
        add_button.pack(fill='x')
    
    def create_sidebar_item(self, parent, icon, text, is_active):
        """Create individual sidebar menu item with glow effect"""
        if is_active:
            item_color = self.colors['accent_neon']
            text_color = self.colors['bg_primary']
        else:
            item_color = "transparent"
            text_color = self.colors['text_secondary']
        
        item_frame = ctk.CTkFrame(
            parent,
            fg_color=item_color,
            corner_radius=15,
            height=50,
            border_width=1 if not is_active else 0,
            border_color=self.colors['card_border']
        )
        item_frame.pack(fill='x', pady=5)
        item_frame.pack_propagate(False)
        
        # Content frame
        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Icon
        icon_label = ctk.CTkLabel(
            content_frame,
            text=icon,
            font=ctk.CTkFont(size=16),
            text_color=text_color
        )
        icon_label.pack(side='left')
        
        # Text
        text_label = ctk.CTkLabel(
            content_frame,
            text=text,
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold" if is_active else "normal"),
            text_color=text_color
        )
        text_label.pack(side='left', padx=(15, 0))
    
    def create_main_content(self, parent):
        """Create main content area with glassmorphism cards"""
        main_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            corner_radius=0
        )
        main_frame.grid(row=0, column=1, sticky='nsew')
        
        # Configure main content grid
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Top section with overview cards
        self.create_overview_cards(main_frame)
        
        # Bottom section with subjects and analytics
        self.create_subjects_analytics(main_frame)
    
    def create_overview_cards(self, parent):
        """Create overview cards with glassmorphism effect"""
        overview_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        overview_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 20))
        
        # Configure grid for cards
        overview_frame.grid_columnconfigure(0, weight=1)
        overview_frame.grid_columnconfigure(1, weight=1)
        overview_frame.grid_columnconfigure(2, weight=1)
        
        # Grade average card
        self.create_glass_card(overview_frame, 0, 0, "📊", "Grade Average", f"{self.current_average:.1f}%", self.colors['accent_neon'])
        
        # Total subjects card
        self.create_glass_card(overview_frame, 0, 1, "📚", "Total Subjects", str(len(self.subjects_data)), self.colors['accent_purple'])
        
        # Performance trend card
        trend = "Improving" if self.improvement_percent >= 0 else "Declining"
        self.create_glass_card(overview_frame, 0, 2, "📈", "Trend", trend, self.colors['success'] if self.improvement_percent >= 0 else self.colors['danger'])
    
    def create_glass_card(self, parent, row, col, icon, title, value, accent_color):
        """Create individual glassmorphism card"""
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_secondary'],
            corner_radius=20,
            border_width=1,
            border_color=accent_color,
            height=120
        )
        card.grid(row=row, column=col, sticky='ew', padx=10, pady=10)
        card.pack_propagate(False)
        
        # Card content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Icon
        icon_label = ctk.CTkLabel(
            content,
            text=icon,
            font=ctk.CTkFont(size=32),
            text_color=accent_color
        )
        icon_label.pack()
        
        # Value
        value_label = ctk.CTkLabel(
            content,
            text=value,
            font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
            text_color=self.colors['text_primary']
        )
        value_label.pack(pady=(5, 0))
        
        # Title
        title_label = ctk.CTkLabel(
            content,
            text=title,
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color=self.colors['text_secondary']
        )
        title_label.pack()
    
    def create_subjects_analytics(self, parent):
        """Create subjects list and analytics section"""
        # Subjects card (left)
        subjects_card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_secondary'],
            corner_radius=20,
            border_width=1,
            border_color=self.colors['accent_neon']
        )
        subjects_card.grid(row=1, column=0, sticky='nsew', padx=(0, 10))
        
        # Subjects header
        subjects_header = ctk.CTkFrame(subjects_card, fg_color="transparent")
        subjects_header.pack(fill='x', padx=20, pady=(20, 10))
        
        subjects_title = ctk.CTkLabel(
            subjects_header,
            text="📚 MY SUBJECTS",
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            text_color=self.colors['accent_neon']
        )
        subjects_title.pack(side='left')
        
        # Subjects list
        if self.subjects_data:
            for i, subject in enumerate(self.subjects_data[:5]):  # Show top 5
                self.create_subject_item(subjects_card, subject, i)
        else:
            empty_label = ctk.CTkLabel(
                subjects_card,
                text="No subjects added yet",
                font=ctk.CTkFont(family="Consolas", size=12),
                text_color=self.colors['text_secondary']
            )
            empty_label.pack(pady=50)
        
        # Analytics card (right)
        self.create_analytics_card(parent)
    
    def create_subject_item(self, parent, subject, index):
        """Create individual subject item with neon styling"""
        colors = [self.colors['accent_neon'], self.colors['accent_purple'], self.colors['success']]
        icons = ["🔵", "🟣", "🟢"]
        
        item_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            height=45
        )
        item_frame.pack(fill='x', padx=20, pady=3)
        item_frame.pack_propagate(False)
        
        # Icon
        icon_frame = ctk.CTkFrame(
            item_frame,
            fg_color=colors[index % 3],
            corner_radius=20,
            width=35,
            height=35
        )
        icon_frame.pack(side='left', pady=5)
        icon_frame.pack_propagate(False)
        
        icon_label = ctk.CTkLabel(
            icon_frame,
            text=icons[index % 3],
            font=ctk.CTkFont(size=14),
            text_color=self.colors['bg_primary']
        )
        icon_label.pack(expand=True)
        
        # Subject info
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.pack(side='left', fill='x', expand=True, padx=15)
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=subject['name'],
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=self.colors['text_primary']
        )
        name_label.pack(anchor='w')
        
        # Grade
        grade_label = ctk.CTkLabel(
            item_frame,
            text=f"{subject['marks']:.1f}%",
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=colors[index % 3]
        )
        grade_label.pack(side='right', padx=10)
    
    def create_analytics_card(self, parent):
        """Create analytics visualization card"""
        analytics_card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_secondary'],
            corner_radius=20,
            border_width=1,
            border_color=self.colors['accent_purple']
        )
        analytics_card.grid(row=1, column=1, sticky='nsew', padx=(10, 0))
        
        # Analytics header
        analytics_header = ctk.CTkFrame(analytics_card, fg_color="transparent")
        analytics_header.pack(fill='x', padx=20, pady=(20, 10))
        
        analytics_title = ctk.CTkLabel(
            analytics_header,
            text="📈 PERFORMANCE ANALYTICS",
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            text_color=self.colors['accent_purple']
        )
        analytics_title.pack()
        
        # Create improved chart
        self.create_neon_chart(analytics_card)
    
    def create_neon_chart(self, parent):
        """Create neon-styled chart for Wuthering Waves aesthetic"""
        chart_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            height=250
        )
        chart_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create matplotlib figure with dark neon theme
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(5, 3.5), facecolor='none')
        fig.patch.set_alpha(0)
        ax.set_facecolor('#0f1117')  # Match our background
        
        if self.subjects_data:
            # Real data with neon colors
            labels = [subj['name'] for subj in self.subjects_data]
            sizes = [subj['marks'] for subj in self.subjects_data]
            neon_colors = [self.colors['accent_neon'], self.colors['accent_purple'], 
                          self.colors['success'], '#ffd700', '#ff4757'][:len(labels)]
        else:
            # Demo data with neon theme
            labels = ['Mathematics', 'Physics', 'Chemistry', 'Biology']
            sizes = [85, 92, 78, 88]
            neon_colors = [self.colors['accent_neon'], self.colors['accent_purple'], 
                          self.colors['success'], '#ffd700']
        
        # Create neon pie chart
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            colors=neon_colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'color': '#ffffff', 'fontsize': 9, 'weight': 'bold'},
            wedgeprops={'linewidth': 2, 'edgecolor': '#ffffff40'}
        )
        
        # Add glow effect to text
        for text in texts:
            text.set_fontfamily('Orbitron')
        for autotext in autotexts:
            autotext.set_fontfamily('Orbitron')
            autotext.set_color('#ffffff')
        
        ax.set_title('PERFORMANCE DISTRIBUTION', 
                    color=self.colors['accent_neon'], 
                    fontsize=12, 
                    fontweight='bold',
                    fontfamily='Orbitron',
                    pad=20)
        
        # Embed chart in tkinter
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        plt.close(fig)  # Prevent memory leaks
    
    def create_stats_cards(self, parent):
        """Create center wallet-style cards with premium design"""
        cards_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            corner_radius=0
        )
        cards_frame.grid(row=0, column=1, sticky='nsew', padx=15)
        
        # Configure cards grid  
        cards_frame.grid_rowconfigure(0, weight=1)
        cards_frame.grid_rowconfigure(1, weight=1)
        cards_frame.grid_columnconfigure(0, weight=1)
        
        # Main wallet card (large gradient card)
        self.create_main_subjects_card(cards_frame, 0)
        
        # Bottom section with smaller cards
        self.create_bottom_cards(cards_frame, 1)
    
    def create_main_subjects_card(self, parent, row):
        """Create main wallet card with gradient background"""
        # Create gradient effect with layered frames
        card_container = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            corner_radius=0
        )
        card_container.grid(row=row, column=0, sticky='ew', pady=10)
        
        # Main wallet card with gradient simulation
        main_card = ctk.CTkFrame(
            card_container,
            fg_color=self.colors['accent_purple'],  # Purple gradient base
            corner_radius=25,
            height=180
        )
        main_card.pack(fill='x', pady=10)
        main_card.pack_propagate(False)
        
        # Header section
        header_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        header_frame.pack(fill='x', padx=30, pady=(20, 10))
        
        # Grade overview title and stats icon
        grade_label = ctk.CTkLabel(
            header_frame,
            text="� WALLET",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            text_color="white"
        )
        grade_label.pack(side='left')
        
        stats_label = ctk.CTkLabel(
            header_frame,
            text="⬜",
            font=ctk.CTkFont(size=16),
            text_color="white"
        )
        stats_label.pack(side='right')
        
        # Main grade display
        grade_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        grade_frame.pack(fill='x', padx=30, pady=10)
        
        # Grade as percentage
        grade_percentage = f"{self.current_average:.1f}%"
        
        self.main_balance_display = ctk.CTkLabel(
            grade_frame,
            text=grade_percentage,
            font=ctk.CTkFont(family="Consolas", size=36, weight="bold"),
            text_color="white"
        )
        self.main_balance_display.pack(anchor='w')
        
        # Improvement indicator
        improvement_text = f"+ ${abs(self.improvement_percent * 10):.2f} ({abs(self.improvement_percent):.1f}%) ↑"
        improvement_color = "lightgreen" if self.improvement_percent >= 0 else "lightcoral"
        
        self.improvement_indicator = ctk.CTkLabel(
            grade_frame,
            text=improvement_text,
            font=ctk.CTkFont(family="SF Pro Text", size=12),
            text_color=improvement_color
        )
        self.improvement_indicator.pack(anchor='w', pady=(5, 0))
    
    def create_bottom_cards(self, parent, row):
        """Create bottom section with My Subjects and performance cards"""
        bottom_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            corner_radius=0
        )
        bottom_frame.grid(row=row, column=0, sticky='ew', pady=10)
        
        # Configure bottom grid
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=1)
        bottom_frame.grid_rowconfigure(0, weight=1)
        
        # My Subjects card (left)
        self.create_my_subjects_card(bottom_frame, 0, 0)
        
        # Performance chart card (right)  
        self.create_performance_chart_card(bottom_frame, 0, 1)
    
    def create_my_subjects_card(self, parent, row, col):
        """Create My Subjects card with subject list"""
        subjects_card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_glass'],
            corner_radius=20,
            height=200
        )
        subjects_card.grid(row=row, column=col, sticky='nsew', padx=(0, 10))
        subjects_card.pack_propagate(False)
        
        # Header
        header_frame = ctk.CTkFrame(subjects_card, fg_color="transparent")
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        wallet_title = ctk.CTkLabel(
            header_frame,
            text="My Subjects",
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            text_color=self.colors['text_primary']
        )
        wallet_title.pack(side='left')
        
        add_coin_btn = ctk.CTkLabel(
            header_frame,
            text="ADD SUBJECT ➕",
            font=ctk.CTkFont(family="SF Pro Text", size=10),
            text_color=self.colors['accent_neon']
        )
        add_coin_btn.pack(side='right')
        
        # Total value
        total_value = f"${(self.current_average * len(self.subjects_data) * 50):.2f}"
        total_label = ctk.CTkLabel(
            subjects_card,
            text=total_value,
            font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
            text_color=self.colors['text_primary']
        )
        total_label.pack(padx=20, pady=(0, 10))
        
        # Subject list as crypto assets
        if self.subjects_data:
            for i, subject in enumerate(self.subjects_data[:3]):  # Show top 3
                self.create_crypto_item(subjects_card, subject, i)
        else:
            empty_label = ctk.CTkLabel(
                subjects_card,
                text="No subjects added yet",
                font=ctk.CTkFont(family="SF Pro Text", size=12),
                text_color=self.colors['text_secondary']
            )
            empty_label.pack(pady=20)
    
    def create_crypto_item(self, parent, subject, index):
        """Create individual crypto-style subject item"""
        colors = [self.colors['warning'], self.colors['accent_neon'], self.colors['accent_purple']]
        icons = ["₿", "Ξ", "◊"]
        
        item_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            height=40
        )
        item_frame.pack(fill='x', padx=20, pady=2)
        item_frame.pack_propagate(False)
        
        # Icon
        icon_frame = ctk.CTkFrame(
            item_frame,
            fg_color=colors[index % 3],
            corner_radius=15,
            width=30,
            height=30
        )
        icon_frame.pack(side='left', pady=5)
        icon_frame.pack_propagate(False)
        
        icon_label = ctk.CTkLabel(
            icon_frame,
            text=icons[index % 3],
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"
        )
        icon_label.pack(expand=True)
        
        # Subject info
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.pack(side='left', fill='x', expand=True, padx=10)
        
        subject_name = ctk.CTkLabel(
            info_frame,
            text=subject['name'][:8],  # Truncate long names
            font=ctk.CTkFont(family="SF Pro Text", size=11, weight="bold"),
            text_color=self.colors['text_primary']
        )
        subject_name.pack(anchor='w')
        
        subject_marks = ctk.CTkLabel(
            info_frame,
            text=f"{subject['marks']:.1f}%",
            font=ctk.CTkFont(family="SF Pro Text", size=9),
            text_color=self.colors['text_secondary']
        )
        subject_marks.pack(anchor='w')
        
        # Value and change
        value_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        value_frame.pack(side='right')
        
        value = f"${subject['marks'] * 50:.0f}"
        value_label = ctk.CTkLabel(
            value_frame,
            text=value,
            font=ctk.CTkFont(family="SF Pro Text", size=11, weight="bold"),
            text_color=self.colors['text_primary']
        )
        value_label.pack(anchor='e')
        
        change = f"+{subject['marks'] * 0.1:.1f}%"
        change_color = self.colors['success'] if subject['marks'] > 70 else self.colors['danger']
        change_label = ctk.CTkLabel(
            value_frame,
            text=change,
            font=ctk.CTkFont(family="SF Pro Text", size=9),
            text_color=change_color
        )
        change_label.pack(anchor='e')
    
    def create_performance_chart_card(self, parent, row, col):
        """Create performance chart card matching the design"""
        chart_card = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_glass'],
            corner_radius=20,
            height=200
        )
        chart_card.grid(row=row, column=col, sticky='nsew', padx=(10, 0))
        chart_card.pack_propagate(False)
        
        # Chart content
        chart_content = ctk.CTkFrame(chart_card, fg_color="transparent")
        chart_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Performance metrics
        metrics_frame = ctk.CTkFrame(chart_content, fg_color="transparent")
        metrics_frame.pack(fill='x', pady=(0, 10))
        
        # Left metric
        left_metric = ctk.CTkFrame(metrics_frame, fg_color="transparent")
        left_metric.pack(side='left', fill='x', expand=True)
        
        left_value = ctk.CTkLabel(
            left_metric,
            text=f"+{self.current_average:.1f}%",
            font=ctk.CTkFont(family="Consolas", size=24, weight="bold"),
            text_color=self.colors['success']
        )
        left_value.pack(anchor='w')
        
        left_label = ctk.CTkLabel(
            left_metric,
            text="Subjects",
            font=ctk.CTkFont(family="SF Pro Text", size=10),
            text_color=self.colors['text_secondary']
        )
        left_label.pack(anchor='w')
        
        # Right metric
        right_metric = ctk.CTkFrame(metrics_frame, fg_color="transparent")
        right_metric.pack(side='right', fill='x', expand=True)
        
        right_value = ctk.CTkLabel(
            right_metric,
            text=f"+{self.improvement_percent:.1f}%",
            font=ctk.CTkFont(family="Consolas", size=24, weight="bold"),
            text_color=self.colors['text_primary']
        )
        right_value.pack(anchor='e')
        
        right_label = ctk.CTkLabel(
            right_metric,
            text="Grades",
            font=ctk.CTkFont(family="SF Pro Text", size=10),
            text_color=self.colors['text_secondary']
        )
        right_label.pack(anchor='e')
        
        # Simple wave chart simulation
        wave_frame = ctk.CTkFrame(
            chart_content,
            fg_color="transparent",
            height=60
        )
        wave_frame.pack(fill='x', pady=10)
        wave_frame.pack_propagate(False)
        
        wave_label = ctk.CTkLabel(
            wave_frame,
            text="📈 Performance trending upward",
            font=ctk.CTkFont(family="SF Pro Text", size=12),
            text_color=self.colors['accent_neon']
        )
        wave_label.pack(expand=True)
    
    def create_charts_panel(self, parent):
        """Create right panel with charts and visualization"""
        charts_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors['bg_glass'],
            corner_radius=20,
            border_width=1,
            border_color=self.colors['accent_purple']
        )
        charts_frame.grid(row=0, column=2, sticky='nsew', padx=(15, 0))
        
        # Charts title
        charts_title = ctk.CTkLabel(
            charts_frame,
            text="📊 PERFORMANCE ANALYTICS",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            text_color=self.colors['accent_purple']
        )
        charts_title.pack(pady=(20, 30))
        
        # Create pie chart
        self.create_pie_chart(charts_frame)
        
        # Add Subject button (gradient-styled)
        self.create_add_button(charts_frame)
    
    def create_pie_chart(self, parent):
        """Create pie chart for subjects distribution"""
        chart_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            height=300
        )
        chart_frame.pack(fill='x', padx=20, pady=20)
        chart_frame.pack_propagate(False)
        
        # Create matplotlib figure with dark theme
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(6, 4), facecolor='none')
        fig.patch.set_alpha(0)
        ax.set_facecolor('none')
        
        if self.subjects_data:
            # Real data
            labels = [subj['name'] for subj in self.subjects_data]
            sizes = [subj['marks'] for subj in self.subjects_data]
            colors = [self.colors['accent_purple'], self.colors['accent_neon'], 
                     self.colors['warning'], self.colors['success'], 
                     self.colors['warning']][:len(labels)]
        else:
            # Dummy data
            labels = ['Mathematics', 'Physics', 'Chemistry', 'Biology']
            sizes = [85, 92, 78, 88]
            colors = [self.colors['accent_purple'], self.colors['accent_neon'], 
                     self.colors['warning'], self.colors['success']]
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            sizes, 
            labels=labels, 
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'color': 'white', 'fontsize': 8}
        )
        
        ax.set_title('Subjects Performance Distribution', 
                    color='white', fontsize=10, pad=20)
        
        # Embed chart in tkinter
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
        plt.close(fig)  # Prevent memory leaks
    
    def create_add_button(self, parent):
        """Create gradient-styled Add Subject button"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(side='bottom', fill='x', padx=20, pady=20)
        
        add_button = ctk.CTkButton(
            button_frame,
            text="➕ ADD SUBJECT",
            command=self.show_add_subject_dialog,
            font=ctk.CTkFont(family="SF Pro Text", size=14, weight="bold"),
            fg_color=self.colors['accent_purple'],
            hover_color=self.colors['accent_glow'],
            text_color=self.colors['text_primary'],
            height=50,
            corner_radius=15
        )
        add_button.pack(fill='x')
    
    def create_footer(self, parent):
        """Create footer with Wuthering Waves styling"""
        footer_frame = ctk.CTkFrame(
            parent,
            height=40,
            fg_color=self.colors['bg_secondary'],
            corner_radius=0,
            border_width=1,
            border_color=self.colors['accent_neon']
        )
        footer_frame.pack(fill='x', padx=20, pady=(0, 20))
        footer_frame.pack_propagate(False)
        
        # Footer content
        footer_content = ctk.CTkFrame(footer_frame, fg_color="transparent")
        footer_content.pack(fill='both', expand=True, padx=20, pady=8)
        
        # User info with neon styling
        user_info = ctk.CTkLabel(
            footer_content,
            text=f"User: {self.user_id}",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            text_color=self.colors['accent_neon']
        )
        user_info.pack(side='left')
        
        # System status with neon effects
        if self.connection:
            sync_status = ctk.CTkLabel(
                footer_content,
                text="⚡ SYSTEM ONLINE • DATABASE CONNECTED",
                font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
                text_color=self.colors['success']
            )
        else:
            sync_status = ctk.CTkLabel(
                footer_content,
                text="⚠️ OFFLINE MODE • NO DATABASE CONNECTION",
                font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
                text_color=self.colors['danger']
            )
        sync_status.pack(side='right')
    
    def get_grade_letter(self, percentage):
        """Convert percentage to letter grade"""
        if percentage >= 90: return "A+"
        elif percentage >= 80: return "A"
        elif percentage >= 70: return "B+"
        elif percentage >= 60: return "B"
        elif percentage >= 50: return "C"
        else: return "F"
    
    def load_user_data(self):
        """Load user data from database"""
        if not self.connection:
            return
            
        try:
            cursor = self.connection.cursor()
            
            # Load subjects
            cursor.execute("SELECT name, marks, max_marks, weightage FROM subjects ORDER BY created_at DESC")
            subjects = cursor.fetchall()
            
            self.subjects_data = []
            total_weighted_marks = 0
            total_weight = 0
            
            for name, marks, max_marks, weightage in subjects:
                percentage = (marks / max_marks) * 100
                self.subjects_data.append({
                    'name': name,
                    'marks': percentage,
                    'weightage': weightage
                })
                total_weighted_marks += percentage * weightage
                total_weight += weightage
            
            # Calculate weighted average
            if total_weight > 0:
                self.current_average = total_weighted_marks / total_weight
            else:
                self.current_average = 0.0
            
            # Calculate improvement (dummy for now)
            self.improvement_percent = np.random.uniform(-5, 15)
            
            cursor.close()
            self.update_displays()
            
        except Error as e:
            print(f"Error loading data: {e}")
    
    def update_displays(self):
        """Update all display elements for Wuthering Waves theme"""
        # The new glassmorphism cards will be updated automatically
        # when data is reloaded via create_overview_cards and create_subjects_analytics
        return
    
    # Navigation functions
    def show_dashboard(self):
        """Show dashboard view"""
        print("📊 Dashboard selected")
    
    def show_add_subject(self):
        """Show add subject view"""
        print("➕ Add Subject selected")
    
    def show_analytics(self):
        """Show analytics view"""
        print("📈 Analytics selected")
    
    def show_performance(self):
        """Show performance view"""
        print("🎯 Performance selected")
    
    def show_add_subject_dialog(self):
        """Show add subject dialog"""
        dialog = AddSubjectDialog(self.root, self.colors, self.add_subject_callback)
    
    def add_subject_callback(self, subject_data):
        """Callback for adding new subject"""
        if not self.connection:
            messagebox.showerror("Error", "Database not connected")
            return
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO subjects (name, marks, max_marks, weightage) VALUES (%s, %s, %s, %s)",
                (subject_data['name'], subject_data['marks'], subject_data['max_marks'], subject_data['weightage'])
            )
            self.connection.commit()
            cursor.close()
            
            # Reload data and refresh UI
            self.load_user_data()
            self.create_charts_panel(self.root.winfo_children()[0].winfo_children()[1])  # Refresh charts
            
            messagebox.showinfo("Success", f"Subject '{subject_data['name']}' added successfully!")
            
        except Error as e:
            messagebox.showerror("Database Error", f"Error adding subject: {e}")

class AddSubjectDialog:
    """Dialog for adding new subjects"""
    def __init__(self, parent, colors, callback):
        self.colors = colors
        self.callback = callback
        
        # Create dialog window
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Add New Subject")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        self.dialog.configure(fg_color=colors['bg_primary'])
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_dialog_content()
    
    def create_dialog_content(self):
        """Create dialog content"""
        # Main frame
        main_frame = ctk.CTkFrame(
            self.dialog,
            fg_color=self.colors['bg_glass'],
            corner_radius=20,
            border_width=2,
            border_color=self.colors['accent_purple']
        )
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="➕ ADD NEW SUBJECT",
            font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
            text_color=self.colors['accent_purple']
        )
        title.pack(pady=(30, 40))
        
        # Input fields
        self.create_input_fields(main_frame)
        
        # Buttons
        self.create_dialog_buttons(main_frame)
    
    def create_input_fields(self, parent):
        """Create input fields"""
        # Subject name
        name_label = ctk.CTkLabel(
            parent,
            text="📚 Subject Name:",
            font=ctk.CTkFont(family="JetBrains Mono", size=12, weight="bold"),
            text_color=self.colors['text_primary']
        )
        name_label.pack(pady=(0, 5))
        
        self.name_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Enter subject name",
            font=ctk.CTkFont(family="SF Pro Text", size=12),
            fg_color=self.colors['bg_secondary'],
            border_color=self.colors['accent_purple'],
            text_color=self.colors['text_primary'],
            height=40,
            width=350
        )
        self.name_entry.pack(pady=(0, 20))
        
        # Marks
        marks_label = ctk.CTkLabel(
            parent,
            text="📊 Marks Obtained:",
            font=ctk.CTkFont(family="JetBrains Mono", size=12, weight="bold"),
            text_color=self.colors['text_primary']
        )
        marks_label.pack(pady=(0, 5))
        
        self.marks_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Enter marks obtained",
            font=ctk.CTkFont(family="SF Pro Text", size=12),
            fg_color=self.colors['bg_secondary'],
            border_color=self.colors['accent_purple'],
            text_color=self.colors['text_primary'],
            height=40,
            width=350
        )
        self.marks_entry.pack(pady=(0, 20))
        
        # Max marks
        max_marks_label = ctk.CTkLabel(
            parent,
            text="🎯 Maximum Marks:",
            font=ctk.CTkFont(family="JetBrains Mono", size=12, weight="bold"),
            text_color=self.colors['text_primary']
        )
        max_marks_label.pack(pady=(0, 5))
        
        self.max_marks_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Enter maximum marks (default: 100)",
            font=ctk.CTkFont(family="SF Pro Text", size=12),
            fg_color=self.colors['bg_secondary'],
            border_color=self.colors['accent_purple'],
            text_color=self.colors['text_primary'],
            height=40,
            width=350
        )
        self.max_marks_entry.pack(pady=(0, 20))
        self.max_marks_entry.insert(0, "100")  # Default value
        
        # Weightage
        weightage_label = ctk.CTkLabel(
            parent,
            text="⚖️ Subject Weightage:",
            font=ctk.CTkFont(family="JetBrains Mono", size=12, weight="bold"),
            text_color=self.colors['text_primary']
        )
        weightage_label.pack(pady=(0, 5))
        
        self.weightage_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Enter weightage (default: 1.0)",
            font=ctk.CTkFont(family="SF Pro Text", size=12),
            fg_color=self.colors['bg_secondary'],
            border_color=self.colors['accent_purple'],
            text_color=self.colors['text_primary'],
            height=40,
            width=350
        )
        self.weightage_entry.pack(pady=(0, 30))
        self.weightage_entry.insert(0, "1.0")  # Default value
    
    def create_dialog_buttons(self, parent):
        """Create dialog buttons"""
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill='x', padx=40, pady=(0, 30))
        
        # Add button
        add_button = ctk.CTkButton(
            button_frame,
            text="✅ ADD SUBJECT",
            command=self.add_subject,
            font=ctk.CTkFont(family="SF Pro Text", size=12, weight="bold"),
            fg_color=self.colors['success'],
            hover_color=self.colors['accent_purple'],
            text_color=self.colors['text_primary'],
            height=45,
            corner_radius=10
        )
        add_button.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        # Cancel button
        cancel_button = ctk.CTkButton(
            button_frame,
            text="❌ CANCEL",
            command=self.cancel,
            font=ctk.CTkFont(family="SF Pro Text", size=12, weight="bold"),
            fg_color=self.colors['danger'],
            hover_color=self.colors['warning'],
            text_color=self.colors['text_primary'],
            height=45,
            corner_radius=10
        )
        cancel_button.pack(side='right', fill='x', expand=True, padx=(10, 0))
    
    def add_subject(self):
        """Add subject and close dialog"""
        try:
            name = self.name_entry.get().strip()
            marks = float(self.marks_entry.get().strip())
            max_marks = float(self.max_marks_entry.get().strip())
            weightage = float(self.weightage_entry.get().strip())
            
            if not name:
                messagebox.showerror("Error", "Subject name cannot be empty")
                return
            
            if marks < 0 or max_marks <= 0 or weightage <= 0:
                messagebox.showerror("Error", "Invalid values entered")
                return
            
            if marks > max_marks:
                messagebox.showerror("Error", "Marks cannot exceed maximum marks")
                return
            
            subject_data = {
                'name': name,
                'marks': marks,
                'max_marks': max_marks,
                'weightage': weightage
            }
            
            self.callback(subject_data)
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")
    
    def cancel(self):
        """Cancel and close dialog"""
        self.dialog.destroy()

def main():
    """Main function to run GradePulse"""
    root = ctk.CTk()
    app = GradePulseApp(root)
    
    # Handle window closing
    def on_closing():
        if app.connection:
            app.connection.close()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
