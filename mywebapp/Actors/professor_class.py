# from mywebapp.webapp.Utils import id_generator
# from mywebapp.webapp.database_engine import DbEngine
#
#
# class Professor:
#     def __init__(self, professor_name, subject, university):
#         self.professor_name = professor_name
#         self.subject = subject
#         self.university = university
#         self.id = id_generator("professor")
#         db = DbEngine.instance()
#         education_entity_id = db.run_query(f"select ID_education_entity from Education_entities where"
#                                            f" Name='{self.university}'")[0][0]
#         db.run_query(f"insert into Professors(ID, EducationEntityID, Name, Subject) values({self.id}, {education_entity_id}, '{self.professor_name}', '{self.subject}')")
#
#     def add_grade_to_student(self, ):
#         pass # de adaugat tranzactie catre facultate si student, de updatat nonce student cu hashul nou
#
#     # def add_milestone_to_student(self, milestone_type, milestone_info, student: StudentBlock):
#     #     """ Metoda adauga un milestone in lista de tranzactii a universitatii si a studentului pentru a fi acceptata.
#     #         Se adauga si un mesaj de tranzactie in jsonul studentului pentru a fi procesata noua cheie hash."""
#     #
#     #     new_milestone = StudentMilestone(milestone_type, milestone_info)
#     #     self.university.transactions_list.append(new_milestone)
#     #     student.transactions_list.append(new_milestone)
#     #
#     #     with open(student.file_path, 'a') as file:
#     #         file.write(f"\n{student.student_name} received {milestone_type} {milestone_info} from "
#     #                    f"{self.professor_name} at {self.subject}")
#     #         file.close()
#     #
#     #     with open(student.file_path, 'r') as file:
#     #         student.block_data = file.read()
#     #         file.close()
#     #
#     #     student.encode_block_data()
#
#
# obj = Professor("Eugen", "Mate", "Poli")
