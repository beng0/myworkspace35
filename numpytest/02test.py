import numpy as np
dt = np.dtype(np.int32)
print(dt)

dt1 = np.dtype('i4')
print(dt1)

dt2 = np.dtype('<i4')
print(dt2)

dt3 = np.dtype([('age', np.int8)])
print(dt3)

dt4 = np.dtype([('age', np.int8)])
a = np.array([(10,),(20,),(30,)],dtype = dt4)
print(a)

dt5 = np.dtype([('age',np.int8)])
a1 = np.array([(10,),(20,),(30,),],dtype = dt5)
print(a1)