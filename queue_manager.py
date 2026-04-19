import heapq
import task
import persistence
import validation

class QueueManager:
    def __init__(self):
        self.tickets = persistence.load_tickets() # flat list for linear search
        self.rebuild_heap()

    def rebuild_heap(self):
        self.heap = [] # heap for priority ordering
        for ticket in self.tickets: # for each ticket, orders them based on priority (or deadline as a tiebreaker (or ticket_id as a tiebreaker if both match))
            heapq.heappush(self.heap, (ticket.priority, ticket.deadline, ticket.ticket_id, ticket))

    def add_ticket(self, title, desc, requester, priority, est_time, deadline):
        if self.tickets == []:
            new_id = 1
        else:
            new_id = max(ticket.ticket_id for ticket in self.tickets) + 1

        # validate inputs
        validation.validate_str(title, 'Title')
        validation.validate_str(desc, 'Description')
        validation.validate_str(requester, 'Requester')
        validation.validate_prio(priority)
        validation.validate_time(est_time)
        validation.validate_deadline(deadline)

        # build new ticket from inputs
        new_ticket = task.Task(
            ticket_id = new_id,
            title = title,
            desc = desc,
            requester = requester,
            priority = priority,
            est_time = est_time,
            deadline = deadline
        )

        # add ticket to flat list and heap, save
        self.tickets.append(new_ticket)
        heapq.heappush(self.heap, (new_ticket.priority, new_ticket.deadline, new_ticket.ticket_id, new_ticket))
        persistence.save_tickets(self.tickets)