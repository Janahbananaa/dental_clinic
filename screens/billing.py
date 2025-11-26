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
        
        # Left side - Billing details form
        form_container = ctk.CTkFrame(main_content, fg_color="#1e293b", corner_radius=10)
        form_container.pack(side="left", fill="both", padx=(0, 15), expand=False)
        
        form_title = ctk.CTkLabel(form_container, text="Billing Details", 
                                 font=("Arial", 13, "bold"), text_color="#ffffff")
        form_title.pack(pady=(15, 10), padx=15)
        
        form_scroll = ctk.CTkScrollableFrame(form_container, fg_color="#1e293b", width=300)
        form_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.form_fields = {}
        
        self._add_form_field(form_scroll, "Patient Name", "name")
        self._add_form_field(form_scroll, "Address", "address")
        self._add_form_field(form_scroll, "Service", "service")
        self._add_form_field(form_scroll, "Service Fee", "service_fee")
        self._add_form_field(form_scroll, "Purchase", "purchase")
        self._add_form_field(form_scroll, "Total Amount", "total_amount")

        # Payment Mode Section
        payment_label = ctk.CTkLabel(form_scroll, text="Payment Mode", font=("Arial", 10, "bold"), 
                                    text_color="#cbd5e1")
        payment_label.pack(anchor="w", padx=0, pady=(10, 5))
        
        payment_frame = ctk.CTkFrame(form_scroll, fg_color="transparent")
        payment_frame.pack(anchor="w", padx=0, pady=(0, 10))
        
        self.cash_var = ctk.BooleanVar()
        self.online_var = ctk.BooleanVar()
        
        cash_check = ctk.CTkCheckBox(payment_frame, text="💵 Cash", variable=self.cash_var,
                                     onvalue=True, offvalue=False, font=("Arial", 10),
                                     text_color="#cbd5e1")
        cash_check.pack(anchor="w", pady=3)
        
        online_check = ctk.CTkCheckBox(payment_frame, text="🌐 Online Payment", variable=self.online_var,
                                       onvalue=True, offvalue=False, font=("Arial", 10),
                                       text_color="#cbd5e1")
        online_check.pack(anchor="w", pady=3)
        
        buttons_frame = ctk.CTkFrame(form_container, fg_color="#1e293b")
        buttons_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.update_btn = CustomButton(buttons_frame, text="Update", 
                                      command=self.update_billing_info,
                                      width=70, height=32, font=("Arial", 9, "bold"),
                                      fg_color="#8b5cf6", hover_color="#7c3aed", state="disabled")
        self.update_btn.pack(side="left", padx=2)
        
        self.complete_btn = CustomButton(buttons_frame, text="Complete", 
                                        command=self.complete_billing,
                                        width=70, height=32, font=("Arial", 9, "bold"),
                                        fg_color="#3b82f6", hover_color="#1d4ed8", state="disabled")
        self.complete_btn.pack(side="left", padx=2)
        
        self.clear_btn = CustomButton(buttons_frame, text="Clear", 
                                     command=self.clear_form,
                                     width=70, height=32, font=("Arial", 9, "bold"),
                                     fg_color="#6b7280", hover_color="#4b5563")
        self.clear_btn.pack(side="left", padx=2)
        
        self.status_label = ctk.CTkLabel(form_container, text="", font=("Arial", 9, "bold"))
        self.status_label.pack(pady=(0, 10))
        
        # Right side - Billing list
        list_container = ctk.CTkFrame(main_content, fg_color="#1e293b", corner_radius=10)
        list_container.pack(side="right", fill="both", expand=True)
        
        list_title = ctk.CTkLabel(list_container, text="Pending Billing Records", 
                                 font=("Arial", 13, "bold"), text_color="#ffffff")
        list_title.pack(pady=(15, 10), padx=15)
        
        table_frame = ctk.CTkFrame(list_container, fg_color="#0f172a", corner_radius=5)
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.billings_table = ctk.CTkTextbox(table_frame, text_color="#e2e8f0", 
                                            fg_color="#0f172a", border_color="#3b82f6", 
                                            border_width=2, font=("Courier", 10))
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
    
    def load_billings(self):
        query = "SELECT * FROM billing WHERE Status='Pending' ORDER BY created_at DESC"
        self.all_billings = self.db.fetch_all(query)
        
        self.billings_table.configure(state="normal")
        self.billings_table.delete("1.0", "end")
        
        if not self.all_billings:
            self.billings_table.insert("end", "No pending billings\n")
        else:
            header = f"{'ID':<5} {'Name':<12} {'Service':<16} {'Fee':<10} {'Purchase':<10} {'Total':<10} {'Payment':<10} {'Status':<10}\n"
            separator = "─" * 105 + "\n"
            
            self.billings_table.insert("end", header)
            self.billings_table.insert("end", separator)
            
            for bill in self.all_billings:
                bill_id = str(bill.get('billing_id', ''))
                name = (bill.get('Name') or 'N/A')[:12]
                service = (bill.get('Dental_service') or 'N/A')[:16]
                fee = f"${bill.get('Total_fee', 0):.2f}"[:10]
                purchase = f"${bill.get('Purchase', 0):.2f}"[:10] if bill.get('Purchase') else "$0.00"[:10]
                total = f"${bill.get('Total_amount', 0):.2f}"[:10] if bill.get('Total_amount') else "$0.00"[:10]
                payment = (bill.get('Payment_method') or 'N/A')[:10]
                status = bill.get('Status', 'Pending')
                
                row = f"{bill_id:<5} {name:<12} {service:<16} {fee:<10} {purchase:<10} {total:<10} {payment:<10} {status:<10}\n"
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
        self.update_btn.configure(state="normal")
        self.complete_btn.configure(state="normal")
        
        self.form_fields['name'].delete(0, "end")
        self.form_fields['name'].insert(0, billing.get('Name', ''))
        
        self.form_fields['address'].delete(0, "end")
        self.form_fields['address'].insert(0, billing.get('Address', ''))
        
        self.form_fields['service'].delete(0, "end")
        self.form_fields['service'].insert(0, billing.get('Dental_service', ''))
        
        self.form_fields['service_fee'].delete(0, "end")
        self.form_fields['service_fee'].insert(0, f"${billing.get('Total_fee', 0):.2f}")
        
        self.form_fields['purchase'].delete(0, "end")
        self.form_fields['purchase'].insert(0, f"${billing.get('Purchase', 0):.2f}" if billing.get('Purchase') else "$0.00")
        
        self.form_fields['total_amount'].delete(0, "end")
        self.form_fields['total_amount'].insert(0, f"${billing.get('Total_amount', 0):.2f}" if billing.get('Total_amount') else "$0.00")
        
        payment = billing.get('Payment_method', '')
        self.cash_var.set('Cash' in payment if payment else False)
        self.online_var.set('Online' in payment if payment else False)
        
        self.status_label.configure(text=f"✏️ Billing ID: {billing.get('billing_id', '')}", 
                                   text_color="#3b82f6")

    def update_billing_info(self):
        """Update billing information"""
        if not self.current_billing:
            self.status_label.configure(text="⚠ No billing selected", text_color="#ef4444")
            return
        
        try:
            billing_id = self.current_billing.get('billing_id')
            purchase = self.form_fields['purchase'].get().replace('$', '')
            total_amount = self.form_fields['total_amount'].get().replace('$', '')
            
            # Build payment method
            payment_methods = []
            if self.cash_var.get():
                payment_methods.append('Cash')
            if self.online_var.get():
                payment_methods.append('Online')
            
            payment_method = ', '.join(payment_methods) if payment_methods else None
            
            purchase_amount = float(purchase) if purchase else 0.0
            total = float(total_amount) if total_amount else 0.0
            
            update_query = "UPDATE billing SET Purchase=%s, Total_amount=%s, Payment_method=%s WHERE billing_id=%s"
            
            if self.db.execute(update_query, (purchase_amount, total, payment_method, billing_id)):
                self.status_label.configure(text="✓ Billing info updated", text_color="#10b981")
                self.load_billings()
            else:
                self.status_label.configure(text="✗ Failed to update", text_color="#ef4444")
        except Exception as e:
            self.status_label.configure(text=f"✗ Error: {str(e)}", text_color="#ef4444")
    
    def complete_billing(self):
        """Complete billing and mark appointment as Done"""
        if not self.current_billing:
            return
        
        try:
            billing_id = self.current_billing.get('billing_id')
            appointment_id = self.current_billing.get('appointment_id')
            
            update_billing_query = "UPDATE billing SET Status='Completed' WHERE billing_id=%s"
            update_apt_query = "UPDATE appointments SET Status='Done' WHERE appointment_id=%s"
            
            if self.db.execute(update_billing_query, (billing_id,)) and self.db.execute(update_apt_query, (appointment_id,)):
                self.status_label.configure(text="✓ Billing completed", text_color="#10b981")
                self.clear_form()
                self.load_billings()
            else:
                self.status_label.configure(text="✗ Failed to complete", text_color="#ef4444")
        except Exception as e:
            self.status_label.configure(text=f"✗ Error: {str(e)}", text_color="#ef4444")
    
    def clear_form(self):
        for field in self.form_fields.values():
            field.delete(0, "end")
        
        self.cash_var.set(False)
        self.online_var.set(False)
        self.current_billing = None
        self.update_btn.configure(state="disabled")
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