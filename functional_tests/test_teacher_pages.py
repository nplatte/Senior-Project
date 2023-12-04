from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User, Group
from selenium.webdriver.common.action_chains import ActionChains
from django.core.files.uploadedfile import InMemoryUploadedFile
from os import getcwd, path, remove

from teacher_view.models import Course

from time import sleep

class TestTeacherClass(LiveServerTestCase):

    def setUp(self):
        self.test_user = User.objects.create_user('new', 'new@gmail.com', 'password')
        staff_group = Group.objects.create(name='staff')
        staff_group.user_set.add(self.test_user)

        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

    def tearDown(self):
        self.browser.quit()
        upload_file = f'{getcwd()}\\class_htmls\\CS_260.xls'
        if path.exists(upload_file):
            remove(upload_file)
        return super().tearDown()

    def teacher_login(self, username='new', password='password'):
        username_input = self.browser.find_element(By.ID, 'username')
        username_input.send_keys(username)
        password_input = self.browser.find_element(By.ID, 'password')
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

    def test_teacher_can_create_new_class(self):
        # A teacher wants to log in to create a new class
        # they go to the Wartburg MCSP Website and see a log in page
        # They enter the log in information and are taken to the staff view of the website
        self.assertIn('Log In', self.browser.title)
        self.teacher_login()
        sleep(1)
        self.assertIn('Wartburg MCSP Teachers', self.browser.title)
        # they see a nav bar on the top of the page, this displays a Home button, Courses button, an Assignments button, and a Grades Button
        chain = ActionChains(self.browser)
        home_btn = self.browser.find_element(By.ID, 'nav-home')
        courses_btn = self.browser.find_element(By.ID, 'nav-courses')
        #assignments_btn = self.browser.find_element(By.ID, 'nav-assignments')
        grades_btn = self.browser.find_element(By.ID, 'nav-grades')
        # they move to the courses dropdown and reveal other options
        chain.move_to_element(courses_btn).perform()
        add_course_btn = self.browser.find_element(By.ID, 'add-course')
        curr_courses_btn = self.browser.find_element(By.ID, 'curr-courses')
        # They move to see the current courses
        curr_courses_btn.click()
        # uh oh! They don't see any
        curr_courses = self.browser.find_elements(By.ID, 'course_title')
        self.assertEqual(len(curr_courses), 0)
        # they decide to fix this by adding a course
        courses_btn = self.browser.find_element(By.ID, 'nav-courses')
        chain.move_to_element(courses_btn).perform()
        add_course_btn = self.browser.find_element(By.ID, 'add-course')
        add_course_btn.click()
        # This takes them to a new page where they see a form to make courses
        # At the top is an upload for files
        # They select the course file from their computer and press enter
        file_upload = self.browser.find_element(By.ID, 'source_file_input')
        file_upload.send_keys(f'{getcwd()}\\teacher_view\\test_class_htmls\\CS_260.xls')
        save_course = self.browser.find_element(By.ID, 'file-submit')
        save_course.click()
        # the teacher is automatically taken to a new course page where theysee the new course title and stuff
        course = Course.objects.all()[0]
        self.assertEqual(self.browser.title, course.title)
        self.browser.find_element(By.ID, 'course-title')

    def test_teacher_can_edit_courses(self):
        # the teacher logs into the website and edit the class they have previously made
        c = _create_course(self.test_user)
        # they log in
        self.teacher_login()
        sleep(1)
        # they see the nav bar and click the course in the course dropdown
        chain = ActionChains(self.browser)
        courses_btn = self.browser.find_element(By.ID, 'nav-courses')
        chain.move_to_element(courses_btn).perform()
        # they see the button for the course in the dropdown
        course_link = self.browser.find_element(By.ID, f'course-{c.pk}-link')
        course_link.click()
        # they are taken to the course page  
        self.assertEqual(self.browser.title, 'Introduction to Comp')
        # They notice the spelling error and go to correct it
        # they click the edit course info button and are taken to a page with the form info
        link = self.browser.find_element(By.ID, 'edit-course-link')
        link.click() 
        # each field has all the course information
        title_edit = self.browser.find_element(By.ID, 'edit-course-title')
        self.assertEqual(title_edit.get_attribute('value'), c.title)
        term_edit = self.browser.find_element(By.ID, 'edit-course-term')
        self.assertEqual(term_edit.get_attribute('value'), c.term)
        code_edit = self.browser.find_element(By.ID, 'edit-course-code')
        self.assertEqual(code_edit.get_attribute('value'), c.code)
        # the techer clicks the title edit, clears it and sends the right title in
        title_edit.clear()
        title_edit.send_keys('Introduction to Computer Graphics')
        # The teacher is satisfied and clicks the submit button
        btn = self.browser.find_element(By.ID, 'edit-course-submit')
        btn.click()
        # the teacher is taken back to the view course page
        self.assertEqual(self.browser.title, 'Introduction to Computer Graphics')


class TestTeacherAssignment(LiveServerTestCase):

    def setUp(self):
        self.test_user = User.objects.create_user('new', 'new@gmail.com', 'password')
        staff_group = Group.objects.create(name='staff')
        staff_group.user_set.add(self.test_user)
        self.base_path = f'{getcwd()}\\teacher_view\\test_class_htmls'
        self.test_user = User.objects.create_user('new', 'new@gmail.com', 'password')
        self.c = _create_course(self.test_user)

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