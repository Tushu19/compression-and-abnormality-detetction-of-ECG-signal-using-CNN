def timing(string,comp,decomp):
    f=open("Timings.csv","a")
    f.write(string)
    f.write(",")
    f.write(str(comp))
    f.write(",")
    f.write(str(decomp))
    f.write("\n")
    f.close()
    return