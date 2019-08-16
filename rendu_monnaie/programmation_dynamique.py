# -*- coding: utf-8 -*-
"""

@author: melkarmo
"""

S = [1,2,5,10,20,50,100,200,500,1000,2000,5000,10000] # liste du stock de pièces

# la fonction suivante est une fonction qui donne le minimum de a et b 
# en autorisant a ou b à être infinis
def mini(a,b):
    if a == "infini" :
        return b
    elif b == "infini" :
        return a
    else :
        return min(a, b)

def monnaie(S,M):
    
    mat = [ [0 for j in range(M+1)] for k in range(len(S)+1)] # matrice des solutions optimales
    memoire = [ [0 for j in range(M+1)] for k in range(len(S)+1)] # matrice de mémorisation
    t = [0 for j in range (len(S))] # liste-solution
    
    # --- double-iteration ---
    
    for i in range(0, len(S)+1):
        for m in range(0, M+1):
            
            if m == 0:
                mat[i][m] = 0
                
            elif i == 0:
                mat[i][m] = "infini"
                
            else:
                ajout = 0
                if (m - S[i-1]) >= 0 :
                    ajout = 1 + mat[i][(m - S[i-1])]
                else : 
                    ajout = "infini"
                declin = 0
                if i >= 1 :
                    declin = mat[i-1][m]
                else :
                    declin = "infini"
                mat[i][m] = mini(ajout, declin)
                
                # --- memorisation ---
                
                if mat[i][m] != "infini":
                    if mat[i][m] == ajout :
                        memoire[i][m] = "ajout"
                    elif mat[i][m] == declin :
                        memoire[i][m] = "declin"
    
    # --- restitution ---
                     
    x, y= M, len(S)
    while x > 0 and y > 0:
        if memoire[y][x] == "ajout":
            t[y-1] += 1
            x = x - S[y-1]
        elif memoire[y][x] == "declin":
            y = y -1
            
    return mat[len(S)][M], t
                
 
# --- tests ---
               
print(monnaie(S,389))        
                
                
                
                
                
                
                
                
                
                
                