# This file is deprecated and should be deleted
# Use models/ folder instead with:
# - models/patient.py
# - models/doctor.py
# - models/appointment.py

import customtkinter as ctk
from components.ui_components import FormFrame, DataTable, CustomButton
from models import Doctor   # ← THIS IS CORRECT

class Doctor:
    def __init__(self, db, first_name=None, last_name=None, specialization=None,
                 license_number=None, years_experience=None):
        self.db = db
        self.first_name = first_name
        self.last_name = last_name
        self.specialization = specialization
        self.license_number = license_number
        self.years_experience = years_experience

    # ---------------------------
    # SAVE NEW DOCTOR
    # ---------------------------
    def save(self):
        try:
            cursor = self.db.cursor()

            query = """
                INSERT INTO dentists (first_name, last_name, specialization, 
                                      license_number, years_experience)
                VALUES (%s, %s, %s, %s, %s)
            """

            values = (
                self.first_name,
                self.last_name,
                self.specialization,
                self.license_number,
                self.years_experience
            )

            cursor.execute(query, values)
            self.db.commit()
            cursor.close()
            return True

        except Exception as e:
            print("Error saving doctor:", e)
            return False

    # ---------------------------
    # GET ALL DOCTORS
    # ---------------------------
    @staticmethod
    def get_all(db):
        try:
            cursor = db.cursor(dictionary=True)

            query = """
                SELECT 
                    dentist_id,
                    first_name,
                    last_name,
                    specialization,
                    license_number,
                    years_experience
                FROM dentists
                ORDER BY dentist_id DESC
            """

            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result

        except Exception as e:
            print("Error loading doctors:", e)
            return []
