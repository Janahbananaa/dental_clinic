import customtkinter as ctk
from components.ui_components import CustomButton

class PatientRecordsScreen:
    def __init__(self, parent, db, on_back):
        self.parent = parent
        self.db = db
        self.on_back = on_back
        self.frame = ctk.CTkFrame(parent)
        self.show_history = False
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self.frame, fg_color="#1e293b", height=70)
        header.pack(fill="x", padx=0, pady=0)
        
        header_content = ctk.CTkFrame(header, fg_color="#1e293b")
        header_content.pack(fill="both", expand=True, padx=20, pady=10)
        
        back_btn = CustomButton(header_content, text="← Back", command=self.on_back, 
                               width=100, height=35, font=("Arial", 11, "bold"))
        back_btn.pack(side="left", padx=10)
        
        title = ctk.CTkLabel(header_content, text="📋 Patient Records", 
                            font=("Arial", 18, "bold"), text_color="#ffffff")
        title.pack(side="left", padx=20)
        
        history_btn = CustomButton(header_content, text="📚 View History", 
                                  command=self.toggle_history,
                                  width=140, height=35, font=("Arial", 11, "bold"),
                                  fg_color="#6b7280", hover_color="#4b5563")
        history_btn.pack(side="right", padx=10)
        
        # Main content
        main_content = ctk.CTkFrame(self.frame, fg_color="transparent")
        main_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Patient list
        list_container = ctk.CTkFrame(main_content, fg_color="#1e293b", corner_radius=10)
        list_container.pack(fill="both", expand=True)
        
        status = "Deleted Patient Records" if self.show_history else "Active Patients"
        list_title = ctk.CTkLabel(list_container, text=status, 
                                 font=("Arial", 14, "bold"), text_color="#ffffff")
        list_title.pack(pady=(15, 10), padx=15)
        
        # Table with scrollbar
        table_frame = ctk.CTkFrame(list_container, fg_color="#0f172a")
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.patients_table = ctk.CTkTextbox(table_frame, text_color="#e2e8f0", 
                                            fg_color="#0f172a", border_color="#3b82f6", 
                                            border_width=2, font=("Courier", 10))
        self.patients_table.pack(fill="both", expand=True)
        self.patients_table.configure(state="disabled")
        
        self.patients_table.bind("<Button-1>", self.on_table_click)
        
        self.load_patients()
    
    def load_patients(self):
        if self.show_history:
            query = "SELECT * FROM patients WHERE is_deleted=1 ORDER BY patient_id DESC"
        else:
            query = "SELECT * FROM patients WHERE is_deleted=0 ORDER BY patient_id DESC"
        
        patients = self.db.fetch_all(query)
        
        self.patients_table.configure(state="normal")
        self.patients_table.delete("1.0", "end")
        
        if not patients:
            status = "deleted" if self.show_history else "active"
            self.patients_table.insert("end", f"No {status} patients\n")
        else:
            header = f"{'ID':<6} {'First Name':<18} {'Last Name':<18} {'Phone':<15} {'Age':<6}\n"
            separator = "─" * 75 + "\n"
            
            self.patients_table.insert("end", header)
            self.patients_table.insert("end", separator)
            
            for patient in patients:
                first = (patient.get('first_name') or '')[:18]
                last = (patient.get('last_name') or '')[:18]
                phone = (patient.get('phone') or '')[:15]
                age = str(patient.get('age', ''))
                
                row = f"{patient['patient_id']:<6} {first:<18} {last:<18} {phone:<15} {age:<6}\n"
                self.patients_table.insert("end", row)
        
        self.patients_table.configure(state="disabled")
    
    def on_table_click(self, event):
        try:
            index = self.patients_table.index(f"@{event.x},{event.y}")
            line_num = int(index.split(".")[0])
            
            if line_num <= 2:
                return
            
            line_text = self.patients_table.get(f"{line_num}.0", f"{line_num}.end").strip()
            
            if not line_text or line_text.startswith("─"):
                return
            
            try:
                patient_id = int(line_text.split()[0])
                query = "SELECT * FROM patients WHERE patient_id=%s"
                patient = self.db.fetch_one(query, (patient_id,))
                if patient:
                    self.show_patient_details(patient)
            except (ValueError, IndexError):
                pass
        except Exception as e:
            print(f"Error: {e}")
    
    def show_patient_details(self, patient):
        # Create popup window
        popup = ctk.CTkToplevel(self.parent)
        popup.title(f"Patient: {patient['first_name']} {patient['last_name']}")
        popup.geometry("900x700")
        popup.resizable(True, True)
        
        # Patient info section
        info_frame = ctk.CTkFrame(popup, fg_color="#1e293b", corner_radius=10)
        info_frame.pack(fill="x", padx=20, pady=20)
        
        patient_name = f"{patient['first_name']} {patient['last_name']}"
        ctk.CTkLabel(info_frame, text=f"Patient: {patient_name}", 
                    font=("Arial", 14, "bold"), text_color="#ffffff").pack(anchor="w", padx=15, pady=10)
        
        info_text = f"Phone: {patient.get('phone', 'N/A')} | Age: {patient.get('age', 'N/A')} | Gender: {patient.get('gender', 'N/A')}"
        ctk.CTkLabel(info_frame, text=info_text, 
                    font=("Arial", 10), text_color="#cbd5e1").pack(anchor="w", padx=15, pady=5)
        
        address = patient.get('address', 'N/A')
        ctk.CTkLabel(info_frame, text=f"Address: {address}", 
                    font=("Arial", 10), text_color="#cbd5e1").pack(anchor="w", padx=15, pady=5)
        
        # Action buttons
        btn_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        btn_frame.pack(anchor="w", padx=15, pady=10)
        
        if not self.show_history:
            edit_btn = CustomButton(btn_frame, text="Edit", 
                                   command=lambda: self.edit_patient(patient, popup),
                                   width=80, height=32, font=("Arial", 9, "bold"),
                                   fg_color="#3b82f6", hover_color="#1d4ed8")
            edit_btn.pack(side="left", padx=5)
            
            delete_btn = CustomButton(btn_frame, text="Delete", 
                                     command=lambda: self.soft_delete_patient(patient['patient_id'], popup),
                                     width=80, height=32, font=("Arial", 9, "bold"),
                                     fg_color="#ef4444", hover_color="#dc2626")
            delete_btn.pack(side="left", padx=5)
        
        # Appointment history section
        history_frame = ctk.CTkFrame(popup, fg_color="#1e293b", corner_radius=10)
        history_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(history_frame, text="Visit History", 
                    font=("Arial", 12, "bold"), text_color="#ffffff").pack(anchor="w", padx=15, pady=10)
        
        table_frame = ctk.CTkFrame(history_frame, fg_color="#0f172a")
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        history_table = ctk.CTkTextbox(table_frame, text_color="#e2e8f0", 
                                      fg_color="#0f172a", border_color="#3b82f6", 
                                      border_width=2, font=("Courier", 9))
        history_table.pack(fill="both", expand=True)
        history_table.configure(state="disabled")
        
        # Load appointment history
        query = """SELECT a.appointment_id, a.`Date/Time`, a.Dental_service, a.Service_fee, a.Status
                  FROM appointments a
                  WHERE a.Name=%s AND a.Status IN ('Done', 'Ongoing')
                  ORDER BY a.`Date/Time` DESC"""
        
        appointments = self.db.fetch_all(query, (patient_name,))
        
        history_table.configure(state="normal")
        
        if not appointments:
            history_table.insert("end", "No visit history\n")
        else:
            header = f"{'Appt ID':<8} {'Date/Time':<20} {'Service':<30} {'Fee':<10} {'Status':<10}\n"
            separator = "─" * 85 + "\n"
            
            history_table.insert("end", header)
            history_table.insert("end", separator)
            
            for apt in appointments:
                apt_id = str(apt.get('appointment_id', ''))
                date_time = str(apt.get('Date/Time', ''))[:20]
                service = (apt.get('Dental_service', ''))[:30]
                fee = f"${apt.get('Service_fee', 0):.2f}"
                status = apt.get('Status', '')
                
                row = f"{apt_id:<8} {date_time:<20} {service:<30} {fee:<10} {status:<10}\n"
                history_table.insert("end", row)
        
        history_table.configure(state="disabled")
    
    def edit_patient(self, patient, parent_window):
        parent_window.destroy()
        # Create edit window - implement based on your patient edit screen
        print(f"Edit patient {patient['patient_id']}")
    
    def soft_delete_patient(self, patient_id, parent_window):
        update_query = "UPDATE patients SET is_deleted=1 WHERE patient_id=%s"
        
        if self.db.execute(update_query, (patient_id,)):
            print(f"Patient {patient_id} moved to history")
            parent_window.destroy()
            self.load_patients()
        else:
            print(f"Failed to delete patient {patient_id}")
    
    def toggle_history(self):
        self.show_history = not self.show_history
        self.load_patients()
    
    def get_frame(self):
        return self.frame
    
    def show(self):
        self.load_patients()
        self.frame.pack(fill="both", expand=True)
        self.frame.tkraise()
    
    def hide(self):
        self.frame.pack_forget()