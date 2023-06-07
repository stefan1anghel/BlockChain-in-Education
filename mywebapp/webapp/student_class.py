import hashlib
from .database_engine import DbEngine
from datetime import datetime


class StudentBlock:
    def __init__(self, email, first_name, last_name, username, password):  # se comporta ca un sign up
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = password
        self.last_transaction_timestamp = datetime.now()
        self.block_data = f"Your blockchain has been initialized at {self.last_transaction_timestamp}"
        self.nonce = hashlib.sha256(self.block_data.encode()).hexdigest()
        self.previous_hash = 0

        db = DbEngine.instance()
        db.run_query(f"insert into Students (Email, FirstName, LastName, Username, Password, Nonce, "
                     f"TransactionMessages) values('{self.email}', '{self.first_name}', '{self.last_name}', "
                     f"'{self.username}', '{self.password}', '{self.nonce}', '{self.block_data}')")
        student_id = db.run_query(f"select ID from Students where Email='{self.email}'")[0][0]
        query = f"insert into Messages (Message, Date, ID_student) values('{self.block_data}', '{self.last_transaction_timestamp}', {student_id})"
        db.run_query(f"insert into Messages (Message, Date, ID_student) values('{self.block_data}', '{self.last_transaction_timestamp}', {student_id})")

    def encode_block_data(self):
        self.previous_hash = self.nonce
        self.nonce = hashlib.sha256(self.block_data.encode()).hexdigest()


