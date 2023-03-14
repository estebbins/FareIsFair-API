# Python program to read
# json file

# https://stackoverflow.com/questions/51577441/how-to-seed-django-project-insert-a-bunch-of-data-into-the-project-for-initi

#  https://www.geeksforgeeks.org/read-json-file-using-python/

# Shape of data
# # [
#     {
#         "model": "api.question",
#         "fields": {
#             "prompt": "test",
#             "additional": "test",
#             "image": "test",
#             "answer": "123"
#         }
#     }
# ]

import json

# Opening JSON file
f = open('red_circle_api_videogames.json')

# returns JSON object as 
# a dictionary
all_data = json.load(f)
data = []
# Iterating through the json
# list
for i in all_data['category_results']:
    try:
        entry = {
            "model": "api.question",
            "fields": {
                "prompt": i["product"]["title"],
                "additional": i["product"]["feature_bullets"][0] or 'None Available',
                "image": i["product"]["main_image"],
                "answer": i["offers"]["primary"]["price"]
            }
        }
    except KeyError:
        entry = {
            "model": "api.question",
            "fields": {
                "prompt": i["product"]["title"],
                "additional": "None Available",
                "image": i["product"]["main_image"],
                "answer": i["offers"]["primary"]["price"]
            }
        }
    data.append(entry)

print(data)
  
# Closing file
f.close()

