f_name = 'error.txt'

f = open('../'+f_name, 'a')
f.write('i am here')
f.write('\r\n')
f.close()
print('end')