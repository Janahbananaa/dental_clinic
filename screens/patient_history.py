import customtkinter as ctk
from components.ui_components import CustomButton
from models import PatientHistory

class PatientHistoryScreen:
    def __init__(self, parent, db, on_back):
        self.parent = parent
        self.db = db
        self.on_back = on_back
        self.frame = ctk.CTkFrame(parent)
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
        
        title = ctk.CTkLabel(header_content, text="📋 Patient History & Records",
                            font=("Arial", 18, "bold"), text_color="#ffffff")
        title.pack(side="left", padx=20)
        
        # Main content frame
        main_content = ctk.CTkFrame(self.frame, fg_color="transparent")
        main_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Search section
        search_frame = ctk.CTkFrame(main_content, fg_color="#1e293b", corner_radius=10)
        search_frame.pack(fill="x", pady=(0, 15))
        
        search_label = ctk.CTkLabel(search_frame, text="Search Patient ID:",
                                   font=("Arial", 11, "bold"), text_color="#ffffff")
        search_label.pack(side="left", padx=15, pady=10)
        
        self.search_entry = ctk.CTkEntry(search_frame, width=200, height=30, font=("Arial", 10),
                                        fg_color="#0f172a", border_color="#3b82f6", border_width=1)
        self.search_entry.pack(side="left", padx=5, pady=10)
        
        search_btn = CustomButton(search_frame, text="Search",
                                 command=self.search_history,
                                 width=80, height=30, font=("Arial", 10, "bold"),
                                 fg_color="#3b82f6", hover_color="#1d4ed8")
        search_btn.pack(side="left", padx=5, pady=10)
        
        all_btn = CustomButton(search_frame, text="Show All",
                              command=self.load_all_history,
                              width=80, height=30, font=("Arial", 10, "bold"),
                              fg_color="#6b7280", hover_color="#4b5563")
        all_btn.pack(side="left", padx=5, pady=10)
        
        # History table
        table_frame = ctk.CTkFrame(main_content, fg_color="#0f172a", corner_radius=5)
        table_frame.pack(fill="both", expand=True)
        
        self.history_table = ctk.CTkTextbox(table_frame, text_color="#e2e8f0",
                                           fg_color="#0f172a", border_color="#3b82f6",
                                           border_width=2, font=("Courier", 10))
        self.history_table.pack(fill="both", expand=True)
        self.history_table.configure(state="disabled")
        
        self.load_all_history()
    
    def load_all_history(self):
        history = PatientHistory.get_all(self.db)
        self.display_history(history)
    
    def search_history(self):
        try:
            patient_id = int(self.search_entry.get())
            history = PatientHistory.get_by_patient(self.db, patient_id)
            self.display_history(history)
        except ValueError:
            self.history_table.configure(state="normal")
            self.history_table.delete("1.0", "end")
            self.history_table.insert("end", "Invalid patient ID\n")
            self.history_table.configure(state="disabled")
    
    def display_history(self, history):
        self.history_table.configure(state="normal")
        self.history_table.delete("1.0", "end")
        
        if not history:
            self.history_table.insert("end", "No records found\n")
        else:
            header = f"{'ID':<6} {'Patient':<20} {'Date':<12} {'Time':<8} {'Fee':<10} {'Status':<12}\n"
            separator = "─" * 80 + "\n"
            
            self.history_table.insert("end", header)
            self.history_table.insert("end", separator)
            
            for record in history:
                patient = f"{record['first_name']} {record['last_name']}"[:20]
                date = record['appointment_date'] or "N/A"
                time = record['appointment_time'] or "N/A"
                fee = f"${record['total_fee']}" if record['total_fee'] else "N/A"
                
                row = f"{record['history_id']:<6} {patient:<20} {date:<12} {time:<8} {fee:<10} {record['status']:<12}\n"
                self.history_table.insert("end", row)
        
        self.history_table.configure(state="disabled")
    
    def get_frame(self):
        return self.frame
    
    def show(self):
        self.load_all_history()
        self.frame.pack(fill="both", expand=True)
        self.frame.tkraise()
    
    def hide(self):
        self.frame.pack_forget()
