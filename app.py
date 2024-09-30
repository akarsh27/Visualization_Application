# <-- 
# Please check the print statements while running the code.
#follow below instructiosn to output resulst into a .Json file
# Comment out the print statements and uncomment the lines of code that write data to a JSON file in each step.
# Additionally, uncomment the function calls that write the results to separate JSON files.
# -->

import json
from collections import defaultdict
from datetime import datetime
from datetime import timedelta

#--> step 1 --> Loding the json data from tranings.txt file
with open('trainings.txt', 'r') as file:
    data = json.load(file)
# print(json.dumps(data, indent=4))

#--> step 2 --> counting the number of people who completed the each training
def count_completed_trainings(data):
    training_counts = defaultdict(int)
    for person in data:
        most_recent_completions = {}

        for completion in person['completions']:
            training_name = completion['name']
            completion_date = datetime.strptime(completion['timestamp'], "%m/%d/%Y")
            
            if training_name not in most_recent_completions or completion_date > most_recent_completions[training_name]:
                most_recent_completions[training_name] = completion_date
        
        for training_name in most_recent_completions:
            training_counts[training_name] += 1
    # return json.dump(training_counts, indent=4)
    with open('completed_trainings.json', 'w') as outfile:
        json.dump(training_counts, outfile, indent = 4)

count_completed_trainings(data)
# print(count_completed_trainings(data))


# --> step 3 --> Filter by specific trainings and fiscal year
def get_people_by_training_and_year(data, trainings, fiscal_year):
    results = defaultdict(list)

    start_year = fiscal_year - 1
    end_year = fiscal_year
    start_date = datetime(start_year, 7, 1)
    end_date = datetime(end_year, 6, 30)
    for person in data:
        most_recent_completions = {}

        for completion in person['completions']:
            training_name = completion['name']
            completion_date = datetime.strptime(completion['timestamp'], "%m/%d/%Y")

            if training_name in trainings and start_date <= completion_date <= end_date:
                if training_name not in most_recent_completions or completion_date > most_recent_completions[training_name]:
                    most_recent_completions[training_name] = completion_date

        for training_name in most_recent_completions:
            results[training_name].append(person['name'])
    
    # return json.dumps(results, indent=4)
    with open('people_by_training_and_year.json', 'w') as outfile:
        json.dump(results, outfile, indent=4)


#testing
trainings = ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"]
fiscal_year = 2024
# print(get_people_by_training_and_year(data, trainings, fiscal_year))
# print('-' * 50)
get_people_by_training_and_year(data, trainings, fiscal_year)  

#--> step 4 --> Finding people with expired or expiring trainings
def get_expired_or_expiring_soon(data, date):
    current_date = datetime.strptime(date, "%m/%d/%Y")
    expiring_soon_date = current_date + timedelta(days=30)
    results = {}

    for person in data:
        most_recent_completions = {}
        for completion in person['completions']:
            training_name = completion['name']
            expiration_date = None
            if completion['expires']:
                expiration_date = datetime.strptime(completion['expires'], "%m/%d/%Y")
            completion_date = datetime.strptime(completion['timestamp'], "%m/%d/%Y")

            if training_name not in most_recent_completions or completion_date > most_recent_completions[training_name]['date']:
                most_recent_completions[training_name] = {'date': completion_date, 'expiration': expiration_date}

        # expired or expiring trainings
        for training_name, info in most_recent_completions.items():
            expiration_date = info['expiration']

            if expiration_date:
                if person['name'] not in results:
                    results[person['name']] = []

                #training has expired or will expire soon
                if expiration_date < current_date:
                    results[person['name']].append({
                        'training': training_name,
                        'status': 'expired',
                        'expires_on': expiration_date.strftime("%m/%d/%Y")
                    })
                elif current_date <= expiration_date <= expiring_soon_date:
                    results[person['name']].append({
                        'training': training_name,
                        'status': 'expiring soon',
                        'expires_on': expiration_date.strftime("%m/%d/%Y")
                    })
    # return json.dumps(results, indent=4)
    with open('expired_or_expiring_soon.json', 'w') as outfile:
        json.dump(results, outfile, indent=4)


# Call the function with October 1, 2023
# # print(get_expired_or_expiring_soon(data, '10/01/2023'))
# print('-' * 50)
get_expired_or_expiring_soon(data, '10/01/2023')
