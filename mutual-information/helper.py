import operator
import json

def load_json(path):
    with open(path) as f:
        data = json.load(f)
    return data
    

fields = ['Title','Input','Output','Description']

for field in fields:
    data = load_json('mutual-information/calculated/'+field+'.json')
    
    sorted_data = sorted(data.items(), key=operator.itemgetter(1), reverse=True)
    print('mutual-information for '+field)
    print(sorted_data[0], sorted_data[1], sorted_data[2])
    
    