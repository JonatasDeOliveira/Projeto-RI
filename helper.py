import json

with open('mutual-information/Title.json') as f:
    data = json.load(f)

print(data['title']['count'])
analyse_data = {}
for i in range(1,100):
    analyse_data[i] = 0
    
for key in data.keys():
    if data[key].get('count') == 337:
        print(key)
    cont = analyse_data.get(data[key].get('count'),0)
    analyse_data[data[key].get('count')] = cont+1
    
print(analyse_data)