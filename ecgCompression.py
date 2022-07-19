#importing libraries required
from pathlib import Path
import numpy as np
import pandas as pd
import wfdb
import glob
import sys


def nameRecord(str):
    global name_of_record
    name_of_record=str+ ".csv"
    

def compression():
    #reading csv files and storing them in list called values
    data=pd.read_csv(name_of_record,header=None)[0]
    global values
    values=data.tolist()
    #rounding off upto three decimal places for accuracy in differences
    for i in range (len(values)):
        values[i]=round(values[i],3)
    #padding extra zeroes when the number of values is not a multiple of 8
    global padd
    padd=len(values)%8
    if(padd!=0):
        for i in range (8-padd):
            values.append(0)
    block_size=50000    #default
    while(len(values)%block_size!=0 or block_size%8!=0):
        block_size-=1
    global block_8
    block_8=int(block_size/8)
    #creating difference array
    diff_array=[]
    for i in range (0, len(values),block_8):
            diff_array.append(int(float(values[i])*10000))
            for value in range(1,block_8):
                    #subtracting value with the previous value in list
                    diff_array.append( int ( ((float(values[value+i])*10000 )- ((float(values[value+i-1])*10000) ) )) ) 
    #creating sign list
    sign_lst=[]
    for val in range(0,len(diff_array),8): 
        sum=0
        for i in range (8):
            if(diff_array[val+i]<0):
                sum=sum+(2**(7-i))
                diff_array[val+i]=diff_array[val+i]*(-1)    #multiplying with -1 to make all values positive in difference aaray
        sign_lst.append(sum)
    rd=[]   #list to hold positions of all critical values in difference array 
    for val in range(0,len(diff_array),8): 
        sum=0
        for i in range (8):
            temp= diff_array[val+i]==48 or diff_array[val+i]==10 or diff_array[val+i]==13 or diff_array[val+i]==26 or diff_array[val+i]==255
            if(temp):
             #variable to store position in bit format
                sum=sum+(2**(7-i))
                diff_array[val+i]=diff_array[val+i]-1
        #each value in rd keeps track of critical values in a group of 8 values
        rd.append(sum)
    rs=[] #to keep track of critical values in sign list as well as that of list rd
    for value in range(len(sign_lst)):
        #temp1=sign_lst[value]
        temp2=rd[value]==48 or rd[value]==10 or rd[value]==13 or rd[value]==26 or rd[value]==255
        #finding critical values and replacing them with value-1
        temp1= sign_lst[value]==48 or sign_lst[value]==13 or sign_lst[value]==10 or sign_lst[value]==26 or sign_lst[value]==255
        if (temp1):
            if(temp2):
                rs.append(3)    #3 is 0011 in binary means both rd and sign list have critical value
                rd[value]=rd[value]-1
            else:
                rs.append(2)    #2 is 0010 in binary means only sign list have critical value
            sign_lst[value]=sign_lst[value]-1
        else:
            if(temp2):
                rs.append(1)    #1 is 0001 in binary means only rd have critical value
                rd[value]=rd[value]-1
            else:             #0 is 0000 in binary means both have no critical value
                rs.append(0)
    
    g=[]  #stores all converted value in ascii
    count=0
    global x
    x=100
    for j in range (0,len(diff_array),8):
        g.append(chr(sign_lst[count]))
        iter=0
        k0=0  #for forward grouping
        z0=0  #for backward grouping
        u0=0  #for no grouping
        for i in range (0,8,2):
            #if both are zero do forward grp only
            if((diff_array[j+i])==0 and diff_array[j+i+1]==0):
                #forward grouping
                g.append(chr(0))
                k0=k0+(2**(3-iter))
                iter+=1
            else:
            #both are not zero check all three grouping styles
                if((diff_array[j+i])!=0 and diff_array[j+i+1]!=0):
                    #forward grouping
                    if((diff_array[j+i]*x+diff_array[j+i+1])<1000):
                        g.append(chr(diff_array[j+i]*x+diff_array[j+i+1]))
                        k0=k0+(2**(3-iter))
                        iter+=1
                    #backward grouping
                    elif((diff_array[j+i+1])*x+diff_array[j+i]<1000):
                        g.append(chr(diff_array[j+i+1]*x+diff_array[j+i]))
                        z0=z0+(2**(3-iter))
                        iter+=1
                #no grouping for both value non zero
                    else:
                        g.append(chr(diff_array[j+i]))
                        g.append(chr(diff_array[j+i+1]))
                        u0=u0+(2**(3-iter))
                        iter+=1
            #no grouping for any one value as zero in pair
                else:
                    g.append(chr(diff_array[j+i]))  
                    g.append(chr(diff_array[j+i+1]))
                    u0=u0+(2**(3-iter))
                    iter+=1
        g.append(chr(k0+100))
        g.append(chr(z0+100))
        g.append(chr(u0+100))
        g.append(chr(rd[count])) 
        g.append(chr(rs[count]))
        g.append(0) #zero appending shows end of block
        count=count+1
    #creating a file and storing compressed data 
    global compressedFileName
    compressedFileName="compressed"+name_of_record
    f=open(compressedFileName,"w+", encoding='UTF-8')
    for i in range(len(g)):
        f.write(str(g[i]))
    f.close()


def decompression():
    #reading compressed file into temp list
    lines = []
    temp=[]
    with open(compressedFileName, encoding='UTF-8') as f:
        temp = f.read()
    for i in range (len(temp)):
        lines.append(ord(temp[i]))  #storing integer equivalent of all compressed values (UNICODE to NUMBER)
    #decompression
    diff_array_c=[]
    sign_bit_c=[]
    rs_c=[]
    rd_c=[]
    i=0
    while(i<len(lines)-7):  #loop to traverse through whole file
        temp=[]
        while(lines[i]!=48 and i<len(lines)-1): #loop to store one block of values at a time in a temporary list
            temp.append(lines[i])
            i=i+1
        i=i+1         #to skip 48
        len_temp=len(temp)
        if(len_temp!=0):
            k=int(bin(temp[len_temp-5]-100).replace("0b", ""))
            z=int(bin(temp[len_temp-4]-100).replace("0b", ""))
            u=int(bin(temp[len_temp-3]-100).replace("0b", ""))

            #taking into account all the indexes of critical values
            if(temp[len_temp-1]==0):
                sign_bit_c.append(int(bin(temp[0]).replace("0b", "")))
                rd_c.append(int(bin(temp[len_temp-2]).replace("0b", "")))
            elif(temp[len_temp-1]==1):
                sign_bit_c.append(int(bin(temp[0]).replace("0b", "")))
                rd_c.append(int(bin(temp[len_temp-2]+1).replace("0b", ""))) 
            elif(temp[len_temp-1]==2):
                sign_bit_c.append(int(bin(temp[0]+1).replace("0b", "")))
                rd_c.append(int(bin(temp[len_temp-2]).replace("0b", "")))
            elif(temp[len_temp-1]==3):
                sign_bit_c.append(int(bin(temp[0]+1).replace("0b", "")))
                rd_c.append(int(bin(temp[len_temp-2]+1).replace("0b", "")))
            #a stack to store value to be appended in difference array
            stk=[]
            j=len_temp-6 
            while(j>0):    #ungrouping of all values and storing them in stack
                if(k%10!=0):
                    stk.append(int(temp[j]%x))
                    stk.append(int(temp[j]/x))
                elif(z%10!=0):
                    stk.append(int(temp[j]/x))
                    stk.append(int(temp[j]%x))
                elif(u%10!=0): 
                    stk.append(int(temp[j]))
                    stk.append(int(temp[j-1]))
                    j=j-1
                k=int(k/10)
                u=int(u/10)
                z=int(z/10)  
                j=j-1
            for d in range (8): #loop to append stack values into difference array
                diff_array_c.append(stk.pop())
    i=0
    for value in range (0,len(diff_array_c),8):
        count=7
        while(rd_c[i]>0):   #checking and replacing original values into difference array
            if(rd_c[i]%10==1):
                diff_array_c[count+value]=diff_array_c[count+value]+1
            rd_c[i]=int(rd_c[i]/10)
            count=count-1
        i=i+1
    i=0
    for value in range (0,len(diff_array_c),8):
        count=7
        while(sign_bit_c[i]>0): #loop to assign proper sign to all the values in array
            if(sign_bit_c[i]%10==1):
                diff_array_c[count+value]=-1*diff_array_c[count+value]
            sign_bit_c[i]=int(sign_bit_c[i]/10)
            count=count-1
        i=i+1
    for br in range (0,len(diff_array_c),block_8): #for every 6250 block of data retreiving back values
        for value in range (1,block_8):
            diff_array_c[value+br]=diff_array_c[value+br]+diff_array_c[value+br-1]   
    for value in range (len(diff_array_c)): #diving values again to get decimal result
        diff_array_c[value]=diff_array_c[value]/10000
    if(padd!=0):    #removing any extra values appended
        for i in range (8-padd):
            diff_array_c.pop()
    for i in range (len(diff_array_c)):
        diff_array_c[i]=round(diff_array_c[i],3)    #rounding off the values upto three decimal places
    #storing result into decompressed file
    global decompressedFileName
    decompressedFileName="decompressed"+name_of_record
    f=open(decompressedFileName,"w+")
    for i in range(len(diff_array_c)):
        f.write(str(diff_array_c[i]))
        f.write("\n")
    f.close()
    n1 = Path(name_of_record).stat().st_size
    n2 = Path(compressedFileName).stat().st_size
    #cr
    cr=n1/n2
    #PRD calculation
    sum1=0
    sum2=0
    for i in range (len(values)):
        sum1+=(values[i]-diff_array_c[i])**2
        sum2+=values[i]**2
    div=sum1/sum2
    prd=div**(1/2)
    return (prd,cr)


nameRecord("102")
compression()
print(decompression())