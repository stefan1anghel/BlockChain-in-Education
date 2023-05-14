from django.urls import path
from . import views

urlpatterns = [
    path('welcome_students/', views.welcome_students, name='welcome_students'),
    path('welcome_professor/', views.welcome_professors, name='welcome_professors'),
    path('login/', views.login, name='login'),
    path('grades/', views.grades_view, name='grades_view'),
    path('blockchain_history/', views.blockchain_view, name='blockchain_view'),
    path('create_student_account/', views.create_student_account, name='create_student_account')
]