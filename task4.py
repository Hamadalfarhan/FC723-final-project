# FC723 Project – Seat Booking Application 

# This application simulates a seat booking system for Apache Airlines.

# It provides a menu for checking seat availability, booking a seat, freeing a seat, showing booking status, and exiting the program.

# The seating chart simulates a plane with 80 rows, an aisle inserted between seats C and D,

def initialize_seating():
    """
    Initializes a seating chart for a plane with 80 rows.
    Each row has 7 columns: seats "A", "B", "C", an aisle, then seats "D", "E", "F".
    The aisle (the fourth column) is permanently marked with "X" (non-bookable).
    For rows 79 and 80 in columns D, E, and F, the seats are designated as storage areas ("S").
    All other seat positions are initially free ('F').
    """
    rows = range(1, 81)  # 80 rows of seats
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
    Returns a message indicating if the seat can be booked.
    """
    if seat_id not in seating:
        return f"Seat {seat_id} does not exist."
    
    status = seating[seat_id]
    if status == 'F':
        return f"Seat {seat_id} is available for booking."
    elif status == 'A':
        return f"Seat {seat_id} is already booked."
    elif status == 'X':
        return f"Seat {seat_id} is an aisle and is not bookable."
    elif status == 'S':
        return f"Seat {seat_id} is a storage area and is not bookable."
    else:
        return f"Seat {seat_id} has an unknown status."

def book_seat(seating, seat_id):
    """
    Books a seat if it is available (status 'F').
    If booking is successful, the seat status is updated to 'A'.
    Returns a message indicating the outcome.
    """
    if seat_id not in seating:
        return f"Seat {seat_id} does not exist."
    
    if seating[seat_id] == 'F':
        seating[seat_id] = 'A'
        return f"Seat {seat_id} has been successfully booked."
    elif seating[seat_id] == 'X':
        return f"Seat {seat_id} is an aisle and cannot be booked."
    elif seating[seat_id] == 'S':
        return f"Seat {seat_id} is a storage area and cannot be booked."
    else:
        return f"Seat {seat_id} cannot be booked because it is already booked."

def free_seat(seating, seat_id):
    """
    Frees a booked seat (status 'A'), marking it as available ('F').
    Returns a message indicating the outcome.
    """
    if seat_id not in seating:
        return f"Seat {seat_id} does not exist."
    
    if seating[seat_id] == 'A':
        seating[seat_id] = 'F'
        return f"Seat {seat_id} has been freed and is now available."
    elif seating[seat_id] == 'X':
        return f"Seat {seat_id} is an aisle and cannot be freed."
    elif seating[seat_id] == 'S':
        return f"Seat {seat_id} is a storage area and cannot be freed."
    else:
        return f"Seat {seat_id} is already free."

def show_booking_status(seating):
    """
    Prints the current seating chart in a formatted way.
    The chart displays rows 1 to 80 with columns: A, B, C, (blank for aisle), D, E, F.
    """
    columns = ['A', 'B', 'C', 'aisle', 'D', 'E', 'F']
    # Prepare header row, replacing "aisle" with a blank.
    header_columns = [col if col != 'aisle' else "" for col in columns]
    
    print("\nCurrent Booking Status:")
    header = "    " + "   ".join(header_columns)
    print(header)
    for row in range(1, 81):
        row_seats = []
        for col in columns:
            seat_id = f"{row}{col}"
            row_seats.append(seating[seat_id])
        print(f"{row:>3} " + "   ".join(row_seats))
    print()  # Blank line for spacing

def main():
    """
    Main function to run the seat booking application.
    Displays a welcome message, a menu, and processes user input until the program is terminated.
    """
    seating = initialize_seating()
    # Lower the welcome text by adding extra newlines for visibility.
    print("Welcome to the Apache Airlines Seat Booking Application!")
    print("We are glad to have you here. Please follow the menu options below to manage your booking.\n\n")
    
    while True:
        print("Menu:")
        print("1. Check availability of seat")
        print("2. Book a seat")
        print("3. Free a seat")
        print("4. Show booking status")
        print("5. Exit program")
        
        choice = input("Please enter your choice (1-5): ").strip()
        
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
            print("Thank you for using the Apache Airlines Seat Booking Application. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please select an option from 1 to 5.")

if __name__ == "__main__":
    main()
