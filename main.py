import customtkinter as ctk
from config import DB_CONFIG, APP_TITLE, APP_GEOMETRY, APP_THEME, APP_COLOR_THEME
from utils.database import DatabaseManager

from screens.login import LoginScreen
from screens.dashboard import DashboardScreen
from screens.patients import PatientsScreen
from screens.doctors import DoctorsScreen

ctk.set_appearance_mode(APP_THEME)
ctk.set_default_color_theme(APP_COLOR_THEME)


class DentalClinicApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)
        
        self.db = DatabaseManager(**DB_CONFIG)
        if not self.db.connect():
            self.show_error_and_exit("Failed to connect to database")
            return
        
        self.current_screen = None
        self.current_user = None
        
        self.login_screen = LoginScreen(self, self.db, self.on_login_success)
        self.dashboard_screen = DashboardScreen(self, self.on_logout, self.on_navigate)
        self.patients_screen = PatientsScreen(self, self.db, self.go_to_dashboard)
        self.doctors_screen = DoctorsScreen(self, self.db, self.go_to_dashboard)
        
        self.show_login()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    

    def show_login(self):
        self._hide_current_screen()
        self.login_screen.show()
        self.current_screen = self.login_screen
    
    def on_login_success(self, user):
        self.current_user = user
        print(f"✓ Login successful for user: {user.username}")
        self.go_to_dashboard()
    
    def go_to_dashboard(self):
        self._hide_current_screen()
        if self.current_user:
            self.dashboard_screen.set_user(self.current_user)
            
        self.dashboard_screen.show()
        self.current_screen = self.dashboard_screen
    
    def on_navigate(self, screen_name: str):
        self._hide_current_screen()
        
        if screen_name == "patients":
            self.patients_screen.show()
            self.current_screen = self.patients_screen
        
        elif screen_name == "doctors": 
            self.doctors_screen.show()
            self.current_screen = self.doctors_screen
        
        elif screen_name == "appointments":
            print("Appointments screen - TODO")
            # Add appointments 
    
    def on_logout(self):
        self.current_user = None
        self.show_login()
    
    def _hide_current_screen(self):
        if self.current_screen:
            self.current_screen.hide()

    def show_error_and_exit(self, message: str):
        print(f"ERROR: {message}")
        self.destroy()
    
    def on_closing(self):
        self.db.disconnect()
        self.destroy()


if __name__ == "__main__":
    app = DentalClinicApp()
    app.mainloop()
