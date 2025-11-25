# screens/doctors.py
import customtkinter as ctk

class DoctorsScreen(ctk.CTkFrame):
    def __init__(self, parent, db, go_to_home_callback):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.go_to_home = go_to_home_callback

        # Table placeholder
        self.table = None

        self.setup_ui()

    def setup_ui(self):
        # Title label
        title = ctk.CTkLabel(self, text="Doctors", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=10)

        # Table: Using CTk Table or a simple frame for rows
        self.table = ctk.CTkScrollableFrame(self)
        self.table.pack(fill="both", expand=True, padx=20, pady=10)

        # Load doctors from DB
        self.load_doctors_table()

        # Back button
        back_btn = ctk.CTkButton(self, text="Back", command=self.go_to_home)
        back_btn.pack(pady=10)

    def load_doctors_table(self):
        # Fetch doctors from DB
        doctors = self.db.fetch_all("SELECT * FROM doctors")

        # Clear current table rows
        for widget in self.table.winfo_children():
            widget.destroy()

        # Create table header
        headers = ["ID", "Name", "License", "Specialization", "Experience"]
        header_frame = ctk.CTkFrame(self.table)
        header_frame.pack(fill="x", pady=2)
        for h in headers:
            lbl = ctk.CTkLabel(header_frame, text=h, width=120, anchor="w", font=("Arial", 12, "bold"))
            lbl.pack(side="left", padx=5)

        # Populate table rows
        for doctor in doctors:
            row_frame = ctk.CTkFrame(self.table)
            row_frame.pack(fill="x", pady=1)

            doctor_id = doctor['dentist_id']
            full_name = f"{doctor['first_name']} {doctor['last_name']}"
            license_number = doctor['license_number'] or ""
            specialization = doctor['specialization'] or ""
            experience = str(doctor['years_experience']) if doctor['years_experience'] is not None else ""

            row_data = [doctor_id, full_name, license_number, specialization, experience]
            for cell in row_data:
                lbl = ctk.CTkLabel(row_frame, text=cell, width=120, anchor="w")
                lbl.pack(side="left", padx=5)

    # Show/hide helpers
    def show(self):
        self.pack(fill="both", expand=True)

    def hide(self):
        self.pack_forget()
