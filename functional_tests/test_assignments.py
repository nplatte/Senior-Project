from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from functional_tests.inherits import BasicSeleniumTest


class TestTeacherAssignment(BasicSeleniumTest):

    def setUp(self):
        super().setUp()
        self.c = self._create_course()
        self.browser.get(self.live_server_url)

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
        date_input = self.browser.find_element(By.ID, 'a-date-input')
        # they add a display date
        due_date_input = self.browser.find_element(By.ID, 'a-due-date-input')
        # they add a discription
        description_input = self.browser.find_element(By.ID, 'a-desc-input')
        description_input.send_keys('google doesnt work, make a new one')
        # they then submit the assignment
        a_submit = self.browser.find_element(By.ID, 'a-submit-btn')
        a_submit.click()
        # they then go to the course view and see the new assignment listed
        self.assertEqual(self.browser.title, self.c.title)
        assignments = self.browser.find_elements(By.CLASS, 'assignment')
        self.assertEqual(len(assignments), 2)

    def test_teacher_can_edit_assignment(self):
        pass

    