import json

errors = json.load(open("errors.json"))


print(len(errors['p1']), len(errors['p2']))