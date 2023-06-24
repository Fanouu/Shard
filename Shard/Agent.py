import json
import os.path
import os
import pickle
import sys
from colorama import Fore, Style

import numpy as np
import tensorflow as tf
import logging
from json import JSONEncoder


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


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


X_train = []  # Liste pour stocker les états du jeu
y_train = []  # Liste pour stocker les actions associées
results = []
recommended_action = []
train = 0
newlayer = 0
rewards = []

class Agent:

    def generateModele(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(3, 3, 1)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(32, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
            tf.keras.layers.Dense(32, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
            tf.keras.layers.Dense(9, activation='softmax')
        ])

        if len(X_train) <= 0:
            X_ = np.random.randint(0, 2, (2, 3, 3, 1))
            y_ = np.random.randint(0, 2, (2, 9))
            reward = np.array([0, 0])
        else:
            X_ = np.array(X_train)
            y_ = np.array(self.convert_results_to_labels(recommended_action))
            reward = np.array(rewards)

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        model.fit(X_, y_, sample_weight=reward, epochs=10, batch_size=32)

        model.save('data/morpion_model')

        return model

    def __init__(self):
        super(Agent, self).__init__()
        global X_train, recommended_action
        # self.load_data()
        if not os.path.exists('data/morpion_model'):
            print("no exists")
            self.generateModele()

        self.model = tf.keras.models.load_model('data/morpion_model')

        print(self.model.summary())

    def add_new_layer(self):
        model = tf.keras.models.load_model('data/morpion_model')

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
            X_ = np.array(X_train)
            y_ = np.array(self.convert_results_to_labels(recommended_action))
            reward = np.array(rewards)

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        model.fit(X_, y_, epochs=10, batch_size=32) #, sample_weight=reward

        self.model = model
        model.save('data/morpion_model')
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
        global train
        data = load_data()
        WIN = data["win"]
        print(WIN[1])
        if WIN[1] == 3000:
            WP = data["wp"]
            data = {"ALLAICOUP": 0, "ALGOAICOUP": 0, "win": [1, 1], "wp": WP}
            save_data(data)
            #self.add_new_layer()

        if train == 70:
            model = tf.keras.models.load_model('data/morpion_model')
            X_new = np.array(X_train)
            y_new = np.array(self.convert_results_to_labels(recommended_action))
            reward = np.array(rewards)
            model.fit(X_new, y_new, epochs=12, batch_size=32) #sample_weight=reward
            model.save('data/morpion_model')
            self.model = model
            print(f"{Fore.GREEN}Le modèle a été mis à jour avec de nouvelles données.{Style.RESET_ALL}")
            train = 0
            reset()
            return
        train = train + 1

    def prediction(self, etat_jeu):
        correct = self.check(etat_jeu)
        newetat = np.expand_dims(etat_jeu, axis=0)
        prediction = self.model.predict(newetat)
        prediction = prediction[0]
        prediction = [x if x != -1 else float('-inf') for x in prediction]
        action = self.epsilon_greedy_action(prediction, 0)

        target = [0] * 9
        for recommend, level in correct:
            target[recommend] = level
        ag = np.argmax(target)
        if ag != action and target[ag] == 3:
            target = []
            for i in range(9):
                if i == ag:
                    target.append((i, 3))
                else:
                    target.append((i, -1))
            X_train.append(etat_jeu)
            recommended_action.append(target)
            #rewards.append(1.0)
        return action

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
        if np.random.uniform(0, 1) < epsilon:
            return np.random.randint(len(prediction))
        else:
            return np.argmax(prediction)

    def save(self, etat_jeu, oldetat_jeux):
        X_train.append(etat_jeu)
        check = self.check(oldetat_jeux)
        recommended_action.append(check)  # ATTENTION SI ALGO CHELOU REMETTRE OLD

        result = 0.0
        for etat in self.convert_results_to_labels([check]):
            for i in etat:
                determine = self.determine_reward(i)
                if determine == 1.0:
                    result = 1.0
                    break
                elif determine > result:
                    result = determine
        #rewards.append(result)

        self.save_data()

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
        for ligne, v in enumerate(oldetat_jeu):
            for colonne, value in enumerate(v):
                if value == 1 or value == 2:
                    expected.append((i, -1))
                else:
                    possible_win = self.possible_win(oldetat_jeu, i)
                    if possible_win == 1:
                        if not victory:
                            expected.append((i, 3))
                            victory = True
                    elif possible_win == 2:
                        if not victory:
                            expected.append((i, 2))

                    else:
                        expected.append((i, 1))

                i = i + 1

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
