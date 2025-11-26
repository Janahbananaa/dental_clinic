from typing import Optional

class PatientHistory:
    def __init__(self, db, history_id: int = None, patient_id: int = None,
                 appointment_id: int = None, billing_id: int = None,
                 status: str = "Active"):
        self.db = db
        self.history_id = history_id
        self.patient_id = patient_id
        self.appointment_id = appointment_id
        self.billing_id = billing_id
        self.status = status
    
    def save(self) -> bool:
        if self.history_id:
            query = """UPDATE patient_history SET patient_id=%s, appointment_id=%s, 
                      billing_id=%s, status=%s WHERE history_id=%s"""
            return self.db.execute_query(query, (self.patient_id, self.appointment_id,
                                                  self.billing_id, self.status, self.history_id))
        else:
            query = """INSERT INTO patient_history (patient_id, appointment_id, billing_id, status) 
                      VALUES (%s, %s, %s, %s)"""
            return self.db.execute_query(query, (self.patient_id, self.appointment_id,
                                                  self.billing_id, self.status))
    
    @staticmethod
    def get_by_patient(db, patient_id: int) -> list:
        query = """SELECT ph.*, p.first_name, p.last_name, a.appointment_date, 
                  a.appointment_time, b.total_fee FROM patient_history ph
                  LEFT JOIN patients p ON ph.patient_id = p.patient_id
                  LEFT JOIN appointments a ON ph.appointment_id = a.appointment_id
                  LEFT JOIN billing b ON ph.billing_id = b.billing_id
                  WHERE ph.patient_id=%s ORDER BY ph.history_id DESC"""
        return db.fetch_all(query, (patient_id,))
    
    @staticmethod
    def get_all(db) -> list:
        query = """SELECT ph.*, p.first_name, p.last_name, a.appointment_date, 
                  a.appointment_time, b.total_fee FROM patient_history ph
                  LEFT JOIN patients p ON ph.patient_id = p.patient_id
                  LEFT JOIN appointments a ON ph.appointment_id = a.appointment_id
                  LEFT JOIN billing b ON ph.billing_id = b.billing_id
                  ORDER BY ph.history_id DESC"""
        return db.fetch_all(query)
    
    def delete(self) -> bool:
        if self.history_id:
            query = "DELETE FROM patient_history WHERE history_id=%s"
            return self.db.execute_query(query, (self.history_id,))
        return False
