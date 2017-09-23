import numpy as np 

from func import forward, forward_affine, backward, backward_affine, cross_entropy

class ThreeLayers(object):
    def __init__(self, case=1, input_dim=14, num_output=4):
        self.W = [] # weights
        self.B = [] # biases
        np.random.seed()
        self.case = case
        if self.case == 1:
            hiddenL1 = 100
            hiddenL2 = 40
            self.B.append(np.zeros((1,hiddenL1)))
            self.W.append(np.random.rand(input_dim, hiddenL1)*0.01)
            self.B.append(np.zeros((1,hiddenL2)))
            self.W.append(np.random.rand(hiddenL1, hiddenL2)*0.01)
            self.B.append(np.zeros((1,num_output)))
            self.W.append(np.random.rand(hiddenL2, num_output)*0.01)
        elif self.case == 2:
            hiddenL1 = 28
            repeat = 6
            self.B.append(np.zeros((1,hiddenL1)))
            self.W.append(np.random.rand(input_dim, hiddenL1)*0.01)
            for i in xrange(repeat-1):
                self.B.append(np.zeros((1,hiddenL1)))
                self.W.append(np.random.rand(hiddenL1, hiddenL1)*0.01)
            self.B.append(np.zeros((1,num_output)))
            self.W.append(np.random.rand(hiddenL1, num_output)*0.01)
        elif self.case == 3:
            hiddenL1 = 14
            repeat = 10
            self.B.append(np.zeros((1,hiddenL1)))
            self.W.append(np.random.rand(input_dim, hiddenL1)*0.01)
            for i in xrange(repeat-1):
                self.B.append(np.zeros((1,hiddenL1)))
                self.W.append(np.random.rand(hiddenL1, hiddenL1)*0.01)
            self.B.append(np.zeros((1,num_output)))
            self.W.append(np.random.rand(hiddenL1, num_output)*0.01)
        

    def compute(self, X, Y=None):
        layers = []
        caches = []

        reg = 1e-3 # regularization strength
        ## Forward calculation and active
        t_x = X
        for i in xrange(len(self.W)):
            t_w = self.W[i]
            t_b = self.B[i]
            if i == len(self.W)-1:
                t_layer, t_cache = forward_affine(t_x, t_w, t_b)
                layers.append(t_layer)  
                caches.append(t_cache)
            else:
                t_layer, t_cache = forward(t_x, t_w, t_b)
                t_x = t_layer
                layers.append(t_layer)
                caches.append(t_cache)
        if Y is None:
            result = layers[len(layers)-1]
            max = np.argmax(result, axis = 1)
            return max
        loss = 0
        gradiens_W = []
        gradiens_B = []
        ## Cross entropy 
        loss, de_loss = cross_entropy(layers[len(layers)-1], Y)
        #reg_loss = 0.5*reg*np.sum(W*W)
        #loss += reg_loss
        ## Back propogation
        dout = de_loss
        for i in xrange(len(caches)):
            index = len(caches) - 1 - i
            t_cache = caches[index]
            if index == len(caches) - 1: 
                ## the last layer
                t_dx, t_dw, t_db = backward_affine(dout, t_cache)
                gradiens_W.append(t_dw)
                gradiens_B.append(t_db)
                dout = t_dx
            else:
                ## normal layer
                t_dx, t_dw, t_db = backward(dout, t_cache)
                gradiens_W.append(t_dw)
                gradiens_B.append(t_db)
                dout = t_dx
        return loss, gradiens_W, gradiens_B

