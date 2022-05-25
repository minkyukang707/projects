from datetime import datetime, timedelta
import time
from influxdb import InfluxDBClient
from copy import deepcopy
from influxdb import DataFrameClient

import pandas as pd 
import numpy as np
from tflite_runtime.interpreter import Interpreter

def get_ifdb(db,host='localhost',port=8086, user='root', passwd='root'):
    
    client = DataFrameClient(host, port, user, passwd, db)
    client2 = InfluxDBClient(host, port, user, passwd, db)
    result = client2.query('select * from networkintrusion')
    df = pd.DataFrame(result)
    #print(df)
    try:
        print('Connection Successful')
        print('=========================')
        print('   Connection Info')
        print('=========================')
        print('host;', host)
        print('port:', port)
        print('username:', user)
        print('database:', db)
    except:
        print('Connection Failed')
        pass
    
    return client

mydb=get_ifdb(db='kdd5')
ifdb=mydb

result = ifdb.query('select * from networkintrusion')
result_onerow=result['networkintrusion'].iloc[1,:]

print(result_onerow)

########################################

import pandas as pd
import numpy as np
from tflite_runtime.interpreter import Interpreter
model_path='/home/pi/tesr/model3_prune_0519_quant.tflite' #prune+quant model 
data_path='/home/pi/bin_data/bin_data.csv'

test_set=pd.read_csv(data_path)
test_set.drop(test_set.columns[0], axis=1, inplace=True)
x=test_set.iloc[0:,0:93]


interpreter = Interpreter(model_path=model_path)
interpreter.allocate_tensors()
    
#input/output tensor set
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

output_list=[]
test_features=np.expand_dims(result_onerow, axis=0)

interpreter.set_tensor(input_details[0]['index'], test_features.astype(np.float32))
interpreter.invoke()
#output get
output_data=interpreter.get_tensor(output_details[0]['index'])
output_list.append(output_data[0])
print(output_list)