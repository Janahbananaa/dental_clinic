import customtkinter as ctk
from components.ui_components import CustomButton

class DentistsScreen:
    def __init__(self, parent, db, on_back):
        self.parent = parent
        self.db = db
        self.on_back = on_back
        self.frame = ctk.CTkFrame(parent)
        self.current_dentist = None
        self.all_dentists = []
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
        
        title = ctk.CTkLabel(header_content, text="👨‍⚕️ Dentists Information", 
                            font=("Arial", 18, "bold"), text_color="#ffffff")
        title.pack(side="left", padx=20)
        
        # Main content
        main_content = ctk.CTkFrame(self.frame, fg_color="transparent")
        main_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Dentists list (full width)
        list_container = ctk.CTkFrame(main_content, fg_color="#1e293b", corner_radius=10)
        list_container.pack(fill="both", expand=True)
        
        list_title = ctk.CTkLabel(list_container, text="Dentists List", 
                                 font=("Arial", 14, "bold"), text_color="#ffffff")
        list_title.pack(pady=(15, 10), padx=15)
        
        table_frame = ctk.CTkFrame(list_container, fg_color="#0f172a")
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        self.dentists_table = ctk.CTkTextbox(table_frame, text_color="#e2e8f0", 
                                            fg_color="#0f172a", border_color="#3b82f6", 
                                            border_width=2, font=("Courier", 10))
        self.dentists_table.pack(fill="both", expand=True)
        self.dentists_table.configure(state="disabled")
        
        self.dentists_table.bind("<Button-1>", self.on_table_click)
        
        self.load_dentists()
    
    def load_dentists(self):
        """Load all dentists"""
        query = "SELECT * FROM doctors WHERE is_deleted=0 ORDER BY first_name"
        self.all_dentists = self.db.fetch_all(query)
        
        self.dentists_table.configure(state="normal")
        self.dentists_table.delete("1.0", "end")
        
        if not self.all_dentists:
            self.dentists_table.insert("end", "No dentists found\n")
        else:
            header = f"{'ID':<5} {'First Name':<20} {'Last Name':<20} {'License':<18} {'Specialization':<25} {'Experience':<12} {'Phone':<15}\n"
            separator = "─" * 130 + "\n"
            
            self.dentists_table.insert("end", header)
            self.dentists_table.insert("end", separator)
            
            for dentist in self.all_dentists:
                d_id = str(dentist.get('dentist_id', ''))
                first = (dentist.get('first_name', ''))[:20]
                last = (dentist.get('last_name', ''))[:20]
                license_num = (dentist.get('license_number', 'N/A'))[:18]
                spec = (dentist.get('specialization', 'N/A'))[:25]
                experience = str(dentist.get('years_experience', ''))[:12]
                phone = (dentist.get('phone', 'N/A'))[:15]
                
                row = f"{d_id:<5} {first:<20} {last:<20} {license_num:<18} {spec:<25} {experience:<12} {phone:<15}\n"
                self.dentists_table.insert("end", row)
        
        self.dentists_table.configure(state="disabled")
    
    def on_table_click(self, event):
        """Handle dentist selection"""
        try:
            index = self.dentists_table.index(f"@{event.x},{event.y}")
            line_num = int(index.split(".")[0])
            
            if line_num <= 2:
                return
            
            line_text = self.dentists_table.get(f"{line_num}.0", f"{line_num}.end").strip()
            
            if not line_text or line_text.startswith("─"):
                return
            
            try:
                dentist_id = int(line_text.split()[0])
                
                for dentist in self.all_dentists:
                    if dentist.get('dentist_id') == dentist_id:
                        self.show_dentist_details(dentist)
                        break
            except (ValueError, IndexError):
                pass
        except Exception as e:
            print(f"Error: {e}")
    
    def show_dentist_details(self, dentist):
        """Show dentist details in popup"""
        popup = ctk.CTkToplevel(self.parent)
        popup.title(f"Dentist: {dentist['first_name']} {dentist['last_name']}")
        popup.geometry("600x400")
        
        info_frame = ctk.CTkFrame(popup, fg_color="#1e293b", corner_radius=10)
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        dentist_name = f"{dentist['first_name']} {dentist['last_name']}"
        ctk.CTkLabel(info_frame, text=f"Dentist: {dentist_name}", 
                    font=("Arial", 16, "bold"), text_color="#ffffff").pack(anchor="w", padx=15, pady=10)
        
        details = f"""
License Number: {dentist.get('license_number', 'N/A')}
Specialization: {dentist.get('specialization', 'N/A')}
Years Experience: {dentist.get('years_experience', 'N/A')}
Phone: {dentist.get('phone', 'N/A')}
Email: {dentist.get('email', 'N/A')}
        """
        
        ctk.CTkLabel(info_frame, text=details, 
                    font=("Arial", 11), text_color="#cbd5e1", justify="left").pack(anchor="w", padx=15, pady=10)
    
    def get_frame(self):
        return self.frame
    
    def show(self):
        self.load_dentists()
        self.frame.pack(fill="both", expand=True)
        self.frame.tkraise()
    
    def hide(self):
        self.frame.pack_forget()
