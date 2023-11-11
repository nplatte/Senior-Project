from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import string, random
from django.urls import reverse


class Student(models.Model):
    
    name = models.CharField(default = '', max_length = 50)
    email = models.CharField(default = '', max_length = 40)
    number = models.IntegerField(default = '')
    year = models.CharField(default = '', max_length = 19)

    def add_info(self, info):
        self.name_parts = info[3].split()
        self.name = self.name_parts[1] + ' ' + self.name_parts[0][:-1]
        self.email = info[6]
        self.number = int(info[2])
        self.year = info[-1]
        self.save()

    def create_account(self):
        password = self.password_gen(8)
        user = User.objects.create(
            username=self.name_parts[1] + '.' + self.name_parts[0][:-1], 
            password=password, 
            email=self.email,
            first_name=self.name_parts[1],
            last_name=self.name_parts[0][:-1]
            )

    def password_gen(self, size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def __str__(self):
        return self.name


class Course(models.Model):
    source_file = models.FileField(upload_to='class_htmls', default='')
    code = models.CharField(default='', max_length=20, blank=True)
    title = models.CharField(default='', max_length=50, blank=True)
    term = models.CharField(default='', max_length=60, blank=True)
    students = models.ManyToManyField(Student, related_name='enrolled_students')
    course_instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('staff_course_page', kwargs={'course_id': self.pk})

    '''def create(self, file=None):
        course_info = self.org_info(file)
        if Course.objects.filter(code=course_info[2], term=course_info[0][11:], title=course_info[3][:course_info[3].find(' (')]).count() < 1:
            self.add_info(course_info, self)
        else:
            course = Course.objects.filter(code=course_info[2], term=course_info[0][11:], title=course_info[3][:course_info[3].find(' (')]).first()
            course.delete()
            self.add_info(course_info, self)
        
    def add_students(self, Course_model):
        students_in_db = Student.objects.all()
        for info in self.student_info:
            student_in_db = students_in_db.filter(number=info[2])
            if student_in_db.count() == 1:
                new_student = student_in_db.first()
            elif student_in_db.count() == 0:
                new_student = Student()
                new_student.add_info(info)
                new_student.create_account()
            Course_model.students.add(new_student)

    def org_info(self, file=None):
        if file is None:
            file = self.source_file.path
        self.Parser = MyHTMLParser()      
        self.Parser.feed_file(file)
        self.Parser.sort_data_list('\t\t\t', '\t\t')
        return self.Parser.data_list[0][1].split(' | ')

    def add_info(self, course_info, course):
        course.student_info = self.Parser.data_list[2:]
        course.code = course_info[2]
        course.term = course_info[0][11:]
        course.title = course_info[3][:course_info[3].find(' (')]
        course.save()
        course.add_students(course)
        course.save()'''

    def __str__(self):
        return self.title


class Assignment(models.Model):
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50, default='')
    description = models.TextField(default='')
    due_date = models.DateTimeField(blank=True, null=True)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title


class Handout(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=25, default='')
    handout = models.FileField()
    post_date = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.title


class Grade(models.Model):

    student = models.ForeignKey('teacher_view.Student', models.CASCADE, null=True)
    course = models.ForeignKey('teacher_view.Course', models.CASCADE, null=True)
    catagories = models.CharField(default='', max_length=200)
    student_scores = models.CharField(default='', max_length=200)
    points_possible = models.CharField(default='', max_length=200)
    letter_grade = models.CharField(default='', max_length=5)

    def __str__(self):
        return self.student.name