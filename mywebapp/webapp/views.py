from django.shortcuts import render, redirect
from .database_engine import DbEngine
from django.http import HttpResponse
from .student_class import StudentBlock
from .student_milestone_class import Transaction
from datetime import datetime
import hashlib


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        entity = request.POST['dropdown']

        db = DbEngine.instance()
        db_username = db.run_query(f"select Username from {entity} where Username='{username}'")[0][0].strip()
        db_password = db.run_query(f"select Password from {entity} where Username='{username}'")[0][0].strip()

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
    data = db.run_query(f"select ID, Message, Date from Messages where ID_student={request.session.get('user_id')}")
    return render(request, 'blockchain_history.html', {'data': data})


@custom_login_required
def welcome_professors(request):
    return render(request, 'welcome_professors.html')


def create_student_account(request):
    if request.method == "POST":
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']

        new_student = StudentBlock(email=email, first_name=first_name, last_name=last_name, username=username, password=password)

        if new_student:
            success_message = "Sign up successful! You can now log in."
            return render(request, 'create_student_account.html', {'success_message': success_message})

    return render(request, 'create_student_account.html')


@custom_login_required
def transactions_view(request):
    db = DbEngine.instance()
    data = db.run_query(f"select Type, Subject, Grade, Info, Student_approval, Education_entity_approval, ID from Transactions where ID_student={request.session.get('user_id')}")

    return render(request, 'transactions.html', {'data': data})


def accept_transaction_student(request, transaction_id):   # asta e o functie, nu view, vezi daca le poti face frumos pe foldere
    # remember when the transaction was approved
    date = datetime.now()

    db = DbEngine.instance()

    # set Student_approval to True
    db.run_query(f"update Transactions set Student_approval='True' where ID={transaction_id}")

    # get the transaction data to form the message
    is_approved_by_ee = db.run_query(f"select Education_entity_approval from Transactions where ID={transaction_id}")[0][0]
    transaction_type = db.run_query(f"select Type from Transactions where ID={transaction_id}")[0][0]

    if not is_approved_by_ee:
        if transaction_type == "Grade":
            grade_data = db.run_query(f"select Subject, Grade from Transactions where ID={transaction_id}")[0]
            message = f"You approved the transaction for Grade: {grade_data[1]} - Subject: {grade_data[0]} at {date}. Waiting for approval from the education entity"

            # get the student data and encode the new nonce
            prev_message = db.run_query(f"select TransactionMessages from Students where ID={request.session.get('user_id')}")[0][0]
            new_message = prev_message + f"; {message}"

            new_nonce = hashlib.sha256(new_message.encode()).hexdigest()
            prev_hash = db.run_query(f"select Nonce from Students where ID={request.session.get('user_id')}")[0][0]

            # update the student in the db with the new info
            db.run_query(f"update Students set Nonce = '{new_nonce}', PreviousHash = '{prev_hash}', TransactionMessages = '{new_message}' where ID={request.session.get('user_id')}")
            db.run_query(f"insert into Messages (Message, Date, ID_student) values('{message}', '{date}', {request.session.get('user_id')})")

            return redirect('transactions_view')

        elif transaction_type == "Diploma":
            pass

    elif is_approved_by_ee == 1:
        if transaction_type == "Grade":
            grade_data = db.run_query(f"select Subject, Grade from Transactions where ID={transaction_id}")[0]
            message = f"You approved the transaction for Grade: {grade_data[1]} - Subject: {grade_data[0]} at {date}. You can see it in the Grades section!"

            # delete transaction from list
            db.run_query(f"delete from Transactions where ID={transaction_id}")

            # insert the grade into the Grades table
            db.run_query(f"insert into Grades(Subject, Grade, Date, ID_student) values('{grade_data[0]}', '{grade_data[1]}', '{date}', {request.session.get('user_id')})")

            # get the student data and encode the new nonce
            prev_message = db.run_query(f"select TransactionMessages from Students where ID={request.session.get('user_id')}")[0][0]
            new_message = prev_message + f"; {message}"

            new_nonce = hashlib.sha256(new_message.encode()).hexdigest()
            prev_hash = db.run_query(f"select Nonce from Students where ID={request.session.get('user_id')}")[0][0]

            # update the student in the db with the new info
            db.run_query(f"update Students set Nonce = '{new_nonce}', PreviousHash = '{prev_hash}', TransactionMessages = '{new_message}' where ID={request.session.get('user_id')}")
            db.run_query(f"insert into Messages (Message, Date, ID_student) values('{message}', '{date}', {request.session.get('user_id')})")

            return redirect('transactions_view')

        elif transaction_type == "Diploma":
            pass

        elif transaction_type == "Enroll":
            # create the new mesage with the info
            db = DbEngine.instance()
            education_entity_name = db.run_query(f"select Name from Education_entities where ID=(select ID_education_entity from Transactions where ID={transaction_id})")[0][0]
            education_entity_id = db.run_query(f"select ID_education_entity from Transactions where ID={transaction_id}")[0][0]
            message = f"You accepted the enrollment into {education_entity_name} at {date}"

            # delete the transaction from the list
            db.run_query(f"delete from Transactions where ID={transaction_id}")

            # add university id to student
            db.run_query(f"update Students set EducationEntityID = {education_entity_id} where ID={request.session.get('user_id')}")

            # make the connections in the ProfessorsStudents table
            prof_list = db.run_query(f"select ID from Professors where ID_education_entity={education_entity_id}")
            for prof in prof_list:
                db.run_query(f"insert into ProfessorsStudents (IDstudent, IDprofessor) values({request.session.get('user_id')}, {prof[0]})")

            # get the student data and encode the new nonce
            prev_message = db.run_query(f"select TransactionMessages from Students where ID={request.session.get('user_id')}")[0][0]
            new_message = prev_message + f"; {message}"

            new_nonce = hashlib.sha256(new_message.encode()).hexdigest()
            prev_hash = db.run_query(f"select Nonce from Students where ID={request.session.get('user_id')}")[0][0]

            # update the student in the db with the new info
            db.run_query(f"update Students set Nonce = '{new_nonce}', PreviousHash = '{prev_hash}', TransactionMessages = '{new_message}' where ID={request.session.get('user_id')}")
            db.run_query(f"insert into Messages (Message, Date, ID_student) values('{message}', '{date}', {request.session.get('user_id')})")

            return redirect('transactions_view')


def decline_transaction_student(request, transaction_id):
    # remember when the transaction was approved
    date = datetime.now()

    db = DbEngine.instance()

    # set Student_approval to False
    db.run_query(f"update Transactions set Student_approval='False' where ID={transaction_id}")

    transaction_type = db.run_query(f"select Type from Transactions where ID={transaction_id}")[0][0]

    # create the message based on the transaction
    if transaction_type == "Grade":
        grade_data = db.run_query(f"select Subject, Grade from Transactions where ID={transaction_id}")[0]
        message = f"You declined the transaction for Grade: {grade_data[1]} - Subject: {grade_data[0]} at {date}."

        # delete transaction from list
        db.run_query(f"delete from Transactions where ID={transaction_id}")

        # get the student data and encode the new nonce
        prev_message = db.run_query(f"select TransactionMessages from Students where ID={request.session.get('user_id')}")[0][0]
        new_message = prev_message + f"; {message}"

        new_nonce = hashlib.sha256(new_message.encode()).hexdigest()
        prev_hash = db.run_query(f"select Nonce from Students where ID={request.session.get('user_id')}")[0][0]

        # update the student in the db with the new info
        db.run_query(f"update Students set Nonce = '{new_nonce}', PreviousHash = '{prev_hash}', TransactionMessages = '{new_message}' where ID={request.session.get('user_id')}")
        db.run_query(f"insert into Messages (Message, Date, ID_student) values('{message}', '{date}', {request.session.get('user_id')})")

        return redirect('transactions_view')

    if transaction_type == "Enroll":
        # create the new mesage with the info
        db = DbEngine.instance()
        education_entity_name = db.run_query(f"select Name from Education_entities where ID=(select ID_education_entity from Transactions where ID={transaction_id})")[0][0]
        education_entity_id = db.run_query(f"select ID_education_entity from Transactions where ID={transaction_id}")[0][0]
        message = f"You declined the enrollment into {education_entity_name} at {date}"

        # delete the transaction from the list
        db.run_query(f"delete from Transactions where ID={transaction_id}")

        # get the student data and encode the new nonce
        prev_message = db.run_query(f"select TransactionMessages from Students where ID={request.session.get('user_id')}")[0][0]
        new_message = prev_message + f"; {message}"

        new_nonce = hashlib.sha256(new_message.encode()).hexdigest()
        prev_hash = db.run_query(f"select Nonce from Students where ID={request.session.get('user_id')}")[0][0]

        # update the student in the db with the new info
        db.run_query(f"update Students set Nonce = '{new_nonce}', PreviousHash = '{prev_hash}', TransactionMessages = '{new_message}' where ID={request.session.get('user_id')}")
        db.run_query(f"insert into Messages (Message, Date, ID_student) values('{message}', '{date}', {request.session.get('user_id')})")

        return redirect('transactions_view')


@custom_login_required
def welcome_education_entities(request):
    return render(request, 'welcome_education_entities.html')


@custom_login_required
def enroll(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST['last_name']

        # get the id of the student
        db = DbEngine.instance()
        student_id = db.run_query(f"select ID from Students where FirstName='{first_name}' and LastName='{last_name}'")[0][0]
        new_transaction = Transaction("Enroll", education_entity_id=request.session.get('user_id'), student_id=student_id)

        if new_transaction:
            success_message = "The student has been successfully enrolled!"
            return render(request, 'enroll.html', {'success_message': success_message})

    return render(request, 'enroll.html')


@custom_login_required
def transactions_view_education(request):
    db = DbEngine.instance()
    data = db.run_query(f"select Type, Subject, Grade, Info, Student_approval, Education_entity_approval, ID from Transactions where ID_education_entity={request.session.get('user_id')}")
    student_ids = db.run_query(f"select ID_student from Transactions")
    name_list = []
    for id in student_ids:
        name = db.run_query(f"select FirstName, LastName from Students where ID={id[0]}")[0]
        concat_name = name[0] + " " + name[1]
        name_list.append(concat_name)

    parsed_data_list = []
    for index in range(len(data)):
        new_data_list = list(data[index])
        new_data_list.insert(0, name_list[index])
        parsed_data_list.append(new_data_list)

    return render(request, 'transactions_education.html', {'data': parsed_data_list})


def accept_transaction_education(request, transaction_id):   # asta e o functie, nu view, vezi daca le poti face frumos pe foldere
    # remember when the transaction was approved
    date = datetime.now()

    db = DbEngine.instance()

    # set Education_entity_approval to True
    db.run_query(f"update Transactions set Education_entity_approval='True' where ID={transaction_id}")

    # get the transaction data to form the message
    student_id = db.run_query(f"select ID_student from Transactions where ID={transaction_id}")[0][0]
    is_approved_by_student = db.run_query(f"select Student_approval from Transactions where ID={transaction_id}")[0][0]
    transaction_type = db.run_query(f"select Type from Transactions where ID={transaction_id}")[0][0]

    if not is_approved_by_student:
        if transaction_type == "Grade":
            grade_data = db.run_query(f"select Subject, Grade from Transactions where ID={transaction_id}")[0]
            message = f"The university approved the transaction for Grade: {grade_data[1]} - Subject: {grade_data[0]} at {date}. Waiting for your approval."

            # get the student data and encode the new nonce
            prev_message = db.run_query(f"select TransactionMessages from Students where ID={student_id}")[0][0]
            new_message = prev_message + f"; {message}"

            new_nonce = hashlib.sha256(new_message.encode()).hexdigest()
            prev_hash = db.run_query(f"select Nonce from Students where ID={student_id}")[0][0]

            # update the student in the db with the new info
            db.run_query(f"update Students set Nonce = '{new_nonce}', PreviousHash = '{prev_hash}', TransactionMessages = '{new_message}' where ID={request.session.get('user_id')}")
            db.run_query(f"insert into Messages (Message, Date, ID_student) values('{message}', '{date}', {student_id})")

            return redirect('transactions_view_education')

        elif transaction_type == "Diploma":
            pass

    elif is_approved_by_student == 1:
        if transaction_type == "Grade":
            grade_data = db.run_query(f"select Subject, Grade from Transactions where ID={transaction_id}")[0]
            message = f"The university approved the transaction for Grade: {grade_data[1]} - Subject: {grade_data[0]} at {date}. You can see it in the Grades section!"

            # delete transaction from list
            db.run_query(f"delete from Transactions where ID={transaction_id}")

            # insert the grade into the Grades table
            db.run_query(f"insert into Grades(Subject, Grade, Date, ID_student) values('{grade_data[0]}', '{grade_data[1]}', '{date}', {student_id})")

            # get the student data and encode the new nonce
            prev_message = db.run_query(f"select TransactionMessages from Students where ID={student_id}")[0][0]
            new_message = prev_message + f"; {message}"

            new_nonce = hashlib.sha256(new_message.encode()).hexdigest()
            prev_hash = db.run_query(f"select Nonce from Students where ID={student_id}")[0][0]

            # update the student in the db with the new info
            db.run_query(f"update Students set Nonce = '{new_nonce}', PreviousHash = '{prev_hash}', TransactionMessages = '{new_message}' where ID={student_id}")
            db.run_query(f"insert into Messages (Message, Date, ID_student) values('{message}', '{date}', {student_id})")

            return redirect('transactions_view_education')

        elif transaction_type == "Diploma":
            pass


def decline_transaction_education(request, transaction_id):
    # remember when the transaction was approved
    date = datetime.now()

    db = DbEngine.instance()

    # set Education_entity_approval to False
    db.run_query(f"update Transactions set Education_entity_approval='False' where ID={transaction_id}")

    student_id = db.run_query(f"select ID_student from Transactions where ID={transaction_id}")[0][0]
    transaction_type = db.run_query(f"select Type from Transactions where ID={transaction_id}")[0][0]

    # create the message based on the transaction
    if transaction_type == "Grade":
        grade_data = db.run_query(f"select Subject, Grade from Transactions where ID={transaction_id}")[0]
        message = f"The university declined the transaction for Grade: {grade_data[1]} - Subject: {grade_data[0]} at {date}."

        # delete transaction from list
        db.run_query(f"delete from Transactions where ID={transaction_id}")

        # get the student data and encode the new nonce
        prev_message = db.run_query(f"select TransactionMessages from Students where ID={student_id}")[0][0]
        new_message = prev_message + f"; {message}"

        new_nonce = hashlib.sha256(new_message.encode()).hexdigest()
        prev_hash = db.run_query(f"select Nonce from Students where ID={student_id}")[0][0]

        # update the student in the db with the new info
        db.run_query(f"update Students set Nonce = '{new_nonce}', PreviousHash = '{prev_hash}', TransactionMessages = '{new_message}' where ID={request.session.get('user_id')}")
        db.run_query(f"insert into Messages (Message, Date, ID_student) values('{message}', '{date}', {student_id})")

        return redirect('transactions_view_education')


@custom_login_required
def new_grade(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST['last_name']
        grade = float(request.POST['grade'])

        # get the id of the student
        db = DbEngine.instance()
        student_id = db.run_query(f"select ID from Students where FirstName='{first_name}' and LastName='{last_name}'")[0][0]

        # check if the student is assigned to the professor
        is_assigned = db.run_query(f"select * from ProfessorsStudents where IDstudent={student_id} and IDprofessor={request.session.get('user_id')}")[0][0]

        # get prof info
        subject = db.run_query(f"select Subject from Professors where ID={request.session.get('user_id')}")[0][0]
        education_entity_id = db.run_query(f"select ID_education_entity from Professors where ID={request.session.get('user_id')}")[0][0]

        if is_assigned:
            new_transaction = Transaction("Grade", subject=subject, grade=grade, professor_id=request.session.get('user_id'), student_id=student_id, education_entity_id=education_entity_id)
            if new_transaction:
                success_message = "The transaction has been initialised"
                return render(request, 'new_grade.html', {'success_message': success_message})
            else:
                fail_message = "The transaction could not be initialised. Try again."
                return render(request, 'new_grade.html', {'success_message': fail_message})
        else:
            message = "The student is not assigned under you."
            return render(request, 'new_grade.html', {'success_message': message})

    return render(request, 'new_grade.html')


@custom_login_required
def grant_diploma(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST['last_name']
        message = request.POST['message']

        db = DbEngine.instance()

        # get ids
        student_id = db.run_query(f"select ID from Students where FirstName='{first_name}' and LastName='{last_name}'")[0][0]
        education_entity_id = request.session.get('user_id')

        # check if student is assigned to the education_entity
        is_assigned = db.run_query(f"select EducationEntityID from Students where ID={student_id}")[0][0]

        if is_assigned:
            new_transaction = Transaction(transaction_type="Diploma", education_entity_id=education_entity_id, student_id=student_id, custom_message=message)
            if new_transaction:
                success_message = "Diploma has been granted!"
                return render(request, 'grant_diploma.html', {'success_message': success_message})
            else:
                message = "Something went wrong. Try again"
                return render(request, 'grant_diploma.html', {'success_message': message})
        else:
            message = "Student could not be found."
            return render(request, 'grant_diploma.html', {'success_message': message})

    return render(request, 'grant_diploma.html')
