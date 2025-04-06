# FC723 Project – Seat Booking Application 

# This application simulates a seat booking system for Apache Airlines.

# It provides a menu for checking seat availability, booking a seat, freeing a seat, showing booking status, and exiting the program.

# The seating chart simulates a plane with 80 rows, an aisle inserted between seats C and D,

import random
import string

def generate_booking_reference(seating):
    """
    Generates a unique 8-character alphanumeric booking reference.
    It checks all current seating values (ignoring "F", "X", and "S")
    to ensure that the generated reference is unique.
    """
    # Collect all booking references currently used in seating
    existing_refs = {value for value in seating.values() if value not in {"F", "X", "S"}}
    while True:
        ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if ref not in existing_refs:
            return ref

def initialize_seating():
    """
    Initializes a seating chart for a plane with 80 rows.
    Each row has 7 columns: seats "A", "B", "C", an aisle, then seats "D", "E", "F".
    The aisle (fourth column) is permanently marked with "X" (non-bookable).
    For rows 79 and 80 in columns D, E, and F, the seats are designated as storage areas ("S").
    All other seat positions are initially free ('F').
    """
    rows = range(1, 81)  # 80 rows
    columns = ['A', 'B', 'C', 'aisle', 'D', 'E', 'F']
    seating = {}
    for row in rows:
        for col in columns:
            seat_id = f"{row}{col}"
            if col == 'aisle':
                seating[seat_id] = 'X'
            elif row in (79, 80) and col in ('D', 'E', 'F'):
                seating[seat_id] = 'S'
            else:
                seating[seat_id] = 'F'
    return seating

def check_availability(seating, seat_id):
    """
    Checks the availability of a seat.
    If the seat is free, it returns that the seat is available.
    Otherwise, it returns that the seat is already booked (without showing the reference).
    """
    if seat_id not in seating:
        return f"Seat {seat_id} does not exist."
    
    status = seating[seat_id]
    if status == 'F':
        return f"Seat {seat_id} is available for booking."
    elif status == 'X':
        return f"Seat {seat_id} is an aisle and is not bookable."
    elif status == 'S':
        return f"Seat {seat_id} is a storage area and is not bookable."
    else:
        # For booked seats, hide the actual booking reference.
        return f"Seat {seat_id} is already booked."

def book_seat(seating, seat_id):
    """
    Books a seat if it is available (status 'F').
    Generates a unique booking reference and updates the seat.
    The booking confirmation message shows the generated reference.
    """
    if seat_id not in seating:
        return f"Seat {seat_id} does not exist."
    
    if seating[seat_id] == 'F':
        ref = generate_booking_reference(seating)
        seating[seat_id] = ref  # Store the booking reference
        return f"Seat {seat_id} has been successfully booked with reference {ref}."
    elif seating[seat_id] == 'X':
        return f"Seat {seat_id} is an aisle and cannot be booked."
    elif seating[seat_id] == 'S':
        return f"Seat {seat_id} is a storage area and cannot be booked."
    else:
        return f"Seat {seat_id} is already booked."

def free_seat(seating, seat_id):
    """
    Frees a booked seat (i.e., a seat that is not 'F', 'X', or 'S'),
    marking it as available ('F').
    """
    if seat_id not in seating:
        return f"Seat {seat_id} does not exist."
    
    if seating[seat_id] == 'X':
        return f"Seat {seat_id} is an aisle and cannot be freed."
    if seating[seat_id] == 'S':
        return f"Seat {seat_id} is a storage area and cannot be freed."
    if seating[seat_id] == 'F':
        return f"Seat {seat_id} is already free."
    
    seating[seat_id] = 'F'
    return f"Seat {seat_id} has been freed and is now available."

def modify_booking(seating, current_seat, new_seat):
    """
    Modifies a booking by changing from current_seat to new_seat.
    Checks that current_seat is booked and new_seat is available.
    If conditions are met, frees the current seat and books the new seat with a new booking reference.
    """
    if current_seat not in seating or new_seat not in seating:
        return "One or both seat IDs do not exist."
    
    if seating[current_seat] == 'F':
        return f"Current seat {current_seat} is not booked."
    
    if seating[new_seat] != 'F':
        return f"New seat {new_seat} is not available for booking."
    
    seating[current_seat] = 'F'
    ref = generate_booking_reference(seating)
    seating[new_seat] = ref
    return f"Booking modified: changed from {current_seat} to {new_seat} with new reference {ref}."

def show_booking_status(seating):
    """
    Prints the current seating chart in a formatted way.
    The chart displays rows 1 to 80 with columns: A, B, C, (blank for aisle), D, E, F.
    If a seat is booked (i.e. its value is not "F", "X", or "S"), it displays "A" instead of the full reference.
    """
    columns = ['A', 'B', 'C', 'aisle', 'D', 'E', 'F']
    header_columns = [col if col != 'aisle' else "" for col in columns]
    
    print("\nCurrent Booking Status:")
    header = "    " + "   ".join(header_columns)
    print(header)
    for row in range(1, 81):
        row_seats = []
        for col in columns:
            seat_id = f"{row}{col}"
            cell = seating[seat_id]
            # For any booked seat, display "A" in the seating chart.
            if cell not in {"F", "X", "S"}:
                cell = "A"
            row_seats.append(cell)
        print(f"{row:>3} " + "   ".join(row_seats))
    print()  # Blank line for spacing

def main():
    """
    Main function to run the seat booking application with modify booking functionality.
    Displays a welcome message and a menu for user input.
    """
    seating = initialize_seating()
    print("Welcome to the Apache Airlines Seat Booking Application!")
    print("We are glad to have you here. Please follow the menu options below to manage your booking.\n\n")
    
    while True:
        print("Menu:")
        print("1. Check availability of seat")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Show booking status")
        print("5. Modify booking")
        print("6. Exit program")
        
        choice = input("Please enter your choice (1-6): ").strip()
        
        if choice == '1':
            show_booking_status(seating)
            seat = input("Enter the seat ID to check (e.g., 2B): ").strip().upper()
            print(check_availability(seating, seat))
        elif choice == '2':
            seat = input("Enter the seat ID to book (e.g., 2B): ").strip().upper()
            print(book_seat(seating, seat))
        elif choice == '3':
            seat = input("Enter the seat ID to free (e.g., 2B): ").strip().upper()
            print(free_seat(seating, seat))
        elif choice == '4':
            show_booking_status(seating)
        elif choice == '5':
            current_seat = input("Enter your current booked seat ID (e.g., 2B): ").strip().upper()
            new_seat = input("Enter the new seat ID you want (e.g., 3A): ").strip().upper()
            print(modify_booking(seating, current_seat, new_seat))
        elif choice == '6':
            print("Thank you for using the Apache Airlines Seat Booking Application. Goodbye!")
            break
        else:
            print("Invalid choice. Please select an option from 1 to 6.")

if __name__ == "__main__":
    main()
