from mywebapp.webapp.database_engine import DbEngine
from mywebapp.webapp.Utils import id_generator


class Grade:
    def __init__(self, subject, student_name, grade):
        db = DbEngine.instance()
        self.student_id = db.run_query(f"select ID from Students where Name='{student_name}'")[0][0]
        self.subject = subject
        self.grade = grade
        self.id = id_generator("grade")

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
