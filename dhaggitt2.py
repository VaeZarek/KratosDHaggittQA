## Devin Haggitt
## Kratos QA question 2

## Description:
## This Python Script creates a set of id objects with names and badge numbers
## using a list of random names. It then iterates through the set of ids and 
## identifies any ids that contain the name specified in STATIC_NAME, and changes
## the name to NEW_NAME. If STATIC_NAME is not found, the script prints that 
## it is not found

import random

# ID class
class ID:
    def __init__(self, name, badge_num):
        self.name = name
        self.badge_num = badge_num

# Print Set Table Function
def print_set(set_to_print):
    # Print out the set of IDs in a formated table
    print("Set of IDs:")
    print(f'{"Name":16}{"Badge #":8}')
    print('-' * 24)
    for index in set_to_print:
        print(f'{index.name:16}{index.badge_num:8}') 
    print() 

# Initialize statics
STATIC_NAME = "joe"
NEW_NAME = "steve"

# Create a list of names to pull ids from
names = ["ashley", "ben", "candace", "daniel", "evan", "frank",
    "george", "hayden", "ian", "joe", "kevin", "louis", "mark",
    "nathan", "oscar", "pepper", "quincy", "roger", "sebastian",
    "tim", "ursula", "victor", "winston", "xavier", "yvonne", "zeke"]

# Create a set of ids using the name list
ids = set()
for i in range(45):
    new_id = ID(names[random.randint(0,25)], random.randint(0,9999))
    ids.add(new_id)
print_set(ids)

# Iterate through the set of ids
found = False
for index in ids:
    # Python allows == operator when checking string equivalency
    if(index.name == STATIC_NAME):
        print(f"Changing {STATIC_NAME} with Badge #{index.badge_num} to {NEW_NAME}")
        index.name = NEW_NAME
        found = True
        print(f'{index.name:16}{index.badge_num:8}') 
        print()


# If STATIC_NAME not found, print message
if(not found):
    print(f"{STATIC_NAME} not found")
else:
    print_set(ids)
    


