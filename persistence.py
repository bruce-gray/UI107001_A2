import json
from task import Task

def load_tickets(): # loads tickets.json if it exists
    try:
        with open('tickets.json', 'r') as f:
            data = json.load(f)
            return [Task.from_dict(ticket) for ticket in data] # convert dictionaries back into Task objects
    except FileNotFoundError:
        return []

def save_tickets(tickets): # writes tickets to tickets.json
    with open('tickets.json', 'w') as f:
        json.dump([ticket.to_dict() for ticket in tickets], f, indent=4) # converts each Task object to a dictionary before writing

def archive_ticket(ticket): # appends a single ticket to archive.json when marked as complwted or closed
    try:
        with open('archive.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    data.append(ticket.to_dict()) # convert Task to dictionary and append to archive list
    with open('archive.json', 'w') as f:
        json.dump(data, f, indent=4) # write full archive with append back to file