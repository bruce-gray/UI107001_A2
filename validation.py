from datetime import date

def validate_str(value, field_name):
    if not value:
        raise ValueError(f'{field_name} Cannot be empty.')

def validate_prio(priority):
    if priority not in [1,2,3]:
        raise ValueError('Priority must be 1, 2 or 3.')
    
def validate_time(est_time):
    if est_time <= 0:
        raise ValueError('The estimated completion time must be greater than 0.')
    
def validate_deadline(deadline):
    if deadline < date.today():
        raise ValueError('Deadline cannot be in the past.')