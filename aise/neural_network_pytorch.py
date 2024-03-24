import torch
import torch.nn as nn
import copy

class NeuralNetwork(nn.Module):  # Inherit from nn.Module
    def __init__(self, config=None):
        super(NeuralNetwork, self).__init__()  # Call superclass constructor

        self.config = config
        layers = []

        for idx in range(len(self.config.training.model.layers)-1):
            layer = self.config.training.model.layers[idx]
            next_layer = self.config.training.model.layers[idx+1]

            if layer.type == "Input":
                in_features = self.get_units(layer)
                out_features = self.get_units(next_layer)
            elif layer.type == "Output":
                continue
            else:
                in_features = self.get_units(layer)
                out_features = self.get_units(next_layer)

            layers.append(nn.Linear(in_features,out_features))  
    
            activation = self.get_activation(layer.activation)
            if activation:
                layers.append( self.get_activation(layer.activation) )


        self.model = nn.Sequential(*layers) 

    def get_units(self, layer):
        if layer.type == "Input":
            return 1 + 1 + 1 + 1 + self.config.training.sensor_count
        elif layer.type == "Output":
            return 4
        else:
            return layer.units

    def forward(self, input):
        data = torch.tensor(input, dtype=torch.float)
        return self.model(data)

    def mutate(self, mutation_rate):
        with torch.no_grad():
            for param in self.model.parameters():
                param += torch.randn_like(param) * mutation_rate
                #param += torch.randn_like(param)

    def mutate_randomly(self):
        with torch.no_grad():
            for param in self.model.parameters():
                param += torch.randn_like(param)  

    def clone(self):
        # Assuming your config object is also copyable
        return copy.deepcopy(self)
    
    def get_activation(self, activation_name):
        if activation_name == 'relu':
            return nn.ReLU()
        elif activation_name == 'leaky_relu':
            return nn.LeakyReLU()
        elif activation_name == 'sigmoid':
            return nn.Sigmoid()
        elif activation_name == 'tanh':
            return nn.Tanh()
        else:
            return None
