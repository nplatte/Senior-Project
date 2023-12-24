from django.urls import reverse
from .inherit import ViewTest


class TestHomePage(ViewTest):

    def setUp(self):
        super().setUp()

    def test_home_page_uses_right_template(self):
        request = self.client.get(reverse('staff_home_page'), follow=True)
        self.assertTemplateUsed(request, 'teacher_view/home.html')

    def test_home_page_passes_current_classes_for_navbar(self):
        
        request = self.client.get(reverse('staff_home_page'))
        course_list = request.context['current_courses']
        self.assertIn(self.c, course_list)


class TestProfilePage(ViewTest):

    def setUp(self):
        super().setUp()

    def test_profile_page_uses_right_template(self):
        request = self.client.get(reverse('staff_profile_page'), follow=True)
        self.assertTemplateUsed(request, 'teacher_view/profile.html')

    def test_profile_page_passes_current_courses_to_navbar(self):
        request = self.client.get(reverse('staff_profile_page'))
        course_list = request.context['current_courses']
        self.assertIn(self.c, course_list)