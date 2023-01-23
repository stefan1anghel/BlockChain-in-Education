

class StudentMilestone:
    def __init__(self, milestone_type, milestone_info):
        self.milestone_type = milestone_type
        self.milestone_info = milestone_info
        self.student_approval = None
        self.education_entity_approval = None

    def return_milestone_info_dict(self):
        milestone_info_dict = {
            "milestone_type": self.milestone_type,
            "milestone_info": self.milestone_info,
        }
        return milestone_info_dict
