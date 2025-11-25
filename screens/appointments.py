import customtkinter as ctk
from components.ui_components import FormFrame, DataTable, CustomButton
from models import Appointment

class AppointmentsScreen:
    def __init__(self, parent, db, on_back):
        self.parent = parent
        self.db = db
        self.on_back = on_back
        self.frame = ctk.CTkFrame(parent)
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self.frame, fg_color="#1a1a1a", height=60)
        header.pack(fill="x", padx=0, pady=0)
        
        back_btn = CustomButton(header, text="← Back", command=self.on_back, width=100)
        back_btn.pack(side="left", padx=20, pady=10)
        
        title = ctk.CTkLabel(header, text="Appointments Management", 
                            font=("Arial", 18, "bold"))
        title.pack(side="left", padx=20, pady=10)
        
        content = ctk.CTkFrame(self.frame)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        form = FormFrame(content, title="Schedule Appointment")
        form.pack(fill="x", padx=10, pady=10)
        
        form.add_field("Patient ID", width=300)
        form.add_field("Doctor ID", width=300)
        form.add_field("Date (YYYY-MM-DD)", width=300)
        form.add_field("Time (HH:MM)", width=300)
        form.add_field("Reason", width=300)
        
        def save_appointment():
            values = form.get_values()
            try:
                appointment = Appointment(self.db, patient_id=int(values['Patient ID']),
                                         doctor_id=int(values['Doctor ID']),
                                         appointment_date=values['Date (YYYY-MM-DD)'],
                                         appointment_time=values['Time (HH:MM)'],
                                         reason=values['Reason'])
                if appointment.save():
                    self.show_message("Appointment scheduled successfully", "success")
                    form.clear_fields()
                    self.load_appointments_table()
                else:
                    self.show_message("Failed to schedule appointment", "error")
            except ValueError:
                self.show_message("Invalid patient or doctor ID", "error")
        
        CustomButton(content, text="Schedule Appointment", 
                    command=save_appointment).pack(pady=10)
        
        table_frame = ctk.CTkFrame(content)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.table = DataTable(table_frame, ["ID", "Patient", "Doctor", "Date", "Time", "Status"])
        self.table.pack(fill="both", expand=True)
        
        self.load_appointments_table()
    
    def load_appointments_table(self):
        self.table.clear_rows()
        appointments = Appointment.get_all(self.db)
        for apt in appointments:
            self.table.insert_row((apt['appointment_id'], apt['patient_id'],
                                 apt['doctor_id'], apt['appointment_date'],
                                 apt['appointment_time'], apt['status']))
    
    def show_message(self, message: str, msg_type: str):
        color = "green" if msg_type == "success" else "red"
        msg_label = ctk.CTkLabel(self.frame, text=message, text_color=color)
        msg_label.pack()
        self.parent.after(3000, msg_label.destroy)
    
    def get_frame(self):
        return self.frame
    
    def show(self):
        self.frame.pack(fill="both", expand=True)
    
    def hide(self):
        self.frame.pack_forget()