import data
import json

teachers=data.teachers
# print(teachers)
with open("data.json", "w",encoding='utf-8') as f:
   json.dump(teachers, f,ensure_ascii=False)

with open("data.json", "r",encoding='utf-8') as f:
   teachers = json.load(f)

print(teachers[0])
