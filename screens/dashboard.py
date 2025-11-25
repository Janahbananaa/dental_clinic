import customtkinter as ctk
from components.ui_components import CustomButton
import mysql.connector
import datetime
from tkinter import messagebox


class DashboardScreen:
    def __init__(self, parent, on_logout, on_navigate):
        self.parent = parent
        self.on_logout = on_logout
        self.on_navigate = on_navigate
        self.current_user = None

        # Database connection
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dental_clinic_db"
        )
        self.cursor = self.conn.cursor()

        self.frame = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        self.setup_ui()

    # -------------------------------
    # Setup UI
    # -------------------------------
    def setup_ui(self):
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

        # Shortcut buttons
        button_frame = ctk.CTkFrame(content, fg_color="#1a1a1a")
        button_frame.pack(fill="x", pady=20)

        # Patient Record button
        CustomButton(button_frame, text="📋 Patients Record",
                     command=lambda: self.on_navigate("patients"),
                     width=180, height=60).pack(side="left", padx=20)

        # Doctor button
        CustomButton(button_frame, text="👨‍⚕️ Doctors",
                     command=lambda: self.on_navigate("doctors"),
                     width=180, height=60).pack(side="left", padx=20)

        # Appointments button
        CustomButton(button_frame, text="📅 Appointments",
                     command=self.show_all_appointments,
                     width=180, height=60).pack(side="left", padx=20)

        self.update_appointments_today()

    # -------------------------------
    # Count for today
    # -------------------------------
    def update_appointments_today(self):
        today = datetime.date.today()
        self.cursor.execute("SELECT COUNT(*) FROM appointments WHERE DATE(`Date/Time`)=%s", (today,))
        count = self.cursor.fetchone()[0]
        self.appt_count_label.configure(text=str(count))
        self.frame.after(60000, self.update_appointments_today)

    # -------------------------------
    # Show All Appointments
    # -------------------------------
    def show_all_appointments(self):
        popup = ctk.CTkToplevel(self.frame)
        popup.title("All Appointments")
        popup.geometry("1200x600")
        popup.grab_set()

        header = ctk.CTkFrame(popup, fg_color="#1a1a1a")
        header.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(header, text="All Appointments",
                     font=("Arial", 20, "bold")).pack(side="left")

        CustomButton(header, text="➕ Add Appointment", width=150,
                     command=self.add_appointment_popup).pack(side="right")

        table = ctk.CTkScrollableFrame(popup, width=1150, height=500)
        table.pack(padx=20, pady=10, fill="both", expand=True)

        columns = ["ID", "Name", "Age", "Contact", "Gender", "Type",
                   "Date/Time", "Dental Service", "Service Fee", "EDIT", "DELETE"]

        for i, col in enumerate(columns):
            ctk.CTkLabel(table, text=col, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=5, pady=5)

        self.cursor.execute("""
            SELECT appointment_id, Name, Age, Contact, Gender, Type,
                   `Date/Time`, Dental_service, Service_fee
            FROM appointments ORDER BY `Date/Time` ASC
        """)
        rows = self.cursor.fetchall()

        for r, row in enumerate(rows, start=1):
            appt_id = row[0]

            for c, value in enumerate(row):
                ctk.CTkLabel(table, text=str(value)).grid(row=r, column=c, padx=5, pady=5)

            CustomButton(table, text="✏️ Edit", width=70,
                         command=lambda id=appt_id: self.edit_appointment_popup(id)
                         ).grid(row=r, column=len(columns)-2)

            CustomButton(table, text="🗑️ Delete", width=70,
                         command=lambda id=appt_id: self.delete_appointment(id)
                         ).grid(row=r, column=len(columns)-1)

    # -------------------------------
    # Add / Edit Appointment & Generic Form
    # -------------------------------
    def add_appointment_popup(self):
        self._appointment_form(mode="add")

    def edit_appointment_popup(self, appt_id):
        self._appointment_form(mode="edit", appointment_id=appt_id)

    def _appointment_form(self, mode="add", appointment_id=None):
        popup = ctk.CTkToplevel(self.frame)
        popup.title("Appointment Form")
        popup.geometry("400x600")
        popup.grab_set()

        fields = {}
        type_options = ["Child", "Adult"]
        dental_services_options = ["Teeth Cleaning", "Extractions", "Veneers", "Fillings",
                                   "Crowns", "Root Canal", "Braces", "Bonding", "Dentures"]

        labels = ["Name", "Age", "Contact", "Gender (Male/Female)", "Type (Child/Adult)",
                  "Date/Time (YYYY-MM-DD HH:MM:SS)", "Dental Service", "Service Fee"]

        for label in labels:
            ctk.CTkLabel(popup, text=label).pack(pady=4)
            if label == "Type (Child/Adult)":
                dropdown = ctk.CTkOptionMenu(popup, values=type_options)
                dropdown.pack(pady=4)
                fields[label] = dropdown
            elif label == "Dental Service":
                dropdown = ctk.CTkOptionMenu(popup, values=dental_services_options)
                dropdown.pack(pady=4)
                fields[label] = dropdown
            else:
                entry = ctk.CTkEntry(popup)
                entry.pack(pady=4)
                fields[label] = entry

        if mode == "edit":
            self.cursor.execute("""
                SELECT Name, Age, Contact, Gender, Type, `Date/Time`, Dental_service, Service_fee
                FROM appointments WHERE appointment_id=%s
            """, (appointment_id,))
            row = self.cursor.fetchone()
            for value, key in zip(row, fields):
                if isinstance(fields[key], ctk.CTkOptionMenu):
                    fields[key].set(value)
                else:
                    fields[key].insert(0, str(value))

        def save():
            try:
                name = fields["Name"].get()
                age = int(fields["Age"].get())
                contact = fields["Contact"].get()
                gender = fields["Gender (Male/Female)"].get()
                ptype = fields["Type (Child/Adult)"].get()
                dt = fields["Date/Time (YYYY-MM-DD HH:MM:SS)"].get()
                dental_service = fields["Dental Service"].get()
                fee = float(fields["Service Fee"].get())

                self.cursor.execute("""
                    SELECT COUNT(*) FROM appointments
                    WHERE `Date/Time`=%s AND appointment_id!=%s
                """, (dt, appointment_id if appointment_id else 0))
                conflict_count = self.cursor.fetchone()[0]
                if conflict_count > 0:
                    messagebox.showwarning("Conflict", "This time slot is already taken. Please select another time.")
                    return

                if mode == "add":
                    self.cursor.execute("""
                        INSERT INTO appointments
                        (Name, Age, Contact, Gender, Type, `Date/Time`, Dental_service, Service_fee)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (name, age, contact, gender, ptype, dt, dental_service, fee))
                else:
                    self.cursor.execute("""
                        UPDATE appointments SET
                        Name=%s, Age=%s, Contact=%s, Gender=%s, Type=%s,
                        `Date/Time`=%s, Dental_service=%s, Service_fee=%s
                        WHERE appointment_id=%s
                    """, (name, age, contact, gender, ptype, dt, dental_service, fee, appointment_id))

                self.conn.commit()
                popup.destroy()
                self.show_all_appointments()
                self.update_appointments_today()

            except Exception as err:
                messagebox.showerror("Error", f"Failed: {err}")

        CustomButton(popup, text="Save", command=save).pack(pady=20)

    # -------------------------------
    # Delete Appointment
    # -------------------------------
    def delete_appointment(self, appt_id):
        if messagebox.askyesno("Confirm", "Delete appointment?"):
            self.cursor.execute("DELETE FROM appointments WHERE appointment_id=%s", (appt_id,))
            self.conn.commit()
            self.show_all_appointments()
            self.update_appointments_today()

    # -------------------------------
    # Dentist Schedule
    # -------------------------------
    def show_dentist_schedule(self):
        popup = ctk.CTkToplevel(self.frame)
        popup.title("Dentist Schedule")
        popup.geometry("1000x600")
        popup.grab_set()

        ctk.CTkLabel(popup, text="Dentist Schedule", font=("Arial", 20, "bold")).pack(pady=20)
        table = ctk.CTkScrollableFrame(popup, width=950, height=500)
        table.pack(padx=20, pady=10, fill="both", expand=True)

        columns = ["ID", "Name", "Age", "Contact", "Gender", "Type", "Date/Time", "Dental Service", "Service Fee"]

        for i, col in enumerate(columns):
            ctk.CTkLabel(table, text=col, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=5, pady=5)

        self.cursor.execute("""
            SELECT appointment_id, Name, Age, Contact, Gender, Type, `Date/Time`, Dental_service, Service_fee
            FROM appointments
            ORDER BY `Date/Time` ASC
        """)
        rows = self.cursor.fetchall()
        for r, row in enumerate(rows, start=1):
            for c, value in enumerate(row):
                ctk.CTkLabel(table, text=str(value)).grid(row=r, column=c, padx=5, pady=5)

    # -------------------------------
    # Appointments Today
    # -------------------------------
    def show_appointments_today(self):
        popup = ctk.CTkToplevel(self.frame)
        popup.title("Appointments Today")
        popup.geometry("1000x600")
        popup.grab_set()

        ctk.CTkLabel(popup, text="Appointments Today", font=("Arial", 20, "bold")).pack(pady=20)
        table = ctk.CTkScrollableFrame(popup, width=950, height=500)
        table.pack(padx=20, pady=10, fill="both", expand=True)

        columns = ["ID", "Name", "Age", "Contact", "Gender", "Type", "Date/Time", "Dental Service", "Service Fee"]

        for i, col in enumerate(columns):
            ctk.CTkLabel(table, text=col, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=5, pady=5)

        today = datetime.date.today()
        self.cursor.execute("""
            SELECT appointment_id, Name, Age, Contact, Gender, Type, `Date/Time`, Dental_service, Service_fee
            FROM appointments
            WHERE DATE(`Date/Time`)=%s
            ORDER BY `Date/Time` ASC
        """, (today,))
        rows = self.cursor.fetchall()
        if not rows:
            ctk.CTkLabel(table, text="No appointments today.", font=("Arial", 14)).grid(row=1, column=0, columnspan=len(columns), pady=20)
        else:
            for r, row in enumerate(rows, start=1):
                for c, value in enumerate(row):
                    ctk.CTkLabel(table, text=str(value)).grid(row=r, column=c, padx=5, pady=5)

    # -------------------------------
    # User info & logout
    # -------------------------------
    def set_user(self, user):
        self.current_user = user
        self.user_info_label.configure(text=f"Welcome, {user.username}")

    def handle_logout(self):
        self.current_user = None
        self.on_logout()

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()
