from queue_manager import QueueManager
from datetime import date

def main():
    qm = QueueManager()

    while True:
        print('\n=== IT Helpdesk Ticketing System ===')
        print('1. View all tickets')
        print('2. View ticket details')
        print('3. Add a new ticket')
        print('4. Assign a ticket')
        print('5. Complete/Close a ticket')
        print('6. Exit')

        choice = input('\nEnter choice: ')

        if choice == '1':
            tickets = qm.get_tickets()
            if not tickets:
                print('\nNo tickets currently exist.')
            else:
                print('\nCurrent tickets: ')
                for ticket in tickets:
                    print(ticket)

        elif choice == '2':
            try:
                ticket_id = int(input('\nEnter ticket ID: '))
            except ValueError:
                print('Please enter a valid integer ticket ID.')
                continue
            try:
                ticket = qm.get_ticket(ticket_id)
                print(ticket)
            except ValueError as e:
                print(e)

        elif choice == '3':
            print('\n=== New ticket ===')
            try:
                title = input('Title: ')
                desc = input('Description: ')
                requester = input('Requested by: ')
                priority = int(input('Priority (1-3): '))
                est_time = float(input('Estimated time (hours): '))
                deadline = date.fromisoformat(input('Deadline (YYYY-MM-DD): '))
            except ValueError:
                print('Invalid input. Priority must be a number (1-3), estimated time a number, and deadline in YYYY-MM-DD format.')
                continue
            try:
                new_ticket = qm.add_ticket(title, desc, requester, priority, est_time, deadline)
                print(f'\nTicket #{new_ticket.ticket_id} created successfully.')
            except ValueError as e:
                print(e)

        elif choice == '4':
            try:
                ticket_id = int(input('\nEnter ticket ID to assign: '))
            except ValueError:
                print('Please enter a valid integer ticket ID.')
                continue
            try:
                ticket = qm.get_ticket(ticket_id)
                assignee = input('\nEnter assignee: ')
                qm.assign_ticket(ticket_id, assignee)
                print(f'\nTicket #{ticket_id} assigned successfully to {assignee}')
            except ValueError as e:
                print(e)


        elif choice == '5':
            try:
                ticket_id = int(input('\nEnter ticket ID to close or mark as completed: '))
            except ValueError:
                print('Please enter a valid integer ticket ID.')
                continue
            try:
                ticket = qm.get_ticket(ticket_id)
                status = input('\nMark as Closed or Completed?: ')
                qm.close_ticket(ticket_id, status)
                print(f"\nTicket #{ticket_id}'s status has been changed to {status}")
            except ValueError as e:
                print(e)


        elif choice == '6':
            break

        else:
            print('Invalid choice, enter an option from 1 to 6.')

if __name__ == '__main__':
    main()