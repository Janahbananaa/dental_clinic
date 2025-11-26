import customtkinter as ctk
from config import DB_CONFIG, APP_TITLE, APP_GEOMETRY, APP_THEME, APP_COLOR_THEME
from utils.database import DatabaseManager
from utils.migrations import DatabaseMigrations
from screens.login import LoginScreen
from screens.home import HomeScreen
from screens.patients import PatientsScreen
from screens.patient_records import PatientRecordsScreen
from screens.doctors import DoctorsScreen
from screens.appointments import AppointmentsScreen
from screens.dentist_schedule import DentistScheduleScreen
from screens.Dentists import DentistsScreen
from screens.billing import BillingScreen

ctk.set_appearance_mode(APP_THEME)
ctk.set_default_color_theme(APP_COLOR_THEME)


class DentalClinicApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(APP_GEOMETRY)

        self.db = DatabaseManager(**DB_CONFIG)
        if not self._initialize_database():
            return

        self.current_screen = None
        self.current_user = None
        self.login_screen = LoginScreen(self, self.db, self.on_login_success)
        self.home_screen = HomeScreen(self, self.on_logout, self.on_navigate)
        self.patients_screen = PatientsScreen(self, self.db, self.go_to_home)
        self.patient_records_screen = PatientRecordsScreen(self, self.db, self.go_to_home)
        self.doctors_screen = DoctorsScreen(self, self.db, self.go_to_home)
        self.appointments_screen = AppointmentsScreen(self, self.db, self.go_to_home, self.on_navigate)
        self.dentist_schedule_screen = DentistScheduleScreen(self, self.db, self.go_to_home, self.on_appointment_status_changed)
        self.dentists_screen = DentistsScreen(self, self.db, self.go_to_home)
        self.billing_screen = BillingScreen(self, self.db, self.go_to_home)

        self.show_login()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # -------------------------------
    # Database initialization
    # -------------------------------
    def _initialize_database(self) -> bool:
        """Initialize database with retry option on failure"""
        if self.db.connect():
            print("✓ Database connection successful")
            
            # Run migrations to update schema
            migrations = DatabaseMigrations()
            if not migrations.run_migrations():
                print("✗ Migration failed - some features may not work")
            
            return True
        
        # Connection failed, show error dialog
        print(f"✗ Database Error: Failed to connect to database")
        print(f"  Host: {DB_CONFIG.get('host')}")
        print(f"  Port: {DB_CONFIG.get('port')}")
        
        self.show_connection_error_dialog()
        return False

    def show_connection_error_dialog(self):
        """Show error dialog with retry option"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Database Connection Error")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        
        # Center dialog
        dialog.transient(self)
        dialog.grab_set()
        
        # Error message
        error_frame = ctk.CTkFrame(dialog)
        error_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        error_label = ctk.CTkLabel(
            error_frame,
            text="Unable to Connect to Database",
            font=("Arial", 14, "bold"),
            text_color="red"
        )
        error_label.pack(pady=10)
        
        details_label = ctk.CTkLabel(
            error_frame,
            text=f"Could not connect to MySQL server:\n\n"
                 f"Host: {DB_CONFIG.get('host')}\n"
                 f"Port: {DB_CONFIG.get('port')}\n\n"
                 f"Please ensure:\n"
                 f"• XAMPP MySQL is running\n"
                 f"• Database credentials are correct\n"
                 f"• Network connection is stable",
            font=("Arial", 11),
            justify="left"
        )
        details_label.pack(pady=10)
        
        # Button frame
        button_frame = ctk.CTkFrame(error_frame, fg_color="transparent")
        button_frame.pack(pady=15, fill="x")
        
        retry_btn = ctk.CTkButton(
            button_frame,
            text="Retry",
            command=lambda: self._retry_connection(dialog)
        )
        retry_btn.pack(side="left", padx=5, expand=True)
        
        exit_btn = ctk.CTkButton(
            button_frame,
            text="Exit",
            command=self.destroy,
            fg_color="red",
            hover_color="darkred"
        )
        exit_btn.pack(side="right", padx=5, expand=True)

    def _retry_connection(self, dialog):
        """Retry database connection"""
        dialog.destroy()
        if self.db.connect():
            print("✓ Database connection successful")
            # Reinitialize screens with successful connection
            self.login_screen = LoginScreen(self, self.db, self.on_login_success)
            self.home_screen = HomeScreen(self, self.on_logout, self.on_navigate)
            self.patients_screen = PatientsScreen(self, self.db, self.go_to_home)
            self.patient_records_screen = PatientRecordsScreen(self, self.db, self.go_to_home)
            self.doctors_screen = DoctorsScreen(self, self.db, self.go_to_home)
            self.appointments_screen = AppointmentsScreen(self, self.db, self.go_to_home, self.on_navigate)
            self.dentist_schedule_screen = DentistScheduleScreen(self, self.db, self.go_to_home, self.on_appointment_status_changed)
            self.dentists_screen = DentistsScreen(self, self.db, self.go_to_home)
            self.billing_screen = BillingScreen(self, self.db, self.go_to_home)
            self.show_login()
        else:
            self.show_connection_error_dialog()

    # -------------------------------
    # Screen management
    # -------------------------------
    def show_login(self):
        self._hide_current_screen()
        self.login_screen.show()
        self.current_screen = self.login_screen

    def on_login_success(self, user):
        self.current_user = user
        print(f"✓ Login successful for user: {user.username}")
        self.go_to_home()

    def go_to_home(self):
        self._hide_current_screen()
        if self.current_user:
            self.home_screen.set_user(self.current_user)
            self.home_screen.refresh()
        self.home_screen.show()
        self.current_screen = self.home_screen

    def on_navigate(self, screen_name: str):
        self._hide_current_screen()

        if screen_name == "patients":
            self.patients_screen.show()
            self.current_screen = self.patients_screen
        elif screen_name == "patient_records":
            self.patient_records_screen.show()
            self.current_screen = self.patient_records_screen
        elif screen_name == "doctors":
            self.doctors_screen.show()
            self.current_screen = self.doctors_screen
        elif screen_name == "appointments":
            self.appointments_screen.show()
            self.current_screen = self.appointments_screen
        elif screen_name == "appointments_today":
            self.appointments_screen.show_today()
            self.current_screen = self.appointments_screen
        elif screen_name == "dentist_schedule":
            self.dentist_schedule_screen.show()
            self.current_screen = self.dentist_schedule_screen
        elif screen_name == "dentists":
            self.dentists_screen.show()
            self.current_screen = self.dentists_screen
        elif screen_name == "billing":
            self.billing_screen.show()
            self.current_screen = self.billing_screen

    def on_logout(self):
        self.current_user = None
        self.show_login()

    def on_appointment_status_changed(self):
        """Called when appointment status changes in dentist schedule"""
        # Refresh the appointments screen if it's currently showing
        if self.current_screen == self.appointments_screen:
            if self.appointments_screen.is_today_view:
                self.appointments_screen.load_today_appointments()
            else:
                self.appointments_screen.load_appointments()

    def _hide_current_screen(self):
        if self.current_screen:
            self.current_screen.hide()

    # -------------------------------
    # Error handling
    # -------------------------------
    def show_error_and_exit(self, message: str):
        print(f"ERROR: {message}")
        self.destroy()

    # -------------------------------
    # App closing
    # -------------------------------
    def on_closing(self):
        self.db.disconnect()
        self.destroy()


if __name__ == "__main__":
    app = DentalClinicApp()
    app.mainloop()
