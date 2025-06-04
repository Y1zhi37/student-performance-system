from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Student, Subject, Grade
from .forms import StudentForm, SubjectForm, GradeForm
from django.db.models import Avg

# Проверка роли администратора
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

# Проверка роли преподавателя
def is_teacher(user):
    return user.groups.filter(name='Teacher').exists()

# Проверка роли студента
def is_student(user):
    return user.groups.filter(name='Student').exists()

def home(request):
    return render(request, 'performance/home.html')

@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'performance/student_list.html', {'students': students})

# Добавление студента (только админ)
@login_required
@user_passes_test(is_admin)
def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('performance:student_list')
    else:
        form = StudentForm()
    return render(request, 'performance/student_form.html', {'form': form})

# Редактирование студента (только админ)
@login_required
@user_passes_test(is_admin)
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('performance:student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'performance/student_form.html', {'form': form})

# Удаление студента (только админ)
@login_required
@user_passes_test(is_admin)
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('performance:student_list')
    return render(request, 'performance/student_delete.html', {'student': student})

# Список предметов
@login_required
def subject_list(request):
    if is_student(request.user):
        return redirect('performance:grade_list')
    subjects = Subject.objects.all()
    return render(request, 'performance/subject_list.html', {'subjects': subjects})

# Добавление предмета (только админ)
@login_required
@user_passes_test(is_admin)
def subject_add(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('performance:subject_list')
    else:
        form = SubjectForm()
    return render(request, 'performance/subject_form.html', {'form': form})

# Редактирование предмета (только админ)
@login_required
@user_passes_test(is_admin)
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('performance:subject_list')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'performance/subject_form.html', {'form': form})

# Удаление предмета (только админ)
@login_required
@user_passes_test(is_admin)
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        return redirect('performance:subject_list')
    return render(request, 'performance/subject_delete.html', {'subject': subject})

# Список оценок
@login_required
def grade_list(request):
    if is_student(request.user):
        grades = Grade.objects.filter(student__email=request.user.email)
    else:
        grades = Grade.objects.all()
    return render(request, 'performance/grade_list.html', {'grades': grades})

# Добавление оценки (только преподаватель)
@login_required
@user_passes_test(is_teacher)
def grade_add(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('performance:grade_list')
    else:
        form = GradeForm()
    return render(request, 'performance/grade_form.html', {'form': form})

# Редактирование оценки (только преподаватель)
@login_required
@user_passes_test(is_teacher)
def grade_edit(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('performance:grade_list')
    else:
        form = GradeForm(instance=grade)
    return render(request, 'performance/grade_form.html', {'form': form})

# Удаление оценки (только админ)
@login_required
@user_passes_test(is_admin)
def grade_delete(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete()
        return redirect('performance:grade_list')
    return render(request, 'performance/grade_delete.html', {'grade': grade})

# Отчеты
@login_required
def report(request):
    if is_student(request.user):
        try:
            student = Student.objects.get(email=request.user.email)
            grades = Grade.objects.filter(student=student)
            avg_score = grades.aggregate(Avg('score'))['score__avg']
            context = {
                'student': student,
                'grades': grades,
                'avg_score': avg_score or 0,
            }
            return render(request, 'performance/grade_list.html', context)
        except Student.DoesNotExist:
            return render(request, 'performance/grade_list.html', {'error': 'Нет связанного объекта Student'})
    
    # Для Admin и Teacher полный отчёт
    student_averages = Student.objects.annotate(avg_score=Avg('grade__score')).order_by('-avg_score')
    subject_averages = Subject.objects.annotate(avg_score=Avg('grade__score'))
    
    best_student = student_averages.first()
    worst_student = student_averages.last()
    
    context = {
        'student_averages': student_averages,
        'subject_averages': subject_averages,
        'best_student': best_student,
        'worst_student': worst_student,
    }
    return render(request, 'performance/report.html', context)