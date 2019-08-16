# -*- coding: utf-8 -*-
"""

@author: melkarmo
"""

S = [1,2,5,10,20,50,100,200,500,1000,2000,5000,10000] # liste du stock de pièces
D = [3 for i in range (len(S))] # liste des disponibilités

# t est la liste-solution
# M est le montant entré
# i l'indice de la pièce maximale utilisable dans S

def glouton_aux_sans_disponibilite(S,M,t,i):
    if M == 0 :
        return t
    else :
        while S[i]>M: 
            i -= 1
        nb_de_pieces = M // S[i]
        t[i] = t[i] + nb_de_pieces
        reste = M - nb_de_pieces*S[i]
        return glouton_aux_sans_disponibilite(S,reste,t,i-1)
        
def glouton_sans_disponibilite(S,M) :
    T = [0 for i in range (len(S))] 
    return glouton_aux_sans_disponibilite(S,M,T,len(S)-1) 
        
        
        
def glouton_aux_avec_disponibilite(S,M,t,i):
    if M == 0 :
        return t
    elif i < 0:
        return "Il n'y a plus d'argent dans la machine!"
    else :
        while S[i]>M:
            i -= 1
            if i<0 : return glouton_aux_avec_disponibilite(S,M,t,i)
        nb_de_pieces = M // S[i]
        nb_de_pieces = min(D[i], nb_de_pieces) # on prend en compte les disponibilités
        D[i] = D[i] - nb_de_pieces # on met à jour la liste des disponibilités
        t[i] = t[i] + nb_de_pieces
        reste = M - nb_de_pieces*S[i]
        return glouton_aux_avec_disponibilite(S,reste,t,i-1)
          
def glouton_avec_disponibilite(S,M) :
    T = [0 for i in range (len(S))] 
    return glouton_aux_avec_disponibilite(S,M,T,len(S)-1)
    

# --- tests ---

print(glouton_sans_disponibilite(S,389))
print(glouton_avec_disponibilite(S,389))
    
