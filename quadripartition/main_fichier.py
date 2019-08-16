# -*- coding: utf-8 -*-
"""

@author: melkarmo
"""



""" ---- PARTIE SPLIT ---- """



from PIL import Image
from math import sqrt

im = Image.open("Image10.bmp")
px = im.load()
w, h = im.size
regions = [] # tableau de sauvegarde des modifications au cours du split



""" Les fonctions de base """


# la fonction suivante lit la valeur d'un pixel
def lirePixel(x,y) : 
    return px[x,y]
    
# la fonction suivante affecte une couleur à un pixel
def affecterPixel(x,y,r,g,b) : 
    px[x,y] = int(r), int(g), int (b)

# la fonction suivante affecte une couleur une zone
# une zone est repérée par sa largeur x, sa hauteur h, et par un pixel (x,y)
def colorierZone(x,y,w,h,r,g,b) :
    for i in range(x,x+w):
        for j in range(y,y+h):
            affecterPixel(i,j,r,g,b)
            
            
""" L'homogénéïté """


# la fonction suivante détermine la couleur moyenne d'une zone en effectuant la moyenne des composantes r,g,b de tous les pixels de la zone
def moyenneZone(x,y,w,h):
    somme = [0,0,0]
    n = w*h
    for i in range(x,x+w):
        for j in range(y,y+h):
            somme[0] += px[i,j][0]
            somme[1] += px[i,j][1]
            somme[2] += px[i,j][2]
    res = [u//n for u in somme]
    return res

# la fonction suivante détermine l'écart-type de chaque composante r,g,b de la zone par la formule de König-Huygens    
def ecartTypeZone(x,y,w,h):
    somme = [0,0,0]
    moy = moyenneZone(x,y,w,h)
    n = w*h
    for i in range(x,x+w):
        for j in range(y,y+h):
            somme[0] += (px[i,j][0])**2
            somme[1] += (px[i,j][1])**2
            somme[2] += (px[i,j][2])**2
    res = [sqrt(somme[k]/n - moy[k]**2) for k in range(3)]
    return res
    
# la fonction suivante renvoie le maximum des écart-type de chaque composante r,g,b d'une zone
def homogene(x,y,w,h):
    e = ecartTypeZone(x,y,w,h)
    return max(e)


""" L'algorithme de Split """


def QT(x,y,w,h,s):
    if (w>1 and h>1):
        if homogene(x,y,w,h)<s:
            red,green,blue = moyenneZone(x,y,w,h) #couleur moyenne
            colorierZone(x,y,w,h,red,green,blue) #coloriage de la zone
            regions.append([x,y,w,h,(red,green,blue)]) #sauvegarde d'informations
        else:
            #on divise en 4 !
            QT(x,y,w//2,h//2,s)
            QT(x+w//2,y,w//2,h//2,s)
            QT(x,y+h//2,w//2,h//2,s)
            QT(x+w//2,y+h//2,w//2,h//2,s)

# la fonction suivante applique l'algorithme de quadripartition à l'image et affiche l'image résultante
# pour un seuil s donné
def split(s):
    QT(0,0,w,h,s)
    im.show()
    
    
    
    
    
    
""" ---- PARTIE MERGE ---- """



""" Adjacence """


# la fonction suivante teste si les régions i et j sont adjacentes
def adjacents(i,j):
    [x1,y1,w1,h1,(r1,g1,b1)] = regions[i]
    [x2,y2,w2,h2,(r2,g2,b2)] = regions[j]
    x1c = x1 + w1/2
    x2c = x2 + w2/2
    y1c = y1 + h1/2
    y2c = y2 + h2/2
    return ( (abs(x2c-x1c)<=((w1+w2)/2)) and (abs(y2c-y1c)<=((h1+h2)/2)) )
    
# la fonction suivante renvoie la liste d'adejacence des régions
def liste_adjacence(reg):
    n = len(reg)
    ral = [[k] for k in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                if adjacents(i,j):
                    ral[i].append(j)
    return ral


""" Couleurs proches """

   
# la fonction suivante teste si les régions i et j sont de couleurs proches par rapport à un seuil
def proches(i,j,reg,seuil):
    ri,gi,bi = reg[i][-1]
    rj,gj,bj = reg[j][-1]
    return max(abs(ri-rj),abs(gi-gj),abs(bi-bj)) <= seuil
    
    
""" L'algorithme de Merge """


# la fonction suivante renvoie la couleur moyenne de régions proches
def moyenneRegions(proches,regions):
    somme = [0,0,0]
    n = len(proches)
    for ind in proches:
        r,g,b = regions[ind][-1]
        somme[0] += r
        somme[1] += g
        somme[2] += b
    return [u//n for u in somme]

# la fonction suivante est la fonction principale de fusion/Merge
def fusion(reg,seuil):
    L = liste_adjacence(reg)
    n = len(reg)
    # Première partie : construction de la liste des proches
    for i in range(n):
        if L[i][-1] != 'D':
            j = 1
            m = len(L[i])
            while j < m :
                ind = L[i][j]
                if L[ind][-1] != 'D' and ind != i:
                    if proches(i,ind,reg,seuil):
                        L[i] = L[i] + L[ind]
                        L[ind].append('D')
                        j += 1
                    else:
                        del(L[i][j])
                elif ind == i:
                    del(L[i][j])
                else:
                    j += 1
                m = len(L[i])
    # Deuxième partie : coloriage
    for k in range(len(L)):
        if L[k][-1] != 'D':
            L[k] = list(set(L[k]))
            rouge,vert,bleu = moyenneRegions(L[k],reg)
            for ind in L[k]:
                x,y,w,h,(r,g,b) = reg[ind]
                colorierZone(x,y,w,h,rouge,vert,bleu)
         
# la fonction suivante applique l'algorithme de fusion à l'image et affiche l'image résultante pour un seuil s donné
# il faut au préalable avoir exécuter la fonction split pour assurer la création de la liste regions
def merge(s):
    fusion(regions,s)
    im.show()
            
        
                
                    
                
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
    
            
            
    
    

    

        
    
    


    
            
            
    
    
            













