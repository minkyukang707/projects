import pandas as pd
import numpy as np
from tflite_runtime.interpreter import Interpreter

model_path='/home/pi/tesr/model3_0519.tflite'
#model_path='/home/pi/tesr/model3_0519_quant.tflite'

#model_path='/home/pi/tesr/model3_prune_0518.tflite'
#model_path='/home/pi/tesr/model3_prune0518_prune_quant.tflite'
data_path='/home/pi/bin_data/bin_data.csv'

if __name__=='__main__':
    # test data load
    test_set=pd.read_csv(data_path)
    
    #index remove
    test_set.drop(test_set.columns[0], axis=1, inplace=True)
    
    #feature set
    x=test_set.iloc[:,0:93].values
    y=test_set[['intrusion']].values
    
    #3data only
    limit_x=x[:20000]
    
    #interpreter load
    interpreter = Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    
    #input/output tensor set
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print(input_details)
    print(output_details)
    
    #Results list array set
    output_list=[]
    
    for t in range(len(limit_x)):
        # dimension expand
        test_features=np.expand_dims(limit_x[t], axis=0)
        #input data
        interpreter.set_tensor(input_details[0]['index'], test_features.astype(np.float32))
        interpreter.invoke()
        #output get
        output_data=interpreter.get_tensor(output_details[0]['index'])
        #add to output list
        if output_data[0]>0.5:
            output_data[0]=1
        else:
            output_data[0]=0
        output_list.append(output_data[0])
    
    # Accuracy return 
    s=0
    
    for i in range(len(output_list)):
        if y[i] == output_list[i]:
            s+=1/len(output_list)
    accuracy=round(s*100,2)    
    print(f"Accuracy = {accuracy}%")