# Wartburg MCSP Teacher Portal

## Project Description

This is an updated portal for teachers to create Math, Computer SCience and Physics courses for students. Additionally, they can add assignments for courses and view student submissions.

This is a Django project, so it is made up of a core project and a some apps. The project folder is teacher_portal and the apps are teacher_view, assignment, course, and login. Each app/project is tested using Test Driven Development, the functional tests using selenium are found in the functional_tests folder and the unit tests for each app are found in APP_NAME/tests folder. The unit tests are split into model tests, form tests and view tests for more seperation and better readability.

## Project Installation

1. Fork the repository into your personal Github account
2. Clone the fork onto your local machine
3. create a virtual environment of at least Python 3.9
4. after activating the virtual environment, run `pip install -r requirements.txt`

You are done with the installation and should be able to run the project. You can test this with `python manage.py test` to run all of the tests present on the master branch, or `python manage.py runserver` to run the server manually.


## Breakdown of Apps

### teacher_view
This app is the base app of the project. It holds the base template, which all of the other html templates are based off of. It has the basic landing page and the teacher profile page. In addition, it has the css files that are applied to all of the templates on the website.

### course
This app has the Course model and the Student model, the forms for creating a course and editing a course, and the views for handling form data for course creation and course editing.

### assignment
This app has the Assignment model, the forms for creating a new assignment for a course, editing an assignment, and the views that control what template gets sent for the webpage and what happens with the form data.

### login
This app handles the login screen and uses Djangos implementation of user authentication. It is built to be easily ported between projects with minimal imports from outside.

# API Guide

The REST API is implemented using Django REST Framework. and can be used to pull course information. The goal is to eventually be abe to pull assignment information, submit assignments, view grades and more. The student portal will use this API to collect data, and display it. The seperation from the database allows for a more secure and controlled experience. 

## Course API

This is written to be used by students, so use will be from their perspective, teachers should be able to do similar functions. Such as viewing courses a student is in.

### View All Courses

A student should be able to view all of the courses they are in for the current year. A teacher should also be able to view what courses a student is enrolled in. However another student should not be able to see what courses a different student is in. The returned information would be a list of courses the student is in, including the id, title, term, code and instructor. This would be a GET request that uses the student id and the year.

### View Course

A student/instructor should be able to view a course by id and see course title, term, instructor, code, and any assignments that are due should have a title, due date, and id sent. This would be a GET request that uses the course id.

### Edit Course

The only people who should be able to edit a course are the course instructors. This includes changing the title, code, term, instructor. This would be a PATCH request as it would only partially modify a resourse.

### Create Course