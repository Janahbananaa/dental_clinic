import customtkinter as ctk
from components.ui_components import CustomButton
from datetime import datetime

class AppointmentsScreen:
    def __init__(self, parent, db, on_back):
        self.parent = parent
        self.db = db
        self.on_back = on_back
        self.frame = ctk.CTkFrame(parent)
        self.current_appointment = None
        self.all_appointments = []
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
        
        title = ctk.CTkLabel(header_content, text="📅 Appointments Management", 
                            font=("Arial", 18, "bold"), text_color="#ffffff")
        title.pack(side="left", padx=20)
        
        today_btn = CustomButton(header_content, text="📋 Today's Appointments", 
                                command=self.show_today_appointments,
                                width=200, height=35, font=("Arial", 10, "bold"),
                                fg_color="#f59e0b", hover_color="#d97706")
        today_btn.pack(side="right", padx=10)
        
        # Main content
        main_content = ctk.CTkFrame(self.frame, fg_color="transparent")
        main_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form container
        form_container = ctk.CTkFrame(main_content, fg_color="#1e293b", corner_radius=10)
        form_container.pack(side="left", fill="both", padx=(0, 15))
        
        form_title = ctk.CTkLabel(form_container, text="Schedule Appointment", 
                                 font=("Arial", 13, "bold"), text_color="#ffffff")
        form_title.pack(pady=(15, 10), padx=15)
        
        form_scroll = ctk.CTkScrollableFrame(form_container, fg_color="#1e293b", width=300)
        form_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.form_fields = {}
        
        self._add_form_field(form_scroll, "Patient Name", "name")
        self._add_form_field(form_scroll, "Contact", "contact")
        self._add_form_field(form_scroll, "Age", "age")
        self._add_combobox_field(form_scroll, "Gender", "gender", ["", "Male", "Female"])
        self._add_combobox_field(form_scroll, "Type", "type", ["", "Walk-in", "Online", "Referral"])
        self._add_form_field(form_scroll, "Date/Time (YYYY-MM-DD HH:MM)", "date_time")
        self._add_form_field(form_scroll, "Dental Service", "dental_service")
        self._add_form_field(form_scroll, "Service Fee", "service_fee")
        
        buttons_frame = ctk.CTkFrame(form_container, fg_color="#1e293b")
        buttons_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.add_btn = CustomButton(buttons_frame, text="Schedule", 
                                   command=self.add_appointment,
                                   width=70, height=32, font=("Arial", 9, "bold"),
                                   fg_color="#10b981", hover_color="#059669")
        self.add_btn.pack(side="left", padx=3)
        
        self.edit_btn = CustomButton(buttons_frame, text="Edit", 
                                    command=self.update_appointment,
                                    width=70, height=32, font=("Arial", 9, "bold"),
                                    fg_color="#3b82f6", hover_color="#1d4ed8", state="disabled")
        self.edit_btn.pack(side="left", padx=3)
        
        self.cancel_btn = CustomButton(buttons_frame, text="Cancel", 
                                      command=self.cancel_appointment,
                                      width=70, height=32, font=("Arial", 9, "bold"),
                                      fg_color="#ef4444", hover_color="#dc2626", state="disabled")
        self.cancel_btn.pack(side="left", padx=3)
        
        self.clear_btn = CustomButton(buttons_frame, text="Clear", 
                                     command=self.clear_form,
                                     width=70, height=32, font=("Arial", 9, "bold"),
                                     fg_color="#6b7280", hover_color="#4b5563")
        self.clear_btn.pack(side="left", padx=3)
        
        self.status_label = ctk.CTkLabel(form_container, text="", font=("Arial", 9, "bold"))
        self.status_label.pack(pady=(0, 10))
        
        # Right side - Appointments list
        list_container = ctk.CTkFrame(main_content, fg_color="#1e293b", corner_radius=10)
        list_container.pack(side="right", fill="both", expand=True)
        
        list_title = ctk.CTkLabel(list_container, text="Appointments", 
                                 font=("Arial", 13, "bold"), text_color="#ffffff")
        list_title.pack(pady=(15, 10), padx=15)
        
        table_frame = ctk.CTkFrame(list_container, fg_color="#0f172a", corner_radius=5)
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.appointments_table = ctk.CTkTextbox(table_frame, text_color="#e2e8f0", 
                                                fg_color="#0f172a", border_color="#3b82f6", 
                                                border_width=2, font=("Courier", 9))
        self.appointments_table.pack(fill="both", expand=True)
        self.appointments_table.configure(state="disabled")
        
        self.appointments_table.bind("<Button-1>", self.on_table_click)
        
        self.load_appointments()
    
    def _add_form_field(self, parent, label_text, field_key):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 9, "bold"), 
                            text_color="#cbd5e1")
        label.pack(anchor="w", padx=0, pady=(8, 2))
        
        entry = ctk.CTkEntry(parent, width=250, height=30, font=("Arial", 9),
                            fg_color="#0f172a", border_color="#3b82f6", border_width=1)
        entry.pack(padx=0, pady=(0, 8), fill="x")
        
        self.form_fields[field_key] = entry
    
    def _add_combobox_field(self, parent, label_text, field_key, values):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 9, "bold"), 
                            text_color="#cbd5e1")
        label.pack(anchor="w", padx=0, pady=(8, 2))
        
        combo = ctk.CTkComboBox(parent, values=values, width=250, height=30, 
                               font=("Arial", 9), fg_color="#0f172a", 
                               border_color="#3b82f6", border_width=1)
        combo.pack(padx=0, pady=(0, 8), fill="x")
        
        self.form_fields[field_key] = combo
    
    def load_appointments(self):
        query = "SELECT * FROM appointments WHERE Status != 'Cancelled' ORDER BY `Date/Time` DESC"
        self.all_appointments = self.db.fetch_all(query)
        
        self.appointments_table.configure(state="normal")
        self.appointments_table.delete("1.0", "end")
        
        if not self.all_appointments:
            self.appointments_table.insert("end", "No appointments found\n")
        else:
            header = f"{'ID':<5} {'Name':<15} {'Date/Time':<20} {'Service':<20} {'Status':<12}\n"
            separator = "─" * 75 + "\n"
            
            self.appointments_table.insert("end", header)
            self.appointments_table.insert("end", separator)
            
            for apt in self.all_appointments:
                apt_id = str(apt.get('appointment_id', ''))
                name = (apt.get('Name', ''))[:15]
                date_time = str(apt.get('Date/Time', ''))[:20]
                service = (apt.get('Dental_service', ''))[:20]
                status = apt.get('Status', 'Scheduled')
                
                row = f"{apt_id:<5} {name:<15} {date_time:<20} {service:<20} {status:<12}\n"
                self.appointments_table.insert("end", row)
        
        self.appointments_table.configure(state="disabled")
    
    def on_table_click(self, event):
        try:
            index = self.appointments_table.index(f"@{event.x},{event.y}")
            line_num = int(index.split(".")[0])
            
            if line_num <= 2:
                return
            
            line_text = self.appointments_table.get(f"{line_num}.0", f"{line_num}.end").strip()
            
            if not line_text or line_text.startswith("─"):
                return
            
            try:
                appointment_id = int(line_text.split()[0])
                
                for apt in self.all_appointments:
                    if apt.get('appointment_id') == appointment_id:
                        self.select_appointment(apt)
                        break
            except (ValueError, IndexError):
                pass
        except Exception as e:
            print(f"Error on table click: {e}")
    
    def select_appointment(self, appointment):
        self.current_appointment = appointment
        
        self.form_fields['name'].delete(0, "end")
        self.form_fields['name'].insert(0, str(appointment.get('Name', '')))
        
        self.form_fields['contact'].delete(0, "end")
        self.form_fields['contact'].insert(0, str(appointment.get('Contact', '')))
        
        self.form_fields['age'].delete(0, "end")
        self.form_fields['age'].insert(0, str(appointment.get('Age', '')))
        
        self.form_fields['gender'].set(appointment.get('Gender', ''))
        self.form_fields['type'].set(appointment.get('Type', ''))
        
        self.form_fields['date_time'].delete(0, "end")
        self.form_fields['date_time'].insert(0, str(appointment.get('Date/Time', '')))
        
        self.form_fields['dental_service'].delete(0, "end")
        self.form_fields['dental_service'].insert(0, str(appointment.get('Dental_service', '')))
        
        self.form_fields['service_fee'].delete(0, "end")
        self.form_fields['service_fee'].insert(0, str(appointment.get('Service_fee', '')))
        
        self.add_btn.configure(state="disabled")
        self.edit_btn.configure(state="normal")
        self.cancel_btn.configure(state="normal")
        
        self.status_label.configure(text=f"✏️ Appointment ID: {appointment.get('appointment_id', '')}", 
                                   text_color="#3b82f6")
    
    def add_appointment(self):
        try:
            name = self.form_fields['name'].get()
            contact = self.form_fields['contact'].get()
            age = int(self.form_fields['age'].get()) if self.form_fields['age'].get() else None
            gender = self.form_fields['gender'].get()
            type_ = self.form_fields['type'].get()
            date_time = self.form_fields['date_time'].get()
            dental_service = self.form_fields['dental_service'].get()
            service_fee = float(self.form_fields['service_fee'].get()) if self.form_fields['service_fee'].get() else 0.0
            
            if not all([name, contact, date_time, dental_service]):
                self.status_label.configure(text="⚠ Required fields missing", text_color="#ef4444")
                return
            
            # Check for double booking
            check_query = "SELECT COUNT(*) as count FROM appointments WHERE `Date/Time` = %s AND Status != 'Cancelled'"
            result = self.db.fetch_one(check_query, (date_time,))
            
            if result and result['count'] > 0:
                self.status_label.configure(text="✗ This time slot is occupied. Choose another.", 
                                           text_color="#ef4444")
                return
            
            insert_query = """INSERT INTO appointments (Name, Contact, Age, Gender, Type, `Date/Time`, Dental_service, Service_fee, Status)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Scheduled')"""
            
            if self.db.execute(insert_query, (name, contact, age, gender, type_, date_time, dental_service, service_fee)):
                self.status_label.configure(text="✓ Appointment scheduled", text_color="#10b981")
                self.clear_form()
                self.load_appointments()
            else:
                self.status_label.configure(text="✗ Failed to schedule", text_color="#ef4444")
        except ValueError as e:
            self.status_label.configure(text=f"✗ Invalid input: {str(e)}", text_color="#ef4444")
    
    def update_appointment(self):
        if not self.current_appointment:
            return
        
        try:
            appointment_id = self.current_appointment.get('appointment_id')
            name = self.form_fields['name'].get()
            contact = self.form_fields['contact'].get()
            age = int(self.form_fields['age'].get()) if self.form_fields['age'].get() else None
            gender = self.form_fields['gender'].get()
            type_ = self.form_fields['type'].get()
            date_time = self.form_fields['date_time'].get()
            dental_service = self.form_fields['dental_service'].get()
            service_fee = float(self.form_fields['service_fee'].get()) if self.form_fields['service_fee'].get() else 0.0
            
            update_query = """UPDATE appointments SET Name=%s, Contact=%s, Age=%s, Gender=%s, Type=%s, `Date/Time`=%s, Dental_service=%s, Service_fee=%s
                            WHERE appointment_id=%s"""
            
            if self.db.execute(update_query, (name, contact, age, gender, type_, date_time, dental_service, service_fee, appointment_id)):
                self.status_label.configure(text="✓ Appointment updated", text_color="#10b981")
                self.clear_form()
                self.load_appointments()
            else:
                self.status_label.configure(text="✗ Failed to update", text_color="#ef4444")
        except ValueError as e:
            self.status_label.configure(text=f"✗ Invalid input: {str(e)}", text_color="#ef4444")
    
    def cancel_appointment(self):
        if not self.current_appointment:
            return
        
        appointment_id = self.current_appointment.get('appointment_id')
        update_query = "UPDATE appointments SET Status='Cancelled' WHERE appointment_id=%s"
        
        if self.db.execute(update_query, (appointment_id,)):
            self.status_label.configure(text="✓ Appointment cancelled", text_color="#10b981")
            self.clear_form()
            self.load_appointments()
        else:
            self.status_label.configure(text="✗ Failed to cancel", text_color="#ef4444")
    
    def show_today_appointments(self):
        query = """SELECT * FROM appointments 
                  WHERE DATE(`Date/Time`) = CURDATE() AND Status != 'Cancelled'
                  ORDER BY `Date/Time` ASC"""
        appointments = self.db.fetch_all(query)
        
        self.appointments_table.configure(state="normal")
        self.appointments_table.delete("1.0", "end")
        
        if not appointments:
            self.appointments_table.insert("end", "No appointments today\n")
        else:
            header = f"{'ID':<5} {'Name':<20} {'Time':<8} {'Service':<25} {'Status':<12}\n"
            separator = "─" * 75 + "\n"
            
            self.appointments_table.insert("end", header)
            self.appointments_table.insert("end", separator)
            
            for apt in appointments:
                apt_id = str(apt.get('appointment_id', ''))
                name = (apt.get('Name', ''))[:20]
                time = str(apt.get('Date/Time', ''))[11:19]
                service = (apt.get('Dental_service', ''))[:25]
                status = apt.get('Status', 'Scheduled')
                
                row = f"{apt_id:<5} {name:<20} {time:<8} {service:<25} {status:<12}\n"
                self.appointments_table.insert("end", row)
        
        self.appointments_table.configure(state="disabled")
    
    def clear_form(self):
        for key, field in self.form_fields.items():
            if hasattr(field, 'delete'):
                field.delete(0, "end")
            else:
                field.set("")
        
        self.current_appointment = None
        self.add_btn.configure(state="normal")
        self.edit_btn.configure(state="disabled")
        self.cancel_btn.configure(state="disabled")
        self.status_label.configure(text="")
    
    def get_frame(self):
        return self.frame
    
    def show(self):
        self.load_appointments()
        self.frame.pack(fill="both", expand=True)
        self.frame.tkraise()
    
    def hide(self):
        self.frame.pack_forget()

