import customtkinter as ctk
from components.ui_components import CustomButton, CustomEntry
from models import User

class LoginScreen:
    def __init__(self, parent, db, on_login_success):
        self.parent = parent
        self.db = db
        self.on_login_success = on_login_success
        self.frame = ctk.CTkFrame(parent)
        self.show_password = False
        self.setup_ui()
    
    def setup_ui(self):
        # Main container with gradient-like background
        main_container = ctk.CTkFrame(self.frame, fg_color="#0f172a")
        main_container.pack(fill="both", expand=True)
        
        # Left side - Branding section
        left_section = ctk.CTkFrame(main_container, fg_color="#1e3a8a", width=400)
        left_section.pack(side="left", fill="both", expand=True)
        
        # Branding content
        brand_frame = ctk.CTkFrame(left_section, fg_color="#1e3a8a")
        brand_frame.pack(expand=True, padx=40, pady=40)
        
        # Logo/Icon placeholder
        logo_label = ctk.CTkLabel(brand_frame, text="🦷", font=("Arial", 80))
        logo_label.pack(pady=20)
        
        clinic_title = ctk.CTkLabel(brand_frame, text="Dental Clinic", 
                                    font=("Arial", 32, "bold"), text_color="#ffffff")
        clinic_title.pack(pady=10)
        
        clinic_subtitle = ctk.CTkLabel(brand_frame, text="Management System",
                                       font=("Arial", 16), text_color="#93c5fd")
        clinic_subtitle.pack(pady=5)
        
        divider = ctk.CTkLabel(brand_frame, text="━" * 25, text_color="#3b82f6")
        divider.pack(pady=20)
        
        tagline = ctk.CTkLabel(brand_frame, 
                              text="Professional dental management\nsolution for modern clinics",
                              font=("Arial", 12), text_color="#bfdbfe", justify="center")
        tagline.pack(pady=20)
        
        # Right side - Login form
        right_section = ctk.CTkFrame(main_container, fg_color="#0f172a")
        right_section.pack(side="right", fill="both", expand=True)
        
        # Login box
        login_container = ctk.CTkFrame(right_section, fg_color="#1e293b", corner_radius=15)
        login_container.pack(expand=True, padx=40, pady=40)
        
        # Form title
        form_title = ctk.CTkLabel(login_container, text="Sign In", 
                                 font=("Arial", 28, "bold"), text_color="#ffffff")
        form_title.pack(pady=(30, 10))
        
        form_subtitle = ctk.CTkLabel(login_container, text="Enter your credentials to access the system",
                                     font=("Arial", 11), text_color="#94a3b8")
        form_subtitle.pack(pady=(0, 30))
        
        # Username field with label
        username_label = ctk.CTkLabel(login_container, text="Username", 
                                      font=("Arial", 12, "bold"), text_color="#cbd5e1")
        username_label.pack(anchor="w", padx=30, pady=(0, 5))
        
        self.username_entry = CustomEntry(login_container, placeholder="Enter your username", 
                                         width=280, height=40, font=("Arial", 12))
        self.username_entry.pack(padx=30, pady=10)
        
        # Password field with label
        password_label = ctk.CTkLabel(login_container, text="Password", 
                                      font=("Arial", 12, "bold"), text_color="#cbd5e1")
        password_label.pack(anchor="w", padx=30, pady=(15, 5))
        
        self.password_entry = ctk.CTkEntry(login_container, placeholder_text="Enter your password", 
                                          width=280, height=40, font=("Arial", 12), show="•")
        self.password_entry.pack(padx=30, pady=10)
        
        # Show/Hide password checkbox
        show_password_frame = ctk.CTkFrame(login_container, fg_color="#1e293b")
        show_password_frame.pack(anchor="w", padx=30, pady=10)
        
        self.show_password_var = ctk.BooleanVar(value=False)
        show_password_check = ctk.CTkCheckBox(show_password_frame, text="Show password", 
                                             variable=self.show_password_var, 
                                             text_color="#94a3b8",
                                             command=self.toggle_password_visibility)
        show_password_check.pack(side="left")
        
        # Error message label
        self.error_label = ctk.CTkLabel(login_container, text="", text_color="#ef4444",
                                       font=("Arial", 11, "bold"))
        self.error_label.pack(pady=10)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(login_container, fg_color="#1e293b")
        buttons_frame.pack(pady=10)
        
        # Login button
        login_btn = CustomButton(buttons_frame, text="Sign In", command=self.handle_login,
                                width=130, height=45, font=("Arial", 13, "bold"),
                                fg_color="#3b82f6", hover_color="#2563eb")
        login_btn.pack(side="left", padx=10)
        
        # Refresh button
        refresh_btn = CustomButton(buttons_frame, text="Refresh", command=self.clear_fields,
                                   width=130, height=45, font=("Arial", 13, "bold"),
                                   fg_color="#6b7280", hover_color="#4b5563")
        refresh_btn.pack(side="left", padx=10)
        
        # Footer
        footer = ctk.CTkLabel(login_container, text="© 2024 Dental Clinic System. All rights reserved.",
                             font=("Arial", 9), text_color="#475569")
        footer.pack(pady=(20, 0))
    
    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="•")
    
    def clear_fields(self):
        """Clears the username, password, and error message (Refresh functionality)."""
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.error_label.configure(text="")
        self.show_password_var.set(False)
        self.toggle_password_visibility()
    
    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Validate input
        if not username or not password:
            self.error_label.configure(text="⚠ Username and password required")
            return
        
        # Authenticate against database
        user = User.authenticate(self.db, username, password)
        if user:
            self.error_label.configure(text="")
            self.on_login_success(user)
        else:
            self.error_label.configure(text="✗ Invalid username or password")
    
    def get_frame(self):
        return self.frame
    
    def show(self):
        self.frame.pack(fill="both", expand=True)
    
    def hide(self):
        self.frame.pack_forget()
