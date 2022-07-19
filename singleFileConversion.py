import numpy as np
import wfdb
def conversion(recordname_new):
        record = wfdb.rdsamp(recordname_new,channels=[1]) # rdsamp() returns the signal as a numpy array  
        record=np.asarray(record[0])
        path="M/"+recordname_new+".csv"
        np.savetxt(path,record,delimiter=",") #Writing the CSV for each record  (,fmt="%.3e")
conversion("220")