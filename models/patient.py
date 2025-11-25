from typing import Optional

class Patient:
    def __init__(self, db, patient_id: int = None, first_name: str = "", last_name: str = "",
                 gender: str = "", birth_date: str = "", phone: str = "", address: str = "",
                 age: int = 0, patient_type: str = ""):
        self.db = db
        self.patient_id = patient_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.birth_date = birth_date
        self.phone = phone
        self.address = address
        self.age = age
        self.patient_type = patient_type
    
    def save(self) -> bool:
        if self.patient_id:
            query = """UPDATE patients SET first_name=%s, last_name=%s, gender=%s, birth_date=%s, 
                      phone=%s, address=%s, age=%s, patient_type=%s WHERE patient_id=%s"""
            return self.db.execute_query(query, (self.first_name, self.last_name, self.gender,
                                                  self.birth_date, self.phone, self.address,
                                                  self.age, self.patient_type, self.patient_id))
        else:
            query = """INSERT INTO patients (first_name, last_name, gender, birth_date, phone, 
                      address, age, patient_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            return self.db.execute_query(query, (self.first_name, self.last_name, self.gender,
                                                  self.birth_date, self.phone, self.address,
                                                  self.age, self.patient_type))
    
    @staticmethod
    def get_all(db) -> list:
        query = "SELECT * FROM patients"
        return db.fetch_all(query)
    
    @staticmethod
    def get_by_id(db, patient_id: int) -> Optional['Patient']:
        query = "SELECT * FROM patients WHERE patient_id=%s"
        result = db.fetch_one(query, (patient_id,))
        if result:
            return Patient(db, result['patient_id'], result['first_name'], result['last_name'],
                          result['gender'], result['birth_date'], result['phone'],
                          result['address'], result['age'], result['patient_type'])
        return None
    
    def delete(self) -> bool:
        if self.patient_id:
            query = "DELETE FROM patients WHERE patient_id=%s"
            return self.db.execute_query(query, (self.patient_id,))
        return False
