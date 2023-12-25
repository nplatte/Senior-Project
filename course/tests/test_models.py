from django.test import TestCase
from course.models import Course, Student
from os import getcwd, path, remove
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse


'''class TestStudentModel(TestCase):

    def setUp(self):
        self.base_path = f'{getcwd()}\\teacher_view\\test_class_htmls'
        file = open(f'{self.base_path}\\CS_260.xls')
        imf = InMemoryUploadedFile(
            file=file,
            field_name='source_file',
            name='CS_260.xls',
            content_type='application/vnd.ms-excel',
            size=14054,
            charset=None,
            content_type_extra={}
        )
        self.test_class = Course.objects.create(
            source_file=imf,
            code='CS 260 01',
            title='Introduction to Computer Graphics',
            term='2019 May Term'
        )

    def test_student_has_name(self):
        test_student = Student.objects.filter(number = 868019).first()
        self.assertEqual(test_student.name, 'Nathan Platte')

    def test_student_saves_to_database(self):
        test_student = Student()
        test_student.add_info(['\t\t\t', 'N', '868019', 'Platte, Nathan Wayne', 'H - History', '\xa0', 'nathan.platte@wartburg.edu', '\xa0', 'Computer Science', 'Fourth Year'])
        
        self.assertEqual(len(Student.objects.all()), 18)
        student = Student.objects.filter(email='nathan.platte@wartburg.edu').first()
        self.assertEqual(student.name, 'Nathan Platte')

    def test_student_has_all_info(self):
        student = Student.objects.filter(name='Trey Hookham').first()
        self.assertEqual(student.email, 'trey.hookham@wartburg.edu')
        self.assertEqual(student.number, 1129224)
        self.assertEqual(student.year, 'Fourth Year')

    def test_student_has_account(self):
        self.assertEqual(User.objects.all().count(), 17)'''


class TestCourseModel(TestCase):
    
    def setUp(self):
        self.base_path = f'{getcwd()}\\teacher_view\\test_class_htmls'
        file = open(f'{self.base_path}\\CS_260.xls')
        imf = InMemoryUploadedFile(
            file=file,
            field_name='source_file',
            name='CS_260.xls',
            content_type='application/vnd.ms-excel',
            size=14054,
            charset=None,
            content_type_extra={}
        )
        self.test_class = Course.objects.create(
            source_file=imf,
            code='CS 260 01',
            title='Introduction to Computer Graphics',
            term='2019 May Term'
        )

    def tearDown(self) -> None:
        upload_file = f'{getcwd()}\\class_htmls\\CS_260.xls'
        if path.exists(upload_file):
            remove(upload_file)
        return super().tearDown()
    
    def test_course_has_info(self):
        self.assertEqual(self.test_class.code, 'CS 260 01')
        self.assertEqual(self.test_class.term, '2019 May Term')
        self.assertEqual(self.test_class.title, 'Introduction to Computer Graphics')

    def test_Course_uses_database(self):
        course = Course.objects.all().first()
        self.assertEqual(course.title, 'Introduction to Computer Graphics')
        self.assertEqual(course.term, '2019 May Term')
        self.assertEqual(course.code, 'CS 260 01')

    def test_Course_model_has_correct_get_absolute_URL(self):
        url = self.test_class.get_absolute_url()
        self.assertEqual(url, reverse('view_course_page', kwargs={'course_id': self.test_class.pk}))
