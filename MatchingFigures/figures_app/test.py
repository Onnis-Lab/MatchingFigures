import pandas as pd


group = []
with open('MatchingFigures/figures_app/random4242.txt', 'r') as file:
    for line in file:
        a = line.strip('\n').split(';')
        participants, pairs = a[0], a[1]

        pairs = list(pairs)



print(participants)
print(pairs)
        
            
# a = [(1, 1), (2, 2), (3, 3)]
