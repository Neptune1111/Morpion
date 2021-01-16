from tkinter import *
from math import *
from copy import deepcopy

#fenetre = Tk()

class Morpion(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.joueur = "J1"
        self.listeCases = []
        self.x, self.y = 300,300
        self.setup_canvas = Canvas(self, height=self.y, width=self.x, bg="grey")

        self.bord = 0
        self.distancePointsGrille = sqrt((self.x//3-self.x//3)**2 + ((self.y-self.bord-self.bord)**2))
        self.cote = self.distancePointsGrille//3
        self.case_bord = 20

        self.listeDebutcanvas = [ [(((self.bord)+j*self.cote),((self.bord)+i*self.cote)) for j in range(3)] for i in range(3)]

        


    def getPos(self,event):
        """
            Donne la positon de la sourie
            Renvoie sous la forme d'u
            n tuple (x,y)
        """
        xPos,yPos = event.x,event.y
        
        cases = self.distancePointsCases(xPos,yPos)
        self.jouer(cases[0],cases[1])
        return (xPos,yPos)
        

    def distancePointsCases(self,xPos,yPos):
        """
            Crée une liste des distances entre chaque point
            et début de canvas.
            Cherche le plus petit et le fais correspondre à
            une case.
        """
            # Liste Distances Points-Cases, [x][y] (case à jouer)
        listeDistance_Cases=[((xPos - (self.listeDebutcanvas[i//3][i%3][0]+self.cote//2))**2 + (yPos - (self.listeDebutcanvas[i//3][i%3][1]+self.cote//2))**2,(i//3,i%3)) for i in range(9)]
            # Trouver le point le plus proche
        listeDistance_Cases.sort()
            # Sort de la première
            #  liste la case à jouer (faciliter la lecture)
        caseJouerX = listeDistance_Cases[0][1][0]
        caseJouerY = listeDistance_Cases[0][1][1]
        
        
        return caseJouerX,caseJouerY
             
    def grille(self):
        """
            Initialise la site des cases vides,
            Crée dans l'interface graphique la grille du morpion.
        """
             #Barres Vertical du Morpion
        self.setup_canvas.create_line(self.x//3, self.bord, self.x//3, self.y-self.bord)
        self.setup_canvas.create_line((2*self.x)//3, self.bord, (2*self.y)//3, self.y-self.bord)
            #Barres Horizontal du Morpion
        self.setup_canvas.create_line(self.bord, self.y//3, self.x-self.bord, self.y//3)
        self.setup_canvas.create_line(self.bord, (2*self.y)//3, self.x-self.bord, (2*self.y)//3)

        self.setup_canvas.bind("<Button-1>",self.getPos)
        self.setup_canvas.pack()
        self.listeCases = [["." for _ in range(3)] for _ in range(3)]
        return self.listeCases

    def jouer(self,caseX,caseY):
        """
            Permet au joueur de jouer
            Rajoute J1 ou J2 dans la listeCases
        """
        if self.joueur == "J1" and caseEstVide(self.listeCases,caseX,caseY):
            self.listeCases[caseX][caseY]="X"
            self.croix(caseX,caseY,self.setup_canvas)
            self.joueur = "J2"
            if self.victoire(caseX,caseY):
                label_victory = Label(self,text="Le Joueur 1 a gagné !")
                label_victory.pack()        
            else :
                meilleur_coup = self.minimax(self.listeCases,9,True)
                self.jouer(meilleur_coup[1][0],meilleur_coup[1][1])
        elif self.joueur == "J2" and caseEstVide(self.listeCases,caseX,caseY) == True:
                self.listeCases[caseX][caseY]="O"
                self.rond(caseX,caseY,self.setup_canvas)
                self.joueur = "J1"
                if self.victoire(caseX,caseY):
                    label_victory = Label(self,text="Le Joueur 2 a gagné !")
                    label_victory.pack()
                    

    def quitter(self):
        """
            Crée un boutton quitter
        """
        but_quit = Button(self, text="Quitter", command=quit)
        but_quit.pack(side="bottom")   
    
    def croix(self,xCase,yCase,canvas):
        """
            Dessine une croix en fonction d'une longueur et d'une largeur max
        """
            # Distance : sqrtroot([x2-x1]**2 + [y2-y1]**2)
        
            #Deux lignes de la croix -eux gènes.
        ligneCroixL = canvas.create_line(self.case_bord,self.case_bord,self.cote-(self.case_bord),self.cote-(self.case_bord),width=5)
        ligneCroixR = canvas.create_line(self.cote-(self.case_bord),self.case_bord,self.case_bord,self.cote-(self.case_bord),width=5)
            #Déplacement des parties de la croix dans la bonne case
        self.setup_canvas.move(ligneCroixL,self.listeDebutcanvas[xCase][yCase][0],self.listeDebutcanvas[xCase][yCase][1])
        self.setup_canvas.move(ligneCroixR,self.listeDebutcanvas[xCase][yCase][0],self.listeDebutcanvas[xCase][yCase][1])
            #Mise en place sur la grille
        self.setup_canvas.pack()
    
    def rond(self, xCase, yCase, canvas):
        """
            Dessine un rond sur la case requise en fonction du point de l'angle du canvas
        """
            #create_oval(x1,y1,x2,y2) les points sont les coins d'un rectangle, où le cercle tient
        rond = canvas.create_oval(self.case_bord,self.case_bord,self.cote-(self.case_bord),self.cote-(self.case_bord),width=5)
            #Déplacement de l'oval
        self.setup_canvas.move(rond, self.listeDebutcanvas[xCase][yCase][0], self.listeDebutcanvas[xCase][yCase][1])       
    
    
    def victoire(self,xCoup,yCoup):
        """
            Vérifie s'il y a un gagnant
            Affiche un label "Victoire JX"
        """
            # Victoire Horizontal
        grille = self.listeCases
        if grille[xCoup][0]==grille[xCoup][1]==grille[xCoup][2] and grille[xCoup][0] != ".":
            return True
            # Victoire Verticale
        if grille[0][yCoup]==grille[1][yCoup]==grille[2][yCoup] and grille[0][yCoup] != ".":
            return True
            # Victoire Diagonale Inf/Sup
        if grille[2][0]==grille[1][1]==grille[0][2] and grille[2][0] != ".":
            return True
            # Victoire Diagonale Sup/Inf
        if grille[0][0]==grille[1][1]==grille[2][2] and grille[0][0] != ".":
            return True
        return False
        
    def reset(self):
        """
            Remet la partie à 0
        """
            # Détruit le canvas
        self.setup_canvas.destroy()
            # Recrée le Canvas
        self.setup_canvas = Canvas(self, height=self.y, width=self.x, bg="grey")
            # Recrée le bouton 
        but_reset = Button(self,text="Recommencer",command=self.grille)
            # Replace le canvas et le bouton
        self.setup_canvas.pack()    
        but_reset.pack(side="top")





    def minimax(self,position,profondeur,maxPlayer):
        """
            Position : est un grille à un instant t du jeu (peut être hypothétique)
            maxPLayer : Selon le joueur, on voudra maximiser les gains (J2, l'IA) ou minimiser les pertes (J1, le joueur).
        """
        if score(position)!=0:
            return (score(position),(0,0))
        if grillePleine(position):
            return (0,(0,0)) 

        g_possible = coup_possible(position,"J2")
        if profondeur == 0:
            return (0,g_possible[0][1])
        
        if maxPlayer == True:
            coup_j = []
            for i in range(len(g_possible)):
                coup_j.append((self.minimax(g_possible[i][0],profondeur-1,not maxPlayer)[0],g_possible[i][1]))
            return max(coup_j)
            
        else :
            g_possible = coup_possible(position,"J1")
            coup_j = []
            for i in range(len(g_possible)):
                coup_j.append((self.minimax(g_possible[i][0],profondeur-1,not maxPlayer)[0],g_possible[i][1]))
            return min(coup_j)
            
                
def grillePleine(grille):
    for i in range(3):
        for j in range(3):
            if grille[i][j] == ".":
                return False
    return True


def coup_possible(grille,joueur):
    """
        A partir d'une grille et d'un joueur,
        crée une liste de différente grille pour chaque coup possible 
    """
    if joueur == "J2":
        liste_grillesPossibles=[]
        for i in range(3):
            for j in range(3):
                if caseEstVide(grille,i,j):
                    nouvelleGrille = deepcopy(grille)
                    nouvelleGrille[i][j]="O"
                    liste_grillesPossibles.append((nouvelleGrille,(i,j)))
    if joueur == "J1":
        liste_grillesPossibles=[]
        for i in range(3):
            for j in range(3):
                if caseEstVide(grille,i,j):
                    nouvelleGrille = deepcopy(grille)
                    nouvelleGrille[i][j]="X"
                    liste_grillesPossibles.append((nouvelleGrille,(i,j)))
    return liste_grillesPossibles

def unGagnant(grille):
    """
        Avec une grille donnée, détermine si il y a un gagnant ou non
    """
    gagnant = ""
        #Victoires Horizontal
            #Victoires J1
    if grille[0][0]==grille[0][1]==grille[0][2] and grille[0][0]=="X":
        gagnant = "J1"
        return gagnant
    if grille[1][0]==grille[1][1]==grille[1][2] and grille[1][0]=="X":
        gagnant = "J1"
        return gagnant
    if grille[2][0]==grille[2][1]==grille[2][2] and grille[2][0]=="X":
        gagnant="J1"
        return gagnant
            #Victoires J2
    if grille[0][0]==grille[0][1]==grille[0][2] and grille[0][0]=="O":
        gagnant = "J2"
        return gagnant
    if grille[1][0]==grille[1][1]==grille[1][2] and grille[1][0]=="O":
        gagnant = "J2"
        return gagnant
    if grille[2][0]==grille[2][1]==grille[2][2] and grille[2][0]=="O":
        gagnant="J2"
        return gagnant
        #Victoires Vertical
            #Victoires J1
    if grille[0][0]==grille[1][0]==grille[2][0] and grille[0][0]=="X":
        gagnant = "J1"
        return gagnant
    if grille[0][1]==grille[1][1]==grille[2][1] and grille[0][1]=="X":
        gagnant = "J1"
        return gagnant
    if grille[0][2]==grille[1][2]==grille[2][2] and grille[0][2]=="X":
        gagnant="J1"
        return gagnant
            #Victoires J2
    if grille[0][0]==grille[1][0]==grille[2][0] and grille[0][0]=="O":
        gagnant = "J2"
        return gagnant
    if grille[0][1]==grille[1][1]==grille[2][1] and grille[0][1]=="O":
        gagnant = "J2"
        return gagnant
    if grille[0][2]==grille[1][2]==grille[2][2] and grille[0][2]=="O":
        gagnant="J2"
        return gagnant
        #Victoires Diagonales
            #Victoires J1
    if grille[2][0]==grille[1][1]==grille[0][2] and grille[2][0]=="X":
        gagnant = "J1"
        return gagnant
    if grille[0][0]==grille[1][1]==grille[2][2] and grille[0][0]=="X":
        gagnant = "J1"
        return gagnant
            #Victoires J2
    if grille[2][0]==grille[1][1]==grille[0][2] and grille[2][0]=="O":
        gagnant = "J2"
        return gagnant
    if grille[0][0]==grille[1][1]==grille[2][2] and grille[0][0]=="O":
        gagnant = "J2"
        return gagnant
    else :
        return gagnant



def score(grille):
    if unGagnant(grille) == "J2":
        score = 1
    elif unGagnant(grille) == "J1":
        score = -1
    else :
        score = 0
    return score
    
def caseEstVide(grille,ligne,colonne):
    """
        Avec les coordonnées d'une case, retourne un booléen pour savoir
        si cette case est vide
    """
    if grille[ligne][colonne] == ".":
        return True
    return False




"""
    Programme Principales
"""
    #Initialise la grille et le cavas
jeux_morpion = Morpion()
jeux_morpion.grille()
coup_possible(jeux_morpion.grille(),"J1")
    #Initialise les deux boutons quitter et reset
jeux_morpion.quitter()
jeux_morpion.reset()


    #Lance la partie




jeux_morpion.mainloop()
