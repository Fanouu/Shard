import json
import os.path
import os
import pickle
import random
import sys

from colorama import Fore, Style

import numpy as np
import tensorflow as tf
from json import JSONEncoder

def save_data(data):
    with open('data/game.json', 'w') as file:
        json.dump(data, file)


def load_data():
    if not os.path.exists('data/game.json'):
        save_data({
            "ALLAICOUP": 0,
            "ALGOAICOUP": 0,
            "win": [1, 1],
            "wp": 0,
            "train": 0,
            "ltrain": 0
        })

    with open('data/game.json', 'r') as file:
        return json.load(file)


X_train = []  # Liste pour stocker les états du jeu
recommended_action = []
loaded_data = load_data()
train = loaded_data["train"]
ltrain = loaded_data["ltrain"]
rewards = []

class Agent:

    def generateModele(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(3, 3, 1)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
            tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
            tf.keras.layers.Dense(9, activation='softmax')
        ])

        if len(X_train) <= 0:
            X_ = np.random.randint(0, 2, (2, 3, 3, 1))
            y_ = np.random.randint(0, 2, (2, 9))
            reward = np.array([0, 0])
        else:
            print("DATA FOUND")
            X_ = np.array(X_train)
            y_ = np.array(self.convert_results_to_labels(recommended_action))
            reward = np.array(rewards)

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        model.fit(X_, y_, sample_weight=reward, epochs=12, batch_size=32)

        model.save('data/morpion_model_old')

        return model

    def __init__(self):
        super(Agent, self).__init__()
        global X_train, recommended_action, train
        self.load_data()
        if not os.path.exists('data/morpion_model_old'):
            print("no exists")
            self.generateModele()

        self.model = tf.keras.models.load_model('data/morpion_model_old')

        print(self.model.summary())
        data = load_data()
        train = data["win"][1]

    def add_new_layer(self):
        model = tf.keras.models.load_model('data/morpion_model_old')

        model.layers[-2].trainable = False
        name = "dense_{n}".format(n=len(model.layers))
        new_layer = tf.keras.layers.Dense(64, activation='relu', name=name)
        model.add(new_layer)
        name = "out_{n}".format(n=len(model.layers))
        output_layer = tf.keras.layers.Dense(9, activation='softmax', name=name)
        model.add(output_layer)

        if len(X_train) <= 0:
            X_ = np.random.randint(0, 2, (2, 3, 3, 1))
            y_ = np.random.randint(0, 2, (2, 9))
            reward = np.array([0, 0])
        else:
            print("DATA FOUND")
            X_ = np.array(X_train)
            y_ = np.array(self.convert_results_to_labels(recommended_action))
            reward = np.array(rewards)

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        model.fit(X_, y_, epochs=12, batch_size=32) #, sample_weight=reward

        self.model = model
        model.save('data/morpion_model_old')
        print(f"{Fore.RED}NOUVELLE LAYER DENSE !{Style.RESET_ALL}")

    def load_data(self):
        global X_train, recommended_action
        if os.path.exists('data/training_data.pkl'):
            with open('data/training_data.pkl', 'rb') as f:
                data = pickle.load(f)
                X_train, recommended_action = data['X_train'], data['recommended_action']

    def save_data(self):
        global X_train, recommended_action
        data = {'X_train': X_train, 'recommended_action': recommended_action}
        with open('data/training_data.pkl', 'wb') as f:
            pickle.dump(data, f)

    def train(self):
        global train, ltrain
        print("Lenght:", len(X_train))
        print(train)
        self.save_data()
        if train >= 100:
            model = tf.keras.models.load_model('data/morpion_model_old')
            X_new = np.array(X_train)
            y_new = np.array(self.convert_results_to_labels(recommended_action))
            model.fit(X_new, y_new, epochs=12, batch_size=32) #sample_weight=reward
            model.save('data/morpion_model_old')

            self.model = model
            print(f"{Fore.GREEN}Le modèle a été mis à jour avec de nouvelles données.{Style.RESET_ALL}")
            reset()
            train = 0
            return
        #ltrain = ltrain+1
        train = train+1

    def prediction(self, etat_jeu):
        correct = self.check(etat_jeu)
        newetat = np.expand_dims(etat_jeu, axis=0)
        prediction = self.model.predict(newetat)
        prediction = prediction[0]
        #prediction = [x if x != -1 else float('-inf') for x in prediction]
        print(prediction)
        action = self.epsilon_greedy_action(prediction, 0)

        X_train.append(etat_jeu)
        check = self.check(etat_jeu)

        victory = []
        strate = []
        valide = []
        for recommend, level in check:
            if level == 1.0:
                victory.append(recommend)
            elif level == 0.5:
                strate.append(recommend)
            elif level == 0.25:
                valide.append(recommend)

        target = []
        if len(victory) > 0:
            recoac = random.choice(victory)
            target.append((recoac, 1.0))
        elif len(strate) > 0:
            recoac = random.choice(strate)
            target.append((recoac, 1.0))
        elif len(valide) > 0:
            recoac = random.choice(valide)
            target.append((recoac, 1.0))

        recommended_action.append(target)
        return action

    def add_data(self, etat_jeu, target):
        X_train.append(etat_jeu)
        recommended_action.append(target)

    def determine_reward(self, result):
        if result == 3:
            return 1.0  # victoire
        elif result == 2:
            return 0.5 #strate
        elif result == 1:
            return 0.25  # tactic
        else:
            return 0.0  # default

    def epsilon_greedy_action(self, prediction, epsilon):
        #if np.random.uniform(0, 1) < epsilon:
        #    return np.random.randint(len(prediction))
        #else:
            return np.argmax(prediction)

    def play(self, etat_jeu):
        action_AI = self.prediction(etat_jeu)
        # print("L'IA joue à la position :", action_AI)
        ligne, colnone = positionToXY(action_AI)
        old_etat = etat_jeu
        etat_jeu[ligne][colnone] = 1

        return [etat_jeu, ligne, colnone, old_etat]

    def check(self, oldetat_jeu):
        expected = []
        i = 0
        victory = False
        nodefeat = 0
        for ligne, v in enumerate(oldetat_jeu):
            for colonne, value in enumerate(v):
                if value == 1 or value == 2:
                    expected.append((i, 0))
                else:
                    possible_win = self.possible_win(oldetat_jeu, i)
                    if possible_win == 1:
                        if not victory:
                            expected.append((i, 1.0))
                            victory = True
                        else:
                            expected.append((i, 1.0))
                    elif possible_win == 2:
                        nodefeat = nodefeat + 0
                        if not victory:
                            expected.append((i, 0.5))
                        else:
                            expected.append((i, 0.5))
                    else:
                        if not victory:
                            expected.append((i, 0.25))
                        else:
                            expected.append((i, 0.25))

                i = i + 1

        #if victory:
        #    new_expected = []
        #    for reco in expected:
        #        case, lvl = reco
        #        if lvl == 3:
        #            new_expected.append((case, 3))
        #            expected = new_expected
        #            break
        #elif nodefeat == 1:
        #    new_expected = []
        #    for reco in expected:
        #        case, lvl = reco
        #        if lvl == 3:
        #            new_expected.append((case, 3))
        #            expected = new_expected
        #            break

        return expected

    def possible_win(self, grille, action):
        ligne, colonne = positionToXY(action)
        if grille[ligne][colonne] == 0:
            grille[ligne][colonne] = 1
            if self.determine_result(grille) == 1:
                grille[ligne][colonne] = 0
                return 1  # ELLE PEUT GAGNER
            grille[ligne][colonne] = 0

        if grille[ligne][colonne] == 0:
            grille[ligne][colonne] = 2
            if self.determine_result(grille) == 2:
                grille[ligne][colonne] = 0
                return 2  # L ALGO PEUT GAGNER
            grille[ligne][colonne] = 0

        return 0

    def determine_result(self, grille):
        for ligne in range(3):
            if grille[ligne][0] == grille[ligne][1] == grille[ligne][2] == 2:
                return 2  # l'ALGO gagne
            elif grille[ligne][0] == grille[ligne][1] == grille[ligne][2] == 1:
                return 1  # L'AI gagne

        for colonne in range(3):
            if grille[0][colonne] == grille[1][colonne] == grille[2][colonne] == 2:
                return 2
            elif grille[0][colonne] == grille[1][colonne] == grille[2][colonne] == 1:
                return 1

        if grille[0][0] == grille[1][1] == grille[2][2] == 2:
            return 2
        elif grille[0][0] == grille[1][1] == grille[2][2] == 1:
            return 1
        if grille[0][2] == grille[1][1] == grille[2][0] == 2:
            return 2
        elif grille[0][2] == grille[1][1] == grille[2][0] == 1:
            return 1

        return 0

    def convert_results_to_labels(self, recommended_action):
        labels = []
        for i in range(len(recommended_action)):
            target = [0] * 9
            for recommend, level in recommended_action[i]:
                target[recommend] = level
            labels.append(target)
        return np.array(labels)


def positionToXY(position_AI):
    ligne, colonne = position_AI // 3, position_AI % 3
    return ligne, colonne

def XYToPosition(ligne, colonne):
    position_AI = ligne * 3 + colonne
    return position_AI


def reset():
    global X_train, y_train, recommended_action, rewards
    X_train = []
    recommended_action = []
    rewards = []

agent = Agent()
etat_jeu = np.array([[0, 0, 0],
                     [0, 0, 0],
                     [0, 0, 0]])
etat_jeu = agent.play(etat_jeu)
print(etat_jeu)

sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__
