import customtkinter as ctk

class PatientsScreen(ctk.CTkFrame):
    def __init__(self, parent, db, go_to_home_callback):
        super().__init__(parent)
        self.parent = parent
        self.db = db
        self.go_to_home = go_to_home_callback
        self.table_frame = None
        self.setup_ui()

    def setup_ui(self):
        title = ctk.CTkLabel(self, text="Patients", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=10)

        self.table_frame = ctk.CTkScrollableFrame(self)
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.load_patients_table()

        back_btn = ctk.CTkButton(self, text="Back", command=self.go_to_home)
        back_btn.pack(pady=10)

    def load_patients_table(self):
        patients = self.db.fetch_all("SELECT * FROM patients")

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        headers = ["ID", "Name", "Age", "Contact", "Address"]
        header_frame = ctk.CTkFrame(self.table_frame)
        header_frame.pack(fill="x", pady=2)
        for h in headers:
            lbl = ctk.CTkLabel(header_frame, text=h, width=120, anchor="w", font=("Arial", 12, "bold"))
            lbl.pack(side="left", padx=5)

        for patient in patients:
            row_frame = ctk.CTkFrame(self.table_frame)
            row_frame.pack(fill="x", pady=1)

            full_name = f"{patient['first_name']} {patient['last_name']}"
            row_data = [
                patient['patient_id'],
                full_name,
                patient.get('age', ''),
                patient.get('contact', ''),
                patient.get('address', '')
            ]

            for cell in row_data:
                lbl = ctk.CTkLabel(row_frame, text=cell, width=120, anchor="w")
                lbl.pack(side="left", padx=5)

    def show(self):
        self.pack(fill="both", expand=True)

    def hide(self):
        self.pack_forget()



