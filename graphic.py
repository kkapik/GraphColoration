from tkinter import *
from tkinter.messagebox import showinfo
import random
from math import *
import time
from noeud import *


# --------------------------------------------------------


class ZoneAffichage(Canvas):
    def __init__(self, parent, w=500, h=400, _bg='white'):  # 500x400 : dessin final !
        self.__w = w
        self.__h = h
        self.__liste_noeuds = []

        # Pour avoir un contour pour le Canevas
        self.__fen_parent=parent
        Canvas.__init__(self, parent, width=w, height=h, bg=_bg, relief=RAISED, bd=5)


    def get_dims(self):
        return (self.__w, self.__h)

    def creer_noeud(self, x_centre, y_centre, rayon , col, fill_color="white",n=0):
        noeud=Balle(self, x_centre, y_centre, rayon , col, fill_color,n)
        self.pack()
        return noeud

    def action_pour_un_clique(self, event):
        print("Trace : (x,y) = ", event.x, event.y)
        #showinfo('Résultat ', "Arrrgh : vous avez dans la fenetre" + '\nThanks !')
        
        # Placer un noeud à l'endroit cliqué
        self.__fen_parent.placer_un_noeud(event.x, event.y)

    def placer_un_noeud_sur_canevas(self, x_centre, y_centre, col=None, fill_color="white", n= 0):
        w,h = self.get_dims()
        rayon=10
        if col == None :
            col= random.choice(['green', 'blue', 'red', 'magenta', 'black', 'maroon', 'purple', 'navy', 'dark cyan'])

        node=self.creer_noeud(x_centre, y_centre, rayon , col, fill_color,n)
        self.update()

        self.__fen_parent.set_coordonnes_du_last_node(x_centre, y_centre)
        return node.get_node_ident()


class FenPrincipale(Tk):
    def __init__(self,n):
        Tk.__init__(self)
        self.title('COLORATION GRAPHE')
        self.__zoneAffichage = ZoneAffichage(self)

        self.__zoneAffichage.pack()
        self.__nodelist = n
        self.__nodetreated = []
        self.__colors = ['red','green','blue', 'orange', 'yellow']

        # ----------------------------
        # Création d'un widget Button (bouton Effacer)
        self.__boutonUpdate = Button(self, text='Update', command=self.update)
        self.__boutonUpdate.pack(side=LEFT, padx=5, pady=5)
        
        # Création d'un widget Button (bouton Quitter)
        self.__boutonQuitter = Button(self, text='Quitter', command=self.destroy).pack(side=LEFT, padx=5, pady=5)

        self.__liste_d_ident_d_objets_crees=[]
        self.__liste_coordonnes_centre_des_nodes=[]

        self.placer_noeud_depart()
        self.placer_aretes()

    def placer_noeud_depart(self):
        w,h = self.__zoneAffichage.get_dims()
        for i in range(len(self.__nodelist)):
            x_centre, y_centre = 250+175*cos((i*2*pi)/len(self.__nodelist)), 200+175*sin((i*2*pi)/len(self.__nodelist))
            node= self.__zoneAffichage.placer_un_noeud_sur_canevas(x_centre, y_centre, col=self.__nodelist[i].get_color(), fill_color=self.__nodelist[i].get_color(), n=i)
            self.add_a_node_to_your_list(node)
            self.__liste_coordonnes_centre_des_nodes.append((x_centre, y_centre))

    def placer_aretes(self):
        for i in range(len(self.__nodelist)):
            neighbours= self.__nodelist[i].get_neighbours()
            for j in neighbours:
                self.__zoneAffichage.create_line(250+175*cos((i*2*pi)/len(self.__nodelist)), 200+175*sin((i*2*pi)/len(self.__nodelist)),250+175*cos((j*2*pi)/len(self.__nodelist)), 200+175*sin((j*2*pi)/len(self.__nodelist)))
                
    def not_finish(self): # on vérifie que les noeuds voisins ont des couleurs différentes. Renvoie True si des voisins sont de la même couleur
        diff = False
        for i in self.__nodelist:
            neighbours = i.get_neighbours()
            color = i.get_color()
            for j in neighbours:
                diff = ((color == self.__nodelist[j].get_color()) or diff)
        print(diff)
        return diff
    
    def update(self):
        if self.not_finish():
            print("C'est pas fini")
            #On reçoit les messages des voisins
            for i in self.__nodelist:
                neighbours = i.get_neighbours()
                new_mess = [0,0,0,0,0]
                for j in neighbours:
                    for c in range(len(self.__colors)):
                        if self.__colors[c] == self.__nodelist[j].get_color():
                            new_mess[c] += 1
                i.set_message(new_mess)
            
            ## On regarde pour quel noeud ont a le maximum de message dans le même sens
            maxinode = (0,0,0) # (indice_noeud, indice_couleur, valeur)
            for i in range(len(self.__nodelist)):
                m = self.__nodelist[i].get_maximum()
                if ((m[1]>= maxinode[2]) and not(i in self.__nodetreated)):
                    maxinode = (i, m[0], m[1])
            print(maxinode)
            #On modifie sa couleur en choisissant une couleur différente de ses voisins
            message = self.__nodelist[maxinode[0]].get_message()
            c=0
            print(message)
            while message[c] != 0: #s'arrete à l'indice d'une couleur qu'aucun de ses voisins a
                c+=1
            
            self.__nodelist[maxinode[0]].set_color(self.__colors[c])
            
            #On le marque comme traité
            self.__nodetreated.append(maxinode[0])
            print('Noeud ', maxinode[0], ' devient ', self.__colors[c], '\n')
            
            #On dessine
            x_centre, y_centre = 250+175*cos((maxinode[0]*2*pi)/len(self.__nodelist)), 200+175*sin((maxinode[0]*2*pi)/len(self.__nodelist))
            node= self.__zoneAffichage.placer_un_noeud_sur_canevas(x_centre, y_centre, col=self.__nodelist[maxinode[0]].get_color(), fill_color=self.__nodelist[maxinode[0]].get_color())
            self.add_a_node_to_your_list(node)
            self.__liste_coordonnes_centre_des_nodes.append((x_centre, y_centre))
        else:
            print("C'est fini")
            self.__boutonUpdate["state"] = DISABLED
    
    
    def add_a_node_to_your_list(self, noeud) :
        self.__liste_d_ident_d_objets_crees.append(noeud)

    def set_coordonnes_du_last_node(self, x_centre, y_centre):
        self.__last_node=(x_centre, y_centre)

    
    #--------------------------
#--------------------------
class Balle:
    def __init__(self, canvas, cx, cy, rayon, couleur, fill_color="white",n= 0):
        self.__cx, self.__cy = cx, cy
        self.__rayon = rayon
        self.__color = couleur
        self.__can = canvas  # Il le faut pour les déplacements

        self.__canid = self.__can.create_oval(cx - rayon, cy - rayon, cx + rayon, cy + rayon, outline=couleur, fill=fill_color)
        self.__canid2 = self.__can.create_text(cx,cy, text = n)
        # Pour 3.6 : col: object  # essaie typage !

    def get_node_ident(self):
        return self.__canid


# ------------------------------------------------------
# Réutilisation des formes

# --------------------------------------------------------
if __name__ == "__main__":
    node=[]
    for i in range(10):
       node.append(Node())
    
    node[0].set_neighbours([1,2,5,6,7])
    node[1].set_neighbours([0,5,6,8])
    node[2].set_neighbours([0])
    node[3].set_neighbours([4,7])
    node[4].set_neighbours([3])
    node[5].set_neighbours([0,1,9])
    node[6].set_neighbours([0,1])
    node[7].set_neighbours([0,3])
    node[8].set_neighbours([1,9])
    node[9].set_neighbours([5,8])
    fen = FenPrincipale(node)
    fen.mainloop()
