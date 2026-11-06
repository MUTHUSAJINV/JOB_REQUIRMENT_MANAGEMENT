import os
T = r"c:\Users\SAJIN\OneDrive\Desktop\job\templates"
def w(n,c):
    open(os.path.join(T,n),"w",encoding="utf-8").write(c)
    print("OK",n)

