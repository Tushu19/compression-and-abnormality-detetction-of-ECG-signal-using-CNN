
import numpy as np
import pandas as pd
import wfdb
import glob

def conversion():
    atr_files=glob.glob('*.atr')
    df=pd.DataFrame(data=atr_files)
    df.to_csv("files_list.csv",index=False,header=None) #Write the list to a CSV file
    files=pd.read_csv("files_list.csv",header=None)
    print(files)

    for i in range (len(files)):
        recordname=str(files.iloc[[i]])
        print(recordname[:-4])
        recordname_new=recordname[-7:-4] #Extracting just the filename part (will differ from database to database)
        record = wfdb.rdsamp(recordname_new,channels=[1]) # rdsamp() returns the signal as a numpy array  
        record=np.asarray(record[0])
        path=recordname_new+".csv"
        np.savetxt(path,record,delimiter=",") #Writing the CSV for each record  (,fmt="%.3e")
    # print("Files done: %s/%s"% (i+1,len(files)))
conversion()