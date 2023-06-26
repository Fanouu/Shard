import os.path
import threading

from keras.preprocessing import image
import numpy as np
import dog
import requests
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator

X_train = []
Y_train = []

CAT_PATH = 'resources/cat'
DOG_PATH = 'resources/dog'


class Agent:

    def generateDog(self):
        i = 0
        while i < 10:
            dog.getDog(directory='resources/dog', filename='dog{i}'.format(i=i))
            i = i + 1

    def generateCat(self):
        url = "https://cataas.com/cat"
        i = 0
        while i < 10:
            rq = requests.get(url)
            filename = 'resources/cat/cat{i}.jpg'.format(i=i)

            with open(filename, 'wb') as file:
                file.write(rq.content)

            i = i + 1

    def generateModel(self):
        datagen = ImageDataGenerator(
            rescale=1. / 255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True
        )

        class_mapping = {'cat': 0, 'dog': 1}

        train_data = datagen.flow_from_directory(
            'resources',
            target_size=(128, 128),
            batch_size=32,
            class_mode='binary',
            classes=class_mapping
        )

        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

        model.fit(train_data, epochs=12)

        model.save('data/model')

        return model

    def __init__(self):
        if not os.path.exists(DOG_PATH):
            os.mkdir(DOG_PATH)
            self.generateDog()
        if not os.path.exists(CAT_PATH):
            os.mkdir(CAT_PATH)
            self.generateCat()
            self.generateModel()

        model = tf.keras.models.load_model('data/model')

        new_image_path = CAT_PATH + "/cat4.jpg" #IMAGE QUE TU VEUT TEST
        new_image = tf.keras.preprocessing.image.load_img(new_image_path, target_size=(128, 128))

        new_image_array = tf.keras.preprocessing.image.img_to_array(new_image)
        new_image_array = np.expand_dims(new_image_array, axis=0)
        new_image_array = new_image_array / 255.0

        prediction = model.predict(new_image_array)

        if prediction[0] >= 0.5:
            print("C'est un chien !")
        else:
            print("C'est un chat !")


agent = Agent()
