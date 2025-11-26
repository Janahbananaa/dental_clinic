import customtkinter as ctk
from components.ui_components import CustomButton

class BillingScreen:
    def __init__(self, parent, db, on_back):
        self.parent = parent
        self.db = db
        self.on_back = on_back
        self.frame = ctk.CTkFrame(parent)
        self.current_billing = None
        self.all_billings = []
        self.setup_ui()
    
    def setup_ui(self):
        header = ctk.CTkFrame(self.frame, fg_color="#1e293b", height=70)
        header.pack(fill="x", padx=0, pady=0)
        
        header_content = ctk.CTkFrame(header, fg_color="#1e293b")
        header_content.pack(fill="both", expand=True, padx=20, pady=10)
        
        back_btn = CustomButton(header_content, text="← Back", command=self.on_back, 
                               width=100, height=35, font=("Arial", 11, "bold"))
        back_btn.pack(side="left", padx=10)
        
        title = ctk.CTkLabel(header_content, text="💳 Billing Management", 
                            font=("Arial", 18, "bold"), text_color="#ffffff")
        title.pack(side="left", padx=20)
        
        main_content = ctk.CTkFrame(self.frame, fg_color="transparent")
        main_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        form_container = ctk.CTkFrame(main_content, fg_color="#1e293b", corner_radius=10)
        form_container.pack(side="left", fill="both", padx=(0, 15), expand=True)
        
        form_title = ctk.CTkLabel(form_container, text="Create Billing", 
                                 font=("Arial", 13, "bold"), text_color="#ffffff")
        form_title.pack(pady=(15, 10), padx=15)
        
        form_scroll = ctk.CTkScrollableFrame(form_container, fg_color="#1e293b", width=300)
        form_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.form_fields = {}
        
        self._add_form_field(form_scroll, "Appointment ID", "appointment_id")
        self._add_form_field(form_scroll, "Patient Name", "name")
        self._add_form_field(form_scroll, "Dental Service", "dental_service")
        self._add_form_field(form_scroll, "Service Fee", "service_fee")
        self._add_form_field(form_scroll, "Total Fee", "total_fee")
        self._add_form_field(form_scroll, "Date/Time", "date_time")
        self._add_combobox_field(form_scroll, "Payment Method", "payment_method", 
                                ["", "Cash", "Online Payment", "GCash"])
        
        buttons_frame = ctk.CTkFrame(form_container, fg_color="#1e293b")
        buttons_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.create_btn = CustomButton(buttons_frame, text="Create", 
                                      command=self.add_billing,
                                      width=65, height=32, font=("Arial", 9, "bold"),
                                      fg_color="#10b981", hover_color="#059669")
        self.create_btn.pack(side="left", padx=3)
        
        self.complete_btn = CustomButton(buttons_frame, text="Complete", 
                                        command=self.complete_billing,
                                        width=65, height=32, font=("Arial", 9, "bold"),
                                        fg_color="#3b82f6", hover_color="#1d4ed8", state="disabled")
        self.complete_btn.pack(side="left", padx=3)
        
        self.clear_btn = CustomButton(buttons_frame, text="Clear", 
                                     command=self.clear_form,
                                     width=65, height=32, font=("Arial", 9, "bold"),
                                     fg_color="#6b7280", hover_color="#4b5563")
        self.clear_btn.pack(side="left", padx=3)
        
        self.status_label = ctk.CTkLabel(form_container, text="", font=("Arial", 9, "bold"))
        self.status_label.pack(pady=(0, 10))
        
        list_container = ctk.CTkFrame(main_content, fg_color="#1e293b", corner_radius=10)
        list_container.pack(side="right", fill="both", expand=True)
        
        list_title = ctk.CTkLabel(list_container, text="Pending Billing Records", 
                                 font=("Arial", 13, "bold"), text_color="#ffffff")
        list_title.pack(pady=(15, 10), padx=15)
        
        table_frame = ctk.CTkFrame(list_container, fg_color="#0f172a", corner_radius=5)
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.billings_table = ctk.CTkTextbox(table_frame, text_color="#e2e8f0", 
                                            fg_color="#0f172a", border_color="#3b82f6", 
                                            border_width=2, font=("Courier", 9))
        self.billings_table.pack(fill="both", expand=True)
        self.billings_table.configure(state="disabled")
        
        self.billings_table.bind("<Button-1>", self.on_table_click)
        
        self.load_billings()
    
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
    
    def load_billings(self):
        query = "SELECT * FROM billing WHERE Status='Pending' ORDER BY created_at DESC"
        self.all_billings = self.db.fetch_all(query)
        
        self.billings_table.configure(state="normal")
        self.billings_table.delete("1.0", "end")
        
        if not self.all_billings:
            self.billings_table.insert("end", "No pending billings\n")
        else:
            header = f"{'ID':<5} {'Name':<15} {'Service':<20} {'Total':<10} {'Payment':<12}\n"
            separator = "─" * 70 + "\n"
            
            self.billings_table.insert("end", header)
            self.billings_table.insert("end", separator)
            
            for bill in self.all_billings:
                bill_id = str(bill.get('billing_id', ''))
                name = (bill.get('Name', 'N/A'))[:15]
                service = (bill.get('Dental_service', 'N/A'))[:20]
                total = f"${bill.get('Total_fee', 0):.2f}"
                payment = bill.get('Payment_method', 'N/A')
                
                row = f"{bill_id:<5} {name:<15} {service:<20} {total:<10} {payment:<12}\n"
                self.billings_table.insert("end", row)
        
        self.billings_table.configure(state="disabled")
    
    def on_table_click(self, event):
        try:
            index = self.billings_table.index(f"@{event.x},{event.y}")
            line_num = int(index.split(".")[0])
            
            if line_num <= 2:
                return
            
            line_text = self.billings_table.get(f"{line_num}.0", f"{line_num}.end").strip()
            
            if not line_text or line_text.startswith("─"):
                return
            
            try:
                billing_id = int(line_text.split()[0])
                
                for bill in self.all_billings:
                    if bill.get('billing_id') == billing_id:
                        self.select_billing(bill)
                        break
            except (ValueError, IndexError):
                pass
        except Exception as e:
            print(f"Error on table click: {e}")
    
    def select_billing(self, billing):
        self.current_billing = billing
        
        self.form_fields['appointment_id'].delete(0, "end")
        self.form_fields['appointment_id'].insert(0, str(billing.get('appointment_id', '')))
        
        self.form_fields['name'].delete(0, "end")
        self.form_fields['name'].insert(0, billing.get('Name', ''))
        
        self.form_fields['dental_service'].delete(0, "end")
        self.form_fields['dental_service'].insert(0, billing.get('Dental_service', ''))
        
        self.form_fields['service_fee'].delete(0, "end")
        self.form_fields['service_fee'].insert(0, str(billing.get('Service_fee', '')))
        
        self.form_fields['total_fee'].delete(0, "end")
        self.form_fields['total_fee'].insert(0, str(billing.get('Total_fee', '')))
        
        self.form_fields['date_time'].delete(0, "end")
        self.form_fields['date_time'].insert(0, str(billing.get('Date/Time', '')))
        
        self.form_fields['payment_method'].set(billing.get('Payment_method', ''))
        
        self.create_btn.configure(state="disabled")
        self.complete_btn.configure(state="normal")
        
        self.status_label.configure(text=f"✏️ Billing ID: {billing.get('billing_id', '')}", 
                                   text_color="#3b82f6")
    
    def add_billing(self):
        try:
            appointment_id = int(self.form_fields['appointment_id'].get()) if self.form_fields['appointment_id'].get() else None
            name = self.form_fields['name'].get()
            dental_service = self.form_fields['dental_service'].get()
            service_fee = float(self.form_fields['service_fee'].get()) if self.form_fields['service_fee'].get() else 0.0
            total_fee = float(self.form_fields['total_fee'].get()) if self.form_fields['total_fee'].get() else 0.0
            date_time = self.form_fields['date_time'].get()
            payment_method = self.form_fields['payment_method'].get()
            
            if not all([appointment_id, name, dental_service, total_fee, payment_method]):
                self.status_label.configure(text="⚠ Required fields missing", text_color="#ef4444")
                return
            
            insert_query = """INSERT INTO billing (appointment_id, Name, Dental_service, Service_fee, Total_fee, `Date/Time`, Payment_method, Status)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, 'Pending')"""
            
            if self.db.execute(insert_query, (appointment_id, name, dental_service, service_fee, total_fee, date_time, payment_method)):
                self.status_label.configure(text="✓ Billing created", text_color="#10b981")
                self.clear_form()
                self.load_billings()
            else:
                self.status_label.configure(text="✗ Failed to create", text_color="#ef4444")
        except ValueError as e:
            self.status_label.configure(text=f"✗ Invalid input: {str(e)}", text_color="#ef4444")
    
    def complete_billing(self):
        if not self.current_billing:
            return
        
        try:
            billing_id = self.current_billing.get('billing_id')
            appointment_id = int(self.form_fields['appointment_id'].get())
            
            # Update billing status to Completed
            update_billing_query = "UPDATE billing SET Status='Completed' WHERE billing_id=%s"
            
            # Update appointment status to Done
            update_apt_query = "UPDATE appointments SET Status='Done' WHERE appointment_id=%s"
            
            if self.db.execute(update_billing_query, (billing_id,)) and self.db.execute(update_apt_query, (appointment_id,)):
                self.status_label.configure(text="✓ Billing completed", text_color="#10b981")
                self.clear_form()
                self.load_billings()
            else:
                self.status_label.configure(text="✗ Failed to complete", text_color="#ef4444")
        except ValueError as e:
            self.status_label.configure(text=f"✗ Invalid input: {str(e)}", text_color="#ef4444")
    
    def clear_form(self):
        for entry in self.form_fields.values():
            if hasattr(entry, 'delete'):
                entry.delete(0, "end")
            else:
                entry.set("")
        
        self.current_billing = None
        self.create_btn.configure(state="normal")
        self.complete_btn.configure(state="disabled")
        self.status_label.configure(text="")
    
    def get_frame(self):
        return self.frame
    
    def show(self):
        self.load_billings()
        self.frame.pack(fill="both", expand=True)
        self.frame.tkraise()
    
    def hide(self):
        self.frame.pack_forget()