from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Create default users and groups'

    def handle(self, *args, **kwargs):
        # Создание групп
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        teacher_group, _ = Group.objects.get_or_create(name='Teacher')
        student_group, _ = Group.objects.get_or_create(name='Student')

        # Создание админа
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            admin.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        # Создание преподавателя
        if not User.objects.filter(username='teacher').exists():
            teacher = User.objects.create_user(
                username='teacher',
                email='teacher@example.com',
                password='teacher123'
            )
            teacher.groups.add(teacher_group)
            self.stdout.write(self.style.SUCCESS('Teacher user created'))

        # Создание студента
        if not User.objects.filter(username='student').exists():
            student = User.objects.create_user(
                username='student',
                email='student@example.com',
                password='student123'
            )
            student.groups.add(student_group)
            self.stdout.write(self.style.SUCCESS('Student user created'))