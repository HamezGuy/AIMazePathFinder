import numpy as np

#Code based on student code. 


with open('allDeaths.csv') as f:
    data = list(f)[1:]

d_dict = {}
for d in data:
    l = d.strip('\n').split(',')
    c = l[8]  # country
    if c in d_dict:
        d_dict[c][0].append(float(l[8])) #lat
        d_dict[c][1].append(float(l[9])) #long
        d_dict[c][2].append(float(l[12])) #population
        
    else:
        d_dict[c] = [[float(l[8])], [float(l[9])], [float(l[12])]]
d_dict = {k:np.array([sum(v[0])/len(v[0]), sum(v[1])/len(v[1]), sum(v[2])]) for k,v in d_dict.items()}

countries = sorted([c for c in d_dict.keys()])