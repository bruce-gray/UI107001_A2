import unittest
from task import Task
from datetime import date
import validation
from queue_manager import QueueManager
from unittest.mock import patch

# TASK.PY TESTS

class TestTask(unittest.TestCase):
    def setUp(self):
        self.task = Task(
            ticket_id = 1,
            title = 'Test Ticket',
            desc = 'This tests the Task dataclass from task.py',
            requester = 'Bruce',
            priority = 1,
            est_time = 0.5,
            deadline = date(2026,5,8)
        )

    def test_default_values(self):
        self.assertEqual(self.task.status, 'Pending')
        self.assertEqual(self.task.assignee, 'Unassigned')

    def test_to_dict(self):
        result = self.task.to_dict()
        self.assertDictEqual(result, {
            'ticket_id': 1,
            'title': 'Test Ticket',
            'desc': 'This tests the Task dataclass from task.py',
            'requester': 'Bruce',
            'priority': 1,
            'est_time': 0.5,
            'deadline': '2026-05-08',
            'status': 'Pending',
            'assignee': 'Unassigned'
        })

    def test_from_dict(self):
        data = {
            'ticket_id': 1,
            'title': 'Test Ticket',
            'desc': 'This tests the Task dataclass from task.py',
            'requester': 'Bruce',
            'priority': 1,
            'est_time': 0.5,
            'deadline': '2026-05-08',
            'status': 'Pending',
            'assignee': 'Unassigned'
        }
        result = Task.from_dict(data)
        self.assertEqual(result.ticket_id, 1)
        self.assertEqual(result.title, 'Test Ticket')
        self.assertEqual(result.desc, 'This tests the Task dataclass from task.py')
        self.assertEqual(result.requester, 'Bruce')
        self.assertEqual(result.priority, 1)
        self.assertEqual(result.est_time, 0.5)
        self.assertEqual(result.deadline, date(2026,5,8))
        self.assertEqual(result.status, 'Pending')
        self.assertEqual(result.assignee, 'Unassigned')

# VALIDATION.PY TESTS

class TestValidation(unittest.TestCase):
    def test_validate_str_valid(self):
        validation.validate_str('Test Ticket', 'Title')

    def test_validate_str_empty(self):
        with self.assertRaises(ValueError):
            validation.validate_str('', 'Title')

    def test_validate_prio_valid(self):
        validation.validate_prio(1)
        validation.validate_prio(2)
        validation.validate_prio(3)

    def test_validate_prio_invalid(self):
        with self.assertRaises(ValueError):
            validation.validate_prio(0)
        with self.assertRaises(ValueError):
            validation.validate_prio(4)

    def test_validate_time_valid(self):
        validation.validate_time(0.1)
        validation.validate_time(1)
        validation.validate_time(3.14)
        validation.validate_time(20)

    def test_validate_time_invalid(self):
        with self.assertRaises(ValueError):
            validation.validate_time(0)
        with self.assertRaises(ValueError):
            validation.validate_time(-1)

    def test_validate_deadline_valid(self):
        validation.validate_deadline(date(2027,5,8))

    def test_validate_deadline_invalid(self):
        with self.assertRaises(ValueError):
            validation.validate_deadline(date(2025,5,8))

# QUEUE_MANAGER.PY TESTS
# uses unittest.mock to patch persistence methods so that tests dont touch real files

class TestQueueManager(unittest.TestCase):
    def setUp(self):
        with patch('persistence.load_tickets', return_value=[]):
            with patch('persistence.save_tickets'):
                self.qm = QueueManager()

    def test_add_ticket(self):
        with patch('persistence.save_tickets'):
            self.qm.add_ticket(
                title='Test Ticket',
                desc='Test description',
                requester='Bruce',
                priority=1,
                est_time=1.5,
                deadline=date(2027,5,8)
            )
        tickets = self.qm.get_tickets()
        self.assertEqual(len(tickets), 1)
        self.assertEqual(tickets[0].ticket_id, 1)
        self.assertEqual(tickets[0].title, 'Test Ticket')
        self.assertEqual(tickets[0].desc, 'Test description')
        self.assertEqual(tickets[0].requester, 'Bruce')
        self.assertEqual(tickets[0].priority, 1)
        self.assertEqual(tickets[0].est_time, 1.5)
        self.assertEqual(tickets[0].deadline, date(2027,5,8))
        self.assertEqual(tickets[0].status, 'Pending')
        self.assertEqual(tickets[0].assignee, 'Unassigned')

    def test_assign_ticket(self):
        with patch('persistence.save_tickets'):
            self.qm.add_ticket(
                title='Test Ticket',
                desc='Test description',
                requester='Bruce',
                priority=1,
                est_time=1.5,
                deadline=date(2027,5,8)
            )
            self.qm.assign_ticket(1, 'BG')
            ticket = self.qm.get_ticket(1)
            self.assertEqual(ticket.assignee, 'BG')
            self.assertEqual(ticket.status, 'In Progress')

    def test_close_ticket_valid(self):
        with patch('persistence.save_tickets'):
            with patch('persistence.archive_ticket'):
                self.qm.add_ticket(
                    title='Test Ticket',
                    desc='Test description',
                    requester='Bruce',
                    priority=1,
                    est_time=1.5,
                    deadline=date(2027,5,8)
                )
                self.qm.close_ticket(1, 'Completed')
                tickets = self.qm.get_tickets()
                self.assertEqual(tickets, [])

    def test_close_ticket_invalid(self):
        with patch('persistence.save_tickets'):
            with patch('persistence.archive_ticket'):
                self.qm.add_ticket(
                    title='Test Ticket',
                    desc='Test description',
                    requester='Bruce',
                    priority=1,
                    est_time=1.5,
                    deadline=date(2027,5,8)
                )
                with self.assertRaises(ValueError):
                    self.qm.close_ticket(2, 'Completed')

    def test_get_ticket(self):
        with patch('persistence.save_tickets'):
            self.qm.add_ticket(
                    title='Test Ticket',
                    desc='Test description',
                    requester='Bruce',
                    priority=1,
                    est_time=1.5,
                    deadline=date(2027,5,8)
                )
            ticket = self.qm.get_ticket(1)
            self.assertEqual(ticket.ticket_id, 1)
            self.assertEqual(ticket.title, 'Test Ticket')
            self.assertEqual(ticket.desc, 'Test description')
            self.assertEqual(ticket.requester, 'Bruce')
            self.assertEqual(ticket.priority, 1)
            self.assertEqual(ticket.est_time, 1.5)
            self.assertEqual(ticket.deadline, date(2027,5,8))
            self.assertEqual(ticket.status, 'Pending')
            self.assertEqual(ticket.assignee, 'Unassigned')

    def test_invalid_priority(self):
        with patch('persistence.save_tickets'):
            with self.assertRaises(ValueError):
                self.qm.add_ticket(
                    title='Test Ticket',
                    desc='Test description',
                    requester='Bruce',
                    priority=4,
                    est_time=1.5,
                    deadline=date(2027,5,8)
                )

if __name__ == '__main__':
    unittest.main()