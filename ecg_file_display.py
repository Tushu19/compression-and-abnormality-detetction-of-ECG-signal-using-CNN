import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#plotting error file
def errorPlot():
    df  = pd.read_csv("error.csv")
    df.plot( figsize=(15,5), kind='line',x=0,y=1)
    plt.ylim(top=0.002)
    plt.ylim(bottom=-0.003)
    plt.xlim(right=3600)
    plt.xlim(left=1800)
    plt.xlabel("Sample Number")
    plt.ylabel("Difference")
    plt.title("Difference between original value and reconstructed value")
    plt.legend(['Difference Obtained'])
    plt.show()
    #plt.savefig("errorDiff_104.jpg")

#plotting original values
def ogPlot(str):
    recName=str+".csv"
    df  = pd.read_csv(recName)
    df.plot( figsize=(15,5), kind='line',y=0)
    # plt.ylim(top=1.5)
    # plt.ylim(bottom=-1)
    # plt.xlim(right=1800)
    # plt.xlim(left=0)
    plt.xlabel("Sample Number")
    plt.ylabel("Voltage")
    plt.title("Original Signal")
    plt.legend(['Original Signal'])
    plt.style.use("bmh")
    plt.show()
    #plt.savefig("OgSig_104.jpg")

#plotting reconstructed values
def rePlot(str):
    recName="decompressed"+str+".csv"
    df  = pd.read_csv(recName)
    df.plot( figsize=(15,5), kind='line',y=0)
    # plt.ylim(top=1.5)
    # plt.ylim(bottom=-1)
    # plt.xlim(right=1800)
    # plt.xlim(left=0)
    plt.xlabel("Sample Number")
    plt.ylabel("Voltage")
    plt.title("Reconstructed Signal")
    plt.legend(['Reconstructed Signal'])
    plt.style.use("bmh")
    plt.show()
    #plt.savefig("ReSig_104.jpg")
