from typing import Optional

class Doctor:
    def __init__(self, db, doctor_id: int = None, name: str = "", specialization: str = "", 
                 phone: str = "", email: str = ""):
        self.db = db
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization
        self.phone = phone
        self.email = email
    
    def save(self) -> bool:
        if self.doctor_id:
            query = """UPDATE doctors SET name=%s, specialization=%s, phone=%s, email=%s 
                      WHERE doctor_id=%s"""
            return self.db.execute_query(query, (self.name, self.specialization, 
                                                  self.phone, self.email, self.doctor_id))
        else:
            query = """INSERT INTO doctors (name, specialization, phone, email) 
                      VALUES (%s, %s, %s, %s)"""
            return self.db.execute_query(query, (self.name, self.specialization, 
                                                  self.phone, self.email))
    
    @staticmethod
    def get_all(db) -> list:
        query = "SELECT * FROM doctors"
        return db.fetch_all(query)
    
    @staticmethod
    def get_by_id(db, doctor_id: int) -> Optional['Doctor']:
        query = "SELECT * FROM doctors WHERE doctor_id=%s"
        result = db.fetch_one(query, (doctor_id,))
        if result:
            return Doctor(db, result['doctor_id'], result['name'], result['specialization'],
                         result['phone'], result['email'])
        return None
    
    def delete(self) -> bool:
        if self.doctor_id:
            query = "DELETE FROM doctors WHERE doctor_id=%s"
            return self.db.execute_query(query, (self.doctor_id,))
        return False
