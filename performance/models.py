from django.db import models

# Модель для студентов
class Student(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Модель для предметов
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название предмета")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self):
        return self.name

# Модель для оценок
class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    score = models.IntegerField(verbose_name="Оценка")  # Оценка от 0 до 100
    date = models.DateField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        unique_together = ['student', 'subject', 'date']  # Уникальность оценки для студента и предмета в день

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.score}"