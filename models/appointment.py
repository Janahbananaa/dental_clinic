from typing import Optional
from datetime import datetime

class Appointment:
    def __init__(self, db, appointment_id: int = None, name: str = "", contact: str = "",
                 age: int = 0, gender: str = "", type_: str = "", date_time: str = "",
                 dental_service: str = "", service_fee: float = 0.0, status: str = "Scheduled"):
        self.db = db
        self.appointment_id = appointment_id
        self.name = name
        self.contact = contact
        self.age = age
        self.gender = gender
        self.type = type_
        self.date_time = date_time
        self.dental_service = dental_service
        self.service_fee = service_fee
        self.status = status
    
    def save(self) -> bool:
        # Check for schedule conflicts
        if self.check_schedule_conflict():
            return False
        
        if self.appointment_id:
            query = """UPDATE appointments SET Name=%s, Contact=%s, Age=%s, Gender=%s, 
                      Type=%s, `Date/Time`=%s, Dental_service=%s, Service_fee=%s, Status=%s 
                      WHERE appointment_id=%s"""
            return self.db.execute_query(query, (self.name, self.contact, self.age, self.gender,
                                                  self.type, self.date_time, self.dental_service,
                                                  self.service_fee, self.status, self.appointment_id))
        else:
            query = """INSERT INTO appointments (Name, Contact, Age, Gender, Type, `Date/Time`, 
                      Dental_service, Service_fee, Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            return self.db.execute_query(query, (self.name, self.contact, self.age, self.gender,
                                                  self.type, self.date_time, self.dental_service,
                                                  self.service_fee, self.status))
    
    def check_schedule_conflict(self) -> bool:
        """Check if same date/time already exists for appointment"""
        if not self.date_time:
            return False
        
        query = """SELECT COUNT(*) as count FROM appointments 
                  WHERE `Date/Time`=%s AND Status != 'Done' AND (appointment_id IS NULL OR appointment_id != %s)"""
        
        result = self.db.fetch_one(query, (self.date_time, self.appointment_id or 0))
        return result and result['count'] > 0 if result else False
    
    @staticmethod
    def get_all(db) -> list:
        query = "SELECT * FROM appointments WHERE Status != 'Done' ORDER BY `Date/Time` DESC"
        return db.fetch_all(query)
    
    @staticmethod
    def get_today(db) -> list:
        query = """SELECT * FROM appointments 
                  WHERE DATE(`Date/Time`) = CURDATE() AND Status != 'Done'
                  ORDER BY `Date/Time`"""
        return db.fetch_all(query)
    
    @staticmethod
    def get_by_id(db, appointment_id: int) -> Optional['Appointment']:
        query = "SELECT * FROM appointments WHERE appointment_id=%s"
        result = db.fetch_one(query, (appointment_id,))
        if result:
            return Appointment(db, result['appointment_id'], result.get('Name', ''),
                             result.get('Contact', ''), result.get('Age', 0),
                             result.get('Gender', ''), result.get('Type', ''),
                             result.get('Date/Time', ''), result.get('Dental_service', ''),
                             result.get('Service_fee', 0.0), result.get('Status', 'Scheduled'))
        return None
    
    def mark_done(self) -> bool:
        if self.appointment_id:
            self.status = "Done"
            query = "UPDATE appointments SET Status=%s WHERE appointment_id=%s"
            return self.db.execute_query(query, (self.status, self.appointment_id))
        return False
    
    def delete(self) -> bool:
        if self.appointment_id:
            query = "DELETE FROM appointments WHERE appointment_id=%s"
            return self.db.execute_query(query, (self.appointment_id,))
        return False
