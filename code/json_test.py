import json

with open("code/test.json", "r") as f:
    items = json.load(f)
    
print(items["items"][0])