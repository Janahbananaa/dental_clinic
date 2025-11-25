import customtkinter as ctk
from tkinter import ttk, messagebox
from components.ui_components import CustomButton
from models import Patient


class PatientsScreen:
    def __init__(self, parent, db, on_back):
        self.parent = parent
        self.db = db  # Use existing DB connection
        self.on_back = on_back
        self.frame = ctk.CTkFrame(parent)
        self.current_patient = None
        self.all_patients = []
        self.setup_ui()
    
    def setup_ui(self):
        # ---------------- HEADER ----------------
        header = ctk.CTkFrame(self.frame, fg_color="#1e293b", height=70)
        header.pack(fill="x", padx=0, pady=0)
        
        header_content = ctk.CTkFrame(header, fg_color="#1e293b")
        header_content.pack(fill="both", expand=True, padx=20, pady=10)
        
        back_btn = CustomButton(header_content, text="← Back", command=self.on_back, 
                               width=100, height=35, font=("Arial", 11, "bold"))
        back_btn.pack(side="left", padx=10)
        
        title = ctk.CTkLabel(header_content, text="👥 Patients Management", 
                            font=("Arial", 18, "bold"), text_color="#ffffff")
        title.pack(side="left", padx=20)
        
        # ---------------- MAIN CONTENT ----------------
        main_content = ctk.CTkFrame(self.frame, fg_color="transparent")
        main_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # -------- LEFT: FORM --------
        form_container = ctk.CTkFrame(main_content, fg_color="#1e293b", corner_radius=10)
        form_container.pack(side="left", fill="both", padx=(0, 15))
        
        form_title = ctk.CTkLabel(form_container, text="Patient Details", 
                                 font=("Arial", 13, "bold"), text_color="#ffffff")
        form_title.pack(pady=(15, 10), padx=15)
        
        form_scroll = ctk.CTkScrollableFrame(form_container, fg_color="#1e293b", width=300)
        form_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.form_fields = {}
        self._add_form_field(form_scroll, "First Name", "first_name")
        self._add_form_field(form_scroll, "Last Name", "last_name")
        self._add_form_field(form_scroll, "Phone", "phone")
        self._add_form_field(form_scroll, "Address", "address")
        self._add_form_field(form_scroll, "Age", "age")
        self._add_form_field(form_scroll, "Birth Date (YYYY-MM-DD)", "birth_date")
        self._add_combobox_field(form_scroll, "Gender", "gender", ["", "Male", "Female"])
        self._add_combobox_field(form_scroll, "Patient Type", "patient_type", ["", "Adult", "Child"])
        
        # Buttons
        buttons_frame = ctk.CTkFrame(form_container, fg_color="#1e293b")
        buttons_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.add_btn = CustomButton(buttons_frame, text="Add", command=self.add_patient,
                                   width=65, height=32, font=("Arial", 9, "bold"),
                                   fg_color="#10b981", hover_color="#059669")
        self.add_btn.pack(side="left", padx=3)
        
        self.update_btn = CustomButton(buttons_frame, text="Update", command=self.update_patient,
                                      width=65, height=32, font=("Arial", 9, "bold"),
                                      fg_color="#3b82f6", hover_color="#1d4ed8", state="disabled")
        self.update_btn.pack(side="left", padx=3)
        
        self.delete_btn = CustomButton(buttons_frame, text="Delete", command=self.delete_patient,
                                      width=65, height=32, font=("Arial", 9, "bold"),
                                      fg_color="#ef4444", hover_color="#dc2626", state="disabled")
        self.delete_btn.pack(side="left", padx=3)
        
        self.clear_btn = CustomButton(buttons_frame, text="Clear", command=self.clear_form,
                                     width=65, height=32, font=("Arial", 9, "bold"),
                                     fg_color="#6b7280", hover_color="#4b5563")
        self.clear_btn.pack(side="left", padx=3)

        # ⭐ NEW BUTTON — PATIENT HISTORY
        self.history_btn = CustomButton(buttons_frame, text="History", command=self.show_patient_history,
                                     width=65, height=32, font=("Arial", 9, "bold"),
                                     fg_color="#8b5cf6", hover_color="#7c3aed")
        self.history_btn.pack(side="left", padx=3)

        self.status_label = ctk.CTkLabel(form_container, text="", font=("Arial", 9, "bold"))
        self.status_label.pack(pady=(0, 10))
        
        # -------- RIGHT: TABLE --------
        list_container = ctk.CTkFrame(main_content, fg_color="#1e293b", corner_radius=10)
        list_container.pack(side="right", fill="both", expand=True)
        
        list_title = ctk.CTkLabel(list_container, text="Patient Records", 
                                 font=("Arial", 13, "bold"), text_color="#ffffff")
        list_title.pack(pady=(15, 10), padx=15)
        
        table_frame = ctk.CTkFrame(list_container, fg_color="#0f172a", corner_radius=5)
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Treeview table
        columns = ("ID", "First Name", "Last Name", "Phone", "Address", "Age", "Type")
        self.patients_table = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        self.patients_table.pack(fill="both", expand=True, side="left")
        
        # Scrollbars
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.patients_table.yview)
        scrollbar_y.pack(side="right", fill="y")
        self.patients_table.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ttk.Scrollbar(list_container, orient="horizontal", command=self.patients_table.xview)
        scrollbar_x.pack(fill="x")
        self.patients_table.configure(xscrollcommand=scrollbar_x.set)
        
        # Headings and column widths
        for col in columns:
            self.patients_table.heading(col, text=col)
            self.patients_table.column(col, width=120, anchor="center")
        
        # Style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#0f172a",
                        foreground="#e2e8f0",
                        rowheight=30,
                        fieldbackground="#0f172a",
                        font=("Arial", 11))
        style.map("Treeview",
                  background=[("selected", "#3b82f6")],
                  foreground=[("selected", "#ffffff")])
        style.configure("Treeview.Heading",
                        background="#1e293b",
                        foreground="#ffffff",
                        font=("Arial", 12, "bold"))
        style.configure("Treeview", bordercolor="#3b82f6", borderwidth=2)
        
        self.patients_table.bind("<<TreeviewSelect>>", self.on_table_select)
        
        self.load_patients()
    
    # ---------------- FORM HELPERS ----------------
    def _add_form_field(self, parent, label_text, field_key):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 9, "bold"), 
                            text_color="#cbd5e1")
        label.pack(anchor="w", pady=(8, 2))
        
        entry = ctk.CTkEntry(parent, width=250, height=30, font=("Arial", 9),
                            fg_color="#0f172a", border_color="#3b82f6", border_width=1)
        entry.pack(pady=(0, 8), fill="x")
        
        self.form_fields[field_key] = entry
    
    def _add_combobox_field(self, parent, label_text, field_key, values):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 9, "bold"), 
                            text_color="#cbd5e1")
        label.pack(anchor="w", pady=(8, 2))
        
        combo = ctk.CTkComboBox(parent, values=values, width=250, height=30, 
                               font=("Arial", 9),
                               fg_color="#0f172a",
                               border_color="#3b82f6", border_width=1)
        combo.pack(pady=(0, 8), fill="x")
        
        self.form_fields[field_key] = combo

    # ---------------- TABLE ----------------
    def load_patients(self):
        self.all_patients = Patient.get_all(self.db)
        self.patients_table.delete(*self.patients_table.get_children())

        for p in self.all_patients:
            age_str = str(p["age"]) if p["age"] is not None else ""
            self.patients_table.insert("", "end", iid=p["patient_id"], values=(
                p["patient_id"],
                p["first_name"] or "",
                p["last_name"] or "",
                p["phone"] or "",
                p["address"] or "",
                age_str,
                p["patient_type"] or ""
            ))
    
    def on_table_select(self, event):
        selected = self.patients_table.selection()
        if not selected:
            return
        patient_id = int(selected[0])
        for p in self.all_patients:
            if p["patient_id"] == patient_id:
                self.select_patient(p)
                return
    
    # ---------------- SELECTION AND CRUD ----------------
    def select_patient(self, patient):
        self.current_patient = patient
        for key in ["first_name", "last_name", "phone", "address", "age", "birth_date"]:
            self.form_fields[key].delete(0, "end")
            self.form_fields[key].insert(0, patient.get(key, "") or "")
        self.form_fields["gender"].set(patient.get("gender", ""))
        self.form_fields["patient_type"].set(patient.get("patient_type", ""))
        self.add_btn.configure(state="disabled")
        self.update_btn.configure(state="normal")
        self.delete_btn.configure(state="normal")
        self.status_label.configure(text=f"✏️ {patient['first_name']} {patient['last_name']}", text_color="#3b82f6")
    
    def add_patient(self):
        data = {k: f.get() for k, f in self.form_fields.items()}
        if not data["first_name"] or not data["last_name"]:
            self.status_label.configure(text="⚠ Name fields required", text_color="#ef4444")
            return
        try:
            patient = Patient(self.db, **{
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "phone": data["phone"],
                "address": data["address"],
                "age": int(data["age"]) if data["age"] else None,
                "birth_date": data["birth_date"],
                "gender": data["gender"],
                "patient_type": data["patient_type"],
            })
            if patient.save():
                self.status_label.configure(text="✓ Patient added", text_color="#10b981")
                self.clear_form()
                self.load_patients()
            else:
                self.status_label.configure(text="✗ Failed to add", text_color="#ef4444")
        except:
            self.status_label.configure(text="✗ Invalid age", text_color="#ef4444")
    
    def update_patient(self):
        if not self.current_patient:
            return
        data = {k: f.get() for k, f in self.form_fields.items()}
        if not data["first_name"] or not data["last_name"]:
            self.status_label.configure(text="⚠ Name fields required", text_color="#ef4444")
            return
        try:
            patient = Patient(self.db, **{
                "patient_id": self.current_patient["patient_id"],
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "phone": data["phone"],
                "address": data["address"],
                "age": int(data["age"]) if data["age"] else None,
                "birth_date": data["birth_date"],
                "gender": data["gender"],
                "patient_type": data["patient_type"],
            })
            if patient.save():
                self.status_label.configure(text="✓ Patient updated", text_color="#10b981")
                self.clear_form()
                self.load_patients()
            else:
                self.status_label.configure(text="✗ Failed to update", text_color="#ef4444")
        except:
            self.status_label.configure(text="✗ Invalid age", text_color="#ef4444")
    
    def delete_patient(self):
        if not self.current_patient:
            return

        # -------------------------
        # ⭐ MOVE TO HISTORY TABLE
        # -------------------------
        data = self.current_patient
        insert_query = """
            INSERT INTO `Patient's_History`
            (Name, Age, Address, Contact, Type, Gender)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.db.execute_query(insert_query, (
            f"{data['first_name']} {data['last_name']}",
            data["age"],
            data["address"],
            data["phone"],
            data["patient_type"],
            data["gender"]
        ))

        # Delete from main table
        patient = Patient(self.db, patient_id=self.current_patient["patient_id"])
        if patient.delete():
            self.status_label.configure(text="✓ Patient moved to history", text_color="#10b981")
            self.clear_form()
            self.load_patients()
        else:
            self.status_label.configure(text="✗ Failed to delete", text_color="#ef4444")
    
    # ------------------------------
    # ⭐ PATIENT HISTORY POPUP
    # ------------------------------
    def show_patient_history(self):
        history_window = ctk.CTkToplevel()
        history_window.title("Patient History")
        history_window.geometry("900x500")

        table_frame = ctk.CTkFrame(history_window)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("Name", "Age", "Address", "Contact", "Type", "Gender")
        table = ttk.Treeview(table_frame, columns=columns, show="headings")
        table.pack(fill="both", expand=True)

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=120, anchor="center")

        # Load history from DB
        rows = self.db.fetch_all("SELECT * FROM `Patient's_History`")

        for r in rows:
            table.insert("", "end", values=(
                r["Name"], r["Age"], r["Address"], r["Contact"], r["Type"], r["Gender"]
            ))

    # ---------------------------------------------------

    def clear_form(self):
        for field in self.form_fields.values():
            try:
                field.delete(0, "end")
            except:
                field.set("")
        self.current_patient = None
        self.add_btn.configure(state="normal")
        self.update_btn.configure(state="disabled")
        self.delete_btn.configure(state="disabled")
        self.status_label.configure(text="")
    
    def get_frame(self):
        return self.frame
    
    def show(self):
        self.load_patients()
        self.frame.pack(fill="both", expand=True)
        self.frame.tkraise()
    
    def hide(self):
        self.frame.pack_forget()

