from django.urls import reverse
from teacher_view.models import Course, Assignment
from teacher_view.forms import CourseModelFileForm, EditCourseForm
from django.utils.timezone import datetime
from os import getcwd, remove, path
from zoneinfo import ZoneInfo
from .inherit import ViewTest



class TestViewCoursePage(ViewTest):

    def setUp(self) -> None:
        super().setUp()
        self.response = self.client.get(reverse('staff_course_page', kwargs={'course_id': self.c.pk}))
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_uses_right_template(self):
        self.assertTemplateUsed(self.response, 'teacher_view/course/view.html')

    def test_passes_navbar_information(self):
        cc = self.response.context['current_courses']
        self.assertIn(self.c, cc)

    def passes_correct_context(self):
        c = self.response.context['course']
        self.assertEqual(c, self.c)
        assignments = self.response.context['assignments']
        self.assertEqual(len(assignments), 0)

    def test_does_not_pass_other_course_assignments(self):
        c2 = self._make_course(self.test_user, 'class 2')
        a1 = Assignment.objects.create(
            title='Make Google',
            description='make Google please',
            due_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=ZoneInfo(key='America/Panama')),
            display_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=ZoneInfo(key='America/Panama')),
            course=self.c
        )
        a2 = Assignment.objects.create(
            title='Make Google 2',
            description='make Google please 2',
            due_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=ZoneInfo(key='America/Panama')),
            display_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=ZoneInfo(key='America/Panama')),
            course=c2
        )
        response = self.client.get(reverse('staff_course_page', kwargs={'course_id': self.c.pk}))
        a_list = response.context['assignments']
        self.assertIn(a1, a_list)
        self.assertNotIn(a2, a_list)


class TestAddCoursePageGET(ViewTest):

    def setUp(self):
        super().setUp()

    def tearDown(self) -> None:
        upload_file = f'{getcwd()}\\class_htmls\\CS_220_May.xls'
        if path.exists(upload_file):
            remove(upload_file)
        return super().tearDown()

    def test_add_course_login_required(self):
        self.client.logout()
        request = self.client.get(reverse('staff_add_course_page'), follow=True)
        self.assertTemplateUsed(request, 'login/login.html')

    def test_page_uses_right_template(self):
        request = self.client.get(reverse('staff_add_course_page'), follow=True)
        self.assertTemplateUsed(request, 'teacher_view/course/create.html')

    def test_add_courses_passes_current_courses_to_navbar(self):
        new_course = self._make_course(self.test_user)
        request = self.client.get(reverse('staff_add_course_page'))
        courses = request.context['current_courses']
        self.assertIn(new_course, courses)

    def test_file_upload_form_is_passed_to_page(self):
        request = self.client.get(reverse('staff_add_course_page'))
        form = request.context['file_form']
        self.assertIsInstance(form, CourseModelFileForm)


class TestAddCoursePagePOST(ViewTest):

    def setUp(self) -> None:
        pth = f'{getcwd()}\\teacher_view\\test_class_htmls\\CS_220_May.xls'
        ofile = open(pth)
        self.data = {
            'source_file': ofile
        }
        return super().setUp()
    
    def tearDown(self) -> None:
        upload_file = f'{getcwd()}\\class_htmls\\CS_220_May.xls'
        if path.exists(upload_file):
            remove(upload_file)
        return super().tearDown()

    def test_file_upload_form_redirects_to_new_course_page(self):
        response = self.client.post(reverse('staff_add_course_page'), follow=True, data=self.data)
        created_course = Course.objects.filter(code='CS 220 01')[0]
        self.assertRedirects(response, f'/teacher/course/{created_course.pk}/')

    def test_file_upload_creates_new_course(self):
        courses = len(Course.objects.all())
        self.assertEqual(1, courses)
        self.client.post(reverse('staff_add_course_page'), follow=True, data=self.data)
        courses = len(Course.objects.all())
        self.assertEqual(2, courses)


class TestEditCoursePageGET(ViewTest):

    def setUp(self):
        super().setUp()
    
    def tearDown(self) -> None:
        upload_dir = f'{getcwd()}\\class_htmls'
        if path.exists(f'{upload_dir}\\CS_260.xls'):
            remove(f'{upload_dir}\\CS_260.xls')
        return super().tearDown()  

    def test_returns_right_html_page(self):
        response = self.client.get(reverse('staff_edit_course_page', kwargs={'course_id': 1}))
        self.assertTemplateUsed(response, 'teacher_view/course/edit.html')

    def test_pass_current_courses_to_navbar(self):
        response = self.client.get(reverse('staff_edit_course_page', kwargs={'course_id': 1}))
        curr_courses = response.context['current_courses']
        edited_course = response.context['course']
        self.assertEqual(len(curr_courses), 1)
        self.assertEqual(self.c, edited_course)
        self.assertIsInstance(edited_course, Course)

    def test_course_uses_right_form_for_editing(self):
        response = self.client.get(reverse('staff_edit_course_page', kwargs={'course_id': 1}))
        edit_form = response.context['edit_form']
        self.assertIsInstance(edit_form, EditCourseForm)

    def test_form_has_existing_course_info(self):
        response = self.client.get(reverse('staff_edit_course_page', kwargs={'course_id': 1}))
        edit_form = response.context['edit_form'].as_p()
        self.assertIn(self.c.title, edit_form)
        self.assertIn(self.c.code, edit_form)


class TestEditCoursePagePOST(ViewTest):

    def setUp(self):
        super().setUp()
        self.data = {
            'title': 'Weird',
            'code': '1234',
            'term': 'May 2024'
        }

    def test_successful_POST_redirects_to_course_page(self):
        response = self.client.post(reverse('staff_edit_course_page', kwargs={'course_id': 1}), data=self.data)
        self.assertRedirects(response, reverse('staff_course_page', kwargs={'course_id': 1}))

    def test_unseccessful_POST_does_not_redirect(self):
        self.data = {
            'title': 'Weird',
            'term': 'May 2024'
        }
        request = self.client.post(reverse('staff_edit_course_page', kwargs={'course_id': 1}), data=self.data)
        self.assertRedirects(request, reverse('staff_course_page', kwargs={'course_id': 1}))

    def test_successful_form_updates_course_info(self):
        self.client.post(reverse('staff_edit_course_page', kwargs={'course_id': self.c.pk}), data=self.data)
        c = Course.objects.get(pk=self.c.pk)
        self.assertNotEqual('test course', c.title)
        self.assertEqual(self.data['title'], c.title)


class TestCoursesViewPage(ViewTest):

    def setUp(self) -> None:
        super().setUp()
    
    def tearDown(self) -> None:
        upload_file = f'{getcwd()}\\class_htmls\\CS_260.xls'
        if path.exists(upload_file):
            remove(upload_file)
        return super().tearDown()
    
    def test_uses_right_template(self):
        response = self.client.get(reverse('staff_courses_page'))
        self.assertTemplateUsed(response, 'teacher_view/course/courses.html')

    def test_passes_navbar_courses(self):
        request = self.client.get(reverse('staff_courses_page'))
        curr_courses = request.context['current_courses']
        self.assertEqual(len(curr_courses), 1)

    def test_passes_logged_in_users_courses(self):
        non_user_course = Course.objects.create(
            code='CS 260 02',
            title='Intro to Comp',
            term='2023 May Term'
        )
        response = self.client.get(reverse('staff_courses_page'))
        all_courses = response.context['all_courses']
        self.assertEqual(1, len(all_courses))
        self.assertNotIn(non_user_course, all_courses)
        self.assertIn(self.c, all_courses)
        