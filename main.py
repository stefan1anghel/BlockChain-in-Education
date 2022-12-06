import hashlib


class EducationEntity:
    def __init__(self, entity_type, entity_name):
        self.entity_type = entity_type
        self.entity_name = entity_name
        self.transactions_list = []

    def approve_transaction(self, transaction_index):
        approved_transaction: StudentMilestone = self.transactions_list[transaction_index]
        approved_transaction.education_entity_approval = True
        self.transactions_list.remove(self.transactions_list[transaction_index])


class StudentMilestone:
    def __init__(self, entity: EducationEntity, milestone_type, milestone_info):
        self.milestone_type = milestone_type
        self.milestone_info = milestone_info
        self.linked_entity = entity
        self.student_approval = None
        self.education_entity_approval = None
        entity.transactions_list.append(self)

    def return_milestone_info_dict(self):
        milestone_info_dict = {
            "milestone_type": self.milestone_type,
            "milestone_info": self.milestone_info,
            "entity_name": self.linked_entity.entity_name,
            "entity_type": self.linked_entity.entity_type
        }
        return milestone_info_dict


class StudentBlock:
    def __init__(self, student_name):
        self.student_name = student_name
        self.transactions_list = []
        self.block_data = student_name + ": "
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()
        self.previous_hash = 0

    def add_milestone(self, milestone_type, milestone_info, entity: EducationEntity):
        new_milestone = StudentMilestone(entity, milestone_type, milestone_info)
        self.transactions_list.append(new_milestone)

    def approve_transaction(self, transaction_index):
        transaction_to_be_approved: StudentMilestone = self.transactions_list[transaction_index]

        if transaction_to_be_approved.education_entity_approval is True:
            transaction_to_be_approved.student_approval = True
            milestone_dict = transaction_to_be_approved.return_milestone_info_dict()

            # tratez cazul primului element ca sa nu am o virgula la sfarsitul stringului de hash
            if self.block_data == f"{self.student_name}: ":
                self.block_data = self.block_data + milestone_dict['milestone_type'] + ' - ' + \
                                  milestone_dict['milestone_info']
            else:
                self.block_data = self.block_data + ', ' + milestone_dict['milestone_type'] + ' - ' + \
                                  milestone_dict['milestone_info']

            self.transactions_list.remove(self.transactions_list[transaction_index])

            self.__encode_block_data()
        else:
            print("Transaction must be approved by the Education Entity first!")

    def __encode_block_data(self):
        self.previous_hash = self.block_hash
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()


student1 = StudentBlock("Stefan")
entity1 = EducationEntity("University", "Poli")
student1.add_milestone("grade", "10", entity1)

student1.approve_transaction(0)

entity1.approve_transaction(0)
student1.approve_transaction(0)
student1.add_milestone("Graduation", "Bachelor's degree", entity1)
print(student1.block_data, student1.transactions_list, entity1.transactions_list)
entity1.approve_transaction(0)
student1.approve_transaction(0)
print(student1.block_data)
