import copy
import keras
from keras import layers
import numpy as np

class NeuralNetwork:
    def __init__(self, config = None):
        self.config = config
        size_input = 1 + 1 + 1 + 1 + self.config.training.sensor_count

        model = keras.Sequential()

        model.add( keras.Input(shape=(size_input,), name="input" ) )

        for layer in self.config.training.model.layers:
            if layer.type == "Dense":
                model.add(layers.Dense(layer.units, activation=layer.activation))

        #model.compile(optimizer='adam', loss='mse')

        self.model = model

    def forward(self, x):
        return self.model.predict(np.array([x]),verbose = 0)[0]

    def mutate_randomly(self):
        weights = self.model.get_weights()
        mutated_weights = [w + np.random.randn(*w.shape) for w in weights]
        self.model.set_weights(mutated_weights)

    def clone(self):
        return copy.deepcopy(self)

