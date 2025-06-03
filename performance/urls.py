from django.urls import path
from . import views

app_name = 'performance'

urlpatterns = [
    path('', views.home, name='home'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/edit/<int:pk>/', views.student_edit, name='student_edit'),
    path('students/delete/<int:pk>/', views.student_delete, name='student_delete'),
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/add/', views.subject_add, name='subject_add'),
    path('subjects/edit/<int:pk>/', views.subject_edit, name='subject_edit'),
    path('subjects/delete/<int:pk>/', views.subject_delete, name='subject_delete'),
    path('grades/', views.grade_list, name='grade_list'),
    path('grades/add/', views.grade_add, name='grade_add'),
    path('grades/edit/<int:pk>/', views.grade_edit, name='grade_edit'),
    path('grades/delete/<int:pk>/', views.grade_delete, name='grade_delete'),
    path('report/', views.report, name='report'),
]