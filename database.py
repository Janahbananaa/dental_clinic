import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Optional, Any
import datetime

class DatabaseManager:
    def __init__(self, host: str = "localhost", user: str = "root", password: str = "", database: str = "dental_clinic_db"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection: Optional[mysql.connector.connection.MySQLConnection] = None


    def connect(self) -> bool:
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Database connected successfully")
                return True
        except Error as e:
            print(f"Database connection error: {e}")
            return False

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

    def execute_query(self, query: str, params: tuple = None) -> bool:
        if not self.connection or not self.connection.is_connected():
            print("Database not connected")
            return False
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
            print(f"Query execution error: {e}")
            return False

    def fetch_all(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        if not self.connection or not self.connection.is_connected():
            print("Database not connected")
            return []
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

    def fetch_one(self, query: str, params: tuple = None) -> Optional[Dict[str, Any]]:
        if not self.connection or not self.connection.is_connected():
            print("Database not connected")
            return None
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

    def get_appointments_today(self) -> List[Dict[str, Any]]:
        today = datetime.date.today()
        query = "SELECT id, name, contact, address, age, `type`, datetime FROM dentist_schedule WHERE DATE(datetime) = %s ORDER BY datetime ASC"
        return self.fetch_all(query, (today,))

    def get_all_appointments(self) -> List[Dict[str, Any]]:
        query = "SELECT id, name, contact, address, age, `type`, datetime FROM dentist_schedule ORDER BY datetime ASC"
        return self.fetch_all(query)

    def get_dentist_schedule(self) -> List[Dict[str, Any]]:
        query = "SELECT id, name, contact, address, age, `type`, datetime FROM dentist_schedule"
        return self.fetch_all(query)

    def get_dental_services(self) -> List[Dict[str, Any]]:
        query = "SELECT service_name, for_patient_type, cost FROM dental_services ORDER BY service_name ASC"
        return self.fetch_all(query)

    def get_appointment_count_today(self) -> int:
        today = datetime.date.today()
        query = "SELECT COUNT(*) AS count FROM dentist_schedule WHERE DATE(datetime) = %s"
        result = self.fetch_one(query, (today,))
        return result["count"] if result else 0
