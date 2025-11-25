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
        
        # Recreate header with better styling
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
        main_content.pack(fill="both", expand=True)
        
        # Welcome section
        welcome_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        welcome_frame.pack(fill="x", padx=30, pady=(20, 30))
        
        welcome_label = ctk.CTkLabel(welcome_frame, text="Dashboard", 
                                    font=("Arial", 28, "bold"), text_color="#ffffff")
        welcome_label.pack(anchor="w")
        
        welcome_desc = ctk.CTkLabel(welcome_frame, 
                                   text="Manage your dental clinic efficiently",
                                   font=("Arial", 12), text_color="#94a3b8")
        welcome_desc.pack(anchor="w", pady=(5, 0))
        
        # Stats section
        stats_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        stats_frame.pack(fill="x", padx=30, pady=(0, 30))
        
        self._create_stat_card(stats_frame, "👥", "Patients", "150", "#3b82f6")
        self._create_stat_card(stats_frame, "👨‍⚕️", "Doctors", "8", "#10b981")
        self._create_stat_card(stats_frame, "📅", "Appointments Today", "12", "#f59e0b")
        self._create_stat_card(stats_frame, "✅", "Completed", "45", "#8b5cf6")
        
        # Quick actions section
        actions_title = ctk.CTkLabel(main_content, text="Quick Actions", 
                                    font=("Arial", 16, "bold"), text_color="#ffffff")
        actions_title.pack(anchor="w", padx=30, pady=(20, 15))
        
        # Action buttons
        button_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        button_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        self._create_action_button(button_frame, "👥 Patients", "Manage patient records", 
                                  lambda: self.on_navigate("patients"), "#3b82f6")
        self._create_action_button(button_frame, "👨‍⚕️ Doctors", "Doctor information", 
                                  lambda: self.on_navigate("doctors"), "#10b981")
        self._create_action_button(button_frame, "📅 Appointments", "Schedule appointments", 
                                  lambda: self.on_navigate("appointments"), "#f59e0b")
    
    def _create_stat_card(self, parent, icon, title, value, color):
        card = ctk.CTkFrame(parent, fg_color="#1e293b", corner_radius=10)
        card.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        content = ctk.CTkFrame(card, fg_color="#1e293b")
        content.pack(fill="both", expand=True, padx=20, pady=15)
        
        icon_label = ctk.CTkLabel(content, text=icon, font=("Arial", 32))
        icon_label.pack()
        
        title_label = ctk.CTkLabel(content, text=title, font=("Arial", 11), text_color="#94a3b8")
        title_label.pack(pady=(10, 5))
        
        value_label = ctk.CTkLabel(content, text=value, font=("Arial", 20, "bold"), text_color=color)
        value_label.pack()
    
    def _create_action_button(self, parent, title, description, command, color):
        btn_frame = ctk.CTkFrame(parent, fg_color="#1e293b", corner_radius=10)
        btn_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        # Create button with hover effect
        btn = CustomButton(btn_frame, text=f"{title}\n{description}", 
                          command=command, font=("Arial", 12, "bold"),
                          fg_color=color, hover_color=self._darken_color(color),
                          width=200, height=80, text_color="#ffffff")
        btn.pack(fill="both", expand=True, padx=1, pady=1)
    
    def _darken_color(self, color):
        # Simple color darkening for hover effect
        color_map = {
            "#3b82f6": "#1d4ed8",
            "#10b981": "#059669",
            "#f59e0b": "#d97706"
        }
        return color_map.get(color, color)
    
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
