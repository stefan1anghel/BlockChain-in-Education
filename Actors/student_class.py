import hashlib
import os


class StudentBlock:
    def __init__(self, student_name):
        self.student_name = student_name
        self.transactions_list = []
        self.block_data = f"{self.student_name}'s blockchain has been initialized"

        working_dir = os.path.abspath('Student_jsons')
        with open(os.path.join(working_dir, f"{self.student_name}.txt"), "w") as file:
            file.write(self.block_data)
            file.close()

        self.file_path = os.path.join(working_dir, f"{self.student_name}.txt")

        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()
        self.previous_hash = 0

    # def approve_transaction(self, transaction_index):
    #     transaction_to_be_approved: StudentMilestone = self.transactions_list[transaction_index]
    #
    #     if transaction_to_be_approved.education_entity_approval is True:
    #         transaction_to_be_approved.student_approval = True
    #         milestone_dict = transaction_to_be_approved.return_milestone_info_dict()
    #
    #         # tratez cazul primului element ca sa nu am o virgula la sfarsitul stringului de hash
    #         if self.block_data == f"{self.student_name}: ":
    #             self.block_data = self.block_data + milestone_dict['milestone_type'] + ' - ' + \
    #                               milestone_dict['milestone_info']
    #         else:
    #             self.block_data = self.block_data + ', ' + milestone_dict['milestone_type'] + ' - ' + \
    #                               milestone_dict['milestone_info']
    #
    #         self.transactions_list.remove(self.transactions_list[transaction_index])
    #
    #         self.__encode_block_data()
    #     else:
    #         print("Transaction must be approved by the Education Entity first!")

    def encode_block_data(self):
        self.previous_hash = self.block_hash
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()
