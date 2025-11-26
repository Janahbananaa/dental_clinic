import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any

class DatabaseManager:
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None
    
    def connect(self):
        """Connect to the database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            return True
        except Error as e:
            print(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the database"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute(self, query: str, params: tuple = None):
        """Execute INSERT, UPDATE, DELETE queries"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Execute error: {e}")
            self.connection.rollback()
            return False
    
    def fetch_one(self, query: str, params: tuple = None):
        """Fetch a single row"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print(f"Fetch error: {e}")
            return None
    
    def fetch_all(self, query: str, params: tuple = None):
        """Fetch all rows"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"Fetch error: {e}")
            return []
