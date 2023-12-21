from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from teacher_view.models import Assignment

from functional_tests.inherits import BasicSeleniumTest
from time import sleep
from django.utils.timezone import datetime
import zoneinfo


TZ = 'America/Chicago'


class TestTeacherAssignment(BasicSeleniumTest):

    def setUp(self):
        super().setUp()
        self.c = self._create_course()
        self.browser.get(f'{self.live_server_url}')

    def tearDown(self) -> None:
        self.browser.quit()
        super().tearDown()
    
    def test_teacher_can_make_assignment(self):
        # the teacher logs on to the teacher portal and decides to create an assignment
        self.assertIn('Log In', self.browser.title)
        self._teacher_login()
        self.assertEqual(self.browser.title, 'Wartburg MCSP Teachers')
        # they see the course they want to add an assingment to
        chain = ActionChains(self.browser)
        courses_btn = self.browser.find_element(By.ID, 'nav-courses')
        chain.move_to_element(courses_btn).perform()
        # they see the button for the course in the dropdown
        course_link = self.browser.find_element(By.ID, f'course-{self.c.pk}-link')
        course_link.click()
        # they click on it and are taken to the course page
        self.assertEqual(self.browser.title, self.c.title)
        assignments = self.browser.find_elements(By.CLASS_NAME, 'assignment')
        self.assertEqual(len(assignments), 1)
        # they click create assignment and are taken to a new page to submit an assignment to
        new_assignment_btn = self.browser.find_element(By.ID, 'create-assignment-link')
        new_assignment_btn.click()
        self.assertEqual(self.browser.title, 'New Assignment')
        # they add a title
        title_input = self.browser.find_element(By.ID, 'a-title-input')
        title_input.send_keys('create google')
        # they add a due date
        display_date_input = self.browser.find_element(By.ID, 'a-display-date-input')
        # they add a display date
        due_date_input = self.browser.find_element(By.ID, 'a-due-date-input')
        # they select the course
        course_selector = Select(self.browser.find_element(By.ID, 'a-course-input'))
        course_selector.select_by_visible_text(f'{self.c.title}')
        # they add a discription
        description_input = self.browser.find_element(By.ID, 'a-description-input')
        description_input.send_keys('google doesnt work, make a new one')
        # they then submit the assignment
        a_submit = self.browser.find_element(By.ID, 'a-submit-btn')
        a_submit.click()
        # they then go to the course view and see the new assignment listed
        self.assertEqual(self.browser.title, self.c.title)
        assignments = self.browser.find_elements(By.CLASS_NAME, 'assignment')
        self.assertEqual(len(assignments), 2)

    def test_teacher_can_edit_assignment(self):
        self.test_a = Assignment.objects.create(
            title='Make Goog',
            description='make Google please',
            due_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
            display_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')),
            course=self.c
        )
        # the teacher logs on to the teacher portal and decides to edit an assignment title and due date
        central_due_date = datetime(2024, 12, 31, 6, 12, 0).strftime("%Y-%m-%d %H:%M:%S")
        self.assertIn('Log In', self.browser.title)
        self._teacher_login()
        self.assertEqual(self.browser.title, 'Wartburg MCSP Teachers')
        # they set the timezone
        btn = self.browser.find_element(By.ID, 'set_tz')
        btn.click()
        # they select the navbar
        chain = ActionChains(self.browser)
        courses_btn = self.browser.find_element(By.ID, 'nav-courses')
        chain.move_to_element(courses_btn).perform()
        # they see the button for the course in the dropdown
        course_link = self.browser.find_element(By.ID, f'course-{self.c.pk}-link')
        course_link.click()
        assignment =  self.browser.find_element(By.ID, f'assignment_{self.test_a.pk}')
        self.assertEqual(assignment.text, self.test_a.title)
        a_due_date = self.browser.find_element(By.ID, f'assignment_{self.test_a.pk}_due_date')
        self.assertEqual(a_due_date.text, f'Due Date: {central_due_date}')
        # next to the assignment is an edit assignment button
        edit_link = self.browser.find_element(By.ID, f'edit_assignment_{self.test_a.pk}')
        edit_link.click()
        # they click it and are taken to a new page
        self.assertEqual(f'Edit {self.test_a.title}', self.browser.title)
        # they find the title box with the current assignment name already filled in
        title_input = self.browser.find_element(By.ID, 'a-title-input')
        title_input.clear()
        # they change it to the right name
        title_input.send_keys('Make Google')
        # they change the date to next week
        due_date_input = self.browser.find_element(By.ID, 'a-due-date-input')
        due_date_input.clear()
        d8 = datetime(2023, 12, 31, 18, 12, 0)  
        new_date = d8.strftime("%Y-%m-%d %I:%M:%S")
        due_date_input.send_keys(new_date)
        # satisfied, they click submit
        submit_btn = self.browser.find_element(By.ID, 'edit-a-submit')
        submit_btn.click()
        # they are taken back to the course view page where they see the assignment with its new title
        self.assertEqual(self.browser.title, self.c.title)
        edited_a = Assignment.objects.get(pk=self.test_a.pk)
        new_a = self.browser.find_element(By.ID, f'assignment_{self.test_a.pk}')
        self.assertEqual(new_a.text, edited_a.title)
        # the due date is also updated to next week
        a_due_date = self.browser.find_element(By.ID, f'assignment_{self.test_a.pk}_due_date')
        self.assertEqual(a_due_date.text, f'Due Date: {new_date}')
        # satisfied, they log off

    