import customtkinter as ctk
from components.ui_components import CustomButton

class PatientRecordsScreen:
    def __init__(self, parent, db, on_back):
        self.parent = parent
        self.db = db
        self.on_back = on_back
        self.frame = ctk.CTkFrame(parent)
        self.show_history = False
        self.current_patient = None
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
        
        if self.show_history:
            self.setup_history_view(main_content)
        else:
            self.setup_active_view(main_content)
    
    def setup_active_view(self, main_content):
        """Setup view for active patients"""
        # Container for both tables
        tables_container = ctk.CTkFrame(main_content, fg_color="transparent")
        tables_container.pack(fill="both", expand=True)
        
        # LEFT TABLE - Active Patients (Need Follow-up)
        active_frame = ctk.CTkFrame(tables_container, fg_color="#1e293b", corner_radius=10)
        active_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        active_title = ctk.CTkLabel(active_frame, text="Active Patients (Follow-up Needed)", 
                                    font=("Arial", 12, "bold"), text_color="#ffffff")
        active_title.pack(pady=(15, 10), padx=15)
        
        active_table_frame = ctk.CTkFrame(active_frame, fg_color="#0f172a")
        active_table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.active_table = ctk.CTkTextbox(active_table_frame, text_color="#e2e8f0", 
                                           fg_color="#0f172a", border_color="#3b82f6", 
                                           border_width=2, font=("Courier", 9))
        self.active_table.pack(fill="both", expand=True)
        self.active_table.configure(state="disabled")
        self.active_table.bind("<Button-1>", lambda e: self.on_table_click(e, "active"))
        
        # RIGHT TABLE - One-Time Patients (No Follow-up)
        onetime_frame = ctk.CTkFrame(tables_container, fg_color="#1e293b", corner_radius=10)
        onetime_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        onetime_title = ctk.CTkLabel(onetime_frame, text="One-Time Patients (No Follow-up)", 
                                     font=("Arial", 12, "bold"), text_color="#ffffff")
        onetime_title.pack(pady=(15, 10), padx=15)
        
        onetime_table_frame = ctk.CTkFrame(onetime_frame, fg_color="#0f172a")
        onetime_table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.onetime_table = ctk.CTkTextbox(onetime_table_frame, text_color="#e2e8f0", 
                                            fg_color="#0f172a", border_color="#3b82f6", 
                                            border_width=2, font=("Courier", 9))
        self.onetime_table.pack(fill="both", expand=True)
        self.onetime_table.configure(state="disabled")
        self.onetime_table.bind("<Button-1>", lambda e: self.on_table_click(e, "onetime"))
        
        # Load patients into both tables
        self.load_active_patients()
    
    def setup_history_view(self, main_content):
        """Setup view for deleted patients"""
        list_container = ctk.CTkFrame(main_content, fg_color="#1e293b", corner_radius=10)
        list_container.pack(fill="both", expand=True)
        
        list_title = ctk.CTkLabel(list_container, text="Deleted Patient Records (Restorable)", 
                                  font=("Arial", 14, "bold"), text_color="#ffffff")
        list_title.pack(pady=(15, 10), padx=15)
        
        table_frame = ctk.CTkFrame(list_container, fg_color="#0f172a")
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.history_table = ctk.CTkTextbox(table_frame, text_color="#e2e8f0", 
                                            fg_color="#0f172a", border_color="#3b82f6", 
                                            border_width=2, font=("Courier", 10))
        self.history_table.pack(fill="both", expand=True)
        self.history_table.configure(state="disabled")
        self.history_table.bind("<Button-1>", self.on_history_click)
        
        # Action buttons for history
        btn_frame = ctk.CTkFrame(list_container, fg_color="#1e293b")
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.restore_btn = CustomButton(btn_frame, text="🔄 Restore", 
                                       command=self.restore_patient,
                                       width=100, height=35, font=("Arial", 10, "bold"),
                                       fg_color="#10b981", hover_color="#059669", state="disabled")
        self.restore_btn.pack(side="left", padx=5)
        
        self.clear_btn = CustomButton(btn_frame, text="Clear", 
                                     command=self.clear_selection,
                                     width=100, height=35, font=("Arial", 10, "bold"),
                                     fg_color="#6b7280", hover_color="#4b5563")
        self.clear_btn.pack(side="left", padx=5)
        
        self.status_label = ctk.CTkLabel(list_container, text="", font=("Arial", 9, "bold"))
        self.status_label.pack(pady=(0, 10))
        
        self.load_deleted_patients()
    
    def load_active_patients(self):
        """Load active patients into two separate tables"""
        query = """SELECT p.*, 
                  COUNT(a.appointment_id) as total_visits,
                  MAX(a.`Date/Time`) as last_visit
                  FROM patients p
                  LEFT JOIN appointments a ON p.first_name = a.Name
                  WHERE p.is_deleted=0
                  GROUP BY p.patient_id
                  ORDER BY p.patient_id DESC"""
        
        patients = self.db.fetch_all(query)
        
        active_patients = []
        onetime_patients = []
        
        for patient in patients:
            total_visits = patient.get('total_visits', 0)
            if total_visits > 1:
                active_patients.append(patient)
            else:
                onetime_patients.append(patient)
        
        # Load active patients table
        self.active_table.configure(state="normal")
        self.active_table.delete("1.0", "end")
        
        if not active_patients:
            self.active_table.insert("end", "No active patients\n")
        else:
            header = f"{'ID':<6} {'First Name':<15} {'Last Name':<15} {'Phone':<12} {'Status':<12}\n"
            separator = "─" * 70 + "\n"
            
            self.active_table.insert("end", header)
            self.active_table.insert("end", separator)
            
            for patient in active_patients:
                row = f"{patient['patient_id']:<6} {(patient.get('first_name') or '')[:15]:<15} {(patient.get('last_name') or '')[:15]:<15} {(patient.get('phone') or '')[:12]:<12} {'Active':<12}\n"
                self.active_table.insert("end", row)
        
        self.active_table.configure(state="disabled")
        
        # Load one-time patients table
        self.onetime_table.configure(state="normal")
        self.onetime_table.delete("1.0", "end")
        
        if not onetime_patients:
            self.onetime_table.insert("end", "No one-time patients\n")
        else:
            header = f"{'ID':<6} {'First Name':<15} {'Last Name':<15} {'Phone':<12} {'Status':<12}\n"
            separator = "─" * 70 + "\n"
            
            self.onetime_table.insert("end", header)
            self.onetime_table.insert("end", separator)
            
            for patient in onetime_patients:
                row = f"{patient['patient_id']:<6} {(patient.get('first_name') or '')[:15]:<15} {(patient.get('last_name') or '')[:15]:<15} {(patient.get('phone') or '')[:12]:<12} {'One-Time':<12}\n"
                self.onetime_table.insert("end", row)
        
        self.onetime_table.configure(state="disabled")
    
    def load_deleted_patients(self):
        """Load deleted patients"""
        query = "SELECT * FROM patients WHERE is_deleted=1 ORDER BY patient_id DESC"
        patients = self.db.fetch_all(query)
        
        self.history_table.configure(state="normal")
        self.history_table.delete("1.0", "end")
        
        if not patients:
            self.history_table.insert("end", "No deleted patients\n")
        else:
            header = f"{'ID':<6} {'First Name':<15} {'Last Name':<15} {'Address':<20} {'Phone':<12}\n"
            separator = "─" * 85 + "\n"
            
            self.history_table.insert("end", header)
            self.history_table.insert("end", separator)
            
            for patient in patients:
                first = (patient.get('first_name') or '')[:15]
                last = (patient.get('last_name') or '')[:15]
                address = (patient.get('address') or '')[:20]
                phone = (patient.get('phone') or '')[:12]
                
                row = f"{patient['patient_id']:<6} {first:<15} {last:<15} {address:<20} {phone:<12}\n"
                self.history_table.insert("end", row)
        
        self.history_table.configure(state="disabled")
    
    def on_table_click(self, event, table_type):
        """Handle table click for active patients"""
        try:
            table = self.active_table if table_type == "active" else self.onetime_table
            index = table.index(f"@{event.x},{event.y}")
            line_num = int(index.split(".")[0])
            
            if line_num <= 2:
                return
            
            line_text = table.get(f"{line_num}.0", f"{line_num}.end").strip()
            
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
    
    def on_history_click(self, event):
        """Handle history table click"""
        try:
            index = self.history_table.index(f"@{event.x},{event.y}")
            line_num = int(index.split(".")[0])
            
            if line_num <= 2:
                return
            
            line_text = self.history_table.get(f"{line_num}.0", f"{line_num}.end").strip()
            
            if not line_text or line_text.startswith("─"):
                return
            
            try:
                patient_id = int(line_text.split()[0])
                query = "SELECT * FROM patients WHERE patient_id=%s"
                patient = self.db.fetch_one(query, (patient_id,))
                if patient:
                    self.current_patient = patient
                    self.restore_btn.configure(state="normal")
                    self.status_label.configure(text=f"✏️ Selected: {patient['first_name']} {patient['last_name']}", 
                                               text_color="#3b82f6")
            except (ValueError, IndexError):
                pass
        except Exception as e:
            print(f"Error: {e}")
    
    def show_patient_details(self, patient):
        """Show patient details popup"""
        popup = ctk.CTkToplevel(self.parent)
        popup.title(f"Patient: {patient['first_name']} {patient['last_name']}")
        popup.geometry("1200x750")
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
        
        edit_btn = CustomButton(btn_frame, text="✏️ Edit", 
                               command=lambda: self.show_edit_dialog(patient, popup),
                               width=90, height=32, font=("Arial", 9, "bold"),
                               fg_color="#3b82f6", hover_color="#1d4ed8")
        edit_btn.pack(side="left", padx=5)
        
        delete_btn = CustomButton(btn_frame, text="🗑️ Delete", 
                                 command=lambda: self.soft_delete_patient(patient['patient_id'], popup),
                                 width=90, height=32, font=("Arial", 9, "bold"),
                                 fg_color="#ef4444", hover_color="#dc2626")
        delete_btn.pack(side="left", padx=5)
        
        # Visit history section
        history_frame = ctk.CTkFrame(popup, fg_color="#1e293b", corner_radius=10)
        history_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(history_frame, text="Visit History", 
                    font=("Arial", 12, "bold"), text_color="#ffffff").pack(anchor="w", padx=15, pady=10)
        
        table_frame = ctk.CTkFrame(history_frame, fg_color="#0f172a")
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        history_table = ctk.CTkTextbox(table_frame, text_color="#e2e8f0", 
                                      fg_color="#0f172a", border_color="#3b82f6", 
                                      border_width=2, font=("Courier", 8))
        history_table.pack(fill="both", expand=True)
        history_table.configure(state="disabled")
        
        query = """SELECT a.appointment_id, a.Name, a.Contact, a.Age, a.Gender, a.Type, a.Address, a.`Date/Time`, a.Dental_service, a.Service_fee, a.Status
                  FROM appointments a
                  WHERE a.Name=%s AND a.Status IN ('Done', 'Ongoing')
                  ORDER BY a.`Date/Time` DESC"""
        
        appointments = self.db.fetch_all(query, (patient_name,))
        
        history_table.configure(state="normal")
        
        if not appointments:
            history_table.insert("end", "No visit history\n")
        else:
            header = f"{'ID':<4} {'Name':<10} {'Contact':<11} {'Age':<4} {'Gender':<7} {'Type':<7} {'Address':<11} {'Service':<11} {'Fee':<8} {'Status':<10}\n"
            separator = "─" * 120 + "\n"
            
            history_table.insert("end", header)
            history_table.insert("end", separator)
            
            for apt in appointments:
                apt_id = str(apt.get('appointment_id', ''))
                name = (apt.get('Name', ''))[:10]
                contact = (apt.get('Contact', '') or 'N/A')[:11]
                age = str(apt.get('Age', ''))[:4]
                gender = (apt.get('Gender', '') or 'N/A')[:7]
                type_ = (apt.get('Type', '') or 'N/A')[:7]
                address = (apt.get('Address', '') or 'N/A')[:11]
                service = (apt.get('Dental_service', '') or 'N/A')[:11]
                fee = f"${apt.get('Service_fee', 0):.2f}"[:8]
                status = apt.get('Status', 'Done')
                
                row = f"{apt_id:<4} {name:<10} {contact:<11} {age:<4} {gender:<7} {type_:<7} {address:<11} {service:<11} {fee:<8} {status:<10}\n"
                history_table.insert("end", row)
        
        history_table.configure(state="disabled")
    
    def show_edit_dialog(self, patient, parent_popup):
        """Show edit dialog for patient"""
        edit_window = ctk.CTkToplevel(self.parent)
        edit_window.title(f"Edit Patient: {patient['first_name']} {patient['last_name']}")
        edit_window.geometry("500x500")
        
        form_frame = ctk.CTkFrame(edit_window, fg_color="#1e293b")
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        fields = {}
        
        field_configs = [
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Phone", "phone"),
            ("Address", "address"),
            ("Age", "age"),
        ]
        
        for label_text, field_key in field_configs:
            label = ctk.CTkLabel(form_frame, text=label_text, font=("Arial", 10, "bold"), 
                                text_color="#cbd5e1")
            label.pack(anchor="w", pady=(10, 2))
            
            entry = ctk.CTkEntry(form_frame, width=400, height=30, font=("Arial", 10),
                                fg_color="#0f172a", border_color="#3b82f6", border_width=1)
            entry.insert(0, str(patient.get(field_key, '')))
            entry.pack(pady=(0, 10), fill="x")
            
            fields[field_key] = entry
        
        label = ctk.CTkLabel(form_frame, text="Gender", font=("Arial", 10, "bold"), 
                            text_color="#cbd5e1")
        label.pack(anchor="w", pady=(10, 2))
        
        gender_combo = ctk.CTkComboBox(form_frame, values=["", "Male", "Female"], 
                                      width=400, height=30, font=("Arial", 10),
                                      fg_color="#0f172a", border_color="#3b82f6", border_width=1)
        gender_combo.set(patient.get('gender', '') or '')
        gender_combo.pack(pady=(0, 20), fill="x")
        
        fields['gender'] = gender_combo
        
        save_btn = CustomButton(form_frame, text="Save Changes", 
                               command=lambda: self.save_patient_changes(patient['patient_id'], fields, edit_window, parent_popup),
                               width=150, height=40, font=("Arial", 11, "bold"),
                               fg_color="#10b981", hover_color="#059669")
        save_btn.pack(pady=20)
    
    def save_patient_changes(self, patient_id, fields, edit_window, parent_popup):
        """Save edited patient data"""
        try:
            update_query = """UPDATE patients SET first_name=%s, last_name=%s, phone=%s, address=%s, age=%s, gender=%s
                            WHERE patient_id=%s"""
            
            values = (
                fields['first_name'].get(),
                fields['last_name'].get(),
                fields['phone'].get(),
                fields['address'].get(),
                int(fields['age'].get()) if fields['age'].get() else None,
                fields['gender'].get() or None,
                patient_id
            )
            
            if self.db.execute(update_query, values):
                print("✓ Patient updated successfully")
                edit_window.destroy()
                parent_popup.destroy()
                self.load_active_patients()
            else:
                print("✗ Failed to update patient")
        except ValueError as e:
            print(f"✗ Invalid input: {str(e)}")
    
    def soft_delete_patient(self, patient_id, parent_window):
        """Soft delete patient (move to history)"""
        update_query = "UPDATE patients SET is_deleted=1 WHERE patient_id=%s"
        
        if self.db.execute(update_query, (patient_id,)):
            print(f"✓ Patient {patient_id} moved to history")
            parent_window.destroy()
            self.load_active_patients()
        else:
            print(f"✗ Failed to delete patient {patient_id}")
    
    def restore_patient(self):
        """Restore deleted patient"""
        if not self.current_patient:
            self.status_label.configure(text="⚠ No patient selected", text_color="#ef4444")
            return
        
        patient_id = self.current_patient['patient_id']
        update_query = "UPDATE patients SET is_deleted=0 WHERE patient_id=%s"
        
        if self.db.execute(update_query, (patient_id,)):
            self.status_label.configure(text="✓ Patient restored successfully", text_color="#10b981")
            self.current_patient = None
            self.restore_btn.configure(state="disabled")
            self.load_deleted_patients()
        else:
            self.status_label.configure(text="✗ Failed to restore patient", text_color="#ef4444")
    
    def clear_selection(self):
        """Clear selection"""
        self.current_patient = None
        self.restore_btn.configure(state="disabled")
        self.status_label.configure(text="")
    
    def toggle_history(self):
        self.show_history = not self.show_history
        
        # Clear and recreate main content
        for widget in self.frame.winfo_children():
            if widget != self.frame.winfo_children()[0]:  # Keep header
                widget.destroy()
        
        main_content = ctk.CTkFrame(self.frame, fg_color="transparent")
        main_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        if self.show_history:
            self.setup_history_view(main_content)
        else:
            self.setup_active_view(main_content)
    
    def get_frame(self):
        return self.frame
    
    def show(self):
        self.frame.pack(fill="both", expand=True)
        self.frame.tkraise()
    
    def hide(self):
        self.frame.pack_forget()