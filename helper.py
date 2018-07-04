import json
import operator

with open('mutual-information/calculated/Input.json') as f:
    data = json.load(f)

sorted_data = sorted(data.items(), key=operator.itemgetter(1))

print(sorted_data)

'''
Title: stage, game, numbers
Description: one, number, two
Output: output, number, line
Input: line, contains, number
'''