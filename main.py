from mywebapp.webapp.student_milestone_class import Transaction
from mywebapp.webapp.database_engine import DbEngine


db = DbEngine.instance()

student_ids = db.run_query(f"select ID_student from Transactions")
name_list = []
for id in student_ids:
    name = db.run_query(f"select FirstName, LastName from Students where ID={id[0]}")[0]
    concat_name = name[0] + " " + name[1]
    name_list.append(concat_name)

data = db.run_query(f"select * from Diplomas where ID=3")
if data:
    print("da veric")

parsed_data_list = []
for index in range (len(data)):
    new_data_list = list(data[index])
    new_data_list.insert(0, name_list[index])
    parsed_data_list.append(new_data_list)

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


