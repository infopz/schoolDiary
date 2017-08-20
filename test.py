import json

f = open('times.json', 'r')
text = f.read()
print(text)
t = json.loads(text)
print(t)
