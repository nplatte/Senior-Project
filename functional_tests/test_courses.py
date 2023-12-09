from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from os import getcwd

from teacher_view.models import Course
from functional_tests.inherits import BasicSeleniumTest


class TestTeacherClass(BasicSeleniumTest):

    def setUp(self):
        super().setUp()
        self.browser.get(f'{self.live_server_url}')

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def test_teacher_can_create_new_class(self):
        # A teacher wants to log in to create a new class
        # they go to the Wartburg MCSP Website and see a log in page
        # They enter the log in information and are taken to the staff view of the website
        self.assertIn('Log In', self.browser.title)
        self._teacher_login()
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
        c = self._create_course(self.test_user)
        # they log in
        self.assertEqual('Log In', self.browser.title)
        self._teacher_login()
        self.assertEqual('Wartburg MCSP Teachers', self.browser.title)
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