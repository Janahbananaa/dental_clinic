import customtkinter as ctk
from components.ui_components import CustomButton

class HomeScreen:
    def __init__(self, parent, on_logout, on_navigate):
        self.parent = parent
        self.on_logout = on_logout
        self.on_navigate = on_navigate
        self.current_user = None
        self.frame = ctk.CTkFrame(parent)
        self.header = None
        self.user_label = None
        self.content = None
        self.setup_ui()
    
    def setup_ui(self):
        # Create content frame
        self.content = ctk.CTkFrame(self.frame)
        self.content.pack(fill="both", expand=True, padx=0, pady=60)
    
    def refresh(self):
        # Destroy existing header if any
        if self.header:
            self.header.destroy()
        
        # Recreate header
        self.header = ctk.CTkFrame(self.frame, fg_color="#1e293b", height=70)
        self.header.pack(fill="x", padx=0, pady=0, side="top", before=self.content)
        
        # Header content frame
        header_content = ctk.CTkFrame(self.header, fg_color="#1e293b")
        header_content.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left side - Title
        left_header = ctk.CTkFrame(header_content, fg_color="#1e293b")
        left_header.pack(side="left", fill="y")
        
        clinic_icon = ctk.CTkLabel(left_header, text="🦷", font=("Arial", 24))
        clinic_icon.pack(side="left", padx=(0, 10))
        
        title_frame = ctk.CTkFrame(left_header, fg_color="#1e293b")
        title_frame.pack(side="left")
        
        title = ctk.CTkLabel(title_frame, text="Dental Clinic Management", 
                            font=("Arial", 16, "bold"), text_color="#ffffff")
        title.pack(anchor="w")
        
        # Right side - User info and logout
        right_header = ctk.CTkFrame(header_content, fg_color="#1e293b")
        right_header.pack(side="right", fill="y")
        
        self.user_label = ctk.CTkLabel(right_header, text="", font=("Arial", 11, "bold"), 
                                       text_color="#93c5fd")
        self.user_label.pack(side="left", padx=20)
        
        logout_btn = CustomButton(right_header, text="🚪 Logout", command=self.handle_logout,
                                 width=120, height=35, font=("Arial", 11, "bold"),
                                 fg_color="#ef4444", hover_color="#dc2626")
        logout_btn.pack(side="left", padx=10)
        
        # Update user label
        if self.current_user:
            self.user_label.configure(text=f"👤 {self.current_user.username}")
        
        # Clear and recreate content
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Main dashboard content
        main_content = ctk.CTkFrame(self.content, fg_color="transparent")
        main_content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title Section
        title_section = ctk.CTkFrame(main_content, fg_color="transparent")
        title_section.pack(fill="x", padx=20, pady=(0, 30))
        
        welcome_label = ctk.CTkLabel(title_section, text="Clinic Dashboard", 
                                    font=("Arial", 28, "bold"), text_color="#ffffff")
        welcome_label.pack(anchor="w")
        
        # Main Action Buttons Section (Large boxes)
        action_section = ctk.CTkFrame(main_content, fg_color="transparent")
        action_section.pack(fill="x", padx=20, pady=(0, 30))
        
        # Dentist Schedule Button
        dentist_btn_frame = ctk.CTkFrame(action_section, fg_color="#1e3a8a", corner_radius=15)
        dentist_btn_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        dentist_btn = ctk.CTkButton(dentist_btn_frame, text="👨‍⚕️\nDentist Schedule", 
                                    command=lambda: self.on_navigate("doctors"),
                                    font=("Arial", 16, "bold"), fg_color="#1e3a8a",
                                    hover_color="#1e40af", text_color="#ffffff",
                                    height=140)
        dentist_btn.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Appointment Today Button
        appt_btn_frame = ctk.CTkFrame(action_section, fg_color="#059669", corner_radius=15)
        appt_btn_frame.pack(side="left", fill="both", expand=True)
        
        appt_btn = ctk.CTkButton(appt_btn_frame, text="📅\nAppointment Today", 
                                command=lambda: self.on_navigate("appointments_today"),
                                font=("Arial", 16, "bold"), fg_color="#059669",
                                hover_color="#047857", text_color="#ffffff",
                                height=140)
        appt_btn.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Secondary Actions Section
        secondary_section = ctk.CTkFrame(main_content, fg_color="transparent")
        secondary_section.pack(fill="x", padx=20, pady=(0, 20))
        
        secondary_label = ctk.CTkLabel(secondary_section, text="Management", 
                                      font=("Arial", 14, "bold"), text_color="#cbd5e1")
        secondary_label.pack(anchor="w", pady=(0, 10))
        
        buttons_frame = ctk.CTkFrame(secondary_section, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        CustomButton(buttons_frame, text="📋 Appointments", 
                    command=lambda: self.on_navigate("appointments"),
                    width=150, height=50, font=("Arial", 12, "bold"),
                    fg_color="#3b82f6", hover_color="#2563eb").pack(side="left", padx=10)
        
        CustomButton(buttons_frame, text="💳 Billing", 
                    command=lambda: self.on_navigate("billing"),
                    width=150, height=50, font=("Arial", 12, "bold"),
                    fg_color="#f59e0b", hover_color="#d97706").pack(side="left", padx=10)
        
        CustomButton(buttons_frame, text="👥 Patient Records", 
                    command=lambda: self.on_navigate("patients"),
                    width=150, height=50, font=("Arial", 12, "bold"),
                    fg_color="#8b5cf6", hover_color="#7c3aed").pack(side="left", padx=10)
    
    def set_user(self, user):
        self.current_user = user
    
    def handle_logout(self):
        self.current_user = None
        self.on_logout()
    
    def get_frame(self):
        return self.frame
    
    def show(self):
        self.refresh()
        self.frame.pack(fill="both", expand=True)
        self.frame.tkraise()
    
    def hide(self):
        self.frame.pack_forget()
