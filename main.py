from Actors.student_class import StudentBlock
from Actors.professor_class import Professor
from Actors.education_entity_class import EducationEntity


student1 = StudentBlock("Stefan Anghel")
entity1 = EducationEntity("University", "Poli")
professor1 = Professor("Caramihai", "OOP", entity1)

professor1.add_milestone_to_student("grade", "10", student1)

# student1.add_milestone("grade", "10", entity1)
#
# student1.approve_transaction(0)
#
# entity1.approve_transaction(0)
# student1.approve_transaction(0)
# student1.add_milestone("Graduation", "Bachelor's degree", entity1)
# print(student1.block_data, student1.transactions_list, entity1.transactions_list)
# entity1.approve_transaction(0)
# student1.approve_transaction(0)
# print(student1.block_data)
