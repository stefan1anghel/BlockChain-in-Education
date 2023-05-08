from mywebapp.webapp.Utils import id_generator
from mywebapp.webapp.database_engine import DbEngine


class EducationEntity:
    def __init__(self, entity_name):
        self.entity_name = entity_name
        self.id = id_generator("education_entity")
        db = DbEngine.instance()
        db.run_query(f"insert into EducationEntities values({self.id}, '{self.entity_name}')")

    # def approve_transaction(self, transaction_index):
    #     approved_transaction: StudentMilestone = self.transactions_list[transaction_index]
    #     approved_transaction.education_entity_approval = True
    #     self.transactions_list.remove(self.transactions_list[transaction_index])
