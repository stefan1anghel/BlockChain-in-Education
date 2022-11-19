import hashlib


class StudentMilestone:
    def __init__(self, milestone_type, milestone_info):
        self.milestone_type = milestone_type
        self.milestone_info = milestone_info

    def return_milestone_info_dict(self):
        milestone_info_dict = {
            "milestone_type": self.milestone_type,
            "milestone_info": self.milestone_info
        }
        return milestone_info_dict


class StudentBlock:
    def __init__(self, student_name):
        self.student_name = student_name
        self.student_info_list = []
        self.block_data = student_name + ": "
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()
        self.previous_hash = 0

    def add_milestone(self, milestone_type, milestone_info):
        new_milestone = StudentMilestone(milestone_type, milestone_info)
        milestone_dict = new_milestone.return_milestone_info_dict()
        self.student_info_list.append(milestone_dict)

        # tratez cazul primului element ca sa nu am o virgula la sfarsitul stringului de hash
        if len(self.student_info_list) == 1:
            self.block_data = self.block_data + milestone_dict['milestone_type'] + ' - ' + \
                              milestone_dict['milestone_info']
        else:
            self.block_data = self.block_data + ', ' + milestone_dict['milestone_type'] + ' - ' + \
                              milestone_dict['milestone_info']

        self.__encode_block_data()

    def __encode_block_data(self):
        self.previous_hash = self.block_hash
        self.block_hash = hashlib.sha256(self.block_data.encode()).hexdigest()


student_record = StudentBlock("Stefan")
print(student_record.block_hash)
student_record.add_milestone("grade", "10")
print(student_record.block_data)
print(student_record.block_hash)
student_record.add_milestone("graduation", "highschool")
print(student_record.block_data)
print(student_record.block_hash)
