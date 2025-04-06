# FC723 Project – Seat Booking Application 

# This application simulates a seat booking system for Apache Airlines.
# It provides a menu for checking seat availability, booking a seat, freeing a seat, showing booking status, and exiting the program.
# The seating chart simulates a plane with 80 rows, an aisle inserted between seats C and D,

import random
import string
import re
import sqlite3

# Global dictionary for in-memory passenger details (optional backup)
passenger_details = {}

# Connect to SQLite database (or create if it doesn't exist)
conn = sqlite3.connect("bookings.db")
cursor = conn.cursor()

# Create bookings table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        booking_ref TEXT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        passport TEXT,
        seat TEXT
    )
''')
conn.commit()

def generate_booking_reference(seating):
    existing_refs = {value for value in seating.values() if value not in {"F", "X", "S"}}
    while True:
        ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if ref not in existing_refs:
            return ref

def initialize_seating():
    seating = {}
    rows = 80
    seats = "ABCDEF"
    storage_seats = {"79D", "79E", "79F", "80D", "80E", "80F"}
    for row in range(1, rows + 1):
        for seat in seats:
            key = f"{row}{seat}"
            seating[key] = "S" if key in storage_seats else "F"
    return seating

def load_seating_from_db(seating):
    cursor.execute("SELECT booking_ref, seat FROM bookings")
    for booking_ref, seat in cursor.fetchall():
        seating[seat] = booking_ref

def display_seating(seating):
    # Updated: Show "R" for booked seats instead of booking reference
    print("\nSeating Layout (F = Free, X = Aisle, S = Storage, R = Reserved)")
    print("     A   B   C       D   E   F")
    for row in range(1, 81):
        row_display = []
        for seat in "ABC":
            val = seating[f"{row}{seat}"]
            # if the seat is not free, storage or aisle, mark as "R"
            row_display.append(val if val in {"F", "S"} else ("R" if val not in {"X", "F", "S"} else val))
        row_display.append("X")
        for seat in "DEF":
            val = seating[f"{row}{seat}"]
            row_display.append(val if val in {"F", "S"} else ("R" if val not in {"X", "F", "S"} else val))
        row_str = str(row).rjust(2)
        print(f"{row_str}   {'   '.join(row_display)}")

def valid_seat_format(seat):
    return re.match(r"^([1-9][0-9]?|80)[A-F]$", seat) is not None

def valid_passport_format(passport):
    return re.match(r"^[A-Z0-9]{6,15}$", passport.upper()) is not None

def book_seat(seating):
    first = input("Enter First Name: ").strip()
    last = input("Enter Last Name: ").strip()
    passport = input("Enter Passport Number: ").strip().upper()

    if not valid_passport_format(passport):
        print("Invalid passport number format. Use 6-15 letters/numbers.")
        return

    seat_choice = input("Enter seat to book (e.g., 12A): ").upper()

    if not valid_seat_format(seat_choice):
        print("Invalid seat format. Use row number (1-80) followed by seat letter A-F.")
        return

    if seating.get(seat_choice) in {"S", "X"}:
        print("That seat cannot be booked.")
        return
    if seating.get(seat_choice) != "F":
        print("That seat is already booked.")
        return

    booking_ref = generate_booking_reference(seating)
    seating[seat_choice] = booking_ref

    # Store in the database
    cursor.execute("INSERT INTO bookings VALUES (?, ?, ?, ?, ?)",
                   (booking_ref, first, last, passport, seat_choice))
    conn.commit()

    # Booking confirmation displays the actual booking reference
    print(f"Seat {seat_choice} successfully booked! Your booking reference is: {booking_ref}")

def cancel_booking(seating):
    booking_ref = input("Enter booking reference to cancel: ").upper()
    cursor.execute("SELECT seat FROM bookings WHERE booking_ref = ?", (booking_ref,))
    result = cursor.fetchone()
    if result:
        seat = result[0]
        seating[seat] = "F"
        cursor.execute("DELETE FROM bookings WHERE booking_ref = ?", (booking_ref,))
        conn.commit()
        print(f"Booking for seat {seat} has been canceled.")
    else:
        print("Booking reference not found.")

def show_user_booking():
    identifier = input("Enter your booking reference, passport number, or full name: ").strip().upper()
    found = False
    cursor.execute("SELECT * FROM bookings")
    for ref, first, last, passport, seat in cursor.fetchall():
        full_name = f"{first} {last}".upper()
        if identifier in {ref, passport.upper(), full_name}:
            print("\nBooking Details:")
            print(f"Name: {first} {last}")
            print(f"Passport: {passport}")
            print(f"Seat: {seat}")
            print(f"Booking Reference: {ref}")
            found = True
            break
    if not found:
        print("No booking found with that information.")

def menu():
    seating = initialize_seating()
    load_seating_from_db(seating)
    print("\nWelcome to the Apache Airlines Seat Booking Application!,  We are glad to have you here. Please follow the menu options below to manage your booking")
    while True:
        print("\nMenu:")
        print("1. Book a seat")
        print("2. Cancel a booking")
        print("3. Show your booking status")
        print("4. Display full seating")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            book_seat(seating)
        elif choice == "2":
            cancel_booking(seating)
        elif choice == "3":
            show_user_booking()
        elif choice == "4":
            display_seating(seating)
        elif choice == "5":
            print("Thank you for using Apache Airlines. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()

