class Node:
    def __init__(self):
        self.__color = 'red'
        self.__neighbours = []
        self.__message = [0,0,0,0,0]
        self.__messagemax = (0,0) # (indice_couleur, valeur)
        return None
    
    def set_color(self, color):
        self.__color = color
    
    def get_color(self):
        return self.__color
    
    def set_neighbours(self,l):
        self.__neighbours= l
    
    def get_neighbours(self):
        return self.__neighbours
    
    def set_message(self,l):
        self.__message =l
        maximum = 0
        for i in range(5):
            if maximum <= self.__message[i]:
                self.__messagemax = (i, self.__message[i])
                maximum = self.__message[i]
    
    def get_message(self):
        return self.__message
    
    def get_maximum(self):
        return self.__messagemax