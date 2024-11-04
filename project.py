import tkinter as tk
from tkinter import messagebox,StringVar,IntVar
import mysql.connector
from PIL import Image, ImageTk
import random



def set_background(window, image_path):
    background_image = Image.open(image_path)
    background_image = background_image.resize((800, 600), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(background_image)

    label_background = tk.Label(window, image=bg_image)
    label_background.image = bg_image  # Keep a reference to avoid garbage collection
    label_background.place(x=0, y=0, relwidth=1, relheight=1)

def login():
    user_id = entry_user_id.get().strip()
    password = entry_password.get().strip()
    
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='project'
        )
        
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()

        if user and user[2] == password:  # Assuming password is the 3rd column
            messagebox.showinfo("Login", "Login successful!")
            root.withdraw()  # Hide the login window
            open_home_page()  # Open the home page
        else:
            messagebox.showerror("Error", "Invalid User ID or Password.")
    
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
    finally:
        if conn:
            cursor.close()
            conn.close()

def register():
    registration_window = tk.Toplevel(root)
    registration_window.title("Register")
    registration_window.geometry("800x600")
    
    set_background(registration_window, "O:\\project\\background.png")

    # Registration Form Labels and Entries
    tk.Label(registration_window, text="Name:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)
    entry_name = tk.Entry(registration_window, font=("Helvetica", 12), width=30)
    entry_name.pack(pady=5)

    tk.Label(registration_window, text="Contact Number:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)
    entry_contact = tk.Entry(registration_window, font=("Helvetica", 12), width=30)
    entry_contact.pack(pady=5)

    tk.Label(registration_window, text="Address:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)
    entry_address = tk.Entry(registration_window, font=("Helvetica", 12), width=30)
    entry_address.pack(pady=5)

    tk.Label(registration_window, text="Blood Group:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)
    entry_blood_group = tk.Entry(registration_window, font=("Helvetica", 12), width=30)
    entry_blood_group.pack(pady=5)

    tk.Label(registration_window, text="Password:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)
    entry_password_reg = tk.Entry(registration_window, show='*', font=("Helvetica", 12), width=30)
    entry_password_reg.pack(pady=5)

    # Submit Button
    button_submit = tk.Button(registration_window, text="Submit", command=lambda: submit_registration(
        entry_name.get(),
        entry_password_reg.get(),
        entry_contact.get(),
        entry_address.get(),
        entry_blood_group.get()
    ), font=("Helvetica", 12), bg="#4CAF50", fg="white", width=15)
    button_submit.pack(pady=20)

def submit_registration(username, password, contact, address, blood_group):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='project'
        )
        
        cursor = conn.cursor()
        
        # Get the next user_id
        cursor.execute("SELECT MAX(user_id) FROM users")
        max_user_id = cursor.fetchone()[0]

        if max_user_id is not None:
            user_id = max_user_id + 1  # Increment the max user_id
        else:
            user_id = 1000  # Start from 1000 if no users exist

        query = "INSERT INTO users (user_id, username, password, contact, address, blood_group) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (user_id, username, password, contact, address, blood_group))
        conn.commit()
        
        messagebox.showinfo("Registration", f"Registration successful! Your User ID is: {user_id}")
        
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")

def open_home_page():
    home_window = tk.Toplevel(root)
    home_window.title("Home Page")
    home_window.geometry("800x600")
    
    set_background(home_window, "O:\\project\\background.png")

    label_title = tk.Label(home_window, text="Welcome to Your Home Page", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
    label_title.pack(pady=20)

    button_appointment = tk.Button(home_window, text="Book Appointment", command=book_appointment, font=("Helvetica", 12), width=20)
    button_appointment.pack(pady=10)

    button_view_appointments = tk.Button(home_window, text="View Appointments", command=view_appointments, font=("Helvetica", 12), width=20)
    button_view_appointments.pack(pady=10)

    button_update_profile = tk.Button(home_window, text="User Profile", command=view_user_profile, font=("Helvetica", 12), width=20)
    button_update_profile.pack(pady=10)

    button_payments = tk.Button(home_window, text="Payments", command=view_payments, font=("Helvetica", 12), width=20)
    button_payments.pack(pady=10)

    button_logout = tk.Button(home_window, text="Logout", command=lambda: [home_window.destroy(), root.deiconify()], font=("Helvetica", 12), width=20)
    button_logout.pack(pady=10)

    button_exit = tk.Button(home_window, text="Exit", command=root.quit, font=("Helvetica", 12), width=20)
    button_exit.pack(pady=10)

def view_user_profile():
    profile_window = tk.Toplevel(root)
    profile_window.title("User Profile")
    profile_window.geometry("800x600")
    
    set_background(profile_window, "O:\\project\\background.png")

    user_id = entry_user_id.get().strip()  # Get the logged-in user ID

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='project'
        )
        cursor = conn.cursor()

        cursor.execute("SELECT user_id, username, password, contact, address, blood_group FROM users WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()

        if user:
            # Display current user info
            tk.Label(profile_window, text=f"User ID: {user[0]}", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)
            tk.Label(profile_window, text="Username:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)
            entry_username = tk.Entry(profile_window, font=("Helvetica", 12), width=30)
            entry_username.insert(0, user[1])
            entry_username.pack(pady=5)

            tk.Label(profile_window, text="Password:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)
            entry_password = tk.Entry(profile_window, show='*', font=("Helvetica", 12), width=30)
            entry_password.insert(0, user[2])
            entry_password.pack(pady=5)

            tk.Label(profile_window, text="Contact:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)
            entry_contact = tk.Entry(profile_window, font=("Helvetica", 12), width=30)
            entry_contact.insert(0, user[3])
            entry_contact.pack(pady=5)

            tk.Label(profile_window, text="Address:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)
            entry_address = tk.Entry(profile_window, font=("Helvetica", 12), width=30)
            entry_address.insert(0, user[4])
            entry_address.pack(pady=5)

            tk.Label(profile_window, text="Blood Group:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)
            entry_blood_group = tk.Entry(profile_window, font=("Helvetica", 12), width=30)
            entry_blood_group.insert(0, user[5])
            entry_blood_group.pack(pady=5)

            # Confirm button to update user info
            button_confirm = tk.Button(profile_window, text="Confirm", command=lambda: update_user_profile(
                user_id,
                entry_username.get(),
                entry_password.get(),
                entry_contact.get(),
                entry_address.get(),
                entry_blood_group.get()
            ), font=("Helvetica", 12), bg="#4CAF50", fg="white", width=15)
            button_confirm.pack(pady=20)
        else:
            messagebox.showerror("Error", "User not found.")
    
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")

def update_user_profile(user_id, username, password, contact, address, blood_group):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='project'
        )
        
        cursor = conn.cursor()

        query = """
            UPDATE users 
            SET username = %s, password = %s, contact = %s, address = %s, blood_group = %s 
            WHERE user_id = %s
        """
        cursor.execute(query, (username, password, contact, address, blood_group, user_id))
        conn.commit()
        
        messagebox.showinfo("Update Profile", "Profile updated successfully!")
        
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")

def book_appointment():
    appointment_window = tk.Toplevel(root)
    appointment_window.title("Book Appointment")
    appointment_window.geometry("800x600")
    
    set_background(appointment_window, "O:\\project\\background.png")

    # Select Department
    tk.Label(appointment_window, text="Select Department:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)
    department_var = StringVar(appointment_window)
    
    # Fetch specialities from the database
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='project'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT speciality_id, speciality_name FROM specialities")
        specialities = cursor.fetchall()

        speciality_menu = tk.OptionMenu(appointment_window, department_var, *[f"{sp[1]}:{sp[0]}" for sp in specialities])
        speciality_menu.pack(pady=5)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
    
    # Next button for selecting doctor
    button_next_doctor = tk.Button(appointment_window, text="Select Doctor", command=lambda: select_doctor(department_var.get().split(':')[1]), font=("Helvetica", 12), bg="#4CAF50", fg="white", width=20)
    button_next_doctor.pack(pady=10)

def select_doctor(speciality_id):
    doctor_window = tk.Toplevel(root)
    doctor_window.title("Select Doctor")
    doctor_window.geometry("800x600")

    set_background(doctor_window, "O:\\project\\background.png")

    tk.Label(doctor_window, text="Select Doctor:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)
    doctor_var = StringVar(doctor_window)

    # Fetch doctors from the database
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='project'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT doctor_id, name FROM doctors WHERE specialty_id = %s", (speciality_id,))
        doctors = cursor.fetchall()

        doctor_menu = tk.OptionMenu(doctor_window, doctor_var, *[f"{doc[1]}:{doc[0]}" for doc in doctors])
        doctor_menu.pack(pady=5)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
    
    # Next button for selecting date
    button_next_date = tk.Button(doctor_window, text="Select Date", command=lambda: select_date(doctor_var.get().split(':')[1]), font=("Helvetica", 12), bg="#4CAF50", fg="white", width=20)
    button_next_date.pack(pady=10)

def select_date(doctor_id):
    date_window = tk.Toplevel(root)
    date_window.title("Select Date")
    date_window.geometry("800x600")

    set_background(date_window, "O:\\project\\background.png")

    tk.Label(date_window, text="Select Appointment Date:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)
    
    entry_date = tk.Entry(date_window, font=("Helvetica", 12), width=30)
    entry_date.pack(pady=5)

    button_next_time = tk.Button(date_window, text="Select Time", command=lambda: select_time(doctor_id, entry_date.get()), font=("Helvetica", 12), bg="#4CAF50", fg="white", width=20)
    button_next_time.pack(pady=10)

def select_time(doctor_id, date):
    time_window = tk.Toplevel(root)
    time_window.title("Select Time")
    time_window.geometry("800x600")

    set_background(time_window, "O:\\project\\background.png")

    tk.Label(time_window, text="Select Time Slot:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=10)
    time_var = StringVar(time_window)

    # Example time slots (you might want to pull these from your database)
    time_slots = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]
    time_menu = tk.OptionMenu(time_window, time_var, *time_slots)
    time_menu.pack(pady=5)

    # Confirm button
    button_confirm = tk.Button(time_window, text="Confirm Appointment", command=lambda: confirm_appointment(doctor_id, date, time_var.get(), time_window), font=("Helvetica", 12), bg="#4CAF50", fg="white", width=15)
    button_confirm.pack(pady=10)

def confirm_appointment(doctor_id, appointment_date, appointment_time, time_window):
    appointment_id = random.randint(1000, 9999)  # Generate a random appointment ID
    user_id = entry_user_id.get()  # Assume the user ID is stored here
    
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='project'
        )
        cursor = conn.cursor()

        query = "INSERT INTO appointments (appointment_id, user_id, doctor_id, appointment_date, appointment_time) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (appointment_id, user_id, doctor_id, appointment_date, appointment_time))
        conn.commit()

        messagebox.showinfo("Appointment", f"Appointment booked successfully!\nAppointment ID: {appointment_id}")
        
        # Proceed to payment
        payment_screen(appointment_id, appointment_date, appointment_time)
    
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")

def payment_screen(appointment_id, date, time):
    payment_window = tk.Toplevel(root)
    payment_window.title("Payment")
    payment_window.geometry("800x600")

    set_background(payment_window, "O:\\project\\background.png")

    tk.Label(payment_window, text="Payment Details", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=20)
    tk.Label(payment_window, text=f"Appointment ID: {appointment_id}", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)
    tk.Label(payment_window, text=f"Date: {date}", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)
    tk.Label(payment_window, text=f"Time: {time}", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)
    tk.Label(payment_window, text="Consultation Fee: 300", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)

    pay_on_visit = IntVar()
    check_box = tk.Checkbutton(payment_window, text="Pay on Visit", variable=pay_on_visit, bg="#f0f0f0")
    check_box.pack(pady=10)

    button_confirm = tk.Button(payment_window, text="Confirm Payment", 
                                command=lambda: confirm_payment(appointment_id, payment_window, pay_on_visit.get()), 
                                font=("Helvetica", 12), bg="#4CAF50", fg="white", width=15)
    button_confirm.pack(pady=20)

def confirm_payment(appointment_id, payment_window, pay_on_visit):
    amount = 300  # Fixed consultation fee
    payment_status = "Pending" if pay_on_visit else "Paid"  # Set status based on checkbox

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='project'
        )
        cursor = conn.cursor()

        # Generate a random unique payment_id
        while True:
            payment_id = random.randint(1000, 9999)  # Generate a random payment ID
            cursor.execute("SELECT COUNT(*) FROM payments WHERE payment_id = %s", (payment_id,))
            if cursor.fetchone()[0] == 0:  # Check if the payment_id is unique
                break

        # Insert payment with SYSDATE() for the current date
        query = """
            INSERT INTO payments (payment_id, appointment_id, amount, payment_date, status) 
            VALUES (%s, %s, %s, SYSDATE(), %s)
        """
        cursor.execute(query, (payment_id, appointment_id, amount, payment_status))
        conn.commit()

        messagebox.showinfo("Payment", "Payment confirmed successfully!")
        payment_window.destroy()  # Close payment window
        # Optionally redirect to homepage
        open_home_page()

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")

def view_appointments():
    appointments_window = tk.Toplevel(root)
    appointments_window.title("Your Appointments")
    appointments_window.geometry("800x600")
    
    set_background(appointments_window, "O:\\project\\background.png")

    tk.Label(appointments_window, text="Your Appointments", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=20)

    # Create a Frame to hold the Listbox and buttons
    frame = tk.Frame(appointments_window)
    frame.pack(pady=10)

    # Create a Listbox to display appointments
    appointments_listbox = tk.Listbox(frame, width=80, height=15)
    appointments_listbox.pack(side=tk.LEFT, padx=10)

    # Scrollbar for the Listbox
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    appointments_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=appointments_listbox.yview)

    user_id = entry_user_id.get()  # Get the logged-in user ID

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='project'
        )
        cursor = conn.cursor()

        query = "SELECT appointment_id, user_id, doctor_id, appointment_date, appointment_time FROM appointments WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        appointments = cursor.fetchall()

        if appointments:
            for appointment in appointments:
                appointment_info = f"Appointment ID: {appointment[0]}, User ID: {appointment[1]}, Doctor ID: {appointment[2]}, Date: {appointment[3]}, Time: {appointment[4]}"
                appointments_listbox.insert(tk.END, appointment_info)

                # Create a cancel button for each appointment
                cancel_button = tk.Button(appointments_window, text="Cancel", command=lambda app_id=appointment[0]: cancel_appointment(app_id, appointments_window), bg="#f44336", fg="white")
                cancel_button.pack(pady=2)

        else:
            appointments_listbox.insert(tk.END, "No appointments found.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")

def cancel_appointment(appointment_id, window):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='project'
        )
        cursor = conn.cursor()

        # Delete from payments table first
        cursor.execute("DELETE FROM payments WHERE appointment_id = %s", (appointment_id,))
        conn.commit()

        # Then delete from appointments table
        cursor.execute("DELETE FROM appointments WHERE appointment_id = %s", (appointment_id,))
        conn.commit()

        messagebox.showinfo("Appointment Cancellation", "Appointment Cancelled Successfully.")
        window.destroy()  # Close the appointments window

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")

def view_payments():
    payments_window = tk.Toplevel(root)
    payments_window.title("Your Payments")
    payments_window.geometry("800x600")

    set_background(payments_window, "O:\\project\\background.png")

    tk.Label(payments_window, text="Your Payments", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=20)

    # Create a Frame to hold the Listbox and buttons
    frame = tk.Frame(payments_window)
    frame.pack(pady=10)

    # Create a Listbox to display payments
    payments_listbox = tk.Listbox(frame, width=80, height=15)
    payments_listbox.pack(side=tk.LEFT, padx=10)

    # Scrollbar for the Listbox
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    payments_listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=payments_listbox.yview)

    user_id = entry_user_id.get()  # Get the logged-in user ID

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1234',
            database='project'
        )
        cursor = conn.cursor()

        query = """
            SELECT payment_id, appointment_id, amount, payment_date, status 
            FROM payments 
            WHERE appointment_id IN (
                SELECT appointment_id FROM appointments WHERE user_id = %s
            )
        """
        cursor.execute(query, (user_id,))
        payments = cursor.fetchall()

        if payments:
            for payment in payments:
                payment_info = f"Payment ID: {payment[0]}, Appointment ID: {payment[1]}, Amount: {payment[2]}, Date: {payment[3]}, Status: {payment[4]}"
                payments_listbox.insert(tk.END, payment_info)
        else:
            payments_listbox.insert(tk.END, "No payment records found.")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")

    # Exit button to return to home page
    button_exit = tk.Button(payments_window, text="Exit", command=payments_window.destroy, font=("Helvetica", 12), width=20)
    button_exit.pack(pady=20)

# Main application
root = tk.Tk()
root.title("Medicare Clinic Appointment")
root.geometry("800x600")

set_background(root, "O:\\project\\background.png")

# Login Form Labels and Entries
tk.Label(root, text="User ID:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)
entry_user_id = tk.Entry(root, font=("Helvetica", 12), width=30)
entry_user_id.pack(pady=5)

tk.Label(root, text="Password:", font=("Helvetica", 12), bg="#f0f0f0").pack(pady=5)
entry_password = tk.Entry(root, show='*', font=("Helvetica", 12), width=30)
entry_password.pack(pady=5)

# Login and Register Buttons
button_login = tk.Button(root, text="Login", command=login, font=("Helvetica", 12), bg="#4CAF50", fg="white", width=15)
button_login.pack(pady=20)

button_register = tk.Button(root, text="Register", command=register, font=("Helvetica", 12), bg="#4CAF50", fg="white", width=15)
button_register.pack(pady=5)

# Run the application
root.mainloop()
