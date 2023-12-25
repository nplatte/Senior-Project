This is an updated portal for teachers to create Math, Computer SCience and Physics courses for students. Additionally, they can add assignments for courses and view student submissions.

This is a Django project, so it is made up of a core project and a some apps. The project folder is teacher_portal and the apps are teacher_view, assignment, course, and login. Each app/project is tested using Test Driven Development, the functional tests using selenium are found in the functional_tests folder and the unit tests for each app are found in APP_NAME/tests folder. The unit tests are split into model tests, form tests and view tests for more seperation and better readability.

Breakdown of each app:
teacher_view
This app is the base app of the project. It holds the base template, which all of the other html templates are based off of. It has the basic landing page and the teacher profile page. In addition, it has the css files that are applied to all of the templates on the website.

course
This app has the Course model and the Student model, the forms for creating a course and editing a course, and the views for handling form data for course creation and course editing.

assignment
This app has the Assignment model, the forms for creating a new assignment for a course, editing an assignment, and the views that control what template gets sent for the webpage and what happens with the form data.

login
This app handles the login screen and uses Djangos implementation of user authentication. It is built to be easily ported between projects with minimal imports from outside.

