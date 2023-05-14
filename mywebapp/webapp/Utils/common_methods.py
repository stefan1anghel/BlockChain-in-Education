import json
import random


def id_generator(class_name):
    is_unique = False

    with open('.Utils.ids.json', "r") as file:
        data = file.read()
        parsed_data = json.loads(data)

    while is_unique is False:
        id = random.randint(0, 1000000000)
        if id not in eval(f"parsed_data['{class_name}_ids']"):
            eval(f"parsed_data['{class_name}_ids'].append(id)")
            data_to_dump = json.dumps(parsed_data)
            with open(".Utils.ids.json", "w") as file:
                file.write(data_to_dump)
            is_unique = True
            return id
