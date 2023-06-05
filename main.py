from mywebapp.webapp.student_milestone_class import Transaction
from mywebapp.webapp.database_engine import DbEngine


db = DbEngine.instance()

prof_list = db.run_query(f"select ID from Professors where ID_education_entity=1")
print(prof_list)
#
# student1 = StudentBlock("Stefan Anghel")
# entity1 = EducationEntity("University", "Poli")
# professor1 = Professor("Caramihai", "OOP", entity1)
#
# professor1.add_milestone_to_student("grade", "10", student1)

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


