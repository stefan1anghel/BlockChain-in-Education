from .database_engine import DbEngine
from datetime import datetime
import hashlib


class Transaction:
    def __init__(self, transaction_type, subject=None, grade: float = None, professor_id=None,
                 education_entity_id=None, student_id=None):
        self.transaction_type = transaction_type
        self.subject = subject
        self.grade = grade
        self.professor_id = professor_id
        self.education_entity_id = education_entity_id
        self.student_id = student_id

        if transaction_type == "Grade":
            db = DbEngine.instance()
            prof_name = db.run_query(f"select FirstName, LastName from Professors where ID={self.professor_id}")
            self.transaction_message = f"A new grade transaction has been initiated by prof. {prof_name[0][0]} {prof_name[0][1]} at {datetime.now()}. Grade: {grade}, Subject: {subject}"
            db.run_query(f"insert into Transactions (ID_student, ID_education_entity, Type, Subject, Grade) values({self.student_id}, {self.education_entity_id}, '{self.transaction_type}', '{self.subject}', {self.grade})")

            # generate new message to encode
            prev_message = db.run_query(f"select TransactionMessages from Students where ID={student_id}")[0][0]
            new_message = prev_message + f"; {self.transaction_message}"

            # encode the new message and the current nonce becomes the prev hash
            new_nonce = hashlib.sha256(new_message.encode()).hexdigest()
            prev_hash = db.run_query(f"select Nonce from Students where ID={student_id}")[0][0]

            # update the student in the db with the new info
            db.run_query(f"update Students set Nonce = '{new_nonce}', PreviousHash = '{prev_hash}', TransactionMessages = '{new_message}' where ID={self.student_id}")

        elif transaction_type == "Enroll":
            db = DbEngine.instance()
            education_entity_name = db.run_query(f"select Name from Education_entities where ID={self.education_entity_id}")[0][0]
            self.info = f"Enrollment by {education_entity_name}"
            query = f"insert into Transactions (ID_student, ID_education_entity, Type, Info, Education_entity_approval) values({self.student_id}, {self.education_entity_id}, '{self.transaction_type}', '{self.info}', 'True')"
            breakpoint()
            db.run_query(f"insert into Transactions (ID_student, ID_education_entity, Type, Info, Education_entity_approval) values({self.student_id}, {self.education_entity_id}, '{self.transaction_type}', '{self.info}', 'True')")

            self.transaction_message = f"A new enrollment request has been initialised by {education_entity_name}"

            # generate new message to encode
            prev_message = db.run_query(f"select TransactionMessages from Students where ID={student_id}")[0][0]
            new_message = prev_message + f"; {self.transaction_message}"

            # encode the new message and the current nonce becomes the prev hash
            new_nonce = hashlib.sha256(new_message.encode()).hexdigest()
            prev_hash = db.run_query(f"select Nonce from Students where ID={student_id}")[0][0]

            # update the student in the db with the new info
            db.run_query(f"update Students set Nonce = '{new_nonce}', PreviousHash = '{prev_hash}', TransactionMessages = '{new_message}' where ID={self.student_id}")

        elif transaction_type == "Diploma":
            pass


class Grade:
    def __init__(self, subject, grade, first_name, last_name):
        db = DbEngine.instance()
        self.student_id = db.run_query(f"select ID from Students where first_name='{first_name}' and last_name='{last_name}'")[0][0]
        self.subject = subject
        self.grade = grade

        db.run_query(f"insert into Grades(Subject, Grade, ID_student, ID_grade) values('{self.subject}', '{self.grade}', {self.student_id}, {self.id})")

# class StudentMilestone:
#     def __init__(self, milestone_type, milestone_info):
#         self.milestone_type = milestone_type
#         self.milestone_info = milestone_info
#         self.student_approval = None
#         self.education_entity_approval = None
#
#     def return_milestone_info_dict(self):
#         milestone_info_dict = {
#             "milestone_type": self.milestone_type,
#             "milestone_info": self.milestone_info,
#         }
#         return milestone_info_dict
