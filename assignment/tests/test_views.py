from django.urls import reverse
from course.models import Course
from assignment.models import Assignment
from django.utils.timezone import datetime
from zoneinfo import ZoneInfo
from assignment.forms import AssignmentForm
from teacher_view.tests.inherit import ViewTest


TZ = 'America/New_York'


class TestCreateAssignmentPage(ViewTest):
    
    def setUp(self) -> None:
        super().setUp()
        self.response = self.client.get(reverse('add_assignment_page', kwargs={'course_id':self.c.pk}))

    def tearDown(self) -> None:
        return super().tearDown()

    def test_uses_right_template(self):
        self.assertTemplateUsed(self.response, 'assignment/create.html')

    def test_sends_navbar_information(self):
        c = Course.objects.get(pk=1)
        courses = self.response.context['current_courses']
        self.assertIn(c, courses)

    def test_uses_right_form(self):
        form = self.response.context['assignment_form']
        self.assertIsInstance(form, AssignmentForm)


class TestCreateAssignmentPOST(ViewTest):

    def setUp(self) -> None:
        super().setUp()
        self.data = {
            'title': 'make Google',
            'description': 'make google please',
            'due_date': datetime.now(),
            'display_date': datetime(2024, 12, 31, 12, 12, 0)
        }
        self.url = reverse('add_assignment_page', kwargs={'course_id':self.c.pk})
    
    def tearDown(self) -> None:
        return super().tearDown()

    def test_good_form_redirects_to_course_page(self):
        response = self.client.post(self.url, data=self.data, follow=True)
        expected_url = reverse('view_course_page', kwargs={'course_id': self.c.pk})
        self.assertRedirects(response, expected_url)

    def test_good_form_makes_new_assignment(self):
        a_list = Assignment.objects.all()
        self.assertEqual(len(a_list), 0)
        self.client.post(self.url, data=self.data)
        a_list = Assignment.objects.all()
        self.assertEqual(len(a_list), 1)

    def test_bad_form_does_not_redirect(self):
        self.data = {
            'description': 'make google please',
            'due_date': datetime.now(),
            'display_date': datetime(2024, 12, 31, 12, 12, 0)
        }
        response = self.client.post(self.url, data=self.data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'assignment/create.html')


class TestEditAssignmentGET(ViewTest):

    def setUp(self) -> None:
        super().setUp()
        self.a = Assignment.objects.create(
            title='Make Goog',
            description='make Google please',
            due_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=ZoneInfo(key=TZ)),
            display_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=ZoneInfo(key=TZ)),
            course=self.c
        )
        self.url = reverse('edit_assignment_page', kwargs={'assignment_id':self.a.pk})
        self.response = self.client.get(self.url, follow=True)
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_uses_right_template(self):
        self.assertTemplateUsed(self.response, 'assignment/edit.html')

    def test_uses_right_form(self):
        edit_assignment_form = self.response.context['form']
        self.assertIsInstance(edit_assignment_form, AssignmentForm)

    def test_passes_courses_to_nav_bar(self):
        c = Course.objects.get(pk=1)
        courses = self.response.context['current_courses']
        self.assertIn(c, courses)

    def test_edit_assignment_uses_login_page(self):
        self.client.logout()
        response = self.client.get(self.url, follow=True)
        self.assertTemplateNotUsed(response, 'assignment/edit.html')
        self.assertTemplateUsed(response, 'login/login.html')


class TestEditAssignmentPOST(ViewTest):

    def setUp(self) -> None:
        super().setUp()
        self.a = Assignment.objects.create(
            title='Make Goog',
            description='make Google please',
            due_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=ZoneInfo(key=TZ)),
            display_date=datetime(2024, 12, 31, 12, 12, 0, tzinfo=ZoneInfo(key=TZ)),
            course=self.c
        )
        self.data = {
            'title': 'dont make Google',
            'description': 'its evil',
            'due_date': datetime(2024, 1, 31, 12, 12, 0, tzinfo=ZoneInfo(key=TZ)),
            'display_date': datetime(2024, 12, 31, 12, 12, 0, tzinfo=ZoneInfo(key=TZ)),
            'course': self.c.pk
        }
        self.url = reverse('edit_assignment_page', kwargs={'assignment_id': self.a.pk})
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_edits_assignment_on_POST(self):
        self.assertEqual(self.a.title, 'Make Goog')
        self.client.post(self.url, self.data)
        self.a = Assignment.objects.get(pk=self.a.pk)
        self.assertEqual(self.a.title, 'dont make Google')
        self.assertEqual(self.a.description, 'its evil')
        self.assertEqual(1, len(Assignment.objects.all()))

    def test_redirects_course_page_on_POST(self):
        response = self.client.post(self.url, self.data)
        redirect_url = reverse('view_course_page', kwargs={'course_id': self.c.pk})
        self.assertRedirects(response, redirect_url)

    def test_assignment_redirects_to_correct_course_page_on_POST(self):
        new_course = self._make_course(self.test_user, 'Make Yahoo')
        self.data['course'] = new_course.pk
        response = self.client.post(self.url, self.data)
        redirect_url = reverse('view_course_page', kwargs={'course_id': new_course.pk})
        self.assertRedirects(response, redirect_url)

    def test_bad_post_does_not_redirect(self):
        bad_data = {
            'description': 'its evil',
            'due_date': datetime(2024, 1, 31, 12, 12, 0, tzinfo=ZoneInfo(key=TZ)),
            'display_date': datetime(2024, 12, 31, 12, 12, 0, tzinfo=ZoneInfo(key=TZ)),
            'course': self.c.pk
        }
        response = self.client.post(self.url, bad_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assignment/edit.html')

    def test_time_submitted_converted_to_UTC(self):
        self.client.post(self.url, self.data)
        utc_time = datetime(2024, 12, 31, 12, 12, 0)
        self.assertEqual(utc_time.strftime("%Y-%m-%d %H:%M:%S"), self.a.due_date.strftime("%Y-%m-%d %H:%M:%S"))
