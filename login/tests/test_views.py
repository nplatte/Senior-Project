from django.test import  LiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime

class TestLoginPage(LiveServerTestCase):

    '''the login page needs to be the first page people see
    it needs to use the right template
    redirect good users to month view
    redirect bad users to login page'''

    def setUp(self):
        self.test_username = 'winkstiddly'
        self.test_password = 'password123'
        User.objects.create_user(username=self.test_username, email='test@test.com', password=self.test_password)

    def tearDown(self):
        pass

    def test_login_uses_right_template(self):
        response = self.client.get(reverse('login_page'))
        self.assertTemplateUsed(response,'login/login.html')

    def test_login_redirects_to_month_view_on_success(self):
        response = self.client.post(reverse('login_page'), {'username': self.test_username, 'password': self.test_password}, follow=True)
        curr_date = datetime.now()
        self.assertRedirects(response, f'month_view/{curr_date.month}-{curr_date.year}/')

    def test_login_redirects_to_login_on_fail(self):
        response = self.client.post(reverse('login_page'), {'username': self.test_username, 'password': 'wrong_password'}, follow=True)
        self.assertRedirects(response, reverse('login_page'))

    def test_login_required_redirects_to_login_page(self):
        response = self.client.get(reverse('month_page', kwargs={'month': 2, 'year': 2022}), follow=True)
        self.assertTemplateUsed(response, 'login/login.html')
