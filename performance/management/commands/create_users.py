from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from performance.models import Student

class Command(BaseCommand):
    help = 'Creates initial users and groups'

    def handle(self, *args, **kwargs):
        # Создание групп
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        teacher_group, _ = Group.objects.get_or_create(name='Teacher')
        student_group, _ = Group.objects.get_or_create(name='Student')

        # Создание администратора
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Админ',
                last_name='Админов'
            )
            admin.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        # Создание преподавателя
        if not User.objects.filter(username='teacher').exists():
            teacher = User.objects.create_user(
                username='teacher',
                email='teacher@example.com',
                password='teacher123',
                first_name='Преподаватель',
                last_name='Преподавателев'
            )
            teacher.groups.add(teacher_group)
            self.stdout.write(self.style.SUCCESS('Teacher user created'))

        # Создание студента
        if not User.objects.filter(username='student').exists():
            student_user = User.objects.create_user(
                username='student',
                email='student@example.com',
                password='student123',
                first_name='Студент',
                last_name='Студентов'
            )
            student_user.groups.add(student_group)
            # Создание объекта Student
            Student.objects.create(
                first_name='Студент',
                last_name='Студентов',
                email=student_user.email
            )
            self.stdout.write(self.style.SUCCESS('Student user and Student object created'))