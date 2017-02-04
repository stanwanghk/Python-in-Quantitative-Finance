'''
Perceptron:
  input:  feature vector
  output: {-1,+1};

*model:

f(x)=sign(w*x+b)

*strategy:

min L(w,b) = -y(w)
'''
import numpy as np

# training data
x = [[3,3],[4,3],[1,1]]
y = [1,1,-1]

def Is_right(xi,yi,w,b):
    # tell us if (xi,yi) is misclassified point by the (w,b);
    A = np.array(xi)
    B = np.array(w)
    sum = A.dot(B) + b
    if sum*yi <= 0:
        return False
    else:
        return True

def perceptron_SGD(x,y,w0,b0,learning_rate):
    # we use the stochastic gradient descent method to estimate (w,b)
    index = 0
    count = 0
    Max_number = len(x) * 10000  # the given max number to caclulate
    w = w0
    b = b0
    while index < len(x) and count <= Max_number:
        count += 1
        if Is_right(x[index],y[index],w,b):
            index += 1
        else:
            print('the {} time,{} wrong:'.format(count,index+1))
            b += learning_rate * y[index]
            for item in range(len(w)):
                w[item] += learning_rate * y[index] * x[index][item]
            # index = 0
            if index > 0: index -= 1
            # Remark: the solution is not unique, dependent on the sequence of misclassified point
    if count == Max_number:
        print("the x is not linearly separable!")
        return 0,0
    else:
        return w,b

w,b = perceptron_SGD(x,y,[0,0],0,1)

if w != 0 and b != 0:
    print("our estimated parameters are",w,b)