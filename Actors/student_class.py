import hashlib
from mywebapp.webapp.database_engine import DbEngine
from datetime import datetime
from mywebapp.webapp.Utils import id_generator


class StudentBlock:
    def __init__(self, student_name, email, password, education_entity):  # se comporta ca un sign up
        self.student_name = student_name
        self.email = email
        self.password = password
        self.id = id_generator("student")
        self.transactions_list = []  # maybe delet dis idk
        self.last_transaction_timestamp = datetime.now()
        self.block_data = f"{self.student_name}'s blockchain has been initialized at {self.last_transaction_timestamp}"
        self.nonce = hashlib.sha256(self.block_data.encode()).hexdigest()
        self.previous_hash = 0
        self.education_entity = education_entity

        db = DbEngine.instance()
        education_entity_id = db.run_query(f"select ID_education_entity from Education_entities where"
                                           f" Name='{self.education_entity}'")[0][0]
        db.run_query(f"insert into Students values({self.id}, '{self.student_name}', '{self.email}', "
                     f"'{self.password}', '{self.previous_hash}', {education_entity_id}, '{self.block_data}', "
                     f"'{self.nonce}')")

    def encode_block_data(self):
        self.previous_hash = self.nonce
        self.nonce = hashlib.sha256(self.block_data.encode()).hexdigest()


