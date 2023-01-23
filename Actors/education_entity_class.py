from Classes.student_milestone_class import StudentMilestone


class EducationEntity:
    def __init__(self, entity_type, entity_name):
        self.entity_type = entity_type
        self.entity_name = entity_name
        self.transactions_list = []

    def approve_transaction(self, transaction_index):
        approved_transaction: StudentMilestone = self.transactions_list[transaction_index]
        approved_transaction.education_entity_approval = True
        self.transactions_list.remove(self.transactions_list[transaction_index])