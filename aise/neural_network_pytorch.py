import torch
import torch.nn as nn
import torch.nn.functional as F
import copy

class NeuralNetworkPyTorch(nn.Module):

    def __init__(self, layer_sizes, activation='relu'):
        super(NeuralNetworkPyTorch, self).__init__()
        self.layer_sizes = layer_sizes
        self.activation = activation

        # Criando camadas da rede
        layers = []
        for i in range(len(layer_sizes) - 1):
            layers.append(nn.Linear(layer_sizes[i], layer_sizes[i+1]))
            if i < len(layer_sizes) - 2:  # Não aplicamos ativação na última camada
                if activation == 'relu':
                    layers.append(nn.ReLU())
                elif activation == 'leaky_relu':
                    layers.append(nn.LeakyReLU(0.01))
                elif activation == 'sigmoid':
                    layers.append(nn.Sigmoid())
                elif activation == 'tanh':
                    layers.append(nn.Tanh())
                else:
                    raise ValueError("Unsupported activation function")
        self.network = nn.Sequential(*layers)

    def forward(self, x):
        return self.network(x)

    def mutate_randomly(self):
        with torch.no_grad():
            for param in self.network.parameters():
                param.add_(torch.randn_like(param))

    def clone(self):
        return copy.deepcopy(self)
