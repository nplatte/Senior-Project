from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from django.core.files.uploadedfile import InMemoryUploadedFile
from os import getcwd, path, remove

from teacher_view.models import Course
from functional_tests.inherits import BasicSeleniumTest

from time import sleep


class TestTeacherAssignment(BasicSeleniumTest):

    def setUp(self):
        super().setUp()
        self.base_path = f'{getcwd()}\\teacher_view\\test_class_htmls'
        self.c = _create_course(self.test_user)
        self.browser.get(self.live_server_url)

    def tearDown(self) -> None:
        self.browser.quit()
        upload_file = f'{getcwd()}\\class_htmls\\CS_260.xls'
        if path.exists(upload_file):
            remove(upload_file)
        return super().tearDown()
    
    def test_teacher_can_make_assignment(self):
        # the teacher logs on to the teacher portal and decides to create an assignment
        self.teacher_login()
        # they see the course they want to add an assingment to
        chain = ActionChains(self.browser)
        courses_btn = self.browser.find_element(By.ID, 'nav-courses')
        chain.move_to_element(courses_btn).perform()
        # they see the button for the course in the dropdown
        course_link = self.browser.find_element(By.ID, f'course-{self.c.pk}-link')
        course_link.click()
        # they click on it and are taken to the course page
        self.assertEqual(self.browser.title, self.c.title)
        assignments = self.browser.find_elements(By.CLASS, 'assignment')
        self.assertEqual(len(assignments), 0)
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
        self.assertEqual(len(assignments), 1)

    def test_teacher_can_edit_assignment(self):
        pass

    def teacher_login(self, username='new', password='password'):
        username_input = self.browser.find_element(By.ID, 'username')
        username_input.send_keys(username)
        password_input = self.browser.find_element(By.ID, 'password')
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

    
def _create_course(instructor):
    base_path = f'{getcwd()}\\teacher_view\\test_class_htmls'
    file = open(f'{base_path}\\CS_260.xls')
    imf = InMemoryUploadedFile(
        file=file,
        field_name='source_file',
        name='CS_260.xls',
        content_type='application/vnd.ms-excel',
        size=14054,
        charset=None,
        content_type_extra={}
    )
    c = Course.objects.create(
        source_file=imf,
        code='CS 260 01',
        title='Introduction to Comp',
        term='2024 May Term',
        course_instructor=instructor
    )
    return c