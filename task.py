from dataclasses import  dataclass
from datetime import date

@dataclass
class Task: # outlining Task object schema and setting some default values
    ticket_id: int
    title: str
    desc: str
    requester: str
    priority: int
    est_time: float
    deadline: date
    status: str = 'Pending'
    assignee: str = 'Unassigned'

    def __str__(self): # formatting print output for CLI
        return (
            f'#{self.ticket_id}: {self.title}\n'
            f'Description: {self.desc}\n'
            f'Requested by: {self.requester}\n'
            f'Priority: {self.priority} | Due: {self.deadline} | Est. time: {self.est_time} hours\n'
            f'Status: {self.status} | Assigned to: {self.assignee}\n'
        )
    
    def to_dict(self): # converting Task object to dictionary to be written to persistence json
        return {
            'ticket_id': self.ticket_id,
            'title': self.title,
            'desc': self.desc,
            'requester': self.requester,
            'priority': self.priority,
            'est_time': self.est_time,
            'deadline': self.deadline.isoformat(),
            'status': self.status,
            'assignee': self.assignee
        }
    
    @classmethod
    def from_dict(cls, data): # return data from dictionary as new Task object
        return cls(
            ticket_id = data['ticket_id'],
            title = data['title'],
            desc = data['desc'],
            requester = data['requester'],
            priority = data['priority'],
            est_time = data['est_time'],
            deadline = date.fromisoformat(data['deadline']),
            status = data['status'],
            assignee = data['assignee'],
        )