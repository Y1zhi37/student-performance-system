Student Performance System
A Django-based web application for managing student performance, including students, subjects, grades, and reports.
Setup Instructions

Clone the repository:
git clone https://github.com/Y1zhi37/student-performance-system.git
cd student-performance-system


Set up virtual environment:
python -m venv venv
or source venv/Scripts/activate  # On Windows


Install dependencies:
pip install -r requirements.txt


Apply migrations:
python manage.py migrate


Create groups and users:
python manage.py create_users


Run the server:
python manage.py runserver


Access the application:

Open http://127.0.0.1:8000/ in your browser.
Login credentials:
Admin: username=admin, password=admin123
Teacher: username=teacher, password=teacher123
Student: username=student, password=student123





Features

Admin: Can create/edit/delete students, subjects, and grades.
Teacher: Can add/edit grades.
Student: Can view their own grades.
Reports: Displays best/worst student and average scores by student and subject.


