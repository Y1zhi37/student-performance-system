from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.db.models import Avg
from .models import Student, Subject, Grade
from .forms import StudentForm, SubjectForm, GradeForm

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_teacher_or_admin(user):
    return user.groups.filter(name__in=['Admin', 'Teacher']).exists()

@login_required
def home(request):
    return render(request, 'performance/home.html')

@login_required
def student_list(request):
    if not request.user.groups.filter(name__in=['Admin', 'Teacher']).exists():
        return redirect('performance:grade_list')
    students = Student.objects.all()
    return render(request, 'performance/student_list.html', {'students': students})

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

@login_required
@user_passes_test(is_admin)
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('performance:student_list')
    return render(request, 'performance/student_delete.html', {'student': student})

@login_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'performance/subject_list.html', {'subjects': subjects})

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

@login_required
@user_passes_test(is_admin)
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        return redirect('performance:subject_list')
    return render(request, 'performance/subject_delete.html', {'subject': subject})

@login_required
def grade_list(request):
    if request.user.groups.filter(name__in=['Admin', 'Teacher']).exists():
        grades = Grade.objects.all()
        return render(request, 'performance/grade_list.html', {'grades': grades})
    try:
        student = Student.objects.get(email=request.user.email)
        grades = Grade.objects.filter(student=student)
        return render(request, 'performance/grade_list.html', {'grades': grades})
    except Student.DoesNotExist:
        grades = Grade.objects.none()
        return render(request, 'performance/grade_list.html', {'grades': grades, 'error': True})

@login_required
@user_passes_test(is_teacher_or_admin)
def grade_add(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('performance:grade_list')
    else:
        form = GradeForm()
    return render(request, 'performance/grade_form.html', {'form': form})

@login_required
@user_passes_test(is_teacher_or_admin)
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

@login_required
@user_passes_test(is_teacher_or_admin)
def grade_delete(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete()
        return redirect('performance:grade_list')
    return render(request, 'performance/grade_delete.html', {'grade': grade})

@login_required
def report(request):
    if request.user.groups.filter(name__in=['Admin', 'Teacher']).exists():
        # Вычисление средних баллов по студентам
        student_averages = Student.objects.annotate(
            avg_score=Avg('grade__score')
        ).filter(avg_score__isnull=False).order_by('-avg_score')

        # Лучший и худший студент
        best_student = student_averages.first()
        worst_student = student_averages.last()

        # Средние баллы по предметам
        subject_averages = Subject.objects.annotate(
            avg_score=Avg('grade__score')
        ).filter(avg_score__isnull=False)

        return render(request, 'performance/report.html', {
            'best_student': best_student,
            'worst_student': worst_student,
            'student_averages': student_averages,
            'subject_averages': subject_averages
        })

    try:
        student = Student.objects.get(email=request.user.email)
        grades = Grade.objects.filter(student=student)
        avg_score = grades.aggregate(Avg('score'))['score__avg'] or 0
        return render(request, 'performance/student_report.html', {'grades': grades, 'avg_score': avg_score})
    except Student.DoesNotExist:
        grades = Grade.objects.none()
        return render(request, 'performance/student_report.html', {'grades': grades, 'avg_score': 0, 'error': True})