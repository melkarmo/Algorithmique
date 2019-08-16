import numpy as np

def copie_mat(m):
    n = len(m)
    res = [[0 for i in range(n)] for j in range(n)]
    for k in range(n):
        for l in range(n):
            res[k][l] = m[k][l]
    return res

def minimum(a,b):
    if a == 'infini':
        return b
    elif b == 'infini':
        return a
    else:
        return min(a,b)

def addition(a,b):
    if a == 'infini' or b == 'infini':
        return 'infini'
    else:
        return a + b

def exception(n,e):
    res = [i for i in range(n)]
    res.pop(e)
    return res

def compare(a,b):
    if b == 'infini':
        return 0
    elif a == 'infini' and b != 'infini':
        return 1
    else:
        if a > b:
            return 1
        else:
            return 0
    
def bellman_ford (m,source):
    n = len(m)
    dist = ['infini' for i in range(n)]
    pere = [None for j in range(n)]
    dist[source] = 0
    pere[source] = source
    t1 = exception(n,source)
    for v in t1:
        t2 = exception(n,v)
        for u in t2:
            a = addition(dist[u],m[u][v])
            if compare(dist[v],a) == 1:
                dist[v] = a
                pere[v] = u
    return [dist, pere]                       

def floyd_warshall (m):
    r = copie_mat(m)
    n = len(r)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                r[i][j] = minimum(r[i][j],
                                 addition(r[i][k],r[k][j])
                                 )
    return r

test = [[0,3,8,'infini',-4],
        ['infini',0,'infini',1,7],
        ['infini',4,0,'infini','infini'],
        [2,'infini',-5,0,'infini'],
        ['infini','infini','infini',6,0]]

test2 = [[0,2,5,1,'infini','infini'],
         [2,0,3,2,'infini','infini'],
         [5,3,0,3,1,5],
         [1,2,3,0,1,'infini'],
         ['infini','infini',1,1,0,2],
         ['infini','infini',5,'infini',2,0]]


                    
                
