from django.urls import path
from . import views

urlpatterns = [
    path('welcome_students/', views.welcome_students, name='welcome_students'),
    path('welcome_professor/', views.welcome_professors, name='welcome_professors'),
    path('welcome_education_entities/', views.welcome_education_entities, name='welcome_education_entities'),
    path('login/', views.login, name='login'),
    path('grades/', views.grades_view, name='grades_view'),
    path('blockchain_history/', views.blockchain_view, name='blockchain_view'),
    path('create_student_account/', views.create_student_account, name='create_student_account'),
    path('transactions/', views.transactions_view, name='transactions_view'),
    path('transactions/<int:transaction_id>/approve/', views.accept_transaction_student, name='accept_transaction_student'),
    path('transactions/<int:transaction_id>/decline/', views.decline_transaction_student, name='decline_transaction_student'),
    path('enroll/', views.enroll, name='enroll'),
    path('new_grade/', views.new_grade, name='new_grade'),
    path('transactions_education/', views.transactions_view_education, name='transactions_view_education'),
    path('transactions_education/<int:transaction_id>/approve/', views.accept_transaction_education, name='accept_transaction_education'),
    path('transactions_education/<int:transaction_id>/decline/', views.decline_transaction_education, name='decline_transaction_education'),
    path('grant_diploma/', views.grant_diploma, name='grant_diploma')
]