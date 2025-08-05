"""
Database Configuration Module for GradeMate
This module handles MySQL database connection and table creation.
"""

import mysql.connector
from mysql.connector import Error

class DatabaseConfig:
    def __init__(self, host='localhost', user='root', password='qwerty', database='grademate_db'):
        """
        Initialize database configuration
        
        Args:
            host (str): MySQL server host
            user (str): MySQL username
            password (str): MySQL password
            database (str): Database name
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def create_connection(self):
        """
        Create connection to MySQL database
        Returns:
            mysql.connector.connection: Database connection object
        """
        try:
            # First, connect to MySQL server without specifying database
            temp_connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            
            if temp_connection.is_connected():
                cursor = temp_connection.cursor()
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.close()
            temp_connection.close()
        
        # Now connect to the specific database
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        
        if self.connection.is_connected():
            print(f"Successfully connected to MySQL database: {self.database}")
            self.create_tables()
            return self.connection        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    def create_tables(self):
        """
        Create required tables if they don't exist
        """
        try:
            cursor = self.connection.cursor()
            
            # Create students table
            students_table = """
            CREATE TABLE IF NOT EXISTS students (
                roll_no INT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                class INT NOT NULL
            )
            """
            
            # Create marks table
            marks_table = """
            CREATE TABLE IF NOT EXISTS marks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                roll_no INT,
                subject VARCHAR(50) NOT NULL,
                marks INT NOT NULL CHECK (marks >= 0 AND marks <= 100),
                FOREIGN KEY (roll_no) REFERENCES students(roll_no) ON DELETE CASCADE
            )
            """
            
            cursor.execute(students_table)
            cursor.execute(marks_table)
            self.connection.commit()
            print("Tables created successfully!")
            
        except Error as e:
            print(f"Error creating tables: {e}")
        finally:
            cursor.close()
    
    def close_connection(self):
        """
        Close database connection
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

# Global database instance
db_config = DatabaseConfig()
