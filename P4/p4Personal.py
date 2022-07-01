import numpy as np

with open('allDeaths.csv') as f:
    data = list(f)[1:]

d_dict = {}


for d in data:
    l = d.strip('\n').split(',')
    c = l[6]  # state

    
    n = 0
    
    for x in l:
        temp = 0
        if( n <= 1):
            if(temp >= 14):
                print("here")
                print(l[(temp)])
            temp +=1
    n = n + 1


for d in data:
    l = d.strip('\n').split(',')
    c = l[6]  # state

    
    if c in d_dict:
        n = 0

        for x in l:
            if(n >= 14):
                t = n - 14
                
                d_dict[c][t] = d_dict[c][t] + float(l[n])
            n = n+1

    else:
        n= len(l) - 14
        #todo, do this for all of them
        d_dict[c] = {k : float(0) for k in range(n) }   



#d_dict = {np.array([sum(v[0])/len(v[0])]) }


for c in d_dict:
    if c == "Wisconsin":
        for x in d_dict[c]:
            print(d_dict[c][x], end = '')
            

    if c=="Alabama":
        for x in d_dict[c]:
            print(d_dict[c][x], end = '')

