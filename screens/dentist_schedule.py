import customtkinter as ctk
from components.ui_components import CustomButton
from datetime import datetime

class DentistScheduleScreen:
    def __init__(self, parent, db, on_back, on_appointment_update=None):
        self.parent = parent
        self.db = db
        self.on_back = on_back
        self.on_appointment_update = on_appointment_update
        self.frame = ctk.CTkFrame(parent)
        self.all_schedules = []
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
        
        title = ctk.CTkLabel(header_content, text="👨‍⚕️ Dentist Schedule", 
                            font=("Arial", 18, "bold"), text_color="#ffffff")
        title.pack(side="left", padx=20)
        
        # Main content
        main_content = ctk.CTkFrame(self.frame, fg_color="transparent")
        main_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Scheduled Patients table
        list_container = ctk.CTkFrame(main_content, fg_color="#1e293b", corner_radius=10)
        list_container.pack(fill="both", expand=True)
        
        list_title = ctk.CTkLabel(list_container, text="Scheduled Patients", 
                                 font=("Arial", 13, "bold"), text_color="#ffffff")
        list_title.pack(pady=(15, 10), padx=15)
        
        table_frame = ctk.CTkFrame(list_container, fg_color="#0f172a", corner_radius=5)
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.schedule_table = ctk.CTkTextbox(table_frame, text_color="#e2e8f0", 
                                            fg_color="#0f172a", border_color="#3b82f6", 
                                            border_width=2, font=("Courier", 11))
        self.schedule_table.pack(fill="both", expand=True)
        self.schedule_table.configure(state="disabled")
        
        self.load_schedules()
        self.schedule_table.bind("<Button-1>", self.on_table_click)
    
    def load_schedules(self):
        """Load scheduled patients from appointments - exclude Done"""
        query = """SELECT a.appointment_id, a.Name, a.Contact, a.Age, a.Gender, a.Type, a.Address, a.`Date/Time`, a.Dental_service, a.Service_fee, a.Status
                   FROM appointments a
                   WHERE a.Status IN ('Scheduled', 'Ongoing')
                   ORDER BY a.`Date/Time` ASC"""
        self.all_schedules = self.db.fetch_all(query)
        
        self.schedule_table.configure(state="normal")
        self.schedule_table.delete("1.0", "end")
        
        if not self.all_schedules:
            self.schedule_table.insert("end", "No scheduled patients\n")
        else:
            header = f"{'ID':<4} {'Name':<10} {'Contact':<11} {'Age':<4} {'Gender':<7} {'Type':<7} {'Address':<11} {'Service':<11} {'Fee':<8} {'Status':<10}\n"
            separator = "─" * 120 + "\n"
            
            self.schedule_table.insert("end", header)
            self.schedule_table.insert("end", separator)
            
            for sched in self.all_schedules:
                apt_id = str(sched.get('appointment_id', ''))
                name = (sched.get('Name') or '')[:10]
                contact = (sched.get('Contact') or 'N/A')[:11]
                age = str(sched.get('Age') or '')[:4]
                gender = (sched.get('Gender') or 'N/A')[:7]
                type_ = (sched.get('Type') or 'N/A')[:7]
                address = (sched.get('Address') or 'N/A')[:11]
                service = (sched.get('Dental_service') or 'N/A')[:11]
                fee = f"${sched.get('Service_fee', 0):.2f}"[:8]
                status = sched.get('Status', 'Scheduled')
                
                row = f"{apt_id:<4} {name:<10} {contact:<11} {age:<4} {gender:<7} {type_:<7} {address:<11} {service:<11} {fee:<8} {status:<10}\n"
                self.schedule_table.insert("end", row)
        
        self.schedule_table.configure(state="disabled")
    
    def on_table_click(self, event):
        """Handle appointment click to change status"""
        try:
            index = self.schedule_table.index(f"@{event.x},{event.y}")
            line_num = int(index.split(".")[0])
            
            if line_num <= 2:
                return
            
            line_text = self.schedule_table.get(f"{line_num}.0", f"{line_num}.end").strip()
            
            if not line_text or line_text.startswith("─"):
                return
            
            try:
                appointment_id = int(line_text.split()[0])
                
                for sched in self.all_schedules:
                    if sched.get('appointment_id') == appointment_id:
                        self.show_status_dialog(sched)
                        break
            except (ValueError, IndexError):
                pass
        except Exception as e:
            print(f"Error: {e}")
    
    def show_status_dialog(self, appointment):
        """Show status change dialog"""
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title(f"Update Status: {appointment['Name']}")
        dialog.geometry("450x350")
        dialog.resizable(False, False)
        
        dialog.transient(self.parent)
        dialog.grab_set()
        
        frame = ctk.CTkFrame(dialog, fg_color="#1e293b")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        info = ctk.CTkLabel(frame, text=f"Patient: {appointment['Name']}\nDate: {appointment['Date/Time']}\nCurrent Status: {appointment['Status']}", 
                           font=("Arial", 12), text_color="#cbd5e1", justify="left")
        info.pack(anchor="w", pady=20)
        
        status_label = ctk.CTkLabel(frame, text="Select New Status:", 
                                   font=("Arial", 12, "bold"), text_color="#ffffff")
        status_label.pack(anchor="w", padx=0, pady=(10, 15))
        
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="both", expand=True, padx=0, pady=10)
        
        scheduled_btn = CustomButton(btn_frame, text="Scheduled", 
                    command=lambda: self.update_status_and_close(appointment['appointment_id'], "Scheduled", dialog),
                    width=150, height=45, font=("Arial", 11, "bold"),
                    fg_color="#f59e0b", hover_color="#d97706")
        scheduled_btn.pack(pady=8, fill="x")
        
        ongoing_btn = CustomButton(btn_frame, text="Ongoing", 
                    command=lambda: self.update_status_and_close(appointment['appointment_id'], "Ongoing", dialog),
                    width=150, height=45, font=("Arial", 11, "bold"),
                    fg_color="#3b82f6", hover_color="#1d4ed8")
        ongoing_btn.pack(pady=8, fill="x")
        
        done_btn = CustomButton(btn_frame, text="Done", 
                    command=lambda: self.update_status_and_close(appointment['appointment_id'], "Done", dialog),
                    width=150, height=45, font=("Arial", 11, "bold"),
                    fg_color="#10b981", hover_color="#059669")
        done_btn.pack(pady=8, fill="x")
    
    def update_status_and_close(self, appointment_id, new_status, dialog):
        """Update appointment status and close dialog"""
        try:
            update_query = "UPDATE appointments SET Status=%s WHERE appointment_id=%s"
            
            if self.db.execute(update_query, (new_status, appointment_id)):
                print(f"✓ Status updated to {new_status}")
                dialog.destroy()
                
                # If status is "Done", create billing record
                if new_status == "Done":
                    self.create_billing_record(appointment_id)
                
                self.load_schedules()
                
                # Notify appointment screen to refresh
                if self.on_appointment_update:
                    self.on_appointment_update()
            else:
                print("✗ Failed to update status")
                dialog.destroy()
        except Exception as e:
            print(f"✗ Error updating status: {e}")
            dialog.destroy()
    
    def create_billing_record(self, appointment_id):
        """Create billing record when appointment is marked Done"""
        try:
            # Get appointment details
            apt_query = "SELECT * FROM appointments WHERE appointment_id=%s"
            apt = self.db.fetch_one(apt_query, (appointment_id,))
            
            if apt:
                # Create billing record
                billing_query = """INSERT INTO billing (appointment_id, Name, Address, Dental_service, Service_fee, Total_fee, Payment_method, Status)
                                 VALUES (%s, %s, %s, %s, %s, %s, %s, 'Pending')"""
                
                self.db.execute(billing_query, (
                    appointment_id,
                    apt.get('Name'),
                    apt.get('Address'),
                    apt.get('Dental_service'),
                    apt.get('Service_fee'),
                    apt.get('Service_fee'),
                    None
                ))
                print(f"✓ Billing record created for appointment {appointment_id}")
        except Exception as e:
            print(f"✗ Error creating billing record: {e}")
    
    def get_frame(self):
        return self.frame
    
    def show(self):
        self.load_schedules()
        self.frame.pack(fill="both", expand=True)
        self.frame.tkraise()
    
    def hide(self):
        self.frame.pack_forget()
