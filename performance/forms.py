from django import forms
from .models import Student, Subject, Grade, Group

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'group']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электронная почта',
            'group': 'Группа',
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description']
        labels = {
            'name': 'Название',
            'description': 'Описание',
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'score', 'date']
        labels = {
            'student': 'Студент',
            'subject': 'Предмет',
            'score': 'Оценка',
            'date': 'Дата',
        }