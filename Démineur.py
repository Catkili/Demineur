# coding=utf-8
"""0,1,2,3... nbr de bombs voisines
-1 il y a une bombe
0 = couvert
1= découvert
2= case marquée"""

import random
from tkinter import *

# Définition des variables globales
# (En pixels : h = 600 et L = 1000)
a = 5
b = 5
n = 5
x = 1
y = 1

# Taille des cases
cote_case = 600 / b

# Objets du canvas
rectangles = []
cases_ouvertes = 0


def cases_voisines(l, m):  # Renvoie les coordonnees des cases voisines dans la grille de taille a.b
    global a, b  # Elle prend en compte les bords et les coins
    if l == 0:
        if m == 0:
            return [[1, 0], [0, 1], [1, 1]]
        elif m == b-1:
            return [[1, m], [0, m - 1], [1, m - 1]]
        else:
            return [[0, m + 1], [0, m - 1], [1, m - 1], [1, m], [1, m + 1]]
    elif l == a-1:
        if m == 0:
            return [[l - 1, m], [l, m + 1], [l - 1, m + 1]]
        elif m == b-1:
            return [[l - 1, m], [l, m - 1], [l - 1, m - 1]]
        else:
            return [[l - 1, m - 1], [l - 1, m], [l - 1, m + 1], [l, m - 1], [l, m + 1]]
    elif m == 0:
        return [[l - 1, 0], [l + 1, 0], [l - 1, 1], [l, 1], [l + 1, 1]]
    elif m == b-1:
        return [[l - 1, m - 1], [l, m - 1], [l + 1, m - 1], [l + 1, m], [l - 1, m]]
    else:
        return [[l - 1, m], [l, m - 1], [l - 1, m - 1], [l + 1, m], [l, m + 1], [l + 1, m + 1], [l - 1, m + 1],
                [l + 1, m - 1]]


def cliquer1(event):  # Que se passe-t-il apres un clic gauche?
    global cote_case, rectangles, x, y, a, b, n, cases_ouvertes
    x = int(event.x / cote_case)  # trouve la coordonnée du clic dans la grille
    y = int(event.y / cote_case)
    if a + 1 > x > -1 and -1 < y < b + 1 and etat_grille[y][x][1] == 0:  # Si on clique sur une case pas découverte
        if etat_grille[y][x][0] == -1:  # S'il y a une bombe, le jeu s'arrete
            global fen1
            fen1 = Tk()
            tex1 = Label(fen1, text='Vous avez perdu !', fg='black')
            tex1.pack()
            bou1 = Button(fen1, text='Arrêter le programme', command=reset)
            bou1.pack()
            fen1.mainloop()
        else:  # Sinon, on ouvre la case
            plateau.delete(rectangles[y][x])
            etat_grille[y][x][1] = 1
            cases_ouvertes += 1
    if etat_grille[y][x][0] == 0:  # Si la case était vide, on ouvre le bloc
        verifier_les_zeros(x, y)
    if cases_ouvertes == a*b-n+1:
        fen1 = Tk()
        tex1 = Label(fen1, text='Vous avez gagné !', fg='black')
        tex1.pack()
        bou1 = Button(fen1, text='Arrêter le programme', command=reset)
        bou1.pack()
        fen1.mainloop()


def reset():  # Quand on  a perdu, on ferme toutes les fenêtres
    global demineur, fen1
    fen1.destroy()
    demineur.destroy()


def cliquer2(event):  # Que se passe-t-il apres un clic droit?
    global rectangles, a, b, cote_case, x, y, n
    x = int(event.x / cote_case)
    y = int(event.y / cote_case)
    if (x > -1) and (x < a) and (y > -1) and (y < b) and etat_grille[y][x][1] == 0:
        plateau.itemconfig(rectangles[y][x], fill="red")
        etat_grille[y][x][1] = 2  # Si la case n'était pas marquée, on la marque
    elif (x > -1) and (x < a) and (y > -1) and (y < b) and etat_grille[y][x][1] == 2:
        plateau.itemconfig(rectangles[y][x], fill="grey")
        etat_grille[y][x][1] = 0  # Si la cae était arquée, on la démarque


def dimensions():
    global a, b, cote_case, rectangles, etat_grille, n
    plateau.delete("all")
    a = int(taille_x.get())
    b = int(taille_y.get())
    pas_x = 1000 / a
    cote_case = 600 / b
    etat_grille = []
    for _ in range(b):  # On cree la variable etat_grille qui decrit toutes les cases
        inter = []
        for _ in range(a):
            inter.append([0, 0])
        etat_grille.append(inter)
    if pas_x < cote_case:
        cote_case = pas_x
    create_the_underframe()
    # tracer la grille - le pas est : cote_case
    # --> creer la famille de rectangles
    rectangles = []
    for k in range(b):
        rectangles.append([])
        for i in range(a):
            rectangles[k].append(plateau.create_rectangle((i * cote_case, k * cote_case),
                                                          ((i + 1) * cote_case, (k + 1) * cote_case),
                                                          fill='grey'))


def create_the_underframe():
    global underframe, a, b, n
    a = int(taille_x.get())
    b = int(taille_y.get())
    n = int(taille_n.get())
    underframe = []
    for k in range(b):
        underframe.append([])
        for i in range(a):
            underframe[k].append(plateau.create_rectangle((i * cote_case, k * cote_case),
                                                          ((i + 1) * cote_case, (k + 1) * cote_case)))


def modif_the_underframe():
    global a, b, n, underframe, etat_grille
    n = int(taille_n.get())
    a = int(taille_x.get())
    b = int(taille_y.get())
    coordinates_bombs = coordonnees_bombes()
    nombre_bombes(coordinates_bombs)
    for k in range(b):
        for i in range(a):  # On colorie toutes les cases
            if etat_grille[k][i][0] == -1:  # S'il y a une bombe
                plateau.itemconfigure(underframe[k][i], fill='black')
            elif etat_grille[k][i][0] == 1:
                plateau.itemconfigure(underframe[k][i], fill='yellow')
            elif etat_grille[k][i][0] == 2:
                plateau.itemconfigure(underframe[k][i], fill='green')
            elif etat_grille[k][i][0] == 3:
                plateau.itemconfigure(underframe[k][i], fill='pink')
            elif etat_grille[k][i][0] == 4:
                plateau.itemconfigure(underframe[k][i], fill='blue')
            elif etat_grille[k][i][0] == 0:
                plateau.itemconfigure(underframe[k][i], fill='brown')
            elif etat_grille[k][i][0] == 5:
                plateau.itemconfigure(underframe[k][i], fill='purple')
            elif etat_grille[k][i][0] == 6:
                plateau.itemconfigure(underframe[k][i], fill='orange')
            elif etat_grille[k][i][0] == 7:
                plateau.itemconfigure(underframe[k][i], fill='white')
            elif etat_grille[k][i][0] == 8:
                plateau.itemconfigure(underframe[k][i], fill='cyan')


def verifier_les_zeros(x, y):
    global etat_grille, rectangles, cases_ouvertes
    bloc_a_ouvrir = cases_vides_connectees(x, y) # Il y a des cases en double qu'il faut enlever
    vrai_bloc_a_ouvrir = []
    for k in range(len(bloc_a_ouvrir)):
        if bloc_a_ouvrir[k] not in vrai_bloc_a_ouvrir:
            vrai_bloc_a_ouvrir.append(bloc_a_ouvrir[k])
    for m in range(len(vrai_bloc_a_ouvrir)):  # On ouvre tout le bloc à ouvrir
        plateau.delete(rectangles[vrai_bloc_a_ouvrir[m][1]][vrai_bloc_a_ouvrir[m][0]])
        etat_grille[vrai_bloc_a_ouvrir[m][1]][vrai_bloc_a_ouvrir[m][0]][1] = 1
        cases_ouvertes = cases_ouvertes + 1


def cases_vides_connectees(ligne, colonne):
    pile = [(ligne, colonne)]
    connexes = []
    traite = []
    while pile != []:  # On procède par dépilage et réempilage de cas à traiter
        afaire = []
        while pile != []:
            retire = pile.pop()
            if retire not in traite:
                traite.append(retire)
                afaire.append(retire)
        for i in range(len(afaire)):
            proches = cases_voisines(afaire[i][0], afaire[i][1])
            for k in range(len(proches)):
                if etat_grille[proches[k][1]][proches[k][0]][0] == 0:
                    if proches[k] not in traite:
                        pile.append(proches[k])
                        connexes.append(proches[k])
    return connexes


def coordonnees_bombes():  # Place les bombes
    global a, b, n, etat_grille
    coordinates_bombs = []
    for i in range(b):  # Reset
        for j in range(a):
            etat_grille[i][j][0] = 0
    for h in range(n):
        position_bombe = [random.randint(0, a - 1), random.randint(0, b - 1)]
        while position_bombe in coordinates_bombs:
            position_bombe = [random.randint(0, a - 1), random.randint(0, b - 1)]
        coordinates_bombs.append(position_bombe)
        etat_grille[position_bombe[1]][position_bombe[0]][0] = -1
    return coordinates_bombs


def nombre_bombes(coordinates_bombs):  # Renvoie le nombre de bombes voisines sachant la position des bombes
    global a, b, n, etat_grille
    for l in range(a):
        for m in range(b):
            voisines = cases_voisines(l, m)
            nombre_bombes_voisines = 0
            for k in range(len(voisines)):
                if voisines[k] in coordinates_bombs:
                    nombre_bombes_voisines = nombre_bombes_voisines + 1
            if etat_grille[m][l][0] != -1:
                etat_grille[m][l][0] = nombre_bombes_voisines


# creation de la fenetre principale
demineur = Tk()
demineur.resizable(False, False)

# Frame de gauche -------------------------------
f_l = Frame(demineur, relief=FLAT, pady=20)
f_l.grid(column=0, row=0)

# canvas - affichage du plateau
plateau = Canvas(f_l, width=1000, height=600, background='white')
plateau.grid(column=0, row=0, columnspan=3)
plateau.bind('<Button-1>', cliquer1)
plateau.bind('<Button-2>', cliquer2)

# Frame de droite -------------------------------
f_d = Frame(demineur, relief=FLAT)
f_d.grid(column=2, row=0)

# choix de la taille
f_x = LabelFrame(f_d, text="Largeur (100 max) : ", padx=10, pady=10, borderwidth=2, relief=GROOVE)
f_x.grid(column=0, row=1)
taille_x = Spinbox(f_x, from_=5, to=100, command=dimensions)
taille_x.grid()
f_y = LabelFrame(f_d, text="Hauteur (100 max) : ", padx=10, pady=10, borderwidth=2, relief=GROOVE)
f_y.grid(column=0, row=2)
taille_y = Spinbox(f_y, from_=5, to=100, command=dimensions)
taille_y.grid()
# choix du nombre de bombes
f_n = LabelFrame(f_d, text="nombre de bombes (100 max) : ", padx=10, pady=10, borderwidth=2, relief=GROOVE)
f_n.grid(column=0, row=3)
taille_n = Spinbox(f_n, from_=5, to=100, command=modif_the_underframe)
taille_n.grid()

create_the_underframe()
demineur.mainloop()
