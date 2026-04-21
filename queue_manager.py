import heapq
import task
import persistence
import validation

def merge_sort(lst): # sorts a list of tickets by deadline
    # base case - list of 1 or 0 elements doesn't need to be sorted
    if len(lst) <= 1:
        return lst
    
    # split the list in half
    mid = len(lst) // 2
    left = merge_sort(lst[:mid])
    right = merge_sort(lst[mid:])

    # merge the sorted halves
    return merge(left,right)

def merge(left,right): # merges two halves by comparing priority and thenm deadlines, appends the earlier deadline first
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if (left[i].priority, left[i].deadline) <= (right[j].priority, right[j].deadline):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    # append any remaining elements from either half
    result += left[i:]
    result += right[j:]
    return result

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
            new_id = max(ticket.ticket_id for ticket in self.tickets) + 1 # generate the next sequential ID from existing tickets

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

        return new_ticket

    def assign_ticket(self, ticket_id, assignee):
        for i in range(len(self.tickets)):
            if self.tickets[i].ticket_id == ticket_id:
                self.tickets[i].assignee = assignee
                self.tickets[i].status = 'In Progress'
                self.rebuild_heap()
                persistence.save_tickets(self.tickets)
                break
        else:
            raise ValueError(f'Ticket with ID {ticket_id} not found.')
        
    def close_ticket(self, ticket_id, status):
        status = status.strip().capitalize()
        if status not in ['Completed', 'Closed']:
            raise ValueError('Status must be Completed or Closed.')
        for i in range(len(self.tickets)):
            if self.tickets[i].ticket_id == ticket_id:
                self.tickets[i].status = status
                persistence.archive_ticket(self.tickets[i])
                self.tickets.remove(self.tickets[i])
                self.rebuild_heap()
                persistence.save_tickets(self.tickets)
                break
        else:
            raise ValueError(f'Ticket with ID {ticket_id} not found.')
        
    def get_tickets(self):
        tickets = [item[3] for item in sorted(self.heap)] # extracts Task objects from heap tuples in heap order
        return merge_sort(tickets) # apply merge sort as a secondary sort by deadline for tasks with equal priority
    
    def get_ticket(self, ticket_id):
        for i in range(len(self.tickets)):
            if self.tickets[i].ticket_id == ticket_id:
                return(self.tickets[i])
        else:
            raise ValueError(f'Ticket with ID {ticket_id} not found.')