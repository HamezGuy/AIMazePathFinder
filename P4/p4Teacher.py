import numpy as np

'''
Todo: 
1. Part 1 in P4.
2. Euclidean distance (currently are all manhattan in my code below)
3. Complete linkage distance
4. Total distortion
5. Output all required information in correct format

PS: Currently, I choose 
	n = num of all distinct countries, and
	m = 3 (latitude, longitude, total deaths until Jun27, 
		  i.e., 1st, 2nd, last number for each country as parameters).
	Also, for countries that have several rows, I average the latitude, longitude and sum up the deaths.

	You may need to change some of that based on your part 1 results.

'''



# For 'South Korea', and "Bonaire Sint Eustatius and Saba" (line 145 and 257), I removed the ',' in name manually
with open('allDeaths.csv') as f:
    data = list(f)[1:]

d_dict = {}
for d in data:
    l = d.strip('\n').split(',')
    c = l[1]  # country
    if c in d_dict:
        d_dict[c][0].append(float(l[8]))
        d_dict[c][1].append(float(l[9]))
        d_dict[c][2].append(float(l[100]))
    else:
        d_dict[c] = [[float(l[8])], [float(l[9])], [float(l[100])]]
d_dict = {k:np.array([sum(v[0])/len(v[0]), sum(v[1])/len(v[1]), sum(v[2])]) for k,v in d_dict.items()}

countries = sorted([c for c in d_dict.keys()])

print(d_dict.keys)

def manhattan(a,b):
    return sum(abs(a[i]-b[i]) for i in range(len(a)))


 # single linkage distance
def sld(cluster1, cluster2): 
    res = float('inf')
    # c1, c2 each is a country in the corresponding cluster
    for c1 in cluster1:
        for c2 in cluster2:
            dist = manhattan(d_dict[c1], d_dict[c2])
            if dist < res:
                res = dist
    return res


k = 7


# hierarchical clustering (sld, 'manhattan')
n = len(d_dict)
clusters = [{d} for d in d_dict.keys()]
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
print(clusters)

## k-means (manhattan)
import copy
def center(cluster):
    for c in cluster:
        print("This is c in CLUSTER", c)
        print("THIS IS D DICT C", d_dict[c])
    return np.average([d_dict[c] for c in cluster], axis=0)

    
init_num = np.random.choice(len(countries) - 1, k)
clusters = [{countries[i]} for i in init_num]
while True:
    new_clusters = [set() for _ in range(k)]
    centers = [center(cluster) for cluster in clusters]
    print("this is clusters", clusters)
    print("this is centers", centers)
    for c in countries:
        clu_ind = np.argmin([manhattan(d_dict[c], centers[i]) for i in range(k)])
        new_clusters[clu_ind].add(c)
    if all(new_clusters[i] == clusters[i] for i in range(k)):
        break
    else:
        clusters = copy.deepcopy(new_clusters)