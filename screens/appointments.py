import customtkinter as ctk
from components.ui_components import CustomButton
from datetime import datetime

class AppointmentsScreen:
    def __init__(self, parent, db, on_back, on_navigate=None):
        self.parent = parent
        self.db = db
        self.on_back = on_back
        self.on_navigate = on_navigate
        self.frame = ctk.CTkFrame(parent)
        self.current_appointment = None
        self.all_appointments = []
        self.is_today_view = False
        self.form_container = None
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
        
        # Main content
        main_content = ctk.CTkFrame(self.frame, fg_color="transparent")
        main_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.form_wrapper = ctk.CTkFrame(main_content, fg_color="transparent")
        self.form_wrapper.pack(side="left", fill="both", padx=(0, 15), expand=False)
        
        self.form_container = ctk.CTkFrame(self.form_wrapper, fg_color="#1e293b", corner_radius=10)
        self.form_container.pack(fill="both", expand=True)
        
        form_title = ctk.CTkLabel(self.form_container, text="Schedule Appointment", 
                                 font=("Arial", 13, "bold"), text_color="#ffffff")
        form_title.pack(pady=(15, 10), padx=15)
        
        form_scroll = ctk.CTkScrollableFrame(self.form_container, fg_color="#1e293b", width=300)
        form_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.form_fields = {}
        
        self._add_form_field(form_scroll, "Name", "name")
        self._add_form_field(form_scroll, "Contact", "contact")
        self._add_form_field(form_scroll, "Age", "age")
        self._add_combobox_field(form_scroll, "Gender", "gender", ["", "Male", "Female"])
        self._add_combobox_field(form_scroll, "Type", "type", ["", "Child", "Adult"])
        self._add_form_field(form_scroll, "Address", "address")
        self._add_form_field(form_scroll, "Date/Time (YYYY-MM-DD HH:MM)", "date_time")
        self._add_form_field(form_scroll, "Dental Service", "dental_service")
        self._add_form_field(form_scroll, "Service Fee", "service_fee")
        
        buttons_frame = ctk.CTkFrame(self.form_container, fg_color="#1e293b")
        buttons_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.schedule_btn = CustomButton(buttons_frame, text="Schedule", 
                                   command=self.add_appointment,
                                   width=50, height=32, font=("Arial", 8, "bold"),
                                   fg_color="#10b981", hover_color="#059669")
        self.schedule_btn.pack(side="left", padx=1)
        
        self.update_btn = CustomButton(buttons_frame, text="Update", 
                                      command=self.update_appointment,
                                      width=50, height=32, font=("Arial", 8, "bold"),
                                      fg_color="#3b82f6", hover_color="#1d4ed8", state="disabled")
        self.update_btn.pack(side="left", padx=1)
        
        self.delete_btn = CustomButton(buttons_frame, text="Delete", 
                                      command=self.delete_appointment,
                                      width=50, height=32, font=("Arial", 8, "bold"),
                                      fg_color="#ef4444", hover_color="#dc2626", state="disabled")
        self.delete_btn.pack(side="left", padx=1)
        
        self.clear_btn = CustomButton(buttons_frame, text="Clear", 
                                     command=self.clear_form,
                                     width=50, height=32, font=("Arial", 8, "bold"),
                                     fg_color="#6b7280", hover_color="#4b5563")
        self.clear_btn.pack(side="left", padx=1)
        
        self.status_label = ctk.CTkLabel(self.form_container, text="", font=("Arial", 9, "bold"))
        self.status_label.pack(pady=(0, 10))
        
        list_container = ctk.CTkFrame(main_content, fg_color="#1e293b", corner_radius=10)
        list_container.pack(side="right", fill="both", expand=True)
        
        self.list_title = ctk.CTkLabel(list_container, text="All Appointments", 
                                       font=("Arial", 13, "bold"), text_color="#ffffff")
        self.list_title.pack(pady=(15, 10), padx=15)
        
        table_frame = ctk.CTkFrame(list_container, fg_color="#0f172a", corner_radius=5)
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.appointments_table = ctk.CTkTextbox(table_frame, text_color="#e2e8f0", 
                                                fg_color="#0f172a", border_color="#3b82f6", 
                                                border_width=2, font=("Courier", 10))
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
    
    def format_datetime(self, datetime_str):
        """Format datetime to YYYY-MM-DD HH:MMAM/PM"""
        if not datetime_str:
            return "N/A"
        
        try:
            dt = datetime.strptime(str(datetime_str), "%Y-%m-%d %H:%M:%S")
            date_part = dt.strftime("%Y-%m-%d")
            start_time = dt.strftime("%I:%M%p").lstrip('0')
            
            end_dt = datetime(dt.year, dt.month, dt.day, dt.hour + 1, dt.minute)
            end_time = end_dt.strftime("%I:%M%p").lstrip('0')
            
            return f"{date_part} {start_time}-{end_time}"
        except:
            return str(datetime_str)[:20]
    
    def load_appointments(self):
        """Load all appointments - exclude Done status"""
        query = "SELECT * FROM appointments WHERE Status NOT IN ('Cancelled', 'Done') ORDER BY `Date/Time` DESC"
        self.all_appointments = self.db.fetch_all(query)
        
        self.appointments_table.configure(state="normal")
        self.appointments_table.delete("1.0", "end")
        
        if not self.all_appointments:
            self.appointments_table.insert("end", "No appointments found\n")
        else:
            header = f"{'ID':<4} {'Name':<10} {'Contact':<11} {'Age':<4} {'Gender':<7} {'Type':<7} {'Address':<11} {'Service':<11} {'Fee':<8} {'Status':<10}\n"
            separator = "─" * 120 + "\n"
            
            self.appointments_table.insert("end", header)
            self.appointments_table.insert("end", separator)
            
            for apt in self.all_appointments:
                apt_id = str(apt.get('appointment_id', ''))
                name = (apt.get('Name', ''))[:10]
                contact = (apt.get('Contact', '') or 'N/A')[:11]
                age = str(apt.get('Age', ''))[:4]
                gender = (apt.get('Gender', '') or 'N/A')[:7]
                type_ = (apt.get('Type', '') or 'N/A')[:7]
                address = (apt.get('Address', '') or 'N/A')[:11]
                service = (apt.get('Dental_service', '') or 'N/A')[:11]
                fee = f"${apt.get('Service_fee', 0):.2f}"[:8]
                status = apt.get('Status', 'Scheduled')
                
                row = f"{apt_id:<4} {name:<10} {contact:<11} {age:<4} {gender:<7} {type_:<7} {address:<11} {service:<11} {fee:<8} {status:<10}\n"
                self.appointments_table.insert("end", row)
        
        self.appointments_table.configure(state="disabled")
    
    def load_today_appointments(self):
        """Load today's appointments - exclude Done status"""
        query = """SELECT * FROM appointments 
                  WHERE DATE(`Date/Time`) = CURDATE() AND Status NOT IN ('Cancelled', 'Done')
                  ORDER BY `Date/Time` ASC"""
        self.all_appointments = self.db.fetch_all(query)
        
        self.appointments_table.configure(state="normal")
        self.appointments_table.delete("1.0", "end")
        
        if not self.all_appointments:
            self.appointments_table.insert("end", "No appointments today\n")
        else:
            header = f"{'ID':<4} {'Name':<10} {'Contact':<11} {'Age':<4} {'Gender':<7} {'Type':<7} {'Address':<11} {'Service':<11} {'Fee':<8} {'Status':<10}\n"
            separator = "─" * 120 + "\n"
            
            self.appointments_table.insert("end", header)
            self.appointments_table.insert("end", separator)
            
            for apt in self.all_appointments:
                apt_id = str(apt.get('appointment_id', ''))
                name = (apt.get('Name', ''))[:10]
                contact = (apt.get('Contact', '') or 'N/A')[:11]
                age = str(apt.get('Age', ''))[:4]
                gender = (apt.get('Gender', '') or 'N/A')[:7]
                type_ = (apt.get('Type', '') or 'N/A')[:7]
                address = (apt.get('Address', '') or 'N/A')[:11]
                service = (apt.get('Dental_service', '') or 'N/A')[:11]
                fee = f"${apt.get('Service_fee', 0):.2f}"[:8]
                status = apt.get('Status', 'Scheduled')
                
                row = f"{apt_id:<4} {name:<10} {contact:<11} {age:<4} {gender:<7} {type_:<7} {address:<11} {service:<11} {fee:<8} {status:<10}\n"
                self.appointments_table.insert("end", row)
        
        self.appointments_table.configure(state="disabled")
    
    def on_table_click(self, event):
        """Handle appointment click to select it"""
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
        """Select appointment and populate form"""
        self.current_appointment = appointment
        
        self.form_fields['name'].delete(0, "end")
        self.form_fields['name'].insert(0, str(appointment.get('Name', '')))
        
        self.form_fields['contact'].delete(0, "end")
        self.form_fields['contact'].insert(0, str(appointment.get('Contact', '')))
        
        self.form_fields['age'].delete(0, "end")
        self.form_fields['age'].insert(0, str(appointment.get('Age', '')))
        
        self.form_fields['gender'].set(appointment.get('Gender', '') or '')
        self.form_fields['type'].set(appointment.get('Type', '') or '')
        
        self.form_fields['address'].delete(0, "end")
        self.form_fields['address'].insert(0, str(appointment.get('Address', '')))
        
        # Extract date/time in correct format (YYYY-MM-DD HH:MM)
        date_time_full = str(appointment.get('Date/Time', ''))
        date_time_input = date_time_full[:16] if len(date_time_full) >= 16 else date_time_full
        
        self.form_fields['date_time'].delete(0, "end")
        self.form_fields['date_time'].insert(0, date_time_input)
        
        self.form_fields['dental_service'].delete(0, "end")
        self.form_fields['dental_service'].insert(0, str(appointment.get('Dental_service', '')))
        
        self.form_fields['service_fee'].delete(0, "end")
        self.form_fields['service_fee'].insert(0, str(appointment.get('Service_fee', '')))
        
        self.schedule_btn.configure(state="disabled")
        self.update_btn.configure(state="normal")
        self.delete_btn.configure(state="normal")
        
        self.status_label.configure(text=f"✏️ ID: {appointment.get('appointment_id', '')}", 
                                   text_color="#3b82f6")
    def add_appointment(self):
        """Add new appointment"""
        try:
            name = self.form_fields['name'].get().strip()
            contact = self.form_fields['contact'].get().strip()
            age_str = self.form_fields['age'].get().strip()
            gender = self.form_fields['gender'].get() or None
            type_ = self.form_fields['type'].get() or None
            address = self.form_fields['address'].get().strip()
            date_time = self.form_fields['date_time'].get().strip()
            dental_service = self.form_fields['dental_service'].get().strip()
            service_fee_str = self.form_fields['service_fee'].get().strip()
            
            if not name or not contact or not date_time or not dental_service:
                self.status_label.configure(text="⚠ Required fields missing", text_color="#ef4444")
                return
            
            try:
                age = int(age_str) if age_str else None
                service_fee = float(service_fee_str) if service_fee_str else 0.0
            except ValueError:
                self.status_label.configure(text="✗ Age and Fee must be numbers", text_color="#ef4444")
                return
            
            # Validate date format
            try:
                apt_date = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
                if apt_date.weekday() == 6:
                    self.status_label.configure(text="✗ Sorry, dentist is off on Sundays. Choose another day.", text_color="#ef4444")
                    return
            except ValueError:
                self.status_label.configure(text="✗ Invalid date format. Use YYYY-MM-DD HH:MM (e.g., 2025-01-15 14:30)", text_color="#ef4444")
                return
            
            check_query = "SELECT COUNT(*) as count FROM appointments WHERE `Date/Time` = %s AND Status != 'Cancelled'"
            result = self.db.fetch_one(check_query, (date_time,))
            
            if result and result['count'] > 0:
                self.status_label.configure(text="✗ Time slot occupied. Choose another.", text_color="#ef4444")
                return
            
            insert_query = """INSERT INTO appointments (Name, Contact, Age, Gender, Type, Address, `Date/Time`, Dental_service, Service_fee, Status)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'Scheduled')"""
            
            if self.db.execute(insert_query, (name, contact, age, gender, type_, address, date_time, dental_service, service_fee)):
                self.status_label.configure(text="✓ Appointment scheduled", text_color="#10b981")
                self.clear_form()
                self.load_appointments()
            else:
                self.status_label.configure(text="✗ Failed to schedule", text_color="#ef4444")
        except Exception as e:
            self.status_label.configure(text=f"✗ Error: {str(e)}", text_color="#ef4444")

    def update_appointment(self):
        """Update selected appointment"""
        if not self.current_appointment:
            self.status_label.configure(text="⚠ No appointment selected", text_color="#ef4444")
            return
        
        try:
            appointment_id = self.current_appointment.get('appointment_id')
            name = self.form_fields['name'].get().strip()
            contact = self.form_fields['contact'].get().strip()
            age_str = self.form_fields['age'].get().strip()
            gender = self.form_fields['gender'].get() or None
            type_ = self.form_fields['type'].get() or None
            address = self.form_fields['address'].get().strip()
            date_time = self.form_fields['date_time'].get().strip()
            dental_service = self.form_fields['dental_service'].get().strip()
            service_fee_str = self.form_fields['service_fee'].get().strip()
            
            if not name or not contact or not date_time or not dental_service:
                self.status_label.configure(text="⚠ Required fields missing", text_color="#ef4444")
                return
            
            try:
                age = int(age_str) if age_str else None
                service_fee = float(service_fee_str) if service_fee_str else 0.0
            except ValueError:
                self.status_label.configure(text="✗ Age and Fee must be numbers", text_color="#ef4444")
                return
            
            # Validate date format
            try:
                apt_date = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
            except ValueError:
                self.status_label.configure(text="✗ Invalid date format. Use YYYY-MM-DD HH:MM (e.g., 2025-01-15 14:30)", text_color="#ef4444")
                return
            
            update_query = """UPDATE appointments SET Name=%s, Contact=%s, Age=%s, Gender=%s, Type=%s, Address=%s, `Date/Time`=%s, Dental_service=%s, Service_fee=%s
                            WHERE appointment_id=%s"""
            
            if self.db.execute(update_query, (name, contact, age, gender, type_, address, date_time, dental_service, service_fee, appointment_id)):
                self.status_label.configure(text="✓ Appointment updated", text_color="#10b981")
                self.clear_form()
                if self.is_today_view:
                    self.load_today_appointments()
                else:
                    self.load_appointments()
            else:
                self.status_label.configure(text="✗ Failed to update", text_color="#ef4444")
        except Exception as e:
            self.status_label.configure(text=f"✗ Error: {str(e)}", text_color="#ef4444")
    
    def delete_appointment(self):
        """Delete selected appointment"""
        if not self.current_appointment:
            self.status_label.configure(text="⚠ No appointment selected", text_color="#ef4444")
            return
        
        try:
            appointment_id = self.current_appointment.get('appointment_id')
            delete_query = "DELETE FROM appointments WHERE appointment_id=%s"
            
            if self.db.execute(delete_query, (appointment_id,)):
                self.status_label.configure(text="✓ Appointment deleted", text_color="#10b981")
                self.clear_form()
                self.load_appointments()
            else:
                self.status_label.configure(text="✗ Failed to delete", text_color="#ef4444")
        except Exception as e:
            self.status_label.configure(text=f"✗ Error: {str(e)}", text_color="#ef4444")
    
    def clear_form(self):
        """Clear form fields"""
        for key, field in self.form_fields.items():
            if hasattr(field, 'delete'):
                field.delete(0, "end")
            else:
                field.set("")
        
        self.current_appointment = None
        self.schedule_btn.configure(state="normal")
        self.update_btn.configure(state="disabled")
        self.delete_btn.configure(state="disabled")
        self.status_label.configure(text="")
    
    def get_frame(self):
        return self.frame
    
    def show(self):
        """Show all appointments with form"""
        self.is_today_view = False
        self.list_title.configure(text="All Appointments")
        self.form_wrapper.pack(side="left", fill="both", padx=(0, 15), expand=False)
        self.load_appointments()
        self.frame.pack(fill="both", expand=True)
        self.frame.tkraise()
    
    def show_today(self):
        """Show today's appointments WITHOUT form"""
        self.is_today_view = True
        self.list_title.configure(text="Today's Appointments")
        self.form_wrapper.pack_forget()
        self.load_today_appointments()
        self.frame.pack(fill="both", expand=True)
        self.frame.tkraise()
    
    def hide(self):
        self.frame.pack_forget()

