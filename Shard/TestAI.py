import json
import os

import pygame
import sys
import random
import Agent
from colorama import Fore, Style

pygame.init()

largeur = 600
hauteur = 600

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
BLEU = (0, 0, 255)

fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu de Morpion")

taille_case = largeur // 3

grille = [[None, None, None],
          [None, None, None],
          [None, None, None]]

def save_data(data):
    with open('data/game.json', 'w') as file:
        json.dump(data, file)


def load_data():
    if not os.path.exists('data/game.json'):
        save_data({
            "ALLAICOUP": 0,
            "ALGOAICOUP": 0,
            "win": [1, 1],
            "wp": 0
        })

    with open('data/game.json', 'r') as file:
        return json.load(file)


loaded_data = load_data()
print(loaded_data)
WP = loaded_data["wp"]

# Joueur actuel (1 ou 2)
joueur = 1
starter = 2

AICOUP = 0
DLCOUP = 0
SAICOUP = loaded_data["ALLAICOUP"]
SDLCOUP = loaded_data["ALGOAICOUP"]

WIN = loaded_data["win"]

agent = Agent.Agent()


def start():
    global starter
    if starter == 1:
        return 2
    else:
        return 1


def etat_jeu():
    etat_jeux = [[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]]
    for i, v in enumerate(grille):
        for ii, vv in enumerate(v):
            if vv == "X":
                vv = 2
            elif vv == "O":
                vv = 1
            else:
                vv = 0

            etat_jeux[i][ii] = vv
    return etat_jeux


def load_grille():
    for ligne in range(3):
        for colonne in range(3):
            x = colonne * taille_case + taille_case // 2
            y = ligne * taille_case + taille_case // 2
            symbole = grille[ligne][colonne]

            if symbole == "X":
                pygame.draw.line(fenetre, NOIR, (x - 50, y - 50), (x + 50, y + 50), 4)
                pygame.draw.line(fenetre, NOIR, (x + 50, y - 50), (x - 50, y + 50), 4)
            elif symbole == "O":
                pygame.draw.circle(fenetre, NOIR, (x, y), 50, 4)


def check_victory(symbole):
    for ligne in range(3):
        if grille[ligne][0] == grille[ligne][1] == grille[ligne][2] == symbole:
            return True

    for colonne in range(3):
        if grille[0][colonne] == grille[1][colonne] == grille[2][colonne] == symbole:
            return True

    if grille[0][0] == grille[1][1] == grille[2][2] == symbole:
        return True
    if grille[0][2] == grille[1][1] == grille[2][0] == symbole:
        return True

    return False


def rectifieAI():
    for ligne in range(3):
        for colonne in range(3):
            if grille[ligne][colonne] is None:
                grille[ligne][colonne] = "O"
                if check_victory("O"):
                    grille[ligne][colonne] = None
                    return ligne, colonne
                grille[ligne][colonne] = None

    for ligne in range(3):
        for colonne in range(3):
            if grille[ligne][colonne] is None:
                grille[ligne][colonne] = "X"
                if check_victory("X"):
                    grille[ligne][colonne] = None
                    return ligne, colonne
                grille[ligne][colonne] = None

    coups_possibles = []
    for ligne in range(3):
        for colonne in range(3):
            if grille[ligne][colonne] is None:
                coups_possibles.append((ligne, colonne))
    return random.choice(coups_possibles)


def choisir_coup_IA2():
    #if random.randint(0, 1) == 1:
        for ligne in range(3):
            for colonne in range(3):
                if grille[ligne][colonne] is None:
                    grille[ligne][colonne] = "X"
                    if check_victory("X"):
                        grille[ligne][colonne] = None
                        return ligne, colonne
                    grille[ligne][colonne] = None

        for ligne in range(3):
            for colonne in range(3):
                if grille[ligne][colonne] is None:
                    grille[ligne][colonne] = "O"
                    if check_victory("O"):
                        grille[ligne][colonne] = None
                        return ligne, colonne
                    grille[ligne][colonne] = None

        coups_possibles = []
        for ligne in range(3):
            for colonne in range(3):
                if grille[ligne][colonne] is None:
                    coups_possibles.append((ligne, colonne))

        return random.choice(coups_possibles)
    #else:
    #    coups_possibles = []
    #    for ligne in range(3):
    #       for colonne in range(3):
    #            if grille[ligne][colonne] is None:
    #                coups_possibles.append((ligne, colonne))
    #
    #    return random.choice(coups_possibles)


while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    if not check_victory("X") and not check_victory("O"):
        if joueur == 1 and not check_victory("O") and not all(None not in ligne for ligne in grille):
            ligne, colonne = choisir_coup_IA2()
            old = etat_jeu()
            grille[ligne][colonne] = "X"
            joueur = 2

        if check_victory("X"):

            print("{LIGHTRED_EX}Victoire de l'{GREEN}Algo {RESET_ALL}".format(LIGHTRED_EX=Fore.LIGHTRED_EX, GREEN=Fore.GREEN, RESET_ALL=Style.RESET_ALL))
            print("{YELLOW}L'AI a mis un certain nombre independant de COUP: {CYAN} {AICOUP}/{DLCOUP}{YELLOW}({CYAN} {PERCENT}%{YELLOW}) {RESET_ALL}".format(AICOUP=AICOUP, DLCOUP=DLCOUP, CYAN=Fore.CYAN, YELLOW=Fore.YELLOW, PERCENT=(AICOUP / DLCOUP) * 100, LIGHTRED_EX=Fore.LIGHTRED_EX, GREEN=Fore.GREEN, RESET_ALL=Style.RESET_ALL))
            AICOUP = 0
            DLCOUP = 0
            WIN[1] = WIN[1] + 1
            total = WIN[0] + WIN[1]
            save_data({
                "ALLAICOUP": SAICOUP,
                "ALGOAICOUP": SDLCOUP,
                "win": WIN,
                "wp": WP
            })
            print("{YELLOW} Elle a aussi gagner {LIGHTGREEN_EX} {WIN}{YELLOW} partie(s) sur {LIGHTRED_EX}{total}{YELLOW}({CYAN}{PERCENT}{YELLOW}%) \nEt sur toute c'est partie {CYAN}{PERCENT2}% {YELLOW}sont mis par l'IA{RESET_ALL}".format(LIGHTGREEN_EX=Fore.LIGHTGREEN_EX, PERCENT2=(SAICOUP / SDLCOUP) * 100, PERCENT=(WIN[0] / total) * 100, total=WIN[1], WIN=WIN[0], AICOUP=AICOUP, DLCOUP=DLCOUP, CYAN=Fore.CYAN, YELLOW=Fore.YELLOW, LIGHTRED_EX=Fore.LIGHTRED_EX, GREEN=Fore.GREEN, RESET_ALL=Style.RESET_ALL))

            agent.train()
            pygame.draw.line(fenetre, BLEU, (0, taille_case // 2), (largeur, taille_case // 2), 4)
            pygame.display.update()
            #pygame.time.wait(2000)
            grille = [[None, None, None], [None, None, None], [None, None, None]]
            starter = start()
            joueur = starter
        elif all(None not in ligne for ligne in grille):

            print("{WHITE}Egaliter {RESET_ALL}".format(WHITE=Fore.WHITE, LIGHTRED_EX=Fore.LIGHTRED_EX, GREEN=Fore.GREEN, RESET_ALL=Style.RESET_ALL))
            print("{YELLOW}L'AI a mis un certain nombre independant de COUP: {CYAN} {AICOUP}/{DLCOUP}{YELLOW}({CYAN} {PERCENT}%{YELLOW}) {RESET_ALL}".format(AICOUP=AICOUP, DLCOUP=DLCOUP, CYAN=Fore.CYAN, YELLOW=Fore.YELLOW, PERCENT=(AICOUP / DLCOUP) * 100, LIGHTRED_EX=Fore.LIGHTRED_EX, GREEN=Fore.GREEN, RESET_ALL=Style.RESET_ALL))
            AICOUP = 0
            DLCOUP = 0
            total = WIN[0] + WIN[1]
            WIN[1] = WIN[1] + 1
            save_data({
                "ALLAICOUP": SAICOUP,
                "ALGOAICOUP": SDLCOUP,
                "win": WIN,
                "wp": WP
            })
            print("{YELLOW} Elle a aussi gagner {LIGHTGREEN_EX} {WIN}{YELLOW} partie(s) sur {LIGHTRED_EX}{total}{YELLOW}({CYAN}{PERCENT}{YELLOW}%) \nEt sur toute c'est partie {CYAN}{PERCENT2}% {YELLOW}sont mis par l'IA{RESET_ALL}".format(LIGHTGREEN_EX=Fore.LIGHTGREEN_EX, PERCENT2=(SAICOUP / SDLCOUP) * 100, PERCENT=(WIN[0] / total) * 100, total=WIN[1], WIN=WIN[0], AICOUP=AICOUP, DLCOUP=DLCOUP, CYAN=Fore.CYAN, YELLOW=Fore.YELLOW, LIGHTRED_EX=Fore.LIGHTRED_EX, GREEN=Fore.GREEN, RESET_ALL=Style.RESET_ALL))

            agent.train()
            pygame.display.update()
            #pygame.time.wait(2000)
            grille = [[None, None, None], [None, None, None], [None, None, None]]
            starter = start()
            joueur = starter
        else:
            play = agent.play(etat_jeu())
            case = grille[play[1]][play[2]]
            DLCOUP = DLCOUP + 1
            SDLCOUP = SDLCOUP + 1
            action = Agent.XYToPosition(play[1], play[2])
            if case == None:
                grille[play[1]][play[2]] = "O"
                AICOUP = AICOUP + 1
                SAICOUP = SAICOUP + 1
            else:
                ligne, colonne = rectifieAI()
                action = Agent.XYToPosition(ligne, colonne)
                grille[ligne][colonne] = "O"

            #agent.save(etat_jeu(), play[3])
            agent.save(play[3], play[3])
            agent.save(etat_jeu(), etat_jeu())
            joueur = 1
            if check_victory("O"):

                print("{LIGHTGREEN_EX}Victoire de l'{RED}IA {RESET_ALL}".format(LIGHTGREEN_EX=Fore.LIGHTGREEN_EX, RED=Fore.RED, WHITE=Fore.WHITE, LIGHTRED_EX=Fore.LIGHTRED_EX, GREEN=Fore.GREEN, RESET_ALL=Style.RESET_ALL))
                print("{YELLOW}L'AI a mis un certain nombre independant de COUP: {CYAN} {AICOUP}/{DLCOUP}{YELLOW}({CYAN} {PERCENT}%{YELLOW}) {RESET_ALL}".format(AICOUP=AICOUP, DLCOUP=DLCOUP, CYAN=Fore.CYAN, YELLOW=Fore.YELLOW, PERCENT=(AICOUP / DLCOUP) * 100, LIGHTRED_EX=Fore.LIGHTRED_EX, GREEN=Fore.GREEN, RESET_ALL=Style.RESET_ALL))
                WIN[0] = WIN[0] + 1
                total = WIN[0] + WIN[1]
                if ((AICOUP / DLCOUP) * 100) >= 100:
                    WP = WP + 1
                AICOUP = 0
                DLCOUP = 0
                save_data({
                    "ALLAICOUP": SAICOUP,
                    "ALGOAICOUP": SDLCOUP,
                    "win": WIN,
                    "wp": WP
                })
                print("{YELLOW} Elle a aussi gagner {LIGHTGREEN_EX} {WIN}{YELLOW} partie(s) sur {LIGHTRED_EX}{total}{YELLOW}({CYAN}{PERCENT}{YELLOW}%) \nEt sur toute c'est partie {CYAN}{PERCENT2}% {YELLOW}sont mis par l'IA{RESET_ALL}".format(LIGHTGREEN_EX=Fore.LIGHTGREEN_EX, PERCENT2=(SAICOUP / SDLCOUP) * 100, PERCENT=(WIN[0] / total) * 100, total=WIN[1], WIN=WIN[0], AICOUP=AICOUP, DLCOUP=DLCOUP, CYAN=Fore.CYAN, YELLOW=Fore.YELLOW, LIGHTRED_EX=Fore.LIGHTRED_EX, GREEN=Fore.GREEN, RESET_ALL=Style.RESET_ALL))

                agent.train()

                fenetre.fill(BLANC)
                for ligne in range(1, 3):
                    pygame.draw.line(fenetre, NOIR, (0, ligne * taille_case), (largeur, ligne * taille_case), 4)
                for colonne in range(1, 3):
                    pygame.draw.line(fenetre, NOIR, (colonne * taille_case, 0),
                                     (colonne * taille_case, hauteur), 4)
                load_grille()
                pygame.display.update()
                #pygame.time.wait(2000)

                grille = [[None, None, None], [None, None, None], [None, None, None]]
                starter = start()
                joueur = starter

    fenetre.fill(BLANC)

    for ligne in range(1, 3):
        pygame.draw.line(fenetre, NOIR, (0, ligne * taille_case), (largeur, ligne * taille_case), 4)
    for colonne in range(1, 3):
        pygame.draw.line(fenetre, NOIR, (colonne * taille_case, 0), (colonne * taille_case, hauteur), 4)

    load_grille()

    pygame.display.update()
