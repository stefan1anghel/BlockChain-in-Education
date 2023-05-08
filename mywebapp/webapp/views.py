from django.shortcuts import render, redirect
from .database_engine import DbEngine


def welcome(request):
    return render(request, 'welcome.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        db = DbEngine.instance()
        db_username = db.run_query(f"select Email from Students where Email='{username}'")[0][0]
        db_password = db.run_query(f"select password from Students where Password='{password}'")[0][0]

        if (username == db_username) & (password == db_password):
            return redirect('welcome')

    return render(request, 'login.html')
