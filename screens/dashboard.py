import customtkinter as ctk
from components.ui_components import CustomButton
import datetime

from screens.doctors import DoctorsScreen
from screens.patients import PatientsScreen
from screens.appointments import AppointmentsScreen

class DashboardScreen:
    def __init__(self, parent, on_logout, on_navigate, db):
        self.parent = parent
        self.on_logout = on_logout
        self.on_navigate = on_navigate
        self.current_user = None
        self.db = db  # Database manager

        self.frame = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        self.setup_ui()

        # Initialize screens
        self.patients_screen = PatientsScreen(parent, self.db, self.show_main_dashboard)
        self.doctors_screen = DoctorsScreen(parent, self.db, self.show_main_dashboard)
        self.appointments_screen = AppointmentsScreen(parent, self.db, self.show_main_dashboard)

    # -------------------------------
    # UI
    # -------------------------------
    def setup_ui(self):
        # Header
        header = ctk.CTkFrame(self.frame, fg_color="#111111", height=60)
        header.pack(fill="x")

        title = ctk.CTkLabel(header, text="Dashboard", font=("Arial", 18, "bold"))
        title.pack(side="left", padx=20, pady=10)

        self.user_info_label = ctk.CTkLabel(header, text="", font=("Arial", 12))
        self.user_info_label.pack(side="left", padx=20, pady=10)

        logout_btn = CustomButton(header, text="Logout",
                                  command=self.handle_logout,
                                  width=100, height=30)
        logout_btn.pack(side="right", padx=20, pady=10)

        # Main content
        content = ctk.CTkFrame(self.frame, fg_color="#1a1a1a")
        content.pack(fill="both", expand=True, padx=20, pady=20)

        cards_frame = ctk.CTkFrame(content, fg_color="#1a1a1a")
        cards_frame.pack(pady=20, fill="x")
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)

        card_color = "#2563eb"

        # Dentist schedule button (placeholder)
        CustomButton(
            cards_frame,
            text="Dentist's Schedule",
            command=self.show_dentist_schedule,
            width=280, height=160,
            font=("Arial", 18, "bold"),
            fg_color=card_color,
            hover_color="#1e40af",
            corner_radius=15
        ).grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        # Appointments today button
        self.appt_count_label = ctk.CTkLabel(cards_frame, text="0",
                                             font=("Arial", 28, "bold"))

        appt_btn = CustomButton(
            cards_frame,
            text="Appointments Today",
            command=self.show_appointments_today,
            width=280, height=160,
            font=("Arial", 18, "bold"),
            fg_color=card_color,
            hover_color="#1e40af",
            corner_radius=15
        )
        appt_btn.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
        self.appt_count_label.place(in_=appt_btn, relx=0.5, rely=0.6, anchor="center")

        # Navigation buttons
        button_frame = ctk.CTkFrame(content, fg_color="#1a1a1a")
        button_frame.pack(fill="x", pady=20)

        CustomButton(button_frame, text="📋 Patients Record",
                     command=self.show_patients_screen,
                     width=180, height=60).pack(side="left", padx=20)

        CustomButton(button_frame, text="👨‍⚕️ Doctors",
                     command=self.show_doctors_screen,
                     width=180, height=60).pack(side="left", padx=20)

        CustomButton(button_frame, text="📅 Appointments",
                     command=self.show_appointments_screen,
                     width=180, height=60).pack(side="left", padx=20)

        self.update_appointments_today()

    # -------------------------------
    # Placeholder methods
    # -------------------------------
    def show_dentist_schedule(self):
        print("Dentist's Schedule button clicked - placeholder")

    def show_appointments_today(self):
        print("Appointments Today button clicked - placeholder")

    # -------------------------------
    # Navigation
    # -------------------------------
    def show_patients_screen(self):
        self.hide_all_screens()
        self.patients_screen.show()

    def show_doctors_screen(self):
        self.hide_all_screens()
        self.doctors_screen.show()

    def show_appointments_screen(self):
        self.hide_all_screens()
        self.appointments_screen.show()

    def show_main_dashboard(self):
        self.hide_all_screens()
        self.show()

    def hide_all_screens(self):
        self.patients_screen.hide()
        self.doctors_screen.hide()
        self.appointments_screen.hide()
        self.hide()

    # -------------------------------
    # Appointments
    # -------------------------------
    def update_appointments_today(self):
        try:
            count = self.db.get_appointment_count_today()
        except Exception:
            count = 0
        self.appt_count_label.configure(text=str(count))
        self.frame.after(60000, self.update_appointments_today)

    # -------------------------------
    # User info & logout
    # -------------------------------
    def set_user(self, user):
        self.current_user = user
        self.user_info_label.configure(text=f"Welcome, {user.username}")

    def handle_logout(self):
        self.current_user = None
        self.on_logout()

    # -------------------------------
    # Show / Hide
    # -------------------------------
    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()




