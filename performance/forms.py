from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Student, Subject, Grade, Group

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'group']
        labels = {
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'email': _('Электронная почта'),
            'group': _('Группа'),
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description']
        labels = {
            'name': _('Название'),
            'description': _('Описание'),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'score', 'date']
        labels = {
            'student': _('Студент'),
            'subject': _('Предмет'),
            'score': _('Оценка'),
            'date': _('Дата'),
        }