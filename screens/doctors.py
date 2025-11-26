import customtkinter as ctk

class DoctorsScreen(ctk.CTkFrame):
    def __init__(self, parent, db, go_to_home_callback):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.go_to_home = go_to_home_callback

        self.table = None
        self.setup_ui()

    def setup_ui(self):
        title = ctk.CTkLabel(self, text="Doctors", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=10)

        self.table = ctk.CTkScrollableFrame(self)
        self.table.pack(fill="both", expand=True, padx=20, pady=10)

        self.load_doctors_table()

        back_btn = ctk.CTkButton(self, text="Back", command=self.go_to_home)
        back_btn.pack(pady=10)

    def load_doctors_table(self):
        doctors = self.db.fetch_all("SELECT * FROM doctors")

        for widget in self.table.winfo_children():
            widget.destroy()

        headers = ["ID", "Name", "License", "Specialization", "Experience"]
        header_frame = ctk.CTkFrame(self.table)
        header_frame.pack(fill="x", pady=2)
        for h in headers:
            lbl = ctk.CTkLabel(header_frame, text=h, width=120, anchor="w", font=("Arial", 12, "bold"))
            lbl.pack(side="left", padx=5)

        for doctor in doctors:
            row_frame = ctk.CTkFrame(self.table)
            row_frame.pack(fill="x", pady=1)

            doctor_id = doctor['dentist_id']
            full_name = f"{doctor['first_name']} {doctor['last_name']}"
            license_number = doctor.get('license_number', "")
            specialization = doctor.get('specialization', "")
            experience = str(doctor.get('years_experience', ""))

            row_data = [doctor_id, full_name, license_number, specialization, experience]
            for cell in row_data:
                lbl = ctk.CTkLabel(row_frame, text=cell, width=120, anchor="w")
                lbl.pack(side="left", padx=5)

    def show(self):
        self.pack(fill="both", expand=True)

    def hide(self):
        self.pack_forget()


