from typing import Optional

class Appointment:
    def __init__(self, db, appointment_id: int = None, patient_id: int = None, 
                 doctor_id: int = None, appointment_date: str = "", 
                 appointment_time: str = "", reason: str = "", status: str = "Scheduled"):
        self.db = db
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.reason = reason
        self.status = status
    
    def save(self) -> bool:
        if self.appointment_id:
            query = """UPDATE appointments SET patient_id=%s, doctor_id=%s, appointment_date=%s, 
                      appointment_time=%s, reason=%s, status=%s WHERE appointment_id=%s"""
            return self.db.execute_query(query, (self.patient_id, self.doctor_id, 
                                                  self.appointment_date, self.appointment_time,
                                                  self.reason, self.status, self.appointment_id))
        else:
            query = """INSERT INTO appointments (patient_id, doctor_id, appointment_date, 
                      appointment_time, reason, status) VALUES (%s, %s, %s, %s, %s, %s)"""
            return self.db.execute_query(query, (self.patient_id, self.doctor_id,
                                                  self.appointment_date, self.appointment_time,
                                                  self.reason, self.status))
    
    @staticmethod
    def get_all(db) -> list:
        query = "SELECT * FROM appointments"
        return db.fetch_all(query)
    
    @staticmethod
    def get_by_id(db, appointment_id: int) -> Optional['Appointment']:
        query = "SELECT * FROM appointments WHERE appointment_id=%s"
        result = db.fetch_one(query, (appointment_id,))
        if result:
            return Appointment(db, result['appointment_id'], result['patient_id'],
                             result['doctor_id'], result['appointment_date'],
                             result['appointment_time'], result['reason'], result['status'])
        return None
    
    def delete(self) -> bool:
        if self.appointment_id:
            query = "DELETE FROM appointments WHERE appointment_id=%s"
            return self.db.execute_query(query, (self.appointment_id,))
        return False
