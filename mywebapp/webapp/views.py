from django.shortcuts import render, redirect
from .database_engine import DbEngine
from django.http import HttpResponse


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        entity = request.POST['dropdown']

        db = DbEngine.instance()
        db_username = db.run_query(f"select Username from {entity} where Username='{username}'")[0][0].strip()
        db_password = db.run_query(f"select password from {entity} where Password='{password}'")[0][0]

        id = db.run_query(f"select ID from {entity} where Username='{username}'")[0][0]

        if (username == db_username) & (password == db_password):
            request.session['user_id'] = id
            response = HttpResponse()
            response.set_cookie('sessionid', value=request.session.session_key, expires='Session')
            return eval(f"redirect('welcome_{entity.lower()}')")

    return render(request, 'login.html')


def custom_login_required(view_func):  # asta e un decorator care verifica daca utilizatorul s-a logat pentru a restrictiona accesul la view-urile urmatoare
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')

        return view_func(request, *args, **kwargs)

    return wrapper


@custom_login_required
def welcome_students(request):
    return render(request, 'welcome_students.html')


@custom_login_required
def grades_view(request):
    db = DbEngine.instance()
    data = db.run_query(f"select Subject, Grade, Date from Grades where ID_student={request.session.get('user_id')}")
    return render(request, 'grades.html', {'data': data})


@custom_login_required
def blockchain_view(request):
    db = DbEngine.instance()
    data = db.run_query(f"select TransactionsMessages from Students where ID={request.session.get('user_id')}")[0][0]
    breakpoint()
    return render(request, 'blockchain_history.html', {'data': data})


@custom_login_required
def welcome_professors(request):
    return render(request, 'welcome_professors.html')
