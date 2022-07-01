from os import stat
import numpy as np
from sklearn.covariance import EmpiricalCovariance
from sklearn.datasets import make_gaussian_quantiles 
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error
from sklearn import linear_model
'''
Todo: 
1. Part 1 in P4.
2. Euclidean distance (currently are all manhattan in my code below)
3. Complete linkage distance
4. Total distortion
5. Output all required information in correct format

PS: Code was based on TA code
https://towardsdatascience.com/modeling-logistic-growth-1367dc971de2 used this website as well
https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html documentation


'''



# For 'South Korea', and "Bonaire Sint Eustatius and Saba" (line 145 and 257), I removed the ',' in name manually
with open('allDeaths.csv') as f:
    data = list(f)[1:]

param_dict = {}
time_dif = {}



for d in data:
    l = d.strip('\n').split(',')
    c = l[6]  # state
    

    if c in time_dif:
        n = 0

        for x in l:
            if n >= 14:
                t = n - 14
                time_dif[c][t].append(float(l[n]))
            n += 1
    else:
        time_dif[c] = {}
        n = 0

        for x in l:
            if n >= 14:
                t = n - 14
                time_dif[c][t] = [(float(l[n]))]
            n += 1


for state in time_dif:

    for x in time_dif[state]:

        sumAll = 0

        for i in time_dif[state][x]:
            sumAll += float(i)

        time_dif[state][x] = sumAll
        

        

#find mean
#u for normal
#number of days to double infection
#linear regression for time

time_dif_final = {}
#time dif data
for state in time_dif:
    time_dif_final[state] = {}
    for x in time_dif[state]:
        if(x != 0.0):
            if time_dif[state][x] != time_dif[state][(x-1)]:
                time_dif_final[state][x] = (time_dif[state][x] - time_dif[state][(x-1)])
            else:
                time_dif_final[state][x] = 0.0



for state in time_dif:
    if(state == "Wisconsin"):
        
        for x in time_dif[state]:
            ()
            #print(time_dif[state][x], ",", end = '', sep = '')

print('\n')

for state in time_dif:
    if(state == "Alabama"):
        
        for x in time_dif[state]:
            ()
            #print(time_dif[state][x], ",", end = '', sep = '')
print('\n')
print('\n')
for state in time_dif_final:
    if(state == "Wisconsin"):
        
        for x in time_dif_final[state]:
            ()
            #print(time_dif_final[state][x], ",", end = '', sep = '')
print('\n')
for state in time_dif_final:
    if(state == "Alabama"):
        
        for x in time_dif_final[state]:
            ()
            #print(time_dif_final[state][x], ",", end = '', sep = '')



mean = {}
for state in time_dif:
    mean[state] = {}

    mean[state][0] = 0.0

    for x in time_dif[state]:
        mean[state][0] += time_dif[state][x]

    mean[state][0] = mean[state][0]/len(time_dif[state])




#  q2

param2 = {}

for state in time_dif:
    param2[state] = {}

    for x in time_dif[state]:
        param2[state][0] = 0.0
        param2[state][0] += -np.sum( np.square(x - time_dif[state][x])/ (2 * np.square(time_dif[state][x]) + 1) )

    #param2[state][0] = EmpiricalCovariance().fit(tempMean)
    
param3 = {}

for state in time_dif:
    param3[state] = {}
    param3[state][0] = 0.0
#time to quadruple
for state in time_dif:
    n = 0
    time = 0.0
    
    for x in time_dif[state]:

        if time_dif[state][x] > 0.0 and n == 0:
            
            n = time_dif[state][x]
            time += 1

        elif time_dif[state][x] > 0.0 and n != 0 and param3[state][0] == 0.0:
            time += 1
            if(time_dif[state][x] >= (n*8)):
                param3[state][0] = time






#estimation of trends    
regression = linear_model.LinearRegression()

def func(a, b, x):
    return a + b*x

param4 = {}

for state in time_dif:
    param4[state] = {}
    numToAdd = 0.0
    for x in time_dif[state]:
        numToAdd += time_dif[state][x]/400.0
    param4[state][0] = 0.0
    param4[state][0] = numToAdd


param5 = {}
# mean squared error
for state in time_dif:
    temp = np.array(0)
    expected = np.array(0)

    expectedNum = 1
    param5[state] = {}
    for x in time_dif[state]:
        expectedNum += ( time_dif[state][x] + expectedNum * 1 )/ 200

    param5[state][0] = 0.0
    param5[state][0] = expectedNum





for state in time_dif_final:
    param_dict[state] = {}
    param_dict[state][0] = mean[state][0]
    param_dict[state][1] = param2[state][0]
    param_dict[state][2] = param3[state][0]
    param_dict[state][3] = param4[state][0]
    param_dict[state][4] = param5[state][0]

    #print(param_dict[state][0], ",", param_dict[state][1], param_dict[state][2], ",", param_dict[state][3], ",", param_dict[state][4],sep = '')

print("single linkage and hierarchical clustering")
countries = sorted([c for c in param_dict.keys()])



def manhattan(a,b):
    return sum( pow((a[i]-b[i]), 2) for i in range(len(a)))


 # single linkage distance
def sld(cluster1, cluster2): 
    res = float('inf')
    # c1, c2 each is a country in the corresponding cluster
    for c1 in cluster1:
        for c2 in cluster2:
            dist = manhattan(param_dict[c1], param_dict[c2])
            if dist < res:
                res = dist
    return res

k = 8



# hierarchical clustering (sld, 'manhattan')
n = len(param_dict)
clusters = [{d} for d in param_dict.keys()]
for _ in range(n-k):
    dist = float('inf')
    best_pair = (None, None)
    for i in range(len(clusters)-1):
        for j in range(i+1, len(clusters)):
            if sld(clusters[i], clusters[j]) < dist:
                dist = sld(clusters[i], clusters[j])
                best_pair = (i,j)
    new_clu = clusters[best_pair[0]] | clusters[best_pair[1]]
    clusters = [clusters[i] for i in range(len(clusters)) if i not in best_pair]
    clusters.append(new_clu)

new_clusters = {}


xTemp = 0

newClusta = {}
for c in countries:
    nTemp = 0
    for cluster in clusters:
        for clusterCountry in cluster:
            if(str(c) == str(clusterCountry)):
                
                newClusta[xTemp] = 0
                newClusta[xTemp] = nTemp

                xTemp += 1
                break
        nTemp += 1


for c in newClusta:
    print(newClusta[c], ",", sep = '', end = '')




#todo complete linkage hierarchical clustering




## k-means (manhattan)
import copy



def center(cluster):
    for c in cluster:
        print("THIS IS D DICT C", param_dict[c])
    return np.average([param_dict[c] for c in cluster], axis=0)
    
    
init_num = np.random.choice(len(countries) - 1, k)
clusters = [{countries[i]} for i in init_num]
while True:
    new_clusters = [set() for _ in range(k)]
    centers = [center(cluster) for cluster in clusters]
    print("this is clusters", clusters)
    print("this is centers", centers)
    for c in countries:
        clu_ind = np.argmin([manhattan(param_dict[c], centers[i]) for i in range(k)])
        new_clusters[clu_ind].add(c)
    if all(new_clusters[i] == clusters[i] for i in range(k)):
        break
    else:
        clusters = copy.deepcopy(new_clusters)