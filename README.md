# UI107001_A2
## UI107001 - Assessment 2 - Individual Project

# IT Helpdesk Ticketing System
A command line ticketing system built with Python. Tickets are managed using a min-heap priority queue and sorted using a merge sort.

- **main.py** - CLI  
- **task.py** - Task dataclass
- **persistence.py** - Handles loading/saving/archiving of tickets in JSON  
- **queue_manager.py** - Priority queue and ticket management methods  
- **validation.py** - Input validation  
- **tests.py** - Unit tests for task, validation and queue_manager  

## Requirements
- Python installed https://www.python.org/downloads/

## Running the program:
```bash
python main.py
```

## Running unit tests:
```bash
python tests.py
```

## Build the executable:
Install PyInstaller if not already installed:
```bash
pip install pyinstaller
```
Then build:
```bash
pyinstaller --onefile main.py
```
The executable will be created in the dist/ folder.

## How to use
On launch, you will be presented with a menu containing 6 options. Enter a number from 1 to 6 to complete the corresponding action.  
**1. View all tickets** - Shows a summary of all currently existing tickets  
**2. View ticket details** - Enter the ID of an existing ticket to view its full details  
**3. Add a new ticket** - Create a new ticket by entering information when prompted  
**4. Assign a ticket** - Enter a ticket ID and name to assign the ticket and mark its status as In Progress  
**5. Complete/Close a ticket** - Update a ticket to 'Completed' or 'Closed' to remove it from the queue and archive it  
**6. Exit** - Exits the application  