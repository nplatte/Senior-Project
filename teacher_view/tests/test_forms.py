from django.test import TestCase
from django.utils.timezone import datetime
from teacher_view.forms import AssignmentForm
from zoneinfo import ZoneInfo
        

class TestAssignmentForm(TestCase):

    def setUp(self) -> None:
        self.data = {
            'title': 'Test Assignment',
            'description': 'this is bout the assignment',
            'due_date': datetime(2024, 12, 30, 12, 12, 1, tzinfo=ZoneInfo(key='America/Panama')),
            'display_date': datetime(2024, 12, 23, 12, 12, 1, tzinfo=ZoneInfo(key='America/Panama'))
        }
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_good_form_is_valid(self):
        form = AssignmentForm(self.data)
        self.assertTrue(form.is_valid())

    def test_form_has_correct_ids(self):
        form = AssignmentForm(self.data)
        self.assertIn('id="a-title-input"', form.as_p())
        self.assertIn('id="a-due-date-input"', form.as_p())
        self.assertIn('id="a-description-input"', form.as_p())
        self.assertIn('id="a-display-date-input"', form.as_p())

    def test_form_makes_assignment(self):
        form = AssignmentForm(self.data)
        a = form.save()
        self.assertEqual(a.title, self.data['title'])
        self.assertEqual(a.description, self.data['description'])
        self.assertEqual(a.due_date, self.data['due_date'])
        self.assertEqual(a.display_date, self.data['display_date'])


