import copy
import numpy as np


class NeuralNetwork:

    def __init__(self, layer_sizes, activation='leaky_relu'):
        self.layer_sizes = layer_sizes
        self.num_layers = len(layer_sizes)
        self.weights = [np.random.randn(y, x) for x, y in zip(layer_sizes[:-1], layer_sizes[1:])]
        self.biases = [np.random.randn(y, 1) for y in layer_sizes[1:]]
        self.activation = activation
        self.layer_outputs = []

    def mutate_randomly(self):
        for layer in range(len(self.weights)):
            for i in range(self.weights[layer].shape[0]):
                for j in range(self.weights[layer].shape[1]):
                    self.weights[layer][i, j] += np.random.randn()

        for layer in range(len(self.biases)):
            for i in range(self.biases[layer].shape[0]):
                self.biases[layer][i, 0] += np.random.randn()

    def activate(self, x):
        if self.activation == 'relu':
            return np.maximum(0, x,)
        elif self.activation == 'leaky_relu':
            return np.where(x > 0, x, x * 0.01)   
        elif self.activation == 'sigmoid':
            return 1 / (1 + np.exp(-x))
        elif self.activation == 'tanh':
            return np.tanh(x)
        else:
            raise ValueError("Unsupported activation function")

    def forward(self, x):
        self.layer_outputs = []

        for b, w in zip(self.biases, self.weights):
            x = self.activate(np.dot(w, x) + b)
            self.layer_outputs.append(x.copy())

        return x

    def clone(self):
        return copy.deepcopy(self)