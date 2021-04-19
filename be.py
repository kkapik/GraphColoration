## Importation
from noeud import *

##Initialisation
colors = ['red','green','blue', 'orange', 'yellow']

#Création des noeuds avec leur voisin
node=[]
for i in range(5):
   node.append(Node())

node[0].set_neighbours([1,3,4])
node[1].set_neighbours([0,2])
node[2].set_neighbours([1])
node[3].set_neighbours([0,4])
node[4].set_neighbours([0,3])


## fonction pour la terminaison

def not_finish(): # on vérifie que les noeuds voisins ont des couleurs différentes. Renvoie True si des voisins sont de la même couleur
    diff = False
    for i in node:
        neighbours = i.get_neighbours()
        color = i.get_color()
        for j in neighbours:
            diff = ((color == node[j].get_color()) or diff)
    return diff


## Itération
treated=[]
while not_finish():
    #On reçoit les messages des voisins
    for i in node:
        neighbours = i.get_neighbours()
        new_mess = [0,0,0,0,0]
        for j in neighbours:
            for c in range(len(colors)):
                if colors[c] == node[j].get_color():
                    new_mess[c] += 1
        i.set_message(new_mess)
    
    ## On regarde pour quel noeud ont a le maximum de message dans le même sens
    maxinode = (0,0,0) # (indice_noeud, indice_couleur, valeur)
    for i in range(len(node)):
        m = node[i].get_maximum()
        if ((m[1]>= maxinode[2]) and not(i in treated)):
            maxinode = (i, m[0], m[1])
    print(maxinode)
    #On modifie sa couleur en choisissant une couleur différente de ses voisins
    message = node[maxinode[0]].get_message()
    c=0
    print(message)
    while message[c] != 0: #s'arrete à l'indice d'une couleur qu'aucun de ses voisins a
        c+=1
    
    node[maxinode[0]].set_color(colors[c])
    
    #On le marque comme traité
    treated.append(maxinode[0])
    print('Noeud ', maxinode[0], ' devient ', colors[c], '\n')



if __name__ == "__main__":
    for i in range(len(node)):
        print('Node ', i, ' is ',node[i].get_color())