from Actors.education_entity_class import EducationEntity
from Actors.student_class import StudentBlock
from Classes.student_milestone_class import StudentMilestone
import json


class Professor:
    def __init__(self, professor_name, subject, university: EducationEntity):
        self.professor_name = professor_name
        self.subject = subject
        self.university = university

    def add_milestone_to_student(self, milestone_type, milestone_info, student: StudentBlock):
        """ Metoda adauga un milestone in lista de tranzactii a universitatii si a studentului pentru a fi acceptata.
            Se adauga si un mesaj de tranzactie in jsonul studentului pentru a fi procesata noua cheie hash."""
        new_milestone = StudentMilestone(milestone_type, milestone_info)
        self.university.transactions_list.append(new_milestone)
        student.transactions_list.append(new_milestone)

        with open(student.file_path, 'a') as file:
            file.write(f"\n{student.student_name} received {milestone_type} {milestone_info} from "
                       f"{self.professor_name} at {self.subject}")
            file.close()

        with open(student.file_path, 'r') as file:
            student.block_data = file.read()
            file.close()

        student.encode_block_data()
