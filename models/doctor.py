from typing import Optional

class Doctor:
    def __init__(self, db, dentist_id: int = None, first_name: str = "", last_name: str = "",
                 license_number: str = "", specialization: str = "", years_experience: int = 0):
        self.db = db
        self.dentist_id = dentist_id
        self.first_name = first_name
        self.last_name = last_name
        self.license_number = license_number
        self.specialization = specialization
        self.years_experience = years_experience
    
    def save(self) -> bool:
        if self.dentist_id:
            query = """UPDATE dentists SET first_name=%s, last_name=%s, license_number=%s, 
                      specialization=%s, years_experience=%s WHERE dentist_id=%s"""
            return self.db.execute_query(query, (self.first_name, self.last_name, 
                                                  self.license_number, self.specialization,
                                                  self.years_experience, self.dentist_id))
        else:
            query = """INSERT INTO dentists (first_name, last_name, license_number, 
                      specialization, years_experience) VALUES (%s, %s, %s, %s, %s)"""
            return self.db.execute_query(query, (self.first_name, self.last_name,
                                                  self.license_number, self.specialization,
                                                  self.years_experience))
    
    @staticmethod
    def get_all(db) -> list:
        query = "SELECT * FROM dentists"
        return db.fetch_all(query)
    
    @staticmethod
    def get_by_id(db, dentist_id: int) -> Optional['Doctor']:
        query = "SELECT * FROM dentists WHERE dentist_id=%s"
        result = db.fetch_one(query, (dentist_id,))
        if result:
            return Doctor(db, result['dentist_id'], result['first_name'], result['last_name'],
                         result['license_number'], result['specialization'], result['years_experience'])
        return None
    
    def delete(self) -> bool:
        if self.dentist_id:
            query = "DELETE FROM dentists WHERE dentist_id=%s"
            return self.db.execute_query(query, (self.dentist_id,))
        return False
