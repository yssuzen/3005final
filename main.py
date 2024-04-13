import psycopg2
import datetime
from psycopg2 import sql
from getpass import getpass

# Database connection
def connect_to_db():
    connection = psycopg2.connect(
        database="final_project",
        user="postgres",
        host="localhost",
        password="fener",
        port="5432"
    )
    return connection

# Initial app menu 
def get_user_choice(options):
    print("0. Quit")
    print("1. Member")
    print("2. Trainer")
    print("3. Admin")
    choice = input("Select an option: ")
    return choice


# Member Login 
def login_user(connection, role):
    print(f"** Logging in as a {role.title()} **")
    username = input("Enter your email: ")
    password = getpass("Enter your password: ")
    with connection.cursor() as cursor:
        cursor.execute(sql.SQL(
            "SELECT member_id, name, %s as role FROM members WHERE email = %s AND password = %s UNION ALL "
            "SELECT trainer_id, name, 'trainer' FROM trainers WHERE email = %s AND password = %s UNION ALL "
            "SELECT administrative_id, name, 'admin' FROM administrative WHERE email = %s AND password = %s"),
            (role, username, password, username, password, username, password))
        user = cursor.fetchone()
    if user:
        print(f"Welcome {user[1]}! You are logged in as a {user[2]}.")
        return user
    else:
        print("Login failed. Please check your credentials.")
        return None

# Member Registration Function
def register_member(connection):
    print("\n** Register a new member **")
    name = input("Enter full name: ")
    email = input("Enter email: ")
    password = getpass("Enter password: ")
    phone = input("Enter phone number: ")
    dob = input("Enter date of birth (YYYY-MM-DD): ")
    gender = input("Enter gender (Male (M)/Female (F)): ")
    fitness_goals = input("Enter your fitness goals: ")
    print('* Health Metrics *')
    current_weight = input("Enter your current weight (kg): ")
    weight_goal = input("Enter your weight goal (kg): ")
    exercise_details = input("Describe your typical weekly exercise routine: ")

    health_metrics = f"Current Weight: {current_weight} kg, Weight Goal: {weight_goal} kg, Exercise: {exercise_details}"

    with connection.cursor() as cursor:
        cursor.execute(sql.SQL(
            "INSERT INTO members (name, email, password, phone, dateofbirth, gender, fitness_goals, health_metrics) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"),
            (name, email, password, phone, dob, gender, fitness_goals, health_metrics))
        connection.commit()

    # A new cursor for fetching member ID
    with connection.cursor() as cursor:
        cursor.execute("SELECT member_ID FROM Members WHERE email = %s", (email,))
        member_id = cursor.fetchone()[0]
    
    # Creating payment for the newly registered member
    create_payment(connection, member_id)
    print("Registration successful!")
    print("Please re-run application and sign-in.")
    return (None, name, 'member') 

# Creating bills for upcoming 6 months
def create_payment(connection, member_id):
    cur = connection.cursor()
    try:
        current_date = datetime.date.today()
        for i in range(1, 7):  # Creating 6 future monthly payments
            due_date = current_date + datetime.timedelta(days=30 * i)
            cur.execute(
                "INSERT INTO Billing (member_ID, amount, status, due_date) VALUES (%s, %s, %s, %s)",
                (member_id, 100, 'unpaid', due_date)
            )
        connection.commit()
        print("Initial payments created successfully.")
    except Exception as e:
        connection.rollback()  
        print("Error creating initial payments:", e)
    finally:
        cur.close()  

# Updating member profile for members
def manage_profile(connection, member_id):
    print("\n** Profile Management **")
    new_email = input("Update email (leave blank to keep current): ")
    new_phone = input("Update phone number (leave blank to keep current): ")
    new_fitness_goals = input("Update fitness goals (leave blank to keep current): ")

    new_health_metrics = ""
    print('* Health Metrics *')
    current_weight = input("Enter your current weight (kg) (leave blank to keep current): ")
    weight_goal = input("Enter your weight goal (kg) (leave blank to keep current): ")
    exercise_details = input("Describe your typical weekly exercise routine (leave blank to keep current): ")

    if current_weight:
        new_health_metrics += f"Current Weight: {current_weight} kg, "
    if weight_goal:
        new_health_metrics += f"Weight Goal: {weight_goal} kg, "
    if exercise_details:
        new_health_metrics += f"Exercise: {exercise_details}"

    # Removing the trailing comma and space from the new_health_metrics string
    if new_health_metrics.endswith(", "):
        new_health_metrics = new_health_metrics[:-2]

    update_parts = []
    update_values = []

    if new_email:
        update_parts.append("email = %s")
        update_values.append(new_email)
    if new_phone:
        update_parts.append("phone = %s")
        update_values.append(new_phone)
    if new_fitness_goals:
        update_parts.append("fitness_goals = %s")
        update_values.append(new_fitness_goals)
    if new_health_metrics:
        update_parts.append("health_metrics = %s")
        update_values.append(new_health_metrics)

    if update_parts:
        update_query = "UPDATE members SET " + ", ".join(update_parts) + " WHERE member_id = %s"
        update_values.append(member_id)
        with connection.cursor() as cursor:
            cursor.execute(sql.SQL(update_query), update_values)
            connection.commit()
        print("Profile updated successfully!")
    else:
        print("No changes made.")

# Displaying Dashboard for members
def display_dashboard(connection, member_id):
    print("\n** Your Dashboard **")
    with connection.cursor() as cursor:
        cursor.execute(sql.SQL("SELECT fitness_goals, health_metrics FROM members WHERE member_id = %s"), [member_id])
        data = cursor.fetchone()
        if data:
            print("Fitness Goals: ", data[0])
            print("Health Metrics: ", data[1])
        else:
            print("No data available.")

# Members can manage their schedule
def manage_schedule(connection, member_id):
    print("\n** Schedule Management **")
    print("1. Fitness Group Class")
    print("2. Personal Training Session")
    choice = input("Select an option: ")

    if choice == '1':
        book_class(connection, member_id)
    elif choice == '2':
        book_personal_training_session(connection, member_id)

# Member Menu
def member_menu(connection, member_id):
    while True:
        print("\n** Member Menu **")
        print("1. Manage Profile")
        print("2. View Dashboard")
        print("3. Manage Schedule")
        print("0. Quit")
        choice = input("Select an option: ")
        if choice == '1':
            manage_profile(connection, member_id)
        elif choice == '2':
            display_dashboard(connection, member_id)
        elif choice == '3':
            manage_schedule(connection, member_id)
        elif choice == '0':
            break

# Trainer Login 
def login_trainer(connection):
    print("** Logging in as a Trainer **")
    username = input("Enter your email: ")
    password = getpass("Enter your password: ")
    with connection.cursor() as cursor:
        cursor.execute(sql.SQL("SELECT trainer_id, name FROM trainers WHERE email = %s AND password = %s"), (username, password))
        user = cursor.fetchone()
    if user:
        print(f"Welcome {user[1]}! You are logged in as a Trainer.")
        return user
    else:
        print("Login failed. Please check your credentials.")
        return None

# Administrative Staff Login
def login_admin(connection):
    print("** Logging in as an Admin **")
    username = input("Enter your email: ")
    password = getpass("Enter your password: ")
    with connection.cursor() as cursor:
        cursor.execute(sql.SQL("SELECT administrative_id, name FROM administrative WHERE email = %s AND password = %s"), (username, password))
        user = cursor.fetchone()
    if user:
        print(f"Welcome {user[1]}! You are logged in as an Admintrative Staff.")
        return user
    else:
        print("Login failed. Please check your credentials.")
        return None


# Registering available fitness group class for members
def register_class(connection, member_id):
    cursor = connection.cursor()
    # Display all available classes
    cursor.execute("SELECT class_id, class_name, schedule FROM GroupFitness WHERE room_id IS NOT NULL")
    classes = cursor.fetchall()

    if not classes:
        print("Currently, no group classes available for booking. Please trying again later.")
        return

    # Printing all available Fitness Group Class
    print("\nAvailable Fitness Group Classes:")
    for cls in classes:
        print(f"Class ID: {cls[0]}, Class Name: {cls[1]}, Schedule: {cls[2]}")

    # Asking user to enter the class ID they want to register for
    class_id = input("Enter the Fitness Group Class ID to register: ")
    if class_id:
        # Checking whether the user can register the group fitness class
        cursor.execute("SELECT * FROM GroupFitness WHERE class_id = %s", (class_id,))
        if cursor.fetchone():
            # Checking for existing registration
            cursor.execute("SELECT * FROM GroupFitnessEnrollment WHERE member_id = %s AND class_id = %s", (member_id, class_id))
            if cursor.fetchone():
                print("You are already registered for this fitness group class.")
            else:
                # Registering the member for the group fitness class
                cursor.execute("INSERT INTO GroupFitnessEnrollment (member_id, class_id, enrollment_status) VALUES (%s, %s, 'enrolled')", (member_id, class_id))
                connection.commit()
                print("You have successfully registered for the group class.")
                extra_payment(connection, member_id)
        else:
            print("Invalid Fitness Group Class ID. Please try again.")

# Cancelling enrolled fitness group class for members
def cancel_class_booking(connection, member_id):
    cursor = connection.cursor()
    cursor.execute("SELECT e.class_id, g.class_name FROM GroupFitnessEnrollment e JOIN GroupFitness g ON e.class_id = g.class_id WHERE e.member_id = %s", (member_id,))
    classes = cursor.fetchall()
    if classes:
        print("\nYour Booked Classes:")
        for cls in classes:
            print(f"Class ID: {cls[0]}, Class Name: {cls[1]}")
        class_id = input("Enter the Class ID to cancel: ")
        cursor.execute("DELETE FROM GroupFitnessEnrollment WHERE member_id = %s AND class_id = %s", (member_id, class_id))
        connection.commit()
        print("Fitness Group Class booking cancelled successfully.")
    else:
        print("No fitness group classes currently booked.")


# Registering fitness group class for members
def book_class(connection, member_id):
    while True:
        print("\n** Book a Group Fitness Class **")
        print("0. Go Back")
        print("1. Register Group Classes")
        print("2. Cancel a Booked Class")
        choice = input("Select an option: ")

        if choice == '0':
            break
        elif choice == '1':
            register_class(connection, member_id)
        elif choice == '2':
            cancel_class_booking(connection, member_id)
        else:
            print("Invalid option, please try again.")

def extra_payment(connection, member_id):
    cur = connection.cursor()
    try:
        # Today's date
        current_date = datetime.date.today()  

        # Due in 30 days
        due_date = current_date + datetime.timedelta(days=30)  
        
        # Insert the extra charge into the Billing table
        cur.execute(
            "INSERT INTO Billing (member_ID, amount, status, due_date) VALUES (%s, %s, %s, %s)",
            (member_id, 50, 'unpaid', due_date)  # $50 charge
        )
        connection.commit()
        print("Extra payment of $50 for additional selection.")
    except Exception as e:
        connection.rollback()  
        print("Error adding extra payment:", e)
    finally:
        cur.close()  

# Registering personal training session for members
def register_for_training_session(connection, member_id):
    cursor = connection.cursor()
    # Display all available trainers and their availability
    cursor.execute("SELECT trainer_id, name, availability FROM trainers WHERE availability IS NOT NULL ORDER BY name")
    trainers = cursor.fetchall()

    if not trainers:
        print("Currently, no trainers are available.")
        return

    print("\nAvailable Trainers:")
    for trainer in trainers:
        print(f"Trainer ID: {trainer[0]}, Name: {trainer[1]}, Available At: {trainer[2]}")

    # After member see available trainers, they will be asked to select a trainer to book a session with
    trainer_id = input("Enter the Trainer ID of the trainer you wish to book a session with, or press Enter to skip: ")
    if trainer_id:
        # User selects a date and time for the session
        selected_time = input("Enter the desired date and time for your session (YYYY-MM-DD HH:MM): ")
        # Check if the trainer is available at the selected time
        cursor.execute("SELECT availability FROM trainers WHERE trainer_id = %s AND availability = %s", (trainer_id, selected_time))
        if cursor.fetchone():
            # Book the session if the trainer is available
            cursor.execute("INSERT INTO PersonalTrainingSession (trainer_id, member_id, dateTime, status) VALUES (%s, %s, %s, 'scheduled')", (trainer_id, member_id, selected_time))
            connection.commit()
            print(f"Your training session with Trainer ID {trainer_id} has been successfully scheduled for {selected_time}.")
            # After successfully registered a personal training session, member will be charged $50
            extra_payment(connection, member_id)
        else:
            print("The selected trainer is not available at that time or an incorrect Trainer ID was entered. Please try again.")

# Cancelling personal training session for members
def cancel_training_session(connection, member_id):
    cursor = connection.cursor()
    cursor.execute("SELECT session_id, dateTime FROM PersonalTrainingSession WHERE member_id = %s", (member_id,))
    sessions = cursor.fetchall()
    if sessions:
        print("\nYour Booked Sessions:")
        for session in sessions:
            print(f"Session ID: {session[0]}, Scheduled Time: {session[1]}")
        session_id = input("Enter the Session ID to cancel: ")
        cursor.execute("DELETE FROM PersonalTrainingSession WHERE session_id = %s", (session_id,))
        connection.commit()
        print("Training session cancelled successfully.")
    else:
        print("No training sessions currently booked.")

# It is a submenu. When user selects Manage Schedule -> Personal Training Session, they can register a Personal Training Session, cancel a booked session. They can go beck previous menu as well.
def book_personal_training_session(connection, member_id):
    while True:
        print("\n** Book a Personal Training Session **")
        print("0. Go Back")
        print("1. Register Personal Training Session")
        print("2. Cancel a Booked Session")
        choice = input("Select an option: ")

        if choice == '0':
            break
        elif choice == '1':
            register_for_training_session(connection, member_id)
        elif choice == '2':
            cancel_training_session(connection, member_id)
        else:
            print("Invalid option, please try again.")

# Updating availability for trainers
def update_trainer_availability(connection, trainer_id):
    print("\n** Update Your Availability **")
    new_availability = input("Enter your new availability dates and times (e.g., 'YYYY-MM-DD HH:MM'): ")
    with connection.cursor() as cursor:
        cursor.execute("UPDATE trainers SET availability = %s WHERE trainer_id = %s", (new_availability, trainer_id))
        connection.commit()
    print("Your availability has been updated successfully.")

# Trainers can search members by searching by their name
def search_member_by_name(connection, trainer_id):
    print("\n** Search for Member Profiles **")
    member_name = input("Enter the member's name to search: ")
    with connection.cursor() as cursor:
        cursor.execute("SELECT member_id, name, fitness_goals, health_metrics FROM members WHERE name LIKE %s", (f"%{member_name}%",))
        members = cursor.fetchall()
        if members:
            for member in members:
                print(f"Member ID: {member[0]}, Name: {member[1]}, Fitness Goals: {member[2]}, Health Metrics: {member[3]}")
        else:
            print("No members found with that name.")

# Trainer Menu
def trainer_menu(connection, trainer_id):
    while True:
        print("\n** Trainer Menu **")
        print("1. Manage Your Schedule")
        print("2. Search Member by Name")
        print("0. Quit")
        choice = input("Select an option: ")

        if choice == '1':
            update_trainer_availability(connection, trainer_id)
        elif choice == '2':
            search_member_by_name(connection, trainer_id)
        elif choice == '0':
            break
        else:
            print("Invalid option, please try again.")

# Admin Menu
def admin_menu(connection, admin_id):
    while True:
        print("\n** Admin Menu **")
        print("1. Room Booking")
        print("2. Equipment Maintenance")
        print("3. Class Schedule")
        print("4. Member Billing")
        print("5. Process Payment")
        print("0. Quit")
        choice = input("Select an option: ")

        if choice == '1':
            room_booking(connection)
        elif choice == '2':
            equipment_maintenance(connection)
        elif choice == '3':
            class_schedule(connection)
        elif choice == '4':
            see_billing(connection)
        elif choice == '5':
            payment_method(connection)
        elif choice == '0':
            break
        else:
            print("Invalid option, please try again.")

# Displaying all available rooms for Administrative Staff
def view_available_rooms(connection):
    print("\n** Viewing Available Rooms **")
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT room_ID, room_name, capacity FROM Rooms WHERE status = 'free'")
        rooms = cursor.fetchall()
        if rooms:
            print("Available Rooms:")
            for room in rooms:
                print(f"Room ID: {room[0]}, Name: {room[1]}, Capacity: {room[2]}")
        else:
            print("No available rooms.")
    except Exception as e:
        print("Failed to retrieve rooms: ", e)
    finally:
        cursor.close()

# Booking room for Administrative Staff use
def book_room(connection):
    room_id = input("Enter the ID of the room to book: ")
    cursor = connection.cursor()
    try:
        # Fetching the current status of the room to check if it is already booked
        cursor.execute("SELECT status FROM Rooms WHERE room_ID = %s", (room_id,))
        result = cursor.fetchone()
        
        if result:
            status = result[0]
            # id status is booked, displaying warning message
            if status == 'booked':
                print("Warning: This room is already booked and cannot be booked for another session or class.")
            elif status == 'free':
                # If the room is free, proceed to book it
                cursor.execute("UPDATE Rooms SET status = 'booked' WHERE room_ID = %s", (room_id,))
                connection.commit()
                print("Room booked successfully.")
            else:
                print("This room is currently not available for booking.")
        else:
            print("Room does not exist. Please check the room ID and try again.")
    except Exception as e:
        print("Failed to book room: ", e)
    finally:
        cursor.close()

# Cancelling room booking for Administrative Staff use
def cancel_room_booking(connection):
    # Asking staff to enter the room id to cancel booking
    room_id = input("Enter the ID of the room to cancel booking: ")
    cursor = connection.cursor()
    try:
        # Checking whether the room is currently booked
        cursor.execute("SELECT status FROM Rooms WHERE room_ID = %s", (room_id,))
        result = cursor.fetchone()
        
        if result:
            status = result[0]
            if status == 'booked':
                # If the room is booked, update its status to 'free'
                cursor.execute("UPDATE Rooms SET status = 'free' WHERE room_ID = %s", (room_id,))
                connection.commit()
                print("Room booking has been successfully canceled.")
            else:
                print("This room is not currently booked, so it cannot be canceled.")
        else:
            print("Room does not exist. Please check the room ID and try again.")
    except Exception as e:
        print("Failed to cancel room booking: ", e)
        connection.rollback()
    finally:
        cursor.close()

# When Administrative Staff selects Room Booking, they will se another submenu
def room_booking(connection):
    while True:
        print("\n** Room Booking Management **")
        print("1. View Available Rooms")
        print("2. Book a Room")
        print("3. Cancel a Room Booking")
        print("0. Return to Main Menu")
        choice = input("Select an option: ")

        if choice == '0':
            break
        elif choice == '1':
            view_available_rooms(connection)
        elif choice == '2':
            book_room(connection)
        elif choice == '3':
            cancel_room_booking(connection)
        else:
            print("Invalid option, please try again.")

# Monitoring equipment maintenance. It displays Equipment name, availability and last maintenance date. 'A' means available and 'M' means under maintenance
def equipment_maintenance(connection):
    print("Function to equipment maintenance.")
    cursor = connection.cursor()
    cursor.execute("Select name, status, last_maintenance_date From Equipment")
    data = cursor.fetchall()
    print('Name - Available - Last Maintenance Date')
    for row in data:
        print(row)
    connection.commit()

# Administrative Staff can create a new fitness gorup class
def add_new_group_class(connection):
    class_name = input("Enter the new class name: ")
    schedule = input("Enter the class schedule (YYYY-MM-DD HH:MM): ")
    trainer_id = input("Enter the trainer ID: ")
    room_id = input("Enter the room ID: ")

    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO GroupFitness (class_name, schedule, trainer_ID, room_ID) VALUES (%s, %s, %s, %s)",
                       (class_name, schedule, trainer_id, room_id))
        cursor.execute("UPDATE Rooms SET status = 'booked' WHERE room_ID = %s", (room_id,))
        connection.commit()
        print("New group class added successfully.")
    except Exception as e:
        print("Failed to add new group class:", e)
        connection.rollback()
    finally:
        cursor.close()

# Administrative staff can update the ftiness group classes
def update_group_class(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT class_ID, class_name, schedule FROM GroupFitness")
    classes = cursor.fetchall()
    # Displaying all fitness group classes
    if classes:
        print("Fitness Group Classes:")
        for cls in classes:
            print(f"Class ID: {cls[0]}, Name: {cls[1]}, Schedule: {cls[2]}")
    class_id = input("Enter the class ID to update: ")
    new_schedule = input("Enter the new schedule (YYYY-MM-DD HH:MM) or press enter to skip: ")
    new_trainer_id = input("Enter the new trainer ID or press enter to skip: ")
    new_room_id = input("Enter the new room ID or press enter to skip: ")

    update_parts = []
    update_values = []

    if new_schedule:
        update_parts.append("schedule = %s")
        update_values.append(new_schedule)
    if new_trainer_id:
        update_parts.append("trainer_ID = %s")
        update_values.append(new_trainer_id)
    if new_room_id:
        update_parts.append("room_ID = %s")
        update_values.append(new_room_id)

    if update_parts:
        update_query = "UPDATE GroupFitness SET " + ", ".join(update_parts) + " WHERE class_ID = %s"
        update_values.append(class_id)
        cursor = connection.cursor()
        try:
            cursor.execute(update_query, update_values)
            if new_room_id:
                # Assuming that changing a room requires updating the old and new room statuses.
                cursor.execute("UPDATE Rooms SET status = 'free' WHERE room_ID IN (SELECT room_ID FROM GroupFitness WHERE class_ID = %s)", (class_id,))
                cursor.execute("UPDATE Rooms SET status = 'booked' WHERE room_ID = %s", (new_room_id,))
            connection.commit()
            print("Group class updated successfully.")
        except Exception as e:
            print("Failed to update group class:", e)
            connection.rollback()
        finally:
            cursor.close()
    else:
        print("No updates made.")

# Administrative staff can cancel fitness group class
def cancel_group_class(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT class_ID, class_name, schedule FROM GroupFitness")
    classes = cursor.fetchall()
    # Displaying all fitness group classes
    if classes:
        print("Fitness Group Classes:")
        for cls in classes:
            print(f"Class ID: {cls[0]}, Name: {cls[1]}, Schedule: {cls[2]}")
        class_id = input("Enter the Class ID to cancel: ")
        try:
            cursor.execute("DELETE FROM GroupFitness WHERE class_ID = %s", (class_id,))
            cursor.execute("UPDATE Rooms SET status = 'free' WHERE room_ID = (SELECT room_ID FROM GroupFitness WHERE class_ID = %s)", (class_id,))
            connection.commit()
            print("Group class cancelled successfully.")
        except Exception as e:
            print("Failed to cancel group class:", e)
            connection.rollback()
    else:
        print("No group classes available to cancel.")
    cursor.close()

# When administrative staff selects Class Schedule, they will see a submenu
def class_schedule(connection):
    while True:
        print("\n** Class Schedule Management **")
        print("1. Add New Group Class")
        print("2. Update Existing Group Class")
        print("3. Cancel Group Class")
        print("0. Return to Admin Menu")
        choice = input("Select an option: ")

        if choice == '0':
            break
        elif choice == '1':
            add_new_group_class(connection)
        elif choice == '2':
            update_group_class(connection)
        elif choice == '3':
            cancel_group_class(connection)
        else:
            print("Invalid option, please try again.")

# Displaying selected member's billing details. 
def see_billing(connection):
    member_id = input('What is your member id: ')
    cursor = connection.cursor()
    cursor.execute("Select * From billing where member_ID = %s", (member_id,))
    data = cursor.fetchall()
    for row in data:
        print(row)
    connection.commit()

def print_member_bills(connection, member_id):
    try:
        cursor = connection.cursor()
        # Retrieve all billing records for the selected member
        cursor.execute("SELECT bill_id, amount, status, due_date FROM Billing WHERE member_id = %s ORDER BY due_date", (member_id,))
        bills = cursor.fetchall()
        
        if bills:
            print("\nAll Bills for Member ID:", member_id)
            print("Bill ID | Amount | Status | Due Date")
            for bill in bills:
                print(f"{bill[0]} | ${bill[1]} | {bill[2]} | {bill[3]}")
        else:
            print("No billing records found for Member ID:", member_id)
    except Exception as e:
        print("Failed to retrieve billing information. Error:", e)
    finally:
        cursor.close()

# Members can pay their bill. For paying, administrative staff has to do that.
def payment_method(connection):
    member_id = input('Please enter the Member ID: ')
    print_member_bills(connection, member_id)
    bill_id = input('Please enter the Billing ID: ')
    try:
        with connection.cursor() as cursor:
            # Checking if the specified bill belongs to the given member and is unpaid
            cursor.execute("SELECT amount, status FROM Billing WHERE bill_id = %s AND member_id = %s AND status = 'unpaid'", (bill_id, member_id))
            bill = cursor.fetchone()
            if bill:
                print(f"Bill ID: {bill_id}, Bill Amount: {bill[0]}, Current Status: {bill[1]}")
                # Confirming payment process
                confirm = input("Do you want to process the payment? (yes/no): ").lower()
                if confirm == 'yes':
                    # Updating the billing status to 'paid'
                    cursor.execute("UPDATE Billing SET status = 'paid' WHERE bill_id = %s AND member_id = %s", (bill_id, member_id))
                    connection.commit()
                    print("Payment processed successfully. The bill has been marked as 'paid'.")
                else:
                    print("Payment process canceled.")
            else:
                print("No unpaid bill found with that ID for the selected member, or the bill is already paid.")
    except Exception as e:
        connection.rollback()  # Ensuring rollback on error
        print(f"Failed to process payment. Error: {e}")
    finally:
        if cursor:
            cursor.close()

# Starting App
def start_app():
    print("**********************************************************")
    print("Welcome to the Health and Fitness Club Management System!")
    print("**********************************************************")
    connection = connect_to_db()
    print("0. Quit")
    print("1. Member")
    print("2. Trainer")
    print("3. Admin")
    role = input("Select an option: ")
    user = None

    if role == '1':
        print("0. Quit")
        print("1. Sign in")
        print("2. Sign up")
        member_action = input("Select an option: ")
        if member_action == '2':
            user = register_member(connection)
            quit()
        elif member_action == '1':
            user = login_user(connection, "member")
    elif role == '2':
        user = login_trainer(connection)
    elif role == '3':
        user = login_admin(connection)

    if user and role == '1':
        member_menu(connection, user[0])
    elif user and role == '2':
        trainer_menu(connection, user[0])
        pass
    elif user and role == '3':
        admin_menu(connection, user[0])
        pass

    connection.close()
#
if __name__ == "__main__":
    start_app()
