import numpy as np

#ADABOOST implementation - using simple h(x,theta) = sign(theta_1(x_k-theta_0)) for theta = [k,theta_0,theta_1]
class ADABeans:
    def __init__(self,num_clf,num_train):
        self.clfs = num_clf #number of classifiers
        self.N = num_train #number of training examples
        self.W = [[1/self.N for i in range(self.N)]] #train weights for first clf is 1/N
        self.thetas = [[i,0,1] for i in range(self.clfs)] #i represents attributes (assumes n_clfs = num dim of X(attributes))
        self.alphas = []#initialize list of alphas (final weights of each classifier)

    #not quite brute force method to find theta
    def get_opt_theta(self, m, X, y, lower, upper, step): #use quartiles
        best_t0 = lower
        best_acc = 0 #(1-eps)
        label = 1
        if lower == upper:
            return[m,best_t0,1],0.5
        for t0 in np.arange(lower,upper,step):
        
            eps = sum([self.W[m][i]*int(np.sign(y[i])!=np.sign(X[i][m]-t0)) for i in range(self.N)])
            if 1-eps > best_acc:
                best_t0 = t0
                best_acc = 1-eps
                label = np.sign(sum([np.sign(X[i][m]-t0) for i in range(self.N)])) #update label of majority class

        return [m,best_t0,label],1-best_acc #return theta and epsilon

    def train_classifiers(self,X,y):
        #train each classifier
        for m in range(self.clfs):
            lower_t = np.min(X,axis=0)[m]
            upper_t = np.max(X,axis=0)[m]
            self.thetas[m],eps = self.get_opt_theta(m,X,y,lower_t,upper_t,(upper_t-lower_t)/self.N)
            if eps == 0:
                alph = 0.5*np.log(1)
            else:
                alph = 0.5*np.log((1-eps)/eps)
            self.alphas.append(alph)#add to final clf weights

            #update weights for next round
            w = []
            for i in range(self.N):
                t0 = self.thetas[m][1]
                t1 = self.thetas[m][2]
                w.append(self.W[m][i]*np.exp(-y[i]*alph*np.sign(t1*(X[i][m]-t0))))
            self.W.append([(1/sum(w))*w[i] for i in range(len(w))])
        return self.thetas,self.alphas

    def predict(self, new_bean):
        return np.sign(sum([self.alphas[m]*np.sign(self.thetas[m][2]*(new_bean[m]-self.thetas[m][1])) for m in range(self.clfs)]))
