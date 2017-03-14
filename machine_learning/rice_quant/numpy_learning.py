import numpy as np

#creat an array with rank 1
a=np.array([1,2,3])

#output
print(type(a))
print(a.shape)
print(a[0],a[1],a[2])
a[0]=5
print(a)

#creat an array with rank 2 and output
b=np.array([[1,2,3], [4,5,6]])
print(b.shape)
print(b[0,0],b[0,1],b[1,0])

#creat arrays with functions

a1=np.zeros((2,2))
print("a1: {0}".format(str(a1)))

a2 = np.ones((1,2))
print("a2: {0}".format(str(a2)))

a3 = np.full((2,2),7)
print("a3: {0}".format(str(a3)))

a4 = np.eye(2)
print("a4: {0}".format(str(a4)))

a5 = np.random.random((2,2))
print("a5: {0}".format(str(a5)))

#index of the array
a = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
b = a[:2,1:3]
print(a[0,1])
b[0,0] = 77
print(a[0,1]) #b[0,0] includes the same data as a[0,1]

print("a: \n {0}, shape: {1}".format(str(a),a.shape))

row_r1 = a[1,:]
row_r2 = a[1:2,:]

print("row_r1: {0}, shape {1}".format(str(row_r1),row_r1.shape))
print("row_r2: {0}, shape {1}".format(str(row_r2),row_r2.shape))

col_r1 = a[:,1]
col_r2 = a[:,1:2]

print("col_r1: {0}, shape {1}".format(str(row_r1),row_r1.shape))
print("col_r2: {0}, shape {1}".format(str(row_r2),row_r2.shape))