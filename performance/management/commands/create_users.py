from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from performance.models import Student, Subject, Grade

class Command(BaseCommand):
    help = 'Creates groups and users with appropriate permissions'

    def handle(self, *args, **kwargs):
        # Создание групп
        admin_group, _ = Group.objects.get_or_create(name='Admin')
        teacher_group, _ = Group.objects.get_or_create(name='Teacher')
        student_group, _ = Group.objects.get_or_create(name='Student')

        # Получение разрешений
        student_ct = ContentType.objects.get_for_model(Student)
        subject_ct = ContentType.objects.get_for_model(Subject)
        grade_ct = ContentType.objects.get_for_model(Grade)

        # Разрешения для администратора (все действия)
        admin_permissions = Permission.objects.filter(
            content_type__in=[student_ct, subject_ct, grade_ct]
        )
        admin_group.permissions.set(admin_permissions)

        # Разрешения для преподавателя (добавление и изменение оценок)
        teacher_permissions = Permission.objects.filter(
            content_type=grade_ct, codename__in=['add_grade', 'change_grade']
        )
        teacher_group.permissions.set(teacher_permissions)

        # Создание пользователей
        admin, _ = User.objects.get_or_create(
            username='admin',
            defaults={'password': 'admin123', 'is_superuser': True, 'is_staff': True}
        )
        admin.set_password('admin123')
        admin.save()
        admin.groups.add(admin_group)

        teacher, _ = User.objects.get_or_create(
            username='teacher',
            defaults={'password': 'teacher123', 'is_staff': True}
        )
        teacher.set_password('teacher123')
        teacher.save()
        teacher.groups.add(teacher_group)

        student, _ = User.objects.get_or_create(
            username='student',
            defaults={'password': 'student123'}
        )
        student.set_password('student123')
        student.save()
        student.groups.add(student_group)

        self.stdout.write(self.style.SUCCESS('Successfully created groups and users'))